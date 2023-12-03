<template>
  <slot v-if="error" name="error">
    <div
      class="justify-center tw-text-red-500 tw-max-w-full tw-min-h-screen tw-col-span-5 tw-text-center tw-flex tw-items-center tw-content-center"
    >
      {{ error }}
    </div>
  </slot>
  <RouterView v-slot="{ Component, route }" v-else :key="$route.fullPath">
    <template v-if="Component">
      <Transition mode="out-in" :enter-active-class="route.meta.transitionName">
        <!-- <KeepAlive> -->
        <Suspense>
          <component :is="Component" :key="route.fullPath"></component>
          <template #fallback>
            <div>
              <slot name="loading">
                <div
                  class="tw-top-0 tw-right-0 tw-h-screen tw-w-screen tw-flex tw-justify-center tw-items-center tw-z-10"
                >
                  <div
                    class="tw-animate-spin tw-rounded-full tw-h-32 tw-w-32 tw-border-t-0 tw-border-b-3 tw-border-pink-700 tw-z-10 tw-border-solid"
                  ></div>
                </div>
              </slot>
            </div>
          </template>
        </Suspense>
        <!-- </KeepAlive> -->
      </Transition>
    </template>
  </RouterView>
</template>
<script>
import { ref, onErrorCaptured } from "vue";
import { defineComponent } from "vue";

export default defineComponent({
  name: "RouterViewSuspense",
  async setup() {
    const error = ref(null);
    onErrorCaptured(({ message }) => {
      error.value = message;
      return true;
    });
    return { error };
  },
});
</script>
