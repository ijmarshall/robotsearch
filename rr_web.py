from flask import Flask
app = Flask(__name__)

# @TODO (?) consider refactoring
rct_clf = rct_robot.RCTRobot()
from robotsearch.robots import rct_robot

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/upload_RIS")
def upload_RIS():
    pass 

if __name__ == '__main__':
    app.run(debug=True)