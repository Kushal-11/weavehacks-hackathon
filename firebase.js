import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCRaZ0os_IoiN9kn3tmDRWeQ26culvne28",
  authDomain: "memewar-c7bb1.firebaseapp.com",
  projectId: "memewar-c7bb1",
  storageBucket: "memewar-c7bb1.firebasestorage.app",
  messagingSenderId: "201626844844",
  appId: "1:201626844844:web:d9e93f3eadfbf434c9e909",
  measurementId: "G-7TP7LCRG2P"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider(); 