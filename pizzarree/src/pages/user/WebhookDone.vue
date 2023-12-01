<template>

  <div class="q-pa-md q-gutter-sm">
    <q-dialog v-model="hasMessage" persistent>
      <q-card>
        <q-card-section
          class="items-center justify-center row"
          style="min-width: 30vw"
        >
          <q-avatar
            :icon="level == 'success' ? 'o_check_circle' : 'o_error_outline'"
            :color="level == 'success' ? 'positive' : 'negative'"
          />
          <span class="q-ml-sm">{{ message }}</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            :label="$t('dismiss')"
            @click="router.push({ name: 'Home' })"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

export default {
  name: "WebhookDone",
  setup() {
    const router = useRouter();
    const route = useRoute();
    let message = ref("Nothing to show!");
    let level = ref("");
    const { t } = useI18n();
    const hasMessage = ref(true);

    onMounted(async () => {
      if (!route.query.message) {
        await router.push({ name: "Home" });
      }
      message.value = route.query.message;
      level.value = route.query.level;
      let query = Object.assign({}, route.query);
      delete query.message;
      delete query.level;
      await router.push({ path: route.path });
    });

    return {
      message,
      level,
      router,
      t,
      hasMessage,
    };
  },
};
</script>
