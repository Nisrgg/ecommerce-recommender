// Mock for Vite's import.meta in Jest tests

// Mock import.meta.env for Jest
Object.defineProperty(global, 'import', {
  value: {
    meta: {
      env: {
        DEV: true,
        PROD: false,
        VITE_API_BASE_URL: 'http://localhost:8000'
      }
    }
  }
});