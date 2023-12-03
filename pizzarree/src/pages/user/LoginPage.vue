<template>
  <user-access-card
    :form="step == 1 ? validateStepForm : loginForm"
    :loading="loading"
    :actionText="step == 1 ? 'user.login' : ''"
  >
    <!--  FORM -->
    <q-form class="q-gutter-md" @submit.prevent="handleSubmit">
      <q-stepper
        v-model="step"
        contracted
        header-class="tw-hidden"
        color="primary"
        animated
        :bordered="false"
        flat
      >
        <q-step :name="1" title="" :done="step > 1">
          <q-input
            outlined
            v-model="validateStepForm.username"
            type="text"
            name="username"
            :label="$t('user.username')"
            :hint="capitalize($t('user.login_hint'))"
            :error="validateStepForm.errors.has('username')"
            :error-message="validateStepForm.errors.get('username')"
            :rules="[requiredField]"
            :lazy-rules="'ondemand'"
            autocomplete
            autofocus
            autocorrect="off"
            spellcheck="false"
            :disable="loading"
          >
          </q-input>
        </q-step>
        <!--  password -->

        <q-step :name="2" title="login" :done="step > 2">
          <div
            class="flex items-center content-center justify-center column tw-mt-0 tw-mb-8"
            :key="step + 1"
            v-if="step == 2"
          >
            <p class="tw-font-bold tw-text-3xl">
              {{ capitalize($t("welcome")) }}
            </p>
            <!-- v-model="loginForm.username" -->
            <!-- :option="loginForm.username" -->
            <q-select
              v-model="store.potentialUsername"
              :options="store.potentialUsers"
              dense
              rounded
              outlined
              item-aligned
              options-dense
              :autofocus="false"
              @popup-show="switchIcons = true"
              @popup-hide="switchIcons = false"
            >
              <!-- @popup-show="step = 1" -->
              <template v-slot:prepend>
                <q-icon
                  :name="switchIcons ? 'o_add' : 'o_account_circle'"
                  :class="
                    switchIcons
                      ? 'tw-text-green-500 cursor-pointer'
                      : 'cursor-pointer'
                  "
                  @click.prevent="
                    step = 1;
                    switchIcons = false;
                  "
                />
              </template>
              <template
                v-slot:option="{ itemProps, opt, selected, toggleOption }"
              >
                <q-item v-bind="itemProps">
                  <q-item-section>
                    <q-item-label>{{ opt }} </q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-icon
                      name="o_remove"
                      class="cursor-pointer tw-text-red-500"
                      :model-value="selected"
                      @update:model-value="toggleOption(opt)"
                      @click.prevent="store.unsetPotentialUsers(opt)"
                    />
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </div>
          <q-input
            outlined
            v-model="loginForm.password"
            :type="isPwd ? 'password' : 'text'"
            :label="$t('user.password')"
            autocomplete
            autocorrect="off"
            spellcheck="false"
            autofocus
            :disable="loading"
            :rules="[requiredField]"
            :lazy-rules="'ondemand'"
          >
            <template v-slot:append>
              <q-icon
                :name="isPwd ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="isPwd = !isPwd"
              />
            </template>
          </q-input>
        </q-step>

        <template v-slot:navigation>
          <q-stepper-navigation>
            <div class="column" :class="step == 1 ? 'tw-mt-14' : ''">
              <div class="justify-between row full-width">
                <!-- Create Account  -->
                <q-btn
                  type="reset"
                  color="primary"
                  :to="{ name: 'Register' }"
                  flat
                  no-caps
                  dense
                  v-if="step == 1"
                >
                  {{ capitalize($t("create")) + " " + $t("account") }}
                </q-btn>
                <!-- Reset password  -->

                <q-btn
                  color="primary"
                  flat
                  no-caps
                  dense
                  :to="{ name: 'PasswordReset' }"
                  v-if="step == 2"
                >
                  {{ capitalize($t("forgot")) + " " + $t("user.password") }} ?
                </q-btn>

                <!-- submit -->

                <q-btn
                  :label="
                    step == 1
                      ? capitalize($t('next'))
                      : capitalize($t('user.login'))
                  "
                  type="submit"
                  color="primary"
                  :loading="loading"
                  no-caps
                />
              </div>
            </div>
          </q-stepper-navigation>
        </template>
      </q-stepper>
    </q-form>
  </user-access-card>
</template>

<script>
import { Notify } from "quasar";
import { reactive, ref, shallowRef, watch } from "vue";
import Form from "src/utils/Form";

import UserAccessCard from "src/components/partials/UserAccessCard.vue";
import { useAuthStore } from "stores/auth";
import { useRoute, useRouter } from "vue-router";
import { format } from "quasar";
import { useI18n } from "vue-i18n";

const validate_username_url = "api/v1/accounts/api-token-auth/validate/";
const login_url = "api/v1/accounts/api-auth-token/";
const profile_url = "api/v1/accounts/api-auth-user/profile/";
export default {
  name: "LoginPage",
  components: { UserAccessCard },
  setup() {
    const { capitalize } = format;
    const { t } = useI18n();
    const store = useAuthStore();
    const router = useRouter();
    const route = useRoute();
    const loading = ref(false);
    const isPwd = ref(true);
    const step = ref(1);
    const switchIcons = shallowRef(false);

    const validateStepForm = reactive(
      new Form({
        username: "",
      })
    );
    const loginForm = reactive(
      new Form({
        username: store.potentialUsername,
        password: "",
      })
    );

    const handleSubmit = async () => {
      loading.value = true;
      if (step.value == 1) {
        await validateStepForm
          .post(validate_username_url)
          .then(async ({ checks, username }) => {
            if (JSON.parse(checks)) await store.setPotenialUser(username);
          })
          .catch((e) => e);
      } else {
        await store.logIn(loginForm, login_url);
      }
    };
    const requiredField = (val) => {
      return (val && val.length > 0) || t("required_field");
    };
    validateStepForm.onSuccess = async () => {
      step.value = 2;
      loginForm.username = validateStepForm.username;
    };
    loginForm.onSuccess = async () => {
      loginForm.reset(); // reset
      await router.push(route.query.redirect || { name: "Dashboard" });
      await store.getProfileData(profile_url);
      Notify.create({
        type: "positive",
        message: `${t("user.welcome_back")}, ${capitalize(
          store.authUser.username
        )}`,
        position: "top",
        progress: true,
        multiLine: true,
        icon: "o_waving_hand",
        // classes: "tw-translate-y-10",
        iconSize: "2.5rem",
        iconColor: "yellow-7",
        // timeout: 5000,
      });
    };

    loginForm.onFinished = validateStepForm.onFinished = () => {
      loading.value = false;
    };
    if (store.potentialUsername && step.value == 1) {
      validateStepForm.username = store.potentialUsername;
      step.value = 2;
    }
    watch(
      () => store.potentialUsername,
      (value) => {
        if (value) {
          loginForm.username = value;
        } else {
          step.value = 1;
          switchIcons.value = false;
        }
      }
    );
    return {
      isPwd,
      loginForm,
      handleSubmit,
      loading,
      requiredField,
      capitalize,
      step,
      validateStepForm,
      switchIcons,
      store,
    };
  },
};
</script>
