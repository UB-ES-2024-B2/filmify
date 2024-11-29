// plugins/firebase.ts
import { initializeApp } from 'firebase/app';
import { getStorage } from 'firebase/storage';
import { firebaseConfig } from '~/firebaseConfig';

export default defineNuxtPlugin(() => {
  const firebaseApp = initializeApp(firebaseConfig);
  const storage = getStorage(firebaseApp);

  return {
    provide: {
      storage,
    },
  };
});