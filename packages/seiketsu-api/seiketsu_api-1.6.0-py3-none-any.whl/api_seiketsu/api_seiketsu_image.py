from google.cloud import firestore
from google.cloud import storage
from google.oauth2 import service_account

import os
import threading
import warnings
import random
import string



# Ignore user warnings to keep the console clean
warnings.filterwarnings("ignore", category=UserWarning)

# List of allowed image file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

class ApiSeiketsuImage:
    def __init__(self):
        # Initialize Firebase Storage client
        self.storage_client = self._get_storage_client()
        self.bucket = self.storage_client.bucket('animomik-20f94.appspot.com')

    def _get_storage_client(self):
        try:
            credentials_file = os.path.join(os.path.dirname(__file__), 'data', 'firebase_credentials.json')
            credentials = service_account.Credentials.from_service_account_file(credentials_file)
            return storage.Client(credentials=credentials, project=credentials.project_id)
        except Exception as e:
            raise Exception(f"Firebase Storage client creation error: {str(e)}")

    def upload_image(self, image_file):
        try:
            # Check if the file extension is allowed
            file_extension = image_file.name.lower().split('.')[-1]
            if file_extension not in ALLOWED_EXTENSIONS:
                raise ValueError('Invalid file format. Only jpg, jpeg, and png files are allowed.')

            # Generate a random suffix of 3 characters
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))

            # Combine the original name (without extension) and random suffix
            original_image_name = os.path.splitext(os.path.basename(image_file.name))[0]
            image_name = f"{original_image_name}_{random_suffix}.jpg"

            # Upload the image to the 'images' folder in Firebase Storage and save it as JPG
            blob = self.bucket.blob(f'images/{image_name}')
            blob.upload_from_file(image_file, content_type='image/jpeg')

            # Generate a signed URL for the uploaded image without an expiration
            url = blob.generate_signed_url(expiration=604800, version='v4')
            return url
        except Exception as e:
            print(f"Image upload error: {str(e)}")
