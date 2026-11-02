// Offline support. The build fills in the version and file list
// (scripts/build_site.py: write_service_worker), so this file stays dumb:
// precache the whole site on install, drop old caches on activate, and
// answer requests from the cache first.
const VERSION = __CACHE_VERSION__;
const FILES = __PRECACHE_FILES__;
const CACHE = `pe-wiki-${VERSION}`;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(FILES.map((f) => new Request(f, { cache: "reload" }))))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("pe-wiki-") && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET" || new URL(request.url).origin !== self.location.origin) return;
  // Routes live in the hash, so every page load is the start page.
  const key = request.mode === "navigate" ? "./" : request;
  event.respondWith(
    caches.open(CACHE)
      .then((cache) => cache.match(key, { ignoreSearch: true }))
      .then((hit) => hit || fetch(request)),
  );
});
