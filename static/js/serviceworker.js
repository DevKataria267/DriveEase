const assets = [
    "/",
    "static/css/style.css",
    "static/js/app.js",
    "static/images/favicon.png",
    "static/icons/128x128.png",
    "static/icons/192x192.png",
    "static/icons/384x384.png",
    "static/icons/512x512.png",
];

const CATALOGUE_ASSETS = "catalogue-assets";

self.addEventListener("install", (installEvent) => {
    installEvent.waitUntil(
        caches
        .open(CATALOGUE_ASSETS)
        .then((cache) => {
            console.log(cache);
            cache.addAll(assets);
        })
        .then(self.skipWaiting())
        .catch((e) => {
            console.log(e);
        })
    );
});

self.addEventListener("activate", function (event) {
    event.waitUntil(
        caches
        .keys()
        .then((keyList) => {
            return Promise.all(
                keyList.map((key) => {
                    if (key === CATALOGUE_ASSETS) {
                        console.log("Removed old cache from", key);
                        return caches.delete(key);
                    }
                })
            );
        })
        .then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", function (event) {
    event.respondWith(
        fetch(event.request).catch(() => {
            return caches.open(CATALOGUE_ASSETS).then((cache) => {
                return cache.match(event.request);
            });
        })
    );
});