import yaml
import os
from .state import env

with open(os.path.join(os.getcwd(), 'config.yml')) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    env.config = config
