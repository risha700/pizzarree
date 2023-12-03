<template>
  <div  v-if="products">
    <div v-for="p in products" :key="p.id">
      {{p.name}}
    </div>
  </div>
</template>

<script>
import {defineComponent} from 'vue'
export default defineComponent({
  name: "MenuComponent",
  props:['products'],
  async setup(){



  }
})
</script>



<style scoped>

</style>
