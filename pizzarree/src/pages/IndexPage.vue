<template>
  <q-page class="flex justify-center items-center q-col-gutter-md row ">

      <q-card class="col-6">
        <q-img src="../assets/hero.png" no-native-menu>
          <div class="absolute-bottom text-subtitle1 text-center">
           <q-toolbar-title>
            Welcome to Pizzarree Store
          </q-toolbar-title>

           <q-card-actions align="center">
            <q-btn unelevated rounded color="primary" :to="{name:'Menu'}" label="Order Now" />
          </q-card-actions>
          </div>
        </q-img>



      </q-card>

  </q-page>


</template>

<script>
import { defineComponent,onMounted } from 'vue'
import CheckoutPage from "pages/shop/CheckoutPage.vue";

export default defineComponent({
  name: 'IndexPage',




})
</script>
