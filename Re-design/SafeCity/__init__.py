from flask import Flask, render_template, Response, request, session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import LoginManager

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from flask_bcrypt import Bcrypt

from werkzeug.utils import secure_filename
import os
import cv2
#from YOLO_Video import video_detection , video_detection2
import numpy as np


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SafeCity.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.app_context().push()


from SafeCity import routes 


app.config['SECRET_KEY'] = '2b7fa43855102cc6bde6984c'


# app.config['UPLOAD_FOLDER'] = r'C:\Users\yassi\Desktop\web app\crowd videos'
#
# class UploadFileForm(FlaskForm):
#     file = FileField("File", validators=[InputRequired()])
#     submit = SubmitField("Run")

# def generate_frames_web(path_x):
#     yolo_output = video_detection(path_x)
#     for detection_ in yolo_output:
#         ref, buffer = cv2.imencode('.jpg', detection_)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

