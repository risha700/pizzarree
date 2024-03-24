/*
 * This file (which will be your service worker)
 * is picked up by the build system ONLY if
 * quasar.config.js > pwa > workboxPluginMode is set to "InjectManifest"
 */

import { precacheAndRoute } from 'workbox-precaching'
import {StaleWhileRevalidate} from 'workbox-strategies';
import {registerRoute} from 'workbox-routing';

// Use with precache injection
precacheAndRoute(self.__WB_MANIFEST)

// Caching strategies
registerRoute(
({url}) => url.pathname.startsWith('/media'),
    new StaleWhileRevalidate()
  )
