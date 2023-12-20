
<template>
  <q-page class="flex justify-center">
    <SuspenseWithErrors>
      <CheckoutComponent></CheckoutComponent>
    </SuspenseWithErrors>
  </q-page>

</template>

<script>
import {defineAsyncComponent, defineComponent} from "vue";
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";

export default defineComponent({
  name: 'CheckoutPage',
  components: {SuspenseWithErrors,
    CheckoutComponent:defineAsyncComponent(()=> import('components/shop/CheckoutComponent.vue')),
  },

})
</script>
<style scoped>

</style>
