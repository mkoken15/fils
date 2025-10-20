const CACHE_NAME = 'nexus-cache-v1';
// Liste des fichiers à mettre en cache. Les chemins sont relatifs.
const urlsToCache = [
    './', // Représente index.html dans le dossier courant
    './index.html',
    './manifest.json',
    './icon-192.png',
    './icon-512.png'
];

// ... (Le reste du code du Service Worker reste inchangé) ...
