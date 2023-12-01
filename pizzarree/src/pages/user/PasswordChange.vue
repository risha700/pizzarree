<template>
  <q-page class="flex items-end content-center justify-center">
    <q-card class="q-px-xl q-pb-xl">
      <h4 class="text-center">{{ capitalize(t("user.password_change")) }}</h4>
      <q-form
        class="q-gutter-sm column tw-min-w-[380px]"
        @submit.prevent="handleSubmit"
      >
        <FormErrors
          :errors="resetForm.errors"
          v-if="resetForm.commonErrors()"
        />
        <q-input
          outlined
          v-model="resetForm.old_password"
          :type="isPwd ? 'password' : 'text'"
          :label="capitalize(t('user.old_password'))"
          autocomplete
          autocorrect="off"
          spellcheck="false"
          :disable="loading"
          :rules="[requiredField]"
          :lazy-rules="'ondemand'"
          :error="resetForm.errors.has('old_password')"
          :error-message="resetForm.errors.get('old_password')"
        >
        </q-input>
        <q-input
          outlined
          v-model="resetForm.password"
          :type="isPwd ? 'password' : 'text'"
          :label="capitalize(t('user.new_password'))"
          autocomplete
          autocorrect="off"
          spellcheck="false"
          :disable="loading"
          :rules="[requiredField]"
          :lazy-rules="'ondemand'"
          :error="resetForm.errors.has('password')"
          :error-message="resetForm.errors.get('password')"
        >
        </q-input>
        <q-input
          outlined
          v-model="resetForm.password2"
          :type="isPwd ? 'password' : 'text'"
          :label="capitalize(t('user.new_password_confirm'))"
          autocomplete
          autocorrect="off"
          spellcheck="false"
          :disable="loading"
          :rules="[requiredField]"
          :lazy-rules="'ondemand'"
          :error="resetForm.errors.has('password2')"
          :error-message="resetForm.errors.get('password2')"
        >
        </q-input>

        <div class="flex items-start">
          <div class="justify-between row full-width">
            <q-checkbox
              :label="capitalize(t('user.show_password'))"
              v-model="showPassword"
              @click="isPwd = !isPwd"
            ></q-checkbox>
            <q-btn
              :label="capitalize(t('change'))"
              type="submit"
              color="primary"
              :loading="loading"
              no-caps
            />
          </div>
        </div>
      </q-form>
    </q-card>
  </q-page>
</template>

<script>
import { reactive, ref } from "vue";
import Form from "src/utils/Form";
import FormErrors from "src/components/partials/FormErrors.vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { Notify } from "quasar";
import { format } from "quasar";
export default {
  components: { FormErrors },
  name: "PasswordChange",
  async setup() {
    const reset_url = "api/v1/api-auth-user/password_change/";
    const loading = ref(false);
    const showPassword = ref(false);
    const { t } = useI18n();
    const router = useRouter();
    const { capitalize } = format;
    const isPwd = ref(true);
    const resetForm = reactive(
      new Form({
        old_password: "",
        password: "",
        password2: "",
      })
    );
    const handleSubmit = async () => {
      loading.value = true;
      await resetForm.post(reset_url).catch((e) => e);
    };
    const requiredField = (val) => {
      return (val && val.length > 0) || t("required_field");
    };
    resetForm.onSuccess = async () => {
      resetForm.reset(); // reset
      await router.push({ name: "dashboard" });
      Notify.create({
        type: "positive",
        message: t("password changed successfully"),
        progress: true,
        position: "top",
      });
    };
    resetForm.onFinished = () => {
      loading.value = false;
    };

    return {
      loading,
      isPwd,
      resetForm,
      requiredField,
      handleSubmit,
      t,
      capitalize,
      showPassword,
    };
  },
};
</script>
