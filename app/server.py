#!~/PycharmProjects/__VENV__/venv_nyxae/bin/python

from app.cnfParser import CNFparser
from app.app_logic import store_logic
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import uuid
import shutil
import time


# TODO 1a : Upload multiple files at once and zip into a single folder and store timer
# TODO 1b : Encrypt the zipped file on the server and
# TODO 1c : Write Email server to email key to recipient directly from the server

# TODO 2a : Rename the zipped file to a hashed key from /dev/urandom
# TODO 2b : Map the hashed key to a memory in db

# TODO 3a : Implement multi-threading for headless automation scripts for clearing db
# TODO 3b : Follow Linux time for file expiry (in seconds) from the server.

# TODO 4  : Setup downloads and auto remove encrypted-zip after download regardless of the timer.

# TODO 5  : A commandline client


__author__ = "salmansamie"


app = Flask(__name__, template_folder='templates')

# Default system internal configurations
app.config['SERVER_IP'] = CNFparser.config_parsed()[0]
app.config['SERVER_PORT'] = CNFparser.config_parsed()[1]
app.config['UPLOAD_FOLDER'] = CNFparser.config_parsed()[3]
app.config['ALLOWED_EXTENSIONS'] = CNFparser.config_parsed()[2]

TIMER_KVAL = CNFparser.timer_KeyVal()[0]
TIMER_LIST = CNFparser.timer_KeyVal()[1]


def mapped_timer(user_timer):
    linuxTime = int(time.time())                # get linux timestamp and convert float to int
    for key, val in TIMER_KVAL.items():
        if key == user_timer:
            return linuxTime + TIMER_KVAL[key]


# Checks for allowed extensions
def allowed_file(args):
    # Split extension and check allowed extension in config.ini
    chk_config = '.' in args and args.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    return chk_config


@app.route("/index")
@app.route("/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files_list = request.files.getlist('file_href')     # 'file_ref' refers to html name attr
        user_timer = request.form.get('TIMER')              # get user timer
        expiry_timer = mapped_timer(user_timer)             # timer set as int
        print(expiry_timer)     # 1518493207

        # The 4 consequtive lines below will create hashed directory
        UPLOAD_BASE = app.config['UPLOAD_FOLDER']
        UID = uuid.uuid4().hex                              # 32-bit hashed uuid
        HASHED_PATH = os.path.join(UPLOAD_BASE + UID)       # Set path to hashed folder
        os.makedirs(HASHED_PATH)                            # Create hashed folder path
        print(HASHED_PATH)      # /tmp/nyxStorage/85a2d35cd76d486989eab7385e07d012

        # Recursively input file names securely and save into hashed directory
        for each in files_list:
            if each and allowed_file(each.filename):        # .filename is referring to extension
                filename = secure_filename(each.filename)
                each.save(os.path.join(HASHED_PATH, filename))      # Save each files to hashed dir

        # Create compressed dir of the hashed dir and remove original dir
        shutil.make_archive(HASHED_PATH, 'zip', HASHED_PATH)
        shutil.rmtree(HASHED_PATH, ignore_errors=True)

        if isinstance(expiry_timer, int):                           # Allow int only, active until
            if expiry_timer in range(1519238051, 1676937599000):    # February 20, 2023 11:59:59 PM
                store_logic(HASHED_PATH, expiry_timer)
        return redirect(url_for('upload'))

    return render_template('index.html', TIMER=TIMER_LIST)


@app.route('/_get_data/', methods=['POST'])
def _get_data():
    myList = ['Element1', 'Element2', 'Element3']
    return render_template('response.html', myList=myList)


if __name__ == "__main__":
    app.run(host=app.config['SERVER_IP'], port=app.config['SERVER_PORT'], debug=True)
