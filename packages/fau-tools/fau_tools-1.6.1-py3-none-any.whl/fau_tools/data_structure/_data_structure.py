import time

import torch
from fau_tools import utils


class ModelManager:
  """Manage the traning model."""

  def __init__(self):
    self.loss, self.accuracy = None, None
    self.model = None
    self.epoch = None

  def update(self, model, loss, accuracy, epoch):
    """
    Update to the best model.

    Parameters
    ----------
    model    : current model
    loss     : current loss value
    accuracy : current accuracy rate
    epoch    : current epoch

    """
    if self.accuracy is None or self.accuracy < accuracy:
      self.loss, self.accuracy = loss, accuracy
      self.model = model
      self.epoch = epoch

  def save(self, file_name, only_param=True):
    """
    Save the selected(optimal) model.

    Parameters
    ----------
    file_name  : the name of the saved model
    only_param : whether only save the parameters of the model

    """
    file_name = f"{file_name}.pth"
    if only_param: torch.save(self.model.state_dict(), rf"{file_name}")
    else: torch.save(self.model, rf"{file_name}")
    utils.cprint(rf"{__class__.__name__}: save a model named {file_name} successfully!", color="green")

  @staticmethod
  def load(model, file_path, device=None):
    """
    Load the trained model that saved only parameters.

    A new feature added in version 1.0.0

    Parameters
    ----------
    model     : the structure of the model.
    file_path : the path of the trained model.
    device    : the calculating device used in pytorch; if None, will be determined automatically


    Returns
    -------
    After this method, the model will be loaded on `device` with the evaluation mode.

    """
    if device is None: device = utils.get_device()
    model.load_state_dict(torch.load(file_path, device))
    model.eval()

  def get_postfix(self): return f"{round(self.accuracy * 10000)}"  # 87.65%  ->  8765


class TrainRecorder:
  """Record the process of training."""

  def __init__(self):
    self.loss_list, self.accuracy_list = list(), list()

  def update(self, loss_value, accuracy):
    """
    Update the training recorder.

    Parameters
    ----------
    loss_value : the current loss value
    accuracy   : the current accuracy rate

    """
    self.loss_list.append(loss_value)
    self.accuracy_list.append(accuracy)

  def save(self, file_name):
    """
    Save the training process.

    Parameters
    ----------
    file_name : the name of the process file

    Returns
    -------
    Generate a csv_file; there are some columns recorded the values variation during training

    """
    file_name = rf"{file_name}.csv"
    with open(rf"{file_name}", "w") as file:
      col_list = ", ".join(("loss", "accuracy")) + "\n"
      file.write(col_list)
      for loss, accuracy in zip(self.loss_list, self.accuracy_list):
        line = f"{loss:.6f}, {accuracy:.6f}\n"
        file.write(line)

    utils.notify(f"{__class__.__name__}", f"Save a record file named {file_name} successfully!", notify_type="success")


class TimeManager:
  """Guess the training time costing."""

  def __init__(self):
    self.time_list = [time.time()]
    self.elapsed_time = 0

  def time_tick(self):
    cur_time = time.time()
    self.elapsed_time += cur_time - self.time_list[-1]
    self.time_list.append(cur_time)

  def get_average_time(self): return self.elapsed_time / (len(self.time_list) - 1)  # interval: len - 1

  def get_elapsed_time(self): return self.elapsed_time


class TrainRunner:
  # TODO: ...
  """Train runner."""

  def __init__(self):
    ...

  def before_train(self): ...
  def after_train(self): ...
