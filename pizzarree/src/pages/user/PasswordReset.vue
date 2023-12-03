<template>
  <user-access-card
    :form="passwordResetForm"
    :loading="loading"
    actionText="user.password"
  >
    <!--  FORM -->
    <q-form class="q-gutter-md" @submit.prevent="handleSubmit">
      <q-input
        outlined
        v-model="passwordResetForm.email"
        type="email"
        name="email"
        :label="$t('user.email')"
        :hint="$t('user.email')"
        :error="passwordResetForm.errors.has('username')"
        :error-message="passwordResetForm.errors.get('username')"
        :rules="[requiredField]"
        :lazy-rules="'ondemand'"
        autocomplete
        autofocus
        autocorrect="off"
        spellcheck="false"
        :disable="loading"
      >
      </q-input>

      <div class="items-start column">
        <div class="justify-between row full-width">
          <q-btn
            color="primary"
            :to="{ name: 'Login' }"
            flat
            no-caps
            class="tw-capitalize"
          >
            sign in instead?
          </q-btn>
          <q-btn
            :label="capitalize($t('submit'))"
            type="submit"
            color="primary"
            :loading="loading"
            no-caps
          />
        </div>
      </div>
    </q-form>
  </user-access-card>
</template>

<script>
import { Notify } from "quasar";
import { reactive, ref } from "vue";
import Form from "src/utils/Form";

import UserAccessCard from "src/components/partials/UserAccessCard.vue";
import { useAuthStore } from "stores/auth";
import { useRoute, useRouter } from "vue-router";
import { format } from "quasar";
import { useI18n } from "vue-i18n";

const reset_url = "api/v1/accounts/api-auth-user/password_reset/";

export default {
  name: "PasswordReset",
  components: { UserAccessCard },
  setup() {
    const { capitalize } = format;
    const { t } = useI18n();
    const store = useAuthStore();
    const router = useRouter();
    const route = useRoute();
    const loading = ref(false);
    const isPwd = ref(true);
    const passwordResetForm = reactive(
      new Form({
        email: "",
      })
    );

    const handleSubmit = async () => {
      loading.value = true;
      await passwordResetForm.post(reset_url);
    };
    const requiredField = (val) => {
      return (val && val.length > 0) || t("required_field");
    };

    passwordResetForm.onSuccess = async () => {
      passwordResetForm.reset(); // reset
      await router.push(route.query.redirect || { name: "Dashboard" });
      Notify.create({
        type: "positive",
        message: `reset email has been set`,
        progress: true,
        position: "top",
      });
    };

    passwordResetForm.onFinished = () => {
      loading.value = false;
    };

    return {
      isPwd,
      passwordResetForm,
      handleSubmit,
      loading,
      requiredField,
      capitalize,
    };
  },
};
</script>
