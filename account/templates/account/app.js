{% load static %}

if ("serviceWorker" in navigator){
    navigator.serviceWorker.register("{% url 'account:sw.js' %}")
    .then((reg) => console.log("registered service worker", reg))
    .catch((err) => console.log("registered service worker not registered", err))
    }