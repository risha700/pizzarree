
<template>
  <q-page class="flex flex-center">
    <SuspenseWithErrors>
      <CartComponent></CartComponent>
    </SuspenseWithErrors>
  </q-page>

</template>

<script>
import {defineComponent, onMounted} from "vue";
import CheckoutComponent from "components/shop/CheckoutComponent.vue";
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";
import CartComponent from "components/shop/CartComponent.vue";


export default defineComponent({
  name: 'CartPage',
  components: {CartComponent, SuspenseWithErrors}
})
</script>
<style scoped>

</style>
