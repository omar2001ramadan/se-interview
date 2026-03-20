declare global {
  interface Window {
    __APP_CONFIG__?: {
      PUBLIC_API_BASE_URL?: string;
    };
  }

  namespace App {}
}

export {};
