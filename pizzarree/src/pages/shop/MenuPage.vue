<template>
  <SuspenseWithErrors>
    <MenuComponent :products="products_list"/>
  </SuspenseWithErrors>
</template>

<script>
import {defineComponent} from 'vue'
import MenuComponent from "components/shop/MenuComponent.vue";
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";
import {api} from "boot/axios";
const products_url = "http://localhost:8000/api/v1/shop/products";
export default defineComponent({
  name: "MenuPage",
  components:{SuspenseWithErrors, MenuComponent},
  async setup(){
     let data = await api.get(products_url);

     let products_list = data.data.results;

     return{products_list}

  }
})
</script>



<style scoped>

</style>
