# open_webui/utils/firebase.py
import os
import logging
import asyncio
from typing import Dict, Any, Optional

import firebase_admin
from firebase_admin import credentials, firestore

from open_webui.env import SRC_LOG_LEVELS

logger = logging.getLogger(__name__)
logger.setLevel(SRC_LOG_LEVELS.get("UTILS", logging.INFO))

class FirestoreClient:
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'FirestoreClient':
        if cls._instance is None:
            cls._instance = FirestoreClient()
        return cls._instance
    
    def __init__(self):
        self.app = None
        self.db = None
        self.initialized = False
        self.init_firebase()
    
    def init_firebase(self) -> None:
        """Initialize Firebase Admin SDK and Firestore client"""
        project_id = os.environ.get("GOOGLE_PROJECT_ID")
        database_id = os.environ.get("DB_NAME")
        
        if not project_id:
            logger.error("Missing GOOGLE_PROJECT_ID environment variable")
            return
            
        logger.info(f"Initializing Firebase with project_id={project_id}, database_id={database_id}")
        
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Try with application default credentials first
                try:
                    cred = credentials.ApplicationDefault()
                    self.app = firebase_admin.initialize_app(
                        cred,
                        {
                            'projectId': project_id,
                        }
                    )
                    logger.info("Firebase initialized with application default credentials")
                except Exception as e:
                    logger.error(f"Failed to initialize with default credentials: {e}")
                    
                    # Try with service account file
                    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
                    if cred_path and os.path.exists(cred_path):
                        try:
                            cred = credentials.Certificate(cred_path)
                            self.app = firebase_admin.initialize_app(
                                cred,
                                {
                                    'projectId': project_id,
                                }
                            )
                            logger.info(f"Firebase initialized with credential file: {cred_path}")
                        except Exception as e:
                            logger.error(f"Failed to initialize with credential file: {e}")
                    else:
                        logger.error(f"No valid Firebase credentials available. GOOGLE_APPLICATION_CREDENTIALS={cred_path}")
            else:
                self.app = firebase_admin.get_app()
                logger.info("Using existing Firebase app")
                
            # Initialize Firestore if we have a Firebase app
            if self.app:
                try:
                    # Use the database_id from environment variables
                    if database_id:
                        # For newer Firebase Admin SDK versions with multiDB support
                        self.db = firestore.client(
                            app=self.app, 
                            database=database_id  # This parameter requires newer SDK versions
                        )
                        logger.info(f"Firestore client initialized with custom database: {database_id}")
                    else:
                        # Default database
                        self.db = firestore.client(app=self.app)
                        logger.info("Firestore client initialized with default database")
            
                    self.initialized = True
                except Exception as e:
                    logger.error(f"Failed to initialize Firestore client: {e}")
            
        except Exception as e:
            logger.error(f"Unexpected error during Firebase initialization: {e}")
    
    async def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a document from Firestore asynchronously"""
        if not self.initialized or not self.db:
            logger.error("Firestore not initialized")
            raise ValueError("Firestore not initialized")
            
        try:
            # Run Firestore operation in a thread to avoid blocking
            loop = asyncio.get_running_loop()
            doc_ref = self.db.collection(collection).document(doc_id)
            doc_snap = await loop.run_in_executor(None, doc_ref.get)
            
            if not doc_snap.exists:
                logger.warning(f"Document {collection}/{doc_id} not found")
                raise ValueError(f"Document with ID {doc_id} not found in {collection}")
                
            # Convert to dict and add id
            result = {"id": doc_snap.id}
            result.update(doc_snap.to_dict() or {})
            return result
            
        except ValueError:
            # Re-raise ValueError for known issues
            raise
        except Exception as e:
            logger.error(f"Error fetching document {collection}/{doc_id}: {e}")
            raise ValueError(f"Failed to fetch document: {str(e)}")

# Create a function to simplify accessing the Firebase client
def get_firestore_client() -> FirestoreClient:
    return FirestoreClient.get_instance()

# Convenience function for other modules
async def get_doc_by_collection_and_id(collection: str, doc_id: str) -> Dict[str, Any]:
    client = get_firestore_client()
    return await client.get_document(collection, doc_id)