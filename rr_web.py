
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import logging
from datetime import datetime, timedelta

from flask import Flask, request, redirect, url_for, abort
from flask import render_template, send_from_directory

from werkzeug.utils import secure_filename

UPLOAD_DIR_NAME = 'uploads'
FILTERED_DIR_NAME = 'filtered'
ALLOWED_EXTENSIONS = set(['txt', 'ris', 'cgi']) # for ovidweb.cgi weird export extensions

log = logging.getLogger(__name__)
log.info("Welcome to RobotSearch server :)")

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = resource_path = os.path.join(app.root_path, UPLOAD_DIR_NAME)
app.config['FILTERED_FOLDER'] = os.path.join(app.root_path, FILTERED_DIR_NAME)

#app.secret_key = os.environ.get("SECRET", "super secret key")

from robotsearch.robots import rct_robot
rct_clf = rct_robot.RCTRobot()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

log.info("RobotSearch ready & awaiting contact...")
@app.route("/about")
def about():
    return render_template("about.html")

log.info("Ready")
@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        if 'file' not in request.files:
            return render_template("select_ris_to_upload.html")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            model = request.form['model']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_RIS',
                                    filename=filename,
                                    model=model))

    return render_template("select_ris_to_upload.html")

@app.route('/uploaded_RIS/<model>/<filename>')
def uploaded_RIS(filename, model):


    # auto choose the right model
    if model == 'sensitive':
        fc = 'svm'
    elif model == 'precise':
        fc = 'cnn'
    elif model == 'balanced':
        fc = 'svm_cnn'
    else:
        abort(404)

    f_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    RIS_data = open(f_path, 'r').read()
    filtered = rct_clf.filter_articles(RIS_data, filter_type=model, filter_class=fc)

    # ok, now dump out to file
    out_f_path =  os.path.join(app.config['FILTERED_FOLDER'], filename)
    with open(out_f_path, 'w') as out_f:
        out_f.write(filtered)

    download_path = url_for('download', filename=filename)
    download_file_name = "robotsearch-" + model + "-filter-" + filename
    return render_template("download_ready.html",
                            download_path=download_path,

                            target_file_name=download_file_name)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    f_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(app.config['FILTERED_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=False)

