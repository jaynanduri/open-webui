import os
import logging
import asyncio
from typing import Dict, Any, Optional

from google.cloud import firestore
from google.oauth2 import service_account

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
        self.db = None
        self.initialized = False
        self.init_firestore()

    def init_firestore(self) -> None:
        """Initialize Firestore client with specific database"""
        project_id = os.environ.get("GOOGLE_PROJECT_ID")
        database_id = os.environ.get("DB_NAME")
        #cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        if not project_id or not database_id:
            logger.error("Missing required environment variables: GOOGLE_PROJECT_ID or DB_NAME")
            return

        logger.info(f"Initializing Firestore: project_id={project_id}, database_id={database_id}")

        try:
            # if not cred_path or not os.path.exists(cred_path):
            #     logger.error(f"GOOGLE_APPLICATION_CREDENTIALS not found at: {cred_path}")
            #     return

            # Load credentials
            #creds = service_account.Credentials.from_service_account_file(cred_path)

            # Create Firestore client for specific database
            self.db = firestore.Client(
                project=project_id,
                #credentials=creds,
                database=database_id
            )
            self.initialized = True
            logger.info(f"Firestore client initialized with database: {database_id}")

        except Exception as e:
            logger.error(f"Error initializing Firestore client: {e}")

    async def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a document from Firestore asynchronously"""
        if not self.initialized or not self.db:
            logger.error("Firestore not initialized")
            raise ValueError("Firestore not initialized")

        try:
            loop = asyncio.get_running_loop()
            doc_ref = self.db.collection(collection).document(doc_id)
            doc_snap = await loop.run_in_executor(None, doc_ref.get)

            if not doc_snap.exists:
                logger.warning(f"Document not found: {collection}/{doc_id}")
                raise ValueError(f"Document with ID {doc_id} not found in {collection}")

            result = {"id": doc_snap.id}
            result.update(doc_snap.to_dict() or {})
            return result

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error fetching document {collection}/{doc_id}: {e}")
            raise ValueError(f"Failed to fetch document: {str(e)}")

# --- Convenience Access Methods ---

def get_firestore_client() -> FirestoreClient:
    return FirestoreClient.get_instance()

async def get_doc_by_collection_and_id(collection: str, doc_id: str) -> Dict[str, Any]:
    client = get_firestore_client()
    return await client.get_document(collection, doc_id)
