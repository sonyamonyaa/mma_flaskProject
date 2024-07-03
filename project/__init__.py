import os
from flask import Flask
from flask_dropzone import Dropzone
app = Flask(__name__)

from project import routes

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE= '.csv',
    DROPZONE_MAX_FILE_SIZE=3, # in MB
    DROPZONE_MAX_FILES=1,
    DROPZONE_UPLOAD_ON_CLICK=True
)
dropzone = Dropzone(app)