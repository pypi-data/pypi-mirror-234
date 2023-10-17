import os
import yaml

BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)))
SRC_PATH = os.path.join(BASE_PATH,'src')

default_file_name = 'dev.yaml'

class Config(object):

  config_dir = os.path.join(SRC_PATH, 'config')

  def __init__(self, file_name=default_file_name):
    self.config_path = os.path.join(self.config_dir,file_name)
    self.config = {}

  def get_config(self):
    with open(self.config_path) as f:
      self.config = yaml.load(f, Loader=yaml.FullLoader)
    return self.config
