<template>
  <q-banner
    inline-actions
    rounded
    class="text-white bg-red"
    v-if="Object.keys(errors.errors).length && !dismissed"
  >
    <span v-for="(err, i) in errors.errors" :key="i" v-html="err"></span>
    <template v-slot:action>
      <q-btn flat :label="$t('dismiss')" @click="dismissed = true" />
    </template>
  </q-banner>
</template>
<script>
import { ref } from "vue";

export default {
  name: "FormErrors",
  props: ["errors"],
  setup() {
    const dismissed = ref(false);
    return {
      dismissed,
    };
  },
};
</script>
