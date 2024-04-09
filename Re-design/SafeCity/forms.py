from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField,ValidationError
from wtforms.validators import Length , DataRequired
from SafeCity.models import User ,  Camera



class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

            

    username = StringField(label='Username' , validators=[Length(min=3,max=20),DataRequired()])  
    password = PasswordField(label='Password' , validators=[Length(max=20),DataRequired()]) 
    location = StringField(label='Location', validators=[DataRequired()])  
    #camera_id = BooleanField(label='CameraID',validators=[DataRequired()])
    submit = SubmitField(label='Sign up')




class LoginForm(FlaskForm):
    username = StringField(label='Username' , validators=[Length(min=3,max=20),DataRequired()])  
    password = PasswordField(label='Password' , validators=[Length(max=20),DataRequired()]) 
    submit = SubmitField(label='Sign in')



class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    password = PasswordField('Password' , validators=[Length(max=20),DataRequired()]) 
    camera_id = StringField('Camera ID')
    submit = SubmitField('Save')

class UpdatePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')