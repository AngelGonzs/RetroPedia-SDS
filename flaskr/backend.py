from google.cloud import storage

from flask import Flask
from flask import render_template
from flask import request
import hashlib


# Initialize:
app = Flask(__name__)



# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage

class Backend:
    
    def __init__(self):
        # Instantiate a new client for Cloud Storage
        self.web_uploads_client = storage.Client()
        self.wiki_content_client = storage.Client()

        # Get a reference to the web-uploads bucket
        self.web_uploads_bucket = self.web_uploads_client.bucket('web-uploads')

        # Get a reference to the wiki-content bucket
        self.wiki_content_bucket = self.wiki_content_client.bucket('wiki-content-bucket')

        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        # List all the blobs in the wiki-content bucket
        blobs = self.wiki_content_bucket.list_blobs()

        # Extract the name of each blob (page) and add it to a list
        page_names = []
        for blob in blobs:
            # Ignore blobs that are not files (i.e., folders)
            if not blob.name.endswith('/'):
                # Extract the page name from the blob name (remove the file extension)
                page_name = blob.name.split('.')[0]
                page_names.append(page_name)

        return page_names

    def upload(self, file):
        # Create a new blob in the web-uploads bucket and upload the file data
        blob = self.web_uploads_bucket.blob(file.filename)
        blob.upload_from_file(file)
        

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




    def sign_up(self, username, password):

        storage_client = storage.Client()
        passwords_bucket = storage_client.bucket("passwords-bucket")

        
        blob_name = username
        user_password = password

        blob_contents = str(int(hashlib.sha256(user_password.encode("utf-8")).hexdigest(),16))


        # Ahead, we will check if a blob for the username already exists.
        blob_check = passwords_bucket.blob(blob_name)

        if blob_check.exists():
            print("Username already exists, please try a different username")
            # We shouldn't exactly print, but somehow render in the sign-up page
            return False
        else:
            # If blob doesn't exist, create new username with password
            blob_check.upload_from_string(blob_contents)
            print("User succesfully created")
            return True

        

    """
    Checks if a password, when hashed, matches the password in the user bucket.

        APPROACH: First, we must make sure that the username is right, for this 
        we will check in a similar manner as it was done in the `sign_up` method.

        Later, when confirming that this username exists, we will read the contents
        of it's blob

        Will return true if the user is properly signed in, otherwise it will return
        false so that then frontend will manage this.

    """
    
    def sign_in(self, username, password):

        storage_client = storage.Client()
        password_buckets = storage_client.bucket("passwords-bucket")
        

        
            
        # Get the username from the form, and then check if a blob exists for the username.
        blob_name = username
        blob_check = password_buckets.blob(blob_name)

        if blob_check.exists():
            
            # Get the hashed password to later compare it to the data inside the username blob
            user_password = password
            hashed_password = str(int(hashlib.sha256(user_password.encode("utf-8")).hexdigest(),16))
            

            # We download the hashed password as a string, thus we must compare it as one
            blob_contents = str(blob_check.download_as_string()) # REAL PASSWORD
            blob_contents = blob_contents[2:-1]

            print("USERNAME" ,blob_name)
            print( "INPUT PASSWORD", hashed_password)
            print(" USER PASSWORD ", blob_contents, type(blob_contents))
            if hashed_password == blob_contents:
                print("Everything good, welcome")
                return True

            else:
                print("Wrong password or username, please try again")

        else:
            print("Username doesn't exist")

        return False


    def get_image(self):
        pass


    def get_user(self, ID):
        storage_client = storage.Client()
        password_buckets = storage_client.bucket("passwords-bucket")
        
        blob_name = ID
        blob_check = password_buckets.blob(blob_name)

        return blob_check.exists()
