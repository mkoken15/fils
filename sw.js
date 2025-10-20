const CACHE_NAME = 'nexus-cache-v1';
// IMPORTANT: Ajoutez ici tous les noms de fichiers exacts de votre dossier (y compris les icônes)
const urlsToCache = [
    '/index.html',
    '/manifest.json'
    // Ajoutez vos icônes ici:
    // '/icon-192.png',
    // '/icon-512.png'
];

// Installation du Service Worker et mise en cache des fichiers
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Cache ouvert');
                return cache.addAll(urlsToCache);
            })
    );
});

// Interception des requêtes pour servir les fichiers à partir du cache
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Le fichier est dans le cache
                if (response) {
                    return response;
                }
                // Le fichier n'est pas dans le cache, on le télécharge
                return fetch(event.request);
            })
    );
});

// Mise à jour du Service Worker (suppression des anciens caches)
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
