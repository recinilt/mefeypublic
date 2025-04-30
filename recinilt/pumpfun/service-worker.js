self.addEventListener("install", e => {
    e.waitUntil(
      caches.open("pumpfun-cache").then(cache => {
        return cache.addAll([
          "/",
          "/index.html",
          "/alarm.wav",
          "/manifest.json"
        ]);
      })
    );
  });
  
  self.addEventListener("fetch", e => {
    e.respondWith(
      caches.match(e.request).then(response => response || fetch(e.request))
    );
  });
  