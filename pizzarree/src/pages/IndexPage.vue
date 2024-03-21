<template>
  <q-page class="flex justify-center items-center q-col-gutter-md row ">

      <q-card class=" tw-columns-md ">
        <q-img src="../assets/hero.png" fit="scale-down" position="50% 0" no-native-menu>
          <div class="absolute-bottom text-subtitle1 text-center sm:tw-mr-3 ">
           <q-card-section>
            Welcome to Pizzarree Store
          </q-card-section>

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
