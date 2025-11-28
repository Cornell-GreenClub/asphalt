'use client';

import { useEffect } from 'react';

const BackendWakeup = () => {
  useEffect(() => {
    const wakeUpBackend = async () => {
      try {
        let backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
        if (!backendUrl.startsWith('http')) {
          backendUrl = `https://${backendUrl}`;
        }
        // Fire and forget - we don't need the result
        fetch(`${backendUrl}/health`).catch((err) =>
          console.log('Wake-up ping failed (expected if offline):', err)
        );
      } catch (e) {
        // Ignore errors
      }
    };
    wakeUpBackend();
  }, []);

  return null; // This component renders nothing
};

export default BackendWakeup;
