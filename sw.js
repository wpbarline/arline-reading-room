const CACHE = 'arline-reading-room-v3';
const SHELL = ['/', '/manifest.webmanifest', '/annotations.js', '/annotations.css', '/icons/icon-192.png', '/icons/icon-512.png', '/api/library', '/api/book/story', '/api/book/guide', '/api/book/premise', '/api/voices', '/api/recordings'];
self.addEventListener('install', event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting())));
self.addEventListener('activate', event => event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('arline-reading-room-') && key !== CACHE).map(key => caches.delete(key)))).then(() => self.clients.claim())));
async function audioResponse(request) {
  const cache = await caches.open(CACHE);
  const clean = new Request(request.url);
  let full = await cache.match(clean);
  if (!full) {
    full = await fetch(clean);
    if (!full.ok) return full;
    try { await cache.put(clean, full.clone()); } catch (error) { /* Playback can continue if browser storage is full. */ }
  }
  const range = request.headers.get('Range');
  if (!range) return full;
  const bytes = await full.arrayBuffer();
  const match = /^bytes=(\d*)-(\d*)$/.exec(range);
  if (!match) return full;
  const start = match[1] ? Number(match[1]) : Math.max(0, bytes.byteLength - Number(match[2]));
  const end = match[1] && match[2] ? Math.min(Number(match[2]), bytes.byteLength - 1) : bytes.byteLength - 1;
  if (start > end || start >= bytes.byteLength) return new Response(null, {status:416, headers:{'Content-Range':`bytes */${bytes.byteLength}`}});
  return new Response(bytes.slice(start,end+1), {status:206, headers:{'Content-Type':'audio/wav','Content-Length':String(end-start+1),'Content-Range':`bytes ${start}-${end}/${bytes.byteLength}`,'Accept-Ranges':'bytes'}});
}
self.addEventListener('fetch', event => {
  const request = event.request, url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin || url.pathname === '/api/status') return;
  if (url.pathname.startsWith('/audio/')) {event.respondWith(audioResponse(request)); return;}
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    try {
      const response = await fetch(request);
      if (response.ok) await cache.put(request,response.clone());
      return response;
    } catch (error) {
      const saved = await cache.match(request);
      if (saved) return saved;
      if (request.mode === 'navigate') return await cache.match('/');
      throw error;
    }
  })());
});
