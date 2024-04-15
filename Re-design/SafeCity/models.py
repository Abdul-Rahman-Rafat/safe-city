from SafeCity import db
from SafeCity import bcrypt
from SafeCity import func # for time
from SafeCity import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    location = db.Column(db.String(length=60), nullable=False)
    e_mail = db.Column(db.String(length=50), nullable=False, unique=True)
    camera_id = db.Column(db.Integer()) #unique=True or False ?
    
    #relationship between User and Snapshots
    alerts = db.relationship('Snapshots', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



class Snapshots(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Detection_img_ref = db.Column(db.String(length=100), nullable=False)
    Detection_type = db.Column(db.String(length=30), nullable=False)
    Loc = db.Column(db.String(length=100), nullable=False)    
    Time = db.Column(db.DateTime(timezone=True),server_default=func.now())

    #relationship between User and Snapshots
    Alert_sentTo = db.Column(db.String(length=50), db.ForeignKey('user.username'), nullable=False)

    

class Camera(db.Model,UserMixin):
    camera_id = db.Column(db.Integer(), primary_key=True)
    limit_crowd = db.Column(db.Integer(), nullable=False)



    def __repr__(self):
        return f'Snapshots {self.Loc}'