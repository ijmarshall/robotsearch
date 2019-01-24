import logging
import os
import json


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

DEBUG_MODE = str2bool(os.environ.get("DEBUG", "false"))
LOG_LEVEL = (logging.DEBUG if DEBUG_MODE else logging.INFO)
_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_ROOT = os.path.join(_ROOT, 'data')
logging.basicConfig(level=LOG_LEVEL, format='[%(levelname)s] %(name)s %(asctime)s: %(message)s')
log = logging.getLogger(__name__)




