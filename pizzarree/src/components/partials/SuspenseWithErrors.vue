<template>
  <slot v-if="error" name="error">
    <q-banner rounded class="bg-red-7 text-white tw-max-w-md tw-mt-1 tw-m-auto ">
      <template v-slot:avatar>
        <q-icon name="warning" color="" />
      </template>
      {{error}}
      <template v-slot:action>
        <q-btn flat color="" label="Dismiss" @click.prevent="error=null"/>
      </template>
    </q-banner>

  </slot>
  <Suspense v-else>
    <template #default>
      <slot name="default"></slot>
    </template>
    <template #fallback>
      <slot name="fallback">
        <div
          class="tw-flex tw-items-center tw-justify-center tw-max-w-full tw-min-h-full tw-col-span-5 tw-text-center"
        >
          <div
            class="tw-animate-spin tw-rounded-full tw-h-32 tw-w-32 tw-border-t-0 tw-border-b-3 tw-border-yellow-300 tw-z-10 tw-border-solid"
          ></div>
        </div>
      </slot>
    </template>
  </Suspense>
</template>
<script>
import { ref, onErrorCaptured } from "vue";
export default {
  name: "SuspenseWithErrors",
  setup() {
    const error = ref(null);
    onErrorCaptured(({ message }) => {
      error.value = message;
      return true;
    });
    return { error };
  },
};
</script>
