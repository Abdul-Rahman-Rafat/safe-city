import os
import sqlite3
from SafeCity import app
from flask import render_template ,redirect , url_for , flash ,jsonify , request ,abort,Response
from SafeCity import db
#when added a table in db u should add his import here too
from SafeCity.models import User , Snapshots , Camera
from SafeCity.forms import RegisterForm , LoginForm 
from flask_login import login_user , logout_user , login_required , current_user
import cv2
from SafeCity.YOLO_Video import model


def setcounts(count,camera):
    # Construct the SQL UPDATE statement
    conn = sqlite3.connect(r'C:\Users\yassi\Desktop\safecity site new\safe-city\Re-design\instance\SafeCity.db')
    cursor = conn.cursor()
    update_query = """
        UPDATE camera
        SET limit_crowd = ?
        WHERE camera_id = ?
        
    """

    # Execute the update query
    cursor.execute(update_query, (count, camera))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()


def setmodel_type(camera, model_type):
    conn = sqlite3.connect(r'C:\Users\yassi\Desktop\safecity site new\safe-city\Re-design\instance\SafeCity.db')
    cursor = conn.cursor()
    update_query = """
        UPDATE camera
        SET model_type = ?
        WHERE camera_id = ?
    """
    cursor.execute(update_query, (model_type, camera))
    conn.commit()
    cursor.close()
    conn.close()

def get_limit(camera_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(r'C:\Users\yassi\Desktop\safecity site new\safe-city\Re-design\instance\SafeCity.db')
    cursor = conn.cursor()

    cursor.execute('SELECT limit_crowd FROM camera WHERE camera_id = ?', (camera_id,))
    limit = cursor.fetchone()

    # Close the connection
    conn.close()
    return limit[0]


def get_model_type(model_type):
    
    conn = sqlite3.connect(r'C:\Users\yassi\Desktop\safecity site new\safe-city\Re-design\instance\SafeCity.db')
    cursor = conn.cursor()

    cursor.execute('SELECT model_type FROM camera WHERE camera_id = ?', (model_type,))
    model_type_ = cursor.fetchone()

    
    conn.close()
    return model_type_[0]

def get_location(camera_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(r'C:\Users\yassi\Desktop\safecity site new\safe-city\Re-design\instance\SafeCity.db')
    cursor = conn.cursor()

    cursor.execute('SELECT location FROM camera WHERE camera_id = ?', (camera_id,))
    loc = cursor.fetchone()

    cursor.execute('SELECT coordinates FROM camera WHERE camera_id = ?', (camera_id,))
    coroodinate = cursor.fetchone()
    # Close the connection
    conn.close()
    print(loc[0])
    return loc[0],coroodinate[0]

#datetime.now()

# previousAlertCount = 0
# def #get_flash_alert():
#     global previousAlertCount
#     # Fetch current count of snapshots
#     currentAlertCount = len(Snapshots.query.all())
#     # Check if the current count is greater than the previous count
#     if currentAlertCount > previousAlertCount:
#         flash("New snapshots have been detected!", category="info")
#         previousAlertCount = currentAlertCount
    
limit1 =  0
limit2 = 0 
model_type_ = ""
model_type_2 = ""

def generate_frames_web(path_x,user_info,user_loc , user_mail , CameraID , coroodinate):
    limit1 = get_limit(0) 
    model_type_ = get_model_type(0)
    if model_type_ == "Gun Model":
        limit1 = -1

    yolo_output = model(path_x,user_info,user_loc,user_mail, CameraID,coroodinate,limit1,model_type=model_type_)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



        
@app.route('/webapp')
def webapp():
    user_info=current_user.username
    
    user_mail = current_user.e_mail
    CameraID = current_user.CameraID[1]
    print(CameraID)
    user_loc= get_location(camera_id=CameraID)

    
    return Response(generate_frames_web(path_x=int(CameraID),user_info=user_info,user_loc=user_loc[0] , user_mail=user_mail,CameraID=CameraID, coroodinate=user_loc[1]), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames_web2(path_x,user_info,user_loc , user_mail,CameraID,coroodinate):
    limit2 = get_limit(1)
    model_type_2 =get_model_type(1)  
    if model_type_2 == "Gun Model":
        limit2 = -1
    
    yolo_output = model(path_x,user_info,user_loc,user_mail,CameraID,coroodinate,limit2,model_type= model_type_2)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        
@app.route('/webapp2')
def webapp2():
    user_info=current_user.username
 
    user_mail = current_user.e_mail
    CameraID = current_user.CameraID[0]
    print(CameraID)
    user_loc= get_location(camera_id=CameraID)

    print(CameraID)
    return Response(generate_frames_web2(path_x=int(CameraID),user_info=user_info,user_loc=user_loc[0] , user_mail=user_mail,CameraID=CameraID,coroodinate=user_loc[1]), mimetype='multipart/x-mixed-replace; boundary=frame')




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
@app.route("/templates/home")
@app.route("/update/home")

@login_required
def home():
    #get_flash_alert()    # flash to see the notification
    alerts_count = len(Snapshots.query.all())
    return render_template("home.html")

@app.route("/admin")
@app.route("/templates/admin")
@app.route("/update/admin")

@login_required
def admin():
    #get_flash_alert()    # flash to see the notification
    if current_user.username == 'admin':
        alerts_count = len(Snapshots.query.all())
        users = User.query.all()
        return render_template("admin.html", users=users)

    else:
        abort(403)

@app.route("/alerts")
@app.route("/templates/alerts")
@app.route("/update/alerts")
@login_required
def snapshot():

    #get_flash_alert()    # flash to see the notification


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
@app.route("/templates/signup" , methods=['POST','GET'])
@app.route("/update/signup" , methods=['POST','GET'])
@login_required
def signup():
    #get_flash_alert()    # flash to see the notification

    if current_user.username == 'admin':
        form = RegisterForm()
        if form.validate_on_submit():
            user_to_create = User(username=form.username.data,
                                password=form.password.data,
                                location=form.location.data ,
                                e_mail=form.e_mail.data,
                                CameraID = form.CameraID.data  
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


@app.route('/handle_people_count', methods=['POST'])
@login_required
def handle_people_count():
    people_count_webapp1 = request.form.get('people_count_webapp1')
    people_count_webapp2 = request.form.get('people_count_webapp2')
    model_webapp1 = request.form.get('model_webapp1')
    model_webapp2 = request.form.get('model_webapp2')

    print(model_webapp1)
    print(model_webapp2)


    setmodel_type(0, model_webapp1)
    setmodel_type(1,model_webapp2)
    setcounts(people_count_webapp1 , 0)
    setcounts(people_count_webapp2,1)
    

    # Redirect back to the livestream page
    return redirect(url_for('live'))

@app.route('/livestream')
@app.route('/templates/livestream')
@app.route('/update/livestream')
@login_required
def live():
    return render_template('livestream.html')

@app.route("/analytics")
@app.route("/templates/analytics")
@app.route("/update/analytics")
@login_required
def analysis():
    #get_flash_alert()    # flash to see the notification
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

    
#charts     
from datetime import datetime, timedelta

@app.route('/get_snapshot_data')
@login_required
def get_snapshot_data():
    # Check if the current user is an admin
    if current_user.username == 'admin':
    # Fetch all snapshots
        snapshot_data_all_users = Snapshots.query.all()
    else:
    # Fetch snapshots associated with the current user
        snapshot_data_all_users = current_user.alerts


    # Countthe number of snapshots per location
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

    # Count the number of snapshots per detection type
    snapshot_counts_detection_type = {}
    for snapshot in snapshot_data_all_users:
        detection_type = snapshot.Detection_type
        if detection_type in snapshot_counts_detection_type:
            snapshot_counts_detection_type[detection_type] += 1
        else:
            snapshot_counts_detection_type[detection_type] = 1

    # Count the number of snapshots per CameraID -> 0 and CameraID -> 1
    count_camera_id_0 = 0
    count_camera_id_1 = 0
    for snapshot in snapshot_data_all_users:
        if snapshot.CameraID == 0:
            count_camera_id_0 += 1
        elif snapshot.CameraID == 1:
            count_camera_id_1 += 1



  # Count the number of snapshots per CameraID -> 0 and CameraID -> 1
    count_camera_id_0_fire = 0
    count_camera_id_1_fire = 0
    count_camera_id_0_gun = 0
    count_camera_id_1_gun = 0
    count_camera_id_0_person = 0
    count_camera_id_1_person = 0
    count_camera_id_0_knife = 0
    count_camera_id_1_knife = 0

    for snapshot in snapshot_data_all_users:
        if snapshot.CameraID == 0:
            if snapshot.Detection_type == 'fire':
                count_camera_id_0_fire += 1
            if snapshot.Detection_type == 'gun':
                count_camera_id_0_gun += 1
            if snapshot.Detection_type == 'person':
                count_camera_id_0_person += 1
            if snapshot.Detection_type == 'knife':
                count_camera_id_0_knife += 1
        elif snapshot.CameraID == 1:
            if snapshot.Detection_type == 'fire':
                count_camera_id_1_fire += 1
            if snapshot.Detection_type == 'gun':
                count_camera_id_1_gun += 1
            if snapshot.Detection_type == 'person':
                count_camera_id_1_person += 1
            if snapshot.Detection_type == 'knife':
                count_camera_id_1_knife += 1



    # Generate labels for the last 7 days
    today = datetime.utcnow().date()
    labels_time = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

    # Create counts for each label, defaulting to 0 if no data for a day
    counts_time = [snapshot_counts_time.get(label, 0) for label in labels_time]

    return jsonify(
        labels_location=list(snapshot_counts_location.keys()),
        counts_location=list(snapshot_counts_location.values()),
        labels_time=labels_time,
        counts_time=counts_time,
        labels_detection_type=list(snapshot_counts_detection_type.keys()),
        counts_detection_type=list(snapshot_counts_detection_type.values()),
        count_camera_id_0=count_camera_id_0,
        count_camera_id_1=count_camera_id_1,
        count_camera_id_0_fire=count_camera_id_0_fire,
        count_camera_id_1_fire=count_camera_id_1_fire,
        count_camera_id_0_knife=count_camera_id_0_knife,
        count_camera_id_1_knife=count_camera_id_1_knife,
        count_camera_id_0_gun=count_camera_id_0_gun,
        count_camera_id_1_gun=count_camera_id_1_gun,
        count_camera_id_0_person=count_camera_id_0_person,
        count_camera_id_1_person=count_camera_id_1_person
    )



