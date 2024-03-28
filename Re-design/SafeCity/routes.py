import os
import sqlite3
from SafeCity import app
from flask import render_template ,redirect , url_for , flash ,g
from SafeCity import db
#when added a table in db u should add his import here too
from SafeCity.models import User , Snapshots , Camera
from SafeCity.forms import RegisterForm , LoginForm
from flask_login import login_user , logout_user , login_required , current_user

from flask import jsonify


@app.route("/signin", methods=['POST','GET'])
@app.route("/", methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Successfully login', category='success')
            if(attempted_user.username=="admin"):
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template("signin.html", form=form)



@app.route("/home")
def home():
    alerts_count = len(Snapshots.query.all())
    return render_template("home.html")

@app.route("/admin")
def admin():
    alerts_count = len(Snapshots.query.all())
    return render_template("admin.html")

@app.route("/alerts")
@login_required
def snapshot():
    if current_user.username == "admin":
        # If the current user is admin, fetch all alerts
        alerts_count = len(Snapshots.query.all())
        snaps = Snapshots.query.all()
       
        return render_template("alerts.html",snaps = snaps)
    else:
         snaps=Snapshots.query.filter_by(Alert_sentTo=current_user.username)
         return render_template("alerts.html",snaps = snaps )
   



@app.route("/signup" , methods=['POST','GET'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              password=form.password.data,
                              location=form.location.data
                              )
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'A user was added successfully ', category='success')
        return redirect(url_for('signup'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    
    
    return render_template("signup.html",form=form)




@app.route("/livestream")
def live():
    return render_template("livestream.html")

@app.route("/analytics")

def analysis():
    return render_template("analytics.html")



@app.route("/get_alert_count")
@login_required
def get_alert_count():
    if current_user.username == "admin":
        # If the current user is admin, fetch all alerts
        alerts_count = len(Snapshots.query.all())
    else:
        alerts_count = Snapshots.query.filter_by(Alert_sentTo=current_user.username).count()
    return jsonify(alertCount=alerts_count)


# @app.route('/', methods=['GET', 'POST'])
# def default():
#     session.clear()
#     return render_template('index.html')

# @app.route('/FrontPage', methods=['GET', 'POST'])
# def front():
#     form = UploadFileForm()
#     if form.validate_on_submit():
#         file = form.file.data
#         file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
#                                secure_filename(file.filename)))
#         session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
#                                              secure_filename(file.filename))
#     return render_template('videoprojectnew.html', form=form)
#
# @app.route('/webapp')
# def webapp():
#     return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')
