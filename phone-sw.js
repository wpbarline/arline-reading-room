const CACHE='arline-phone-__REVISION__';
const SHELL=__SHELL__;
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('arline-phone-')&&k!==CACHE).map(async k=>{const old=await caches.open(k),fresh=await caches.open(CACHE);for(const request of await old.keys())if(new URL(request.url).pathname.includes('/audio/')){try{await fresh.put(request,await old.match(request));}catch{}}await caches.delete(k);}))).then(()=>self.clients.claim())));
async function recording(request){
  const cache=await caches.open(CACHE),clean=new Request(request.url);let response=await cache.match(clean);
  if(!response){response=await fetch(clean);if(!response.ok)return response;try{await cache.put(clean,response.clone());}catch{}}
  const range=request.headers.get('Range');if(!range)return response;
  const bytes=await response.arrayBuffer(),match=/^bytes=(\d*)-(\d*)$/.exec(range);if(!match)return response;
  const first=match[1]?Number(match[1]):Math.max(0,bytes.byteLength-Number(match[2])),last=match[1]&&match[2]?Math.min(Number(match[2]),bytes.byteLength-1):bytes.byteLength-1;
  if(first>last||first>=bytes.byteLength)return new Response(null,{status:416,headers:{'Content-Range':`bytes */${bytes.byteLength}`}});
  return new Response(bytes.slice(first,last+1),{status:206,headers:{'Content-Type':'audio/wav','Content-Length':String(last-first+1),'Content-Range':`bytes ${first}-${last}/${bytes.byteLength}`,'Accept-Ranges':'bytes'}});
}
self.addEventListener('fetch',e=>{const r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==self.location.origin)return;
  if(u.pathname.includes('/audio/')){e.respondWith(recording(r));return;}
  e.respondWith((async()=>{const c=await caches.open(CACHE);try{const response=await fetch(r);if(response.ok){try{await c.put(r,response.clone());}catch{}}return response;}catch(error){const saved=await c.match(r);if(saved)return saved;if(r.mode==='navigate')return await c.match(new URL('./',self.registration.scope));throw error;}})());
});
