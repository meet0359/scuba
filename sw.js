const CACHE_NAME = 'scuba-v1.0';
const STATIC_ASSETS = [
    './',
    './index.html',
    './css/style.min.css',
    './css/bootstrap.min.css',
    './js/jquery.js',
    './js/bootstrap.min.js',
    './js/custom-script.min.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            // We use add All but catch errors so a single failed asset doesn't stop installation
            return Promise.allSettled(
                STATIC_ASSETS.map(url => cache.add(url).catch(err => console.log('Failed to cache', url, err)))
            );
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') return;

    // Stale-while-revalidate strategy
    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            const fetchPromise = fetch(event.request).then(networkResponse => {
                // Cache valid responses
                if (networkResponse.ok) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        // ignore chrome-extension:// and other non-http requests
                        if (event.request.url.startsWith('http')) {
                            cache.put(event.request, responseClone);
                        }
                    });
                }
                return networkResponse;
            }).catch(error => {
                console.error('Fetch failed:', error);
                throw error;
            });

            return cachedResponse || fetchPromise;
        })
    );
});
