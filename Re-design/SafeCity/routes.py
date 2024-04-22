import os
import sqlite3
from SafeCity import app
from flask import render_template ,redirect , url_for , flash ,jsonify , request ,abort
from SafeCity import db
#when added a table in db u should add his import here too
from SafeCity.models import User , Snapshots , Camera
from SafeCity.forms import RegisterForm , LoginForm 
from flask_login import login_user , logout_user , login_required , current_user

previousAlertCount = 0
def get_flash_alert():
    global previousAlertCount
    # Fetch current count of snapshots
    currentAlertCount = len(Snapshots.query.all())
    # Check if the current count is greater than the previous count
    if currentAlertCount > previousAlertCount:
        flash("New snapshots have been detected!", category="info")
        previousAlertCount = currentAlertCount
    


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
    get_flash_alert()    # flash to see the notification
    alerts_count = len(Snapshots.query.all())
    return render_template("home.html")


@app.route("/admin")
@login_required
def admin():
    get_flash_alert()    # flash to see the notification
    if current_user.username == 'admin':
        alerts_count = len(Snapshots.query.all())
        users = User.query.all()
        return render_template("admin.html", users=users)

    else:
        abort(403)

@app.route("/alerts")
@login_required
def snapshot():

    get_flash_alert()    # flash to see the notification


    # Fetch all alerts
    snaps = Snapshots.query.all()
       

    if current_user.username == "admin":
        # If the current user is admin, fetch all alerts
        alerts_count = len(Snapshots.query.all())
        snaps = Snapshots.query.all()
       
        return render_template("alerts.html",snaps = snaps)
    else:
         snaps=Snapshots.query.filter_by(Alert_sentTo=current_user.username)
         return render_template("alerts.html",snaps = snaps )
   

@app.route("/delete_snapshot/<int:snapshot_id>", methods=['DELETE'])
@login_required
def delete_snapshot(snapshot_id):
    snapshot = Snapshots.query.get_or_404(snapshot_id)
    db.session.delete(snapshot)
    db.session.commit()
    return jsonify({'message': 'Snapshot deleted successfully'})





@app.route("/signup" , methods=['POST','GET'])
@login_required
def signup():
    get_flash_alert()    # flash to see the notification

    if current_user.username == 'admin':
        form = RegisterForm()
        if form.validate_on_submit():
            user_to_create = User(username=form.username.data,
                                password=form.password.data,
                                location=form.location.data ,
                                e_mail=form.e_mail.data
                                )
            db.session.add(user_to_create)
            db.session.commit()
            flash(f'A user was added successfully ', category='success')
            return redirect(url_for('signup'))

        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger')
        
        
        return render_template("signup.html",form=form)

    else:
         abort(403)


@app.route("/livestream")
@login_required
def live():
    get_flash_alert()    # flash to see the notification
    return render_template('livestream.html')

@app.route("/analytics")
@login_required
def analysis():
    get_flash_alert()    # flash to see the notification
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


@app.route("/delete_user/<int:user_id>", methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Delete associated rows from Snapshots table
    snapshots_to_delete = Snapshots.query.filter_by(owned_user=user).all()
    for snapshot in snapshots_to_delete:
        db.session.delete(snapshot)
    
    # Delete the user
    db.session.delete(user)
    
    # Commit changes to the database
    db.session.commit()
    
    return jsonify({'message': 'User and associated snapshots deleted successfully'})




@app.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='success')
    return redirect('signin')



#################

# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = RegisterForm()
	name_to_update = User.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.location = request.form['location']
		name_to_update.e_mail = request.form['e_mail']
		name_to_update.password = request.form['password']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated Successfully!",category='success')
			return render_template("update.html", form=form,name_to_update = name_to_update, id=id)
		except:
			flash("Error!  Looks like there was a problem...try again!" , category='danger')
			return render_template("update.html", form=form,name_to_update = name_to_update,id=id)
	else:
		return render_template("update.html", form=form,name_to_update = name_to_update,id = id)

    
     
from datetime import datetime, timedelta

@app.route('/get_snapshot_data')
@login_required
def get_snapshot_data():
    # Check if the current user is an admin
    if current_user.username=='admin':
        # Fetch snapshots for all users
        snapshot_data_all_users = Snapshots.query.all()
    else:
        # Fetch snapshots associated with the current user
        snapshot_data_all_users = current_user.alerts
    
    # Count the number of snapshots per location
    snapshot_counts_location = {}
    for snapshot in snapshot_data_all_users:
        loc = snapshot.Loc
        if loc in snapshot_counts_location:
            snapshot_counts_location[loc] += 1
        else:
            snapshot_counts_location[loc] = 1
    
    # Fetch timestamps for all snapshots
    snapshot_data_time = db.session.query(Snapshots.Time).all()
    
    # Count the number of snapshots per day
    snapshot_counts_time = {}
    for snapshot_time in snapshot_data_time:
        # Extract the date from the timestamp
        day_key = snapshot_time[0].strftime('%Y-%m-%d')
        if day_key in snapshot_counts_time:
            snapshot_counts_time[day_key] += 1
        else:
            snapshot_counts_time[day_key] = 1
    
    # Generate labels for the last 7 days
    today = datetime.utcnow().date()
    labels_time = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

    # Create counts for each label, defaulting to 0 if no data for a day
    counts_time = [snapshot_counts_time.get(label, 0) for label in labels_time]

    return jsonify(labels_location=list(snapshot_counts_location.keys()), counts_location=list(snapshot_counts_location.values()), labels_time=labels_time, counts_time=counts_time)






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
