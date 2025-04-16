import { db } from './firestore-admin';

/**
 * Get a Firestore document by ID
 */
export async function getDocByCollectionAndId(collectionName: string, docId: string) {
  try {
    const docRef = db.collection(collectionName).doc(docId);
    const docSnap = await docRef.get();

    if (!docSnap.exists) {
      throw new Error(`Document with ID ${docId} not found`);
    }

    return { id: docSnap.id, ...docSnap.data() };
  } catch (error) {
    console.error('Error fetching Firestore document:', error);
    throw error;
  }
}