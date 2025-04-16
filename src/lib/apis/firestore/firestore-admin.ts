
import dotenv from 'dotenv';
dotenv.config();

import { initializeApp, applicationDefault, getApps, type App } from 'firebase-admin/app';
import { Firestore } from 'firebase-admin/firestore';


let app: App;

const projectId = process.env.FIREBASE_PROJECT_ID;
const databaseId = process.env.FIREBASE_DATABASE_ID;

if (!getApps().length) {
  app = initializeApp({
    credential: applicationDefault(),
    projectId: projectId,
  });
} else {
  app = getApps()[0];
}

const db = new Firestore({
  projectId,
  databaseId
} );

export { db };

