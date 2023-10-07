import torch

from fau_tools import utils
from fau_tools.data_structure import ModelManager, TimeManager, TrainRecorder


# ------------------------------------------------------------
# --------------- Function --- training
# ------------------------------------------------------------
def __show_progress(now, total, loss=None, accuracy=None, time_manager=None):
  """
  Display the training process bar.

  Parameters
  ----------
  now          : the current epoch (start from zero)
  total        : the total epoch
  loss         : current loss value; if None, will not be displayed
  accuracy     : current accuracy; if None, will not be displayed
  time_manager : for showing the training time process; if None, will not be displayed

  """
  now += 1  # remap 0 -> 1
  FINISH, UNFINISH = '█', ' '
  LENGTH = 30  # the length

  # for showing blocks
  percent  = now / total
  finish   = int(percent * LENGTH) * FINISH
  unfinish = (LENGTH - len(finish)) * UNFINISH
  show     = f"|{finish}{unfinish}| {percent:.2%}"

  if time_manager:  # for showing time process
    average_time, elapsed_time = time_manager.get_average_time(), time_manager.get_elapsed_time()
    total_time = total * average_time

    elapsed_time = utils.time_to_human(elapsed_time)
    total_time   = utils.time_to_human(total_time)

    show += utils.cprint(f"  [{elapsed_time}<{total_time}]", color="cyan", show=False)

  if loss:     show += utils.cprint(f"  loss: {loss:.6f}", color="red", show=False)
  if accuracy: show += utils.cprint(f"  accuracy: {accuracy:.2%}", color="green", show=False)

  print(show)


def __stop_training(epoch, model_manager, threshold):
  """
  Determine whether satisfy early stop.

  Parameters
  ----------
  epoch         : current epoch
  model_manager : the model manager
  threshold     : early_stop threshold

  Returns
  -------
  Boolean value, indicating whether should stop training.

  """
  gap = epoch - model_manager.epoch
  return gap >= threshold


def calc_accuracy(model, test_loader, device=None):
  """
  Calculate the accuracy rate in the test dataset.

  Parameters
  ----------
  model       : the training model
  test_loader : the test data loader
  device      : the calculating device used in pytorch; if None, will be determined automatically

  Returns
  -------
  The accuracy rate in the test dataset. (Rounded to 6 decimal places.)

  """
  if not device: device = utils.get_device()

  model.eval()  # evaluation mode
  with torch.no_grad():
    test_result = list()  # for calculating the average accuracy rate.
    for (test_x, test_y) in test_loader:
      test_x, test_y = test_x.to(device), test_y.to(device)
      test_output: torch.Tensor = model(test_x)
      test_prediction: torch.Tensor = test_output.argmax(1)  # get classification result set
      cur_accuracy: torch.Tensor = sum(test_prediction.eq(test_y)) / test_y.size(0)
      test_result.append(cur_accuracy.item())  # tensor -> scalar
    accuracy: float = sum(test_result) / len(test_result)  # get average accuracy

  model.train()  # recover
  return round(accuracy, 6)



@utils.calc_time
def torch_train(
  model, train_loader, test_loader,
  optimizer, loss_function,
  *,
  total_epoch=100, early_stop=None,
  name=None, save_model=True,
  clearml_task=None,
  device=None
):
  """
  Train the model.

  Parameters
  ----------
  model         : the model needs to be trained
  train_loader  : train data loader
  test_loader   : test data loader
  optimizer     : optimizer function
  loss_function : loss function
  total_epoch   : the total epoch of training
  early_stop    : the early stop threshold; if None to disable
  name          : if the training process needs to be saved, please passing the file name without postfix
  save_model    : whether to save the trained model; if needed please ensuring the name parameter is not None
  clearml_task  : should be the `Task` type in `clearml` module, which means using `clearml` to record experiment
  device        : the calculating device used in pytorch; if None, will be determined automatically

  Returns
  -------
  Some files may be generated:
    1. the trained model file named f"{name}.pth".
    2. the scalars variation during the training file named f"{name}.csv".
    3. the hyperparameters and time cost file named f"{name}.txt".

  """
  # Acquire device information
  if device is None: device, device_name = utils.get_device(return_name=True)
  else:
    device_name = torch.cuda.get_device_name(0) if device[:4] == "cuda" else device
    device = torch.device(device)
  utils.cprint(f"{'='*10} Training in {device_name} {'='*10}", color="green")

  if train_loader.batch_size == 1: utils.notify(torch_train.__name__, "You should not set the batch_size to 1; since if the NN uses BN, it will arise an error.", notify_type="warn")

  # Check clearml_task
  if clearml_task is not None:
    from clearml import Task
    if not isinstance(clearml_task, Task): utils.notify(torch_train.__name__, "TypeError, clearml_task should be the `Task` type.", notify_type="error"); return
    utils.notify(torch_train.__name__, "ClearML task is enabled.", notify_type="info")

  # For saving training data.
  model_manager  = ModelManager()
  train_recorder = TrainRecorder()

  # Begin training
  model = model.to(device); model.train()  # initialization

  # For showing training time
  time_manager = TimeManager()

  for epoch in range(total_epoch):
    loss_list = list()
    for _, (train_x, train_y) in enumerate(train_loader):
      train_x, train_y = train_x.to(device), train_y.to(device)
      output: torch.Tensor = model(train_x)
      loss: torch.Tensor   = loss_function(output, train_y)
      loss_list.append(loss.item())

      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

    # BUG: loss calc is wrong when the last batch is not a whole batch.
    # End of epoch
    loss_value, accuracy = sum(loss_list) / len(loss_list), calc_accuracy(model, test_loader, device)  # get loss and accuracy
    time_manager.time_tick()  # tick current time
    __show_progress(epoch, total_epoch, loss_value, accuracy, time_manager)

    # Update and record
    model_manager.update(model, loss_value, accuracy, epoch)
    train_recorder.update(loss_value, accuracy)

    # clearml
    if clearml_task is not None:
      clearml_logger = clearml_task.get_logger()
      clearml_logger.report_scalar("train/loss", "loss", loss_value, epoch)
      clearml_logger.report_scalar("val/accuracy", "accuracy", accuracy, epoch)
      clearml_logger.report_scalar("learning_rate", "learning_rate", optimizer.param_groups[0]["lr"], epoch)

    # Judge early stop
    if early_stop is not None and __stop_training(epoch, model_manager, early_stop):
      utils.cprint(f"Early stop: The model has gone through {early_stop} epochs without being optimized.", color="yellow")
      break

  if name is None: return  # no save

  # Save model and process
  SAVE_NAME = f"{name}_{model_manager.get_postfix()}"
  if save_model: model_manager.save(SAVE_NAME)
  train_recorder.save(SAVE_NAME)

  # Save the parameters
  parameters_filename = f"{SAVE_NAME}.txt"
  with open(parameters_filename, "w") as file:
    file.write(f"optimizer:\n{str(optimizer)}\n")
    file.write(f"{'-' * 20}\n")
    file.write(f"loss function:\n{str(loss_function)}\n")
    file.write(f"{'-' * 20}\n")
    file.write(f"batch size: {train_loader.batch_size}\n")
    file.write(f"total_epoch: {total_epoch}\n")
    try:  # for saving the number of train and test data
      train_data_num = len(train_loader.batch_sampler.sampler.data_source.labels)
      test_data_num  = len(test_loader.batch_sampler.sampler.data_source.labels)
    except AttributeError: utils.cprint("Saving the number of train and test data error.", color="red")
    else:
      file.write(f"{'-' * 20}\n")
      file.write(f"train_data_number: {train_data_num}\n")
      file.write(f"test_data_number:  {test_data_num}\n")

    # save best info
    file.write(f"{'-' * 20}\n")
    file.write(f"The best model in the {model_manager.epoch} epoch.\n")

    # save time
    file.write(f"{'-' * 20}\n")
    cost_time = time_manager.get_elapsed_time()
    cost_time = utils.time_to_human(cost_time)
    file.write(f"Training cost: {cost_time}\n")

  utils.cprint(f"{torch_train.__name__}: save a parameter file named {parameters_filename} successfully!", color="green")


# ------------------------------------------------------------
# --------------- Function --- plot
# ------------------------------------------------------------
def load_record(file_path):
  """
  Load the traning record.

  Parameters
  ----------
  file_path : the record file path

  Returns
  -------
  (loss_list, accuracy_list)

  Raises
  ------
  ValueError : File path is illegal.

  """
  if len(file_path) < 4: raise ValueError("The file name is too short! (Missing postfix)")

  if file_path[-4:] == '.csv':
    import pandas as pd
    csv = pd.read_csv(file_path, skipinitialspace=True)
    loss_list     = csv["loss"].tolist()
    accuracy_list = csv["accuracy"].tolist()
    return loss_list, accuracy_list
  else: raise ValueError("The file name postfix is illegal.")


def draw_plot(*args, legend_names=None, x_name=None, y_name=None, percent=False):
  """
  Display a comparison of multiple models on a single plot.

  For example, you can draw the accuracy of multiple models in a plot.
  Notes: Please manually use 'plt.show()'.

  Parameters
  ----------
  args         : the list of `values`; `values`: loss_values, accuracy rates ...
  legend_names : if the legend is required, please pass a list of names in order of the args
  x_name       : set the name for the x-axis
  y_name       : set the name for the y-axis
  percent      : display the values of the y-axis as a percentage

  """
  import matplotlib.pyplot as plt
  from matplotlib import ticker

  if legend_names is not None and len(args) != len(legend_names):
    raise ValueError("The length of legend is not equal to the number of args.")

  plt.figure()

  # Draw plot
  plt_list = list() if legend_names is not None else None
  for cur in args:
    cur_plt, = plt.plot(range(1, len(cur) + 1), cur)  # unpack
    if legend_names is not None: plt_list.append(cur_plt)

  # Add effects
  if legend_names is not None: plt.legend(handles=plt_list, labels=legend_names)
  if x_name is not None: plt.xlabel(x_name)
  if y_name is not None: plt.ylabel(y_name)
  if percent:
    plt.ylim(0, 1)
    plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))

  # plt.show()  # Note: This will lead to show the figure one by one.


# ------------------------------------------------------------
# --------------- Function --- Loading model
# ------------------------------------------------------------
def load_model(model, file_path, device=None):
  """See ModelManager.load function in data_structure module."""
  ModelManager.load(model, file_path, device)
