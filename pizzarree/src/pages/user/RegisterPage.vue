<template>

  <user-access-card
    :loading="loading"
    actionText="menu.register"
    :form="registerForm"
  >
    <q-form class="q-gutter-md" @submit.prevent="handleSubmit">
      <q-input
        label="username"
        type="text"
        v-model="registerForm.username"
        outlined
        autocomplete
        autocorrect="off"
        :rules="[requiredField]"
        autofocus
        :error="registerForm.errors.has('username')"
        :error-message="registerForm.errors.get('username')"
      ></q-input>
      <q-input
        label="email"
        type="email"
        v-model="registerForm.email"
        outlined
        autocomplete
        autocorrect="off"
        :rules="[requiredField]"
        :error="registerForm.errors.has('email')"
        :error-message="registerForm.errors.get('email')"
      ></q-input>
      <q-input
        label="phone"
        type="tel"
        v-model="registerForm.phone"
        outlined
        autocomplete
        autocorrect="off"
        :rules="[requiredField]"
        :error="registerForm.errors.has('phone')"
        :error-message="registerForm.errors.get('phone')"
      ></q-input>
      <div class="items-start md:tw-flex tw-justify-between q-gutter-y-md">
        <q-input
          label="password"
          v-model="registerForm.password"
          :type="isPwd ? 'password' : 'text'"
          outlined
          name="password"
          autocomplete
          autocorrect="off"
          :rules="[requiredField]"
          :error="registerForm.errors.has('password')"
          :error-message="registerForm.errors.get('password')"
        ></q-input>
        <q-input
          label="confirm"
          :type="isPwd ? 'password' : 'text'"
          name="password2"
          v-model="registerForm.password2"
          outlined
          autocomplete
          autocorrect="off"
          :rules="[requiredField]"
          :error="registerForm.errors.has('password2')"
          :error-message="registerForm.errors.get('password2')"
        ></q-input>
      </div>
      <q-checkbox
        label="show password"
        v-model="showPassword"
        @click="isPwd = !isPwd"
      ></q-checkbox>
      <div>
        <!-- <q-toggle
          v-model="agreeTOS"
          checked-icon="check"
          color="green"
          unchecked-icon="clear"
          label="Agree with Terms of Service"
        /> -->
        <q-field
          ref="toggle"
          :value="agreeTOS"
          :rules="[() => agreeTOS || 'please agree to our terms.']"
          borderless
          dense
          lazy-rules
          for="tos"
        >
          <template v-slot:control>
            <q-toggle
              v-model="agreeTOS"
              checked-icon="check"
              color="green"
              unchecked-icon="clear"
              name="tos"
              label="Agree with Terms of Service"
            />
          </template>
        </q-field>
      </div>
      <div class="items-start column">
        <div class="justify-between row full-width">
          <q-btn
            type="reset"
            color="primary"
            :to="{ name: 'Login' }"
            flat
            no-caps
          >
            sign in instead?
          </q-btn>
          <q-btn
            label="create"
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

<script setup name="RegisterPage">
import { Notify } from "quasar";
import { useRouter } from "vue-router";
import UserAccessCard from "components/partials/UserAccessCard.vue";

const { ref, reactive } = require("@vue/reactivity");
const { default: Form } = require("src/utils/Form");
const { useI18n } = require("vue-i18n");
const register_url = "api/v1/accounts/api-auth-register/";
const router = useRouter();
const { t } = useI18n();
let loading = ref(false);
let showPassword = ref(false);
let isPwd = ref(true);
let agreeTOS = ref(false);
const registerForm = reactive(
  new Form({
    username: "",
    password: "",
    password2: "",
    email: "",
    phone: "",
  })
);

const handleSubmit = async () => {
  loading.value = true;
  await registerForm
    .post(register_url)
    .then(async (response) => {
      // TODO
      // redirect to login with notify that we got registration request
      Notify.create({
        type: "warning",
        message: `${t("user.register_thankyou")} ${response.email}`,
        closeBtn: `${t("dismiss")}`,
        multiLine: true,
        position: "top",
        timeout: 0,
        classes: "tw-mt-14",
      });
      await router.push({ name: "Login" });
    })
    .catch((err) => err)
    .finally(() => (loading.value = false));
};

const requiredField = (val) => {
  return (val && val.length > 2) || t("required_field");
};
</script>
