from google.cloud import storage

from flask import Flask
from flask import render_template
from flask import request
import hashlib


# Initialize:
app = Flask(__name__)



# TODO(Project 1): Implement Backend according to the requirements.


class Backend:

    def __init__(self):
        pass
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    """
    Adds data to the content bucket.
    """
    def upload(self):

        pass

    """
    Adds user data if it does not exist along with a hashed password.

        We will proceed by creating a Blob for every username. We will verify if the
        Username already exists by using the Blob.Exists() method, some worries with this
        could be:
            -Case sensitivity
            -That's it for now

        I don't exactly know which hash function we will use right now, so I'll use something
        basic from `hashlib` or something and later on change it.

    """



    @app.route('/signup', methods=['GET', 'POST'])
    def sign_up(self):

        storage_client = storage.Client()
        passwords_bucket = storage_client.bucket("passwords-bucket")

        if request.method == 'POST':
            blob_name = request.form['username']
            user_password = request.form['password']

            blob_contents = str(int(hashlib.sha256(user_password.encode("utf-8")).hexdigest(),16))


            # Ahead, we will check if a blob for the username already exists.
            blob_check = passwords_bucket.blob(blob_name)

            if blob_check.exists():
                print("Username already exists, please try a different username")
                # We shouldn't exactly print, but somehow render in the sign-up page
            else:
                # If blob doesn't exist, create new username with password
                blob_check.upload_from_string(blob_contents)
                print("User succesfully created")

        

    """
    Checks if a password, when hashed, matches the password in the user bucket.

        APPROACH: First, we must make sure that the username is right, for this 
        we will check in a similar manner as it was done in the `sign_up` method.

        Later, when confirming that this username exists, we will read the contents
        of it's blob

    """
    @app.route('/login', methods=['GET','POST'])
    def sign_in(self):

        storage_client = storage.Client()
        password_buckets = storage_client.bucket("passwords-bucket")
        

        if request.method == "POST":
            
            # Get the username from the form, and then check if a blob exists for the username.
            blob_name = request.form['username']
            blob_check = password_buckets.blob(blob_name)

            if blob_check.exists():

                # Get the hashed password to later compare it to the data inside the username blob
                user_password = request.form['password']
                hashed_password = str(int(hashlib.sha256(user_password.encode("utf-8")).hexdigest(),16))
                

                # We download the hashed password as a string, thus we must compare it as one
                blob_contents = blob_check.download_as_string().rstrip() # REAL PASSWORD

                if hashed_password == blob_contents:
                    print("Everything good, welcome")

                else:
                    print("Wrong password or username, please try again")

            else:
                print("Username doesn't exist")






    def get_image(self):
        pass
