<script async setup>

</script>

<template>
  <q-form class="q-my-lg flex justify-between items-center">
      <q-input dense hide-bottom-space item-aligned label="Coupon Code" hint="Do you have a coupon?" outlined>
        <template v-slot:append>
          <q-btn unelevated dense label="apply" />
        </template>
      </q-input>
  </q-form>
</template>

<style scoped>

</style>
