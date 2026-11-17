// Very small service worker: makes the app installable ("Add to Home Screen")
// and keeps the app shell available when the network is slow.
const CACHE = 'trekmate-v1'

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(['/', '/icon-192.png'])))
  self.skipWaiting()
})

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))),
  )
})

// network first, fall back to cache. API calls are never cached here.
self.addEventListener('fetch', (e) => {
  const req = e.request
  if (req.method !== 'GET' || req.url.includes('/api/')) return
  e.respondWith(fetch(req).catch(() => caches.match(req).then((r) => r || caches.match('/'))))
})
