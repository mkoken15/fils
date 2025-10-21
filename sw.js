const CACHE_NAME = 'nexus-cache-v1';

// Les chemins sont relatifs au Service Worker, donc relatifs au dossier /fils/
const urlsToCache = [
    './', // index.html dans le dossier courant
    './index.html',
    './manifest.json',
    './archive.html',
    './icon-192.png',
    './icon-512.png',
    // Ajout des fichiers d'archive pour le mode hors ligne
    './archive/projets.html',
    './archive/competences.html',
    './archive/cv.html'
];

// Installation du Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Cache ouvert. Ajout des ressources Nexus.');
                return cache.addAll(urlsToCache);
            })
            .catch(error => {
                console.error('Échec de la mise en cache des ressources :', error);
            })
    );
});

// Interception des requêtes pour servir les fichiers à partir du cache
self.addEventListener('fetch', event => {
    // Si la requête est pour des ressources externes (CDN), on les laisse passer
    if (event.request.url.startsWith('https://fonts.googleapis.com/') ||
        event.request.url.startsWith('https://fonts.gstatic.com/') ||
        event.request.url.startsWith('https://kit.fontawesome.com/')) {
        return; 
    }
    
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});

// Mise à jour du Service Worker
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
