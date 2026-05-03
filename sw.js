// Service Worker — オフライン完全動作のためのキャッシュ戦略
// 更新時は CACHE_VERSION を上げる
const CACHE_VERSION = 'v4';
const CACHE_NAME = `food-pwa-${CACHE_VERSION}`;

// アプリシェル + データ + 全アセットをプリキャッシュ
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './data/foods.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png',
  './icons/favicon-32.png',
  // OK/NG パーツSVG (一覧サムネイル + 詳細図解で使用)
  './svg/parts/daikon_ok.svg',
  './svg/parts/daikon_ng.svg',
  './svg/parts/carrot_ok.svg',
  './svg/parts/carrot_ng.svg',
  './svg/parts/negi_ok.svg',
  './svg/parts/negi_ng.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Cache-first, network-fallback。HTML だけは network-first にしておくと
// 更新が反映されやすい(オフライン時はキャッシュにフォールバック)。
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  const isHTML = req.mode === 'navigate' ||
                 (req.headers.get('accept') || '').includes('text/html');

  if (isHTML) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((r) => r || caches.match('./index.html')))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((res) => {
        if (res.ok && url.origin === location.origin) {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() => cached);
    })
  );
});
