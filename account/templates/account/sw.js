{% load static %}

const staticCacheName = 'site-static-v3';
const dynamicCacheName = 'site-dynamic-v3';
const assets = [
  "{% url 'account:home' %}",
  "{% url 'account:faq' %}",
  "{% url 'account:contact' %}",
  "{% url 'account:login' %}",
  "{% url 'account:signup' %}",
  "{% url 'account:about' %}",
  "{% static 'account/js/jquery.min.js' %}",
  "{% static 'account/js/browser.min.js' %}",
  "{% static 'account/js/breakpoints.min.js' %}",
  "{% static 'account/js/util.js' %}",
  "{% static 'account/js/main.js' %}",
  "{% url 'account:app.js' %}",
  "{% static 'account/css/bootstrap.css' %}",
  "{% static 'account/css/main.css' %}",
  "{% static 'account/css/font-awesome.css' %}",
  "{% static 'account/css/custom.css' %}",
  "{% url 'account:offline' %}"
];

// cache size limit function
const limitCacheSize = (name, size) => {
  caches.open(name).then(cache => {
    cache.keys().then(keys => {
      if(keys.length > size){
        cache.delete(keys[0]).then(limitCacheSize(name, size));
      }
    });
  });
};

// install event
self.addEventListener('install', evt => {
  //console.log('service worker installed');
  evt.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      // console.log('caching shell assets');
      cache.addAll(assets);
    })
  );
});

// activate event
self.addEventListener('activate', evt => {
  //console.log('service worker activated');
  evt.waitUntil(
    caches.keys().then(keys => {
      //console.log(keys);
      return Promise.all(keys
        .filter(key => key !== staticCacheName && key !== dynamicCacheName)
        .map(key => caches.delete(key))
      );
    })
  );
});

// fetch event
self.addEventListener('fetch', evt => {
  //console.log('fetch event', evt);
  evt.respondWith(
    caches.match(evt.request).then(cacheRes => {
      return cacheRes || fetch(evt.request).then(fetchRes => {
        return caches.open(dynamicCacheName).then(cache => {
          cache.put(evt.request.url, fetchRes.clone());
          // check cached items size
          limitCacheSize(dynamicCacheName, 15);
          return fetchRes;
        })
      });
    }).catch(() => {
    
        return caches.match("{% url 'account:offline' %}");
      
    })
  );
});