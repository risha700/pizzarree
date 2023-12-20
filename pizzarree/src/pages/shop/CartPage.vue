
<template>
  <q-page class="flex flex-center">
    <SuspenseWithErrors>
      <CartComponent></CartComponent>
    </SuspenseWithErrors>
  </q-page>

</template>

<script>
import {defineAsyncComponent, defineComponent} from "vue";
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";


export default defineComponent({
  name: 'CartPage',
  components: {SuspenseWithErrors,
    CartComponent:defineAsyncComponent(()=>import('components/shop/CartComponent.vue')), }
})
</script>
<style scoped>

</style>
