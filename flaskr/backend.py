from google.cloud import storage
from flask import Flask
import io
import hashlib
from flask import Flask, render_template


# Initialize:
app = Flask(__name__)



class Backend:
    """
    The Backend serves as a tool to assist our Frontend with user authentication,
    storage, data manipulation, acquiring data and anything else necessary to assist
    the frontend in its tasks.

    Authentication Methods:

        `sign_in` and `sign_up` are our authentication methods, they take the same parameters,
        `username` and `password` they verify whether the username exists or not, and depending
         on what is to be done next, then it will either add the password to the User Blob or
         compare the password passed by the frontend to the one that is already stored in the
         blob.
        
    Upload Method:


    Getter Methods:


    Attributes:
        web_uploads_client  - 

        wiki_content_client - 

        web_uploads_bucket  - 

        wiki_content_bucket - 
    """
    
    def __init__(self):
        # Instantiate a new client for Cloud Storage
        self.web_uploads_client = storage.Client()
        self.wiki_content_client = storage.Client()

        # Get a reference to the web-uploads bucket
        self.web_uploads_bucket = self.web_uploads_client.bucket('web-uploads')

        # Get a reference to the wiki-content bucket
        self.wiki_content_bucket = self.wiki_content_client.bucket('wiki-content-bucket')
        
        # Set the default bucket to wiki-content-bucket
        self.bucket = self.wiki_content_bucket



        # Initiate buckets and clients for `sign_in` and `sign_up` methods

        self.user_client = storage.Client()
        self.password_bucket = self.user_client.bucket("passwords-bucket")

    def get_all_page_names(self):
        # List all the blobs in the wiki-content bucket
        blobs = self.bucket.list_blobs()

        # Extract the name of each blob (page) and add it to a list
        page_names = []
        for blob in blobs:
            # Ignore blobs that are not files (i.e., folders)
            if not blob.name.endswith('/'):
                # Extract the page name from the blob name (remove the file extension)
                page_name = blob.name.split('.')[0]
                page_names.append(page_name)

        return page_names
        
    def get_wiki_page(self, name):
        #Lists all the blobs in the wiki-content bucket
        blobs = self.bucket.list_blobs()

        #Search through each blob and see if it's the same as page name provided
        for blob in blobs:
            #Ignore blobs that are not files
            if not blob.name.endswith('/'):
                if(name == blob.name):
                    return render_template(name)
        return None
    
    def get_page_text(self, page_name):
        # Get a reference to the blob that contains the content for the specified page
        blob = self.bucket.get_blob(f"{page_name}.txt")

        if blob is not None:
            # Download the content from the blob
            content = blob.download_as_text()

            # Return the content
            return content

        else:
            # If the blob does not exist, return None
            return None

    def upload(self, file):
        # Create a new blob in the web-uploads bucket and upload the file data
        blob = self.web_uploads_bucket.blob(file.filename)
        blob.upload_from_file(file)
        


    def sign_up(self, username, password):
        """
        This method allows users to sign up for our Wiki! It takes a username and
        a password. The username should be unique, so if it already exists, then the
        user should input a new username.

        Args:
            username - As previously said, this should be a unique username. Every username
            will have a blob named after it, and it's contents will be the hashed password.

            password - a password passed form the frontend, it should be prefixed and if
            the username is indeed unique, then we will store this password to the blob
            after being hashed.


        Returns:
            Boolean value determining if the process went right or not. The only case
            in which it will return `False` is if the username already exists, otherwise
            it will create the blob for the User and return True.
        
        """  
        blob_name = username
        user_password = password

        blob_contents = str(int(hashlib.sha256(user_password.encode("utf-8")).hexdigest(),16))


        # Ahead, we will check if a blob for the username already exists.
        blob_check = self.password_bucket.blob(blob_name)

        if blob_check.exists():
            print("Username already exists, please try a different username")
            # We shouldn't exactly print, but somehow render in the sign-up page
            return False
        else:
            # If blob doesn't exist, create new username with password
            blob_check.upload_from_string(blob_contents)
            print("User succesfully created")
            return True

        


    
    def sign_in(self, username, password):
        """
        This is our method to authenticate the sign in process. It takes a username and a
        password provided from the `request.form` in the frontend and verifies if these 
        match up with the information in the `passwords-bucket`. It first checks if the
        username exists, and if it does, then it will check if the password is right.

        Args:
            username - This is a unique username, every user should have one and it is also
            how the blob will be named, that is, every user will have a unique blob.

            password - This password, which is passed from the frontend with a prefix, and
            it will be hashed within this method to then check if it matches with the 
            already hashed password that is in the blob.

        Returns:
            Boolean value which determines whether the authentication of the user went right
            or not. In cases the username doesn't exist or the password doesn't match up, then
            it will return False.
        
        """
        
     
        blob_name = username
        blob_check = self.password_bucket.blob(blob_name)

        if blob_check.exists():
            
            # Get the hashed password to later compare it to the data inside the username blob
            user_password = password
            hashed_password = str(int(hashlib.sha256(user_password.encode("utf-8")).hexdigest(),16))
            

            # We download the hashed password as a string, thus we must compare it as one
            blob_contents = str(blob_check.download_as_string()) # REAL PASSWORD
            blob_contents = blob_contents[2:-1]

            if hashed_password == blob_contents:
                #Everything good, welcome 
                return True

            else:
                print("Wrong password or username, please try again")

        else:
            print("Username doesn't exist")

        return False

    def get_image(self, name):
        #Grabs a list of all the blobs in a 
        blobs = self.web_uploads_bucket.list_blobs()
        for blob in blobs:
            #Once again ignoring blobs that are not files
            if not blob.name.endswith('/'):
                #Compares the name passed in the function to the name of the current blob.
                if(name == blob.name):
                    img_file = open(blob.name, "r")
        img_data = img_file.read()
        img_bytes = io.BytesIO(img_data)
        return img_bytes    
                


    def get_user(self, ID):

        """
        This method serves as a helper for the `login_manager()` from Flask Login.
        It's purpose is to check if a user of a specific ID exists or not.

        Args:
            ID - This is the ID of the User, it it equivalent to a unique username.
        
        Returns:
            Boolean which determines if the ID exists as a user or not.
        """        
        blob_name = ID
        blob_check = self.password_bucket.blob(blob_name)
        return blob_check.exists()
