import os 

from flask import Flask, request, redirect, url_for
from flask import render_template

from werkzeug.utils import secure_filename

UPLOAD_DIR_NAME = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'ris'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = resource_path = os.path.join(app.root_path, UPLOAD_DIR_NAME) 

# @TODO (?) consider refactoring

# from robotsearch.robots import rct_robot
# rct_clf = rct_robot.RCTRobot()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        import pdb; pdb.set_trace()
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_RIS',
                                    filename=filename))

    return render_template("select_ris_to_upload.html")

methods=['GET', 'POST']
@app.route("/uploaded_RIS")
def uploaded_RIS():
    import pdb; pdb.set_trace()


#@app.route('/start_page')
#def start_page():
#    return render_template('select_ris_to_upload.html')


if __name__ == '__main__':
    app.run(debug=True)