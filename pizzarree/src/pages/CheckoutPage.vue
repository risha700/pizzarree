
<template>
  <q-page class="flex flex-center">
    <SuspenseWithErrors>
      <CheckoutComponent></CheckoutComponent>
    </SuspenseWithErrors>
  </q-page>

</template>

<script>
import {defineComponent, onMounted} from "vue";
import CheckoutComponent from "components/CheckoutComponent.vue";
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";


export default defineComponent({
  name: 'CheckoutPage',
  components: {SuspenseWithErrors, CheckoutComponent}
})
</script>
<style scoped>

</style>
