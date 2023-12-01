<template>
  <q-page class="content-center justify-center tw-h-full tw-w-full column">
    <q-card class="column tw-min-w-[440px] tw-min-h-[440px] q-pa-lg" rounded>
      <q-linear-progress
        indeterminate
        color="primary"
        class="absolute-top"
        v-if="loading"
      />

      <div class="text-center q-pb-lg">


        <div
          class="tw-font-extrabold tw-text-xl tw-underline tw-underline-offset-[0.78rem] tw-my-4"
          v-if="actionText.length"
        >
          {{ capitalize($t(actionText)) }}
        </div>
      </div>
      <FormErrors :errors="form.errors" v-if="form && form.commonErrors()" />

      <q-card-section class="col">
        <slot></slot>
      </q-card-section>
    </q-card>
    <div class="column tw-max-h-6 q-pt-sm">
      <div class="justify-between row tw-mx-6">

        <div class="justify-around row">
          <q-btn
            :label="capitalize($t('terms_of_service'))"
            dense
            no-caps
            flat
            unelevated
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { format } from "quasar";
import FormErrors from "components/partials/FormErrors";


export default {
  name: "UserAccessCard",
  components: {  FormErrors },

  props: {
    form: {
      type: Object,
      default: () => {},
    },
    loading: {
      type: Boolean,
      default: false,
    },
    actionText: {
      type: String,
      default: "",
    },
  },
  setup() {
    const { capitalize } = format;

    return {
      capitalize,
    };
  },
};
</script>
