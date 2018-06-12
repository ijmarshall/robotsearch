from flask import Flask
from flask import render_template

app = Flask(__name__)

# @TODO (?) consider refactoring

# from robotsearch.robots import rct_robot
# rct_clf = rct_robot.RCTRobot()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/upload_RIS")
def upload_RIS():
    pass 


@app.route('/start_page')
def start_page():
    return render_template('select_ris_to_upload.html')


if __name__ == '__main__':
    app.run(debug=True)