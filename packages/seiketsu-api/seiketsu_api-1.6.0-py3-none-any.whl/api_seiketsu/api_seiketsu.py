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

# Define a class for managing interactions with Firestore and messages
class ApiSeiketsu:
    def __init__(self, token):
        try:
            # Initialize Firestore client
            self.db = self._get_firestore_client()
            # Create a threading event to signal new messages
            self.new_message_event = threading.Event()
            # Store the user's token
            self.token = token
            # Reference to the 'messages' collection in Firestore
            self.messages_ref = self.db.collection('messages')



            # Initialize Firebase Storage client
            #self.storage_client = self._get_storage_client()
            # Reference to the Firebase Storage bucket
            #self.bucket = self.storage_client.bucket('animomik-20f94.appspot.com')



            # Reference to 'bot_token' collection in Firestore
            token_collection_ref = self.db.collection('bot_token')
            # Query to find the provided token
            query = token_collection_ref.where(field_path='value', op_string='==', value=self.token)
            # Stream the query results (should be one or none)
            docs = query.limit(1).stream()

            # Check if the token is valid; raise an exception if not
            if len(list(docs)) == 0:
                raise ValueError('Invalid token.')

            # Start listening for changes in the 'messages' collection
            self._listen_for_changes()
        except Exception as e:
            # Handle any exceptions that occur during initialization
            print(f"Initialization error: {str(e)}")

    # Initialize the Firestore client using service account credentials
    def _get_firestore_client(self):
        try:
            credentials_file = os.path.join(os.path.dirname(__file__), 'data', 'firebase_credentials.json')
            credentials = service_account.Credentials.from_service_account_file(credentials_file)
            return firestore.Client(credentials=credentials, project=credentials.project_id)
        except Exception as e:
            # Handle any exceptions related to Firestore client creation
            raise Exception(f"Firestore client creation error: {str(e)}")

    # Start listening for changes in the 'messages' collection
    def _listen_for_changes(self):
        try:
            query = self.messages_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
            # Set up a listener that triggers the _on_snapshot method
            query_watch = query.on_snapshot(self._on_snapshot)
        except Exception as e:
            # Handle any exceptions related to query setup
            print(f"Query setup error: {str(e)}")

    # Handle changes in the 'messages' collection
    def _on_snapshot(self, col_snapshot, changes, read_time):
        try:
            for change in changes:
                if change.type.name == 'ADDED':
                    # Extract the latest message's alias and text
                    latest_message = change.document.to_dict()
                    alias = latest_message['alias']
                    message_text = latest_message['text']
                    # Signal that a new message has arrived
                    self.new_message_event.set()
        except Exception as e:
            # Handle any exceptions that may occur during snapshot handling
            print(f"Snapshot handling error: {str(e)}")

    # Read the latest message from the 'messages' collection
    def read_message(self):
        try:
            # Wait until a new message event is set
            self.new_message_event.wait()

            query = self.messages_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
            message_docs = query.stream()

            for message_doc in message_docs:
                # Extract the latest message's alias and text
                latest_message = message_doc.to_dict()
                alias = latest_message['alias']
                message_text = latest_message['text']
                # Clear the event and return the alias and message text
                self.new_message_event.clear()
                return alias, message_text
        except Exception as e:
            # Handle any exceptions that may occur during message reading
            print(f"Message reading error: {str(e)}")

    # Write a new message to the 'messages' collection
    def write_message(self, alias, message_text):
        try:
            # Create a new document reference
            doc_ref = self.messages_ref.document()
            batch = self.db.batch()
            # Set the document with the provided alias, message text, and a timestamp
            batch.set(doc_ref, {
                'alias': alias + '#BOT',
                'text': message_text,
                'timestamp': firestore.SERVER_TIMESTAMP
            })
            # Commit the batch operation to Firestore
            batch.commit()
        except Exception as e:
            # Handle any exceptions that may occur during message writing
            print(f"Message writing error: {str(e)}")
