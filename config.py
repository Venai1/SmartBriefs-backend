import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Service Account JSON Setup
cred = credentials.Certificate("serviceAccountKey.json")  # Your downloaded JSON key
firebase_admin.initialize_app(cred)

# Firestore Client
db = firestore.client()
