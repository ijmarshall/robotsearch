#
#   RobotPICO
#
#
#
from robotpico.robots import cochrane_pico_robot
import json
from flask import Flask, request
import os

app = Flask(__name__)

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

DEBUG_MODE = str2bool(os.environ.get("DEBUG", "true"))

picobot = cochrane_pico_robot.CochranePicoRobot()

@app.route('/annotate', methods=['POST'])
def annotator():
    """
    processes JSON and returns for calls from web API
    """
    json_data = request.json
    annotations = picobot.annotate(json_data)
    return json.dumps(annotations)


