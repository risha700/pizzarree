<template>
  <router-view />
</template>

<script>
import { TailwindDarkFix } from 'src/composables/tw-dark-fix';

import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App',
  setup(){
    TailwindDarkFix();
  }
})
</script>
