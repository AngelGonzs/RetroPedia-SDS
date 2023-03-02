# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage

class Backend:

    def __init__(self):
        # Instantiate a new client for Cloud Storage
        self.client = storage.Client()

        # Get a reference to the GCS bucket
        self.bucket = self.client.bucket('web-uploads')
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self, file):
        # Create a new blob in the bucket and upload the file data
        blob = self.bucket.blob(file.filename)
        blob.upload_from_file(file)
        

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass

