<template>
  <user-access-card
    :form="confirmForm"
    :loading="loading"
    actionText="user.password_reset"
  >
    <!--  FORM -->
    <q-form class="q-gutter-md" @submit.prevent="handleSubmit">
      <q-input
        outlined
        v-model="confirmForm.password"
        :type="isNotPwd ? 'text' : 'password'"
        name="password"
        :label="$t('user.password')"
        :hint="$t('user.password')"
        :error="confirmForm.errors.has('password')"
        :error-message="confirmForm.errors.get('password')"
        :rules="[requiredField]"
        :lazy-rules="'ondemand'"
        autocomplete
        autocorrect="off"
        spellcheck="false"
        :disable="loading"
      >
      </q-input>
      <q-input
        outlined
        v-model="confirmForm.password2"
        :type="isNotPwd ? 'text' : 'password'"
        name="password2"
        :label="$t('confirm')"
        :hint="$t('confirm')"
        :error="confirmForm.errors.has('password2')"
        :error-message="confirmForm.errors.get('password2')"
        :rules="[requiredField]"
        :lazy-rules="'ondemand'"
        autocomplete
        autocorrect="off"
        spellcheck="false"
        :disable="loading"
      >
      </q-input>
      <q-checkbox
        label="show password"
        v-model="showPassword"
        @click.prevent="() => (isNotPwd = !isNotPwd)"
      ></q-checkbox>
      <div class="items-center row">
        <div class="justify-end row full-width">
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
import { reactive, ref, shallowRef } from "vue";
import Form from "src/utils/Form";

import UserAccessCard from "src/components/partials/UserAccessCard.vue";
import { useAuthStore } from "stores/auth";
import { useRoute, useRouter } from "vue-router";
import { format } from "quasar";
import { useI18n } from "vue-i18n";

const reset_url = "api/v1/api-auth-user/password_change/";

export default {
  name: "PasswordResetConfirm",
  components: { UserAccessCard },
  async setup() {
    const { capitalize } = format;
    const { t } = useI18n();
    const authStore = useAuthStore();
    const router = useRouter();
    const route = useRoute();
    const loading = ref(false);
    const isNotPwd = shallowRef(false);
    const showPassword = shallowRef(false);

    const confirmForm = reactive(
      new Form({
        password: "",
        password2: "",
      })
    );
    let token_param = route.query.auth_token;
    const validateTempToken = async (interval) =>
      setTimeout(async () => {
        await authStore.validateTempToken();
      }, interval * 60000);

    const handleSubmit = async () => {
      loading.value = true;
      await confirmForm.patch(reset_url);
    };
    const requiredField = (val) => {
      return (val && val.length > 0) || t("required_field");
    };

    confirmForm.onSuccess = async () => {
      confirmForm.reset(); // reset
      await router.push(route.query.redirect || { name: "dashboard" });
      await authStore.clearTempToken();
      Notify.create({
        type: "positive",
        message: t("password changed you can login now"),
        progress: true,
        position: "top",
      });
    };

    confirmForm.onFinished = () => {
      loading.value = false;
    };

    const bounceNotAuthorized = async () => {
      await authStore.clearTempToken();
      clearTimeout(validateTempToken);
      if (route.name === "PasswordResetConfirm") {
        await router.isReady();
        await router.push({ name: "home" });
      }
    };
    authStore.$subscribe(async (mutations) => {
      if (
        mutations.events.key === "expired" &&
        mutations.events.newValue === true
      ) {
        await bounceNotAuthorized();
      }
    });

    if (token_param && token_param.length) {
      await authStore.setTempToken({ value: token_param, expiryMinutes: 5 });
      let query = Object.assign({}, route.query);
      delete query.auth_token;
      await router.push({ path: route.path });
      await validateTempToken(5.1);
    }
    if (authStore.tempToken.expired && !token_param)
      await bounceNotAuthorized();

    return {
      isNotPwd,
      showPassword,
      confirmForm,
      handleSubmit,
      loading,
      requiredField,
      capitalize,
    };
  },
};
</script>
