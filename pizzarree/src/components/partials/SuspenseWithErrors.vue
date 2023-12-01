<template>
  <slot v-if="error" name="error">
    <div
      class="flex items-center content-center justify-center max-w-full min-h-screen col-span-5 text-center text-red-500"
    >
      {{ error }}
    </div>
  </slot>
  <Suspense v-else>
    <template #default>
      <slot name="default"></slot>
    </template>
    <template #fallback>
      <slot name="fallback">
        <div
          class="flex items-center justify-center max-w-full min-h-full col-span-5 text-center"
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
