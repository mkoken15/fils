const CACHE_NAME = 'nexus-cache-v1';
// Liste des fichiers à mettre en cache. Les chemins sont relatifs au Service Worker.
const urlsToCache = [
    '/fils/', // La page racine
    '/fils/index.html',
    '/fils/manifest.json',
    '/fils/icon-192.png',
    '/fils/icon-512.png'
];

// Installation du Service Worker et mise en cache des fichiers
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Cache ouvert');
                // IMPORTANT : L'ajout du premier élément (la racine) doit être géré correctement
                // On met en cache tous les chemins avec le préfixe du dossier 'fils'
                return cache.addAll(urlsToCache);
            })
            .catch(error => {
                console.error('Échec de la mise en cache des ressources :', error);
            })
    );
});

// Interception des requêtes pour servir les fichiers à partir du cache
self.addEventListener('fetch', event => {
    // Si la requête est pour Google Fonts ou Font Awesome (CDN), on la laisse passer
    if (event.request.url.startsWith('https://fonts.googleapis.com/') ||
        event.request.url.startsWith('https://fonts.gstatic.com/') ||
        event.request.url.startsWith('https://kit.fontawesome.com/')) {
        return; 
    }
    
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
