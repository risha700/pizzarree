<template>

  <router-view />
</template>

<script>
import { TailwindDarkFix } from 'src/composables/tw-dark-fix';

import { defineComponent } from 'vue'
import {api} from "boot/axios";

let API_BASE_URL = process.env.VUE_APP_API_BASE_URL;

export default defineComponent({
  name: 'App',
  setup(){
    TailwindDarkFix();
      api.interceptors.request.use((config) => {
      config.baseURL = API_BASE_URL;
      return config;
    });
  }
})
</script>
