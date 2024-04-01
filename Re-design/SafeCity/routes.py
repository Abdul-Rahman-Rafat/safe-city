import os
import sqlite3
from SafeCity import app
from flask import render_template ,redirect , url_for , flash ,jsonify , request
from SafeCity import db
#when added a table in db u should add his import here too
from SafeCity.models import User , Snapshots , Camera
from SafeCity.forms import RegisterForm , LoginForm
from flask_login import login_user , logout_user , login_required , current_user


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
@login_required
def home():
    alerts_count = len(Snapshots.query.all())
    return render_template("home.html")

@app.route("/admin")
@login_required
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
@login_required
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
@login_required
def live():
    return render_template("livestream.html")

@app.route("/analytics")
@login_required
def analysis():
    return render_template("analytics.html")


#alert_count
@app.route("/get_alert_count")
@login_required
def get_alert_count():
    if current_user.username == "admin":
        # If the current user is admin, fetch all alerts
        alerts_count = len(Snapshots.query.all())
    else:
        alerts_count = Snapshots.query.filter_by(Alert_sentTo=current_user.username).count()
    return jsonify(alertCount=alerts_count)



@app.route("/logout")
@login_required
def logout():
    print( 'bye')
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('signin'))  # Redirect to the login page

# Function to send notifications
def send_notification(message):
    # Implement your notification logic here
    # This could be sending an email, push notification, or any other method
    print(f"Notification sent: {message}")

# Endpoint to handle notifications
@app.route("/notify", methods=["POST"])
def notify():
    # Check if the alerts table has increased in row count
    previous_row_count = app.config.get("previous_row_count", 0)
    current_row_count = Snapshots.query.count()

    if current_row_count > previous_row_count:
        # Trigger notification if row count has increased
        send_notification("New alerts have been added to the database!")
        # Update the previous_row_count in the app config
        app.config["previous_row_count"] = current_row_count

    return jsonify({"message": "Notification check complete"}), 200



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

@app.route('/users', methods=['GET', 'POST'])
@login_required
def admin_users():
    users = User.query.all()
    return render_template('users.html', users=users)

