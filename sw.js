// Service Worker — オフライン完全動作のためのキャッシュ戦略
// 更新時は CACHE_VERSION を上げる
const CACHE_VERSION = 'v29';
const CACHE_NAME = `food-pwa-${CACHE_VERSION}`;

// 食材IDの配列(parts SVG をプリキャッシュするため)
const FOOD_IDS = [
  'daikon', 'carrot', 'negi',
  // Phase A
  'tomato', 'onion', 'egg', 'chicken', 'potato',
  'cabbage', 'cucumber', 'banana', 'apple',
  // Phase B - 野菜
  'garlic', 'komatsuna', 'lettuce', 'hakusai', 'nasu',
  'piman', 'broccoli', 'ginger', 'pumpkin',
  // Phase B - きのこ
  'shiitake', 'shimeji', 'enoki', 'eringi', 'maitake',
  // Phase B - 果物
  'mikan', 'lemon', 'avocado', 'ichigo', 'kiwi',
  'grape', 'peach', 'kaki', 'pear',
  // Phase C - 豆製品
  'tofu', 'natto',
  // Phase C - 肉類
  'pork', 'beef', 'ground_meat',
  // Phase C - 魚介
  'salmon', 'saba', 'aji', 'ebi', 'whole_fish',
  // Phase C - 乳製品
  'yogurt',
  // Phase D - ジビエ
  'venison', 'boar',
];

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
  ...FOOD_IDS.flatMap((id) => [
    `./svg/parts/${id}_ok.svg`,
    `./svg/parts/${id}_ng.svg`,
  ]),
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

// 戦略:
//  HTML / data/*.json: network-first(更新を即反映、オフライン時はキャッシュ)
//  その他のアセット   : cache-first(イラスト/アイコン等の不変リソース向け)
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // 外部ドメイン (Google Analytics, googletagmanager.com 等) はSWを介さず
  // ブラウザにそのまま処理させる(キャッシュもしない)
  if (url.origin !== location.origin) return;

  const isHTML = req.mode === 'navigate' ||
                 (req.headers.get('accept') || '').includes('text/html');
  // data/*.json は内容が後から更新されうるので必ず最新を取りにいく
  const isFreshData = url.pathname.includes('/data/') && url.pathname.endsWith('.json');

  if (isHTML || isFreshData) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res.ok && url.origin === location.origin) {
            const copy = res.clone();
            caches.open(CACHE_NAME).then((c) => c.put(req, copy));
          }
          return res;
        })
        .catch(() => caches.match(req).then((r) => r || caches.match('./index.html')))
    );
    return;
  }

  // 静的アセット (svg/png/manifest 等): cache-first
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
