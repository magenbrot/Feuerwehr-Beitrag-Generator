// sw.js - Service Worker für Offline-Support
const CACHE_NAME = 'fw-post-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  '/android-chrome-192x192.png',
  '/android-chrome-512x512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      const fetchPromise = fetch(event.request).then(networkResponse => {
        // Cache auch 'opaque' responses (type: basic ist zu restriktiv für CDNs)
        // Aber Status muss 200 sein (oder 0 für opaque)
        if (!networkResponse || (networkResponse.status !== 200 && networkResponse.status !== 0)) {
          return networkResponse;
        }

        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseToCache);
        });

        return networkResponse;
      });

      // Stale-while-revalidate: Zeige Cache, update im Hintergrund
      if (cachedResponse) {
        // Fehler im Hintergrund-Update abfangen, damit waitUntil nicht meckert
        event.waitUntil(fetchPromise.catch(() => {}));
        return cachedResponse;
      }

      return fetchPromise;
    })
  );
});
