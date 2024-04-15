from SafeCity import app, db
from SafeCity.models import User

# Define a function to create a user with predefined values
def create_user():
    # Create a new user
    user = User(
        username='admin',
        password='admin',
        location='Basement',
        e_mail='abdorafat73646854@gmail.com'
    )
    
    # Add the user to the database session
    db.session.add(user)
    
    # Commit the session to persist the changes
    db.session.commit()

# Run the function to create the user
create_user()


# go to terminal and write this  'python create_user.py' to excute this statment