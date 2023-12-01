<template>
  <q-page padding>
    <q-page-container>
    <q-card bordered class="tw-h-[500px]">
        <q-card-section>
          <p class="tw-text-lg">{{ authStore.authUser.username }}</p>
        </q-card-section>
      </q-card>
      <q-card bordered class="tw-mt-2">
        <q-card-section>
          <p class="tw-text-lg">{{ authStore.authUser.email }}</p>
        </q-card-section>
      </q-card>

    </q-page-container>
  </q-page>
</template>

<script>
import { useAuthStore } from "src/stores/auth";

export default {
  name: "DashboardPage",

  setup() {
    let authStore = useAuthStore();

    return {
      authStore,
    };
  },
};
</script>
