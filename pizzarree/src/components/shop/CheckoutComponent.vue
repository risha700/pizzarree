
<template>
  <q-page-container>
    <q-card class="q-pa-lg">
      <q-banner rounded v-if="errors"  class="text-white bg-red q-mb-lg">
        {{errors}}
      </q-banner>

      <form id="checkout-form" class="column" @submit.prevent="handleSubmit" >
        <div id="payment-methods"></div>
        <div id="link-authentication-element" />
        <q-btn type="submit" align="center" color="secondary" stretch label="Pay Now" class="q-mt-lg" :disable="processing"/>
      </form>
    </q-card>
  </q-page-container>

</template>

<script>
import {defineComponent, onMounted, ref} from 'vue'
import {loadStripe} from '@stripe/stripe-js';
import {useShopStore} from "stores/shop";
import {storeToRefs} from "pinia";
import {Dark, Notify} from "quasar";
import {api} from "boot/axios";
import {useRouter} from "vue-router";

export default defineComponent({
  name: "CheckoutComponent",
  async setup(){
    const store = useShopStore();
    let {order} = storeToRefs(store);
    const router = useRouter();
    const errors = ref(null);
    const processing = ref(false);

    const handleErrors = (err)=>errors.value = err;
    onMounted(()=>{
      console.log(order.value.id)
        paymentElement.mount('#payment-methods')
        // linkAuthenticationElement.mount("#link-authentication-element");
    })
    const stripe = await loadStripe('pk_test_RUZqAN8CkTK39VGr7FuIxPWE', {
          // stripeAccount: '{{CONNECTED_STRIPE_ACCOUNT_ID}}',
    });


    var elements = await stripe.elements({
        mode: 'payment',
        // amount: 9999,
        amount: Math.round(order.value.total_cost.toFixed(2)*100),
        currency: 'usd',
        paymentMethodCreation: 'manual',
        appearance:{theme:Dark.isActive?'night':'stripe'},

    });
  const paymentElement = await elements.create('payment',{
      layout: {
        type: 'tabs',
      },
  });
    const handleSubmit = async (e) => {
        // Trigger form validation and wallet collection
      processing.value = true;
      const {error: submitError} = await elements.submit();
      if (submitError) {
        return handleErrors(submitError.message)
      }
    // Create the PaymentMethod using the details collected by the Payment Element
      const {error, paymentMethod} = await stripe.createPaymentMethod({
        elements,
        params: {
          billing_details: {
            address:{},
            name:'guest-user',
            email:order.value.email,
            phone:order.value.phone
          }
        }
      });

      if (error) {
        return handleErrors(error.message);
      }

       await api.post(`api/v1/shop/payment/checkout/${order.value.id}/`, {paymentMethodId:paymentMethod.id})
         .then(async (res)=> await handleServerResponse(res))
         .catch((err)=>{
           return handleErrors(err.message);
         })

      processing.value = false;
    }

    const handleServerResponse = async (response) => {
      if (response.data && response.data.error) {
        // Show error from server on payment form
        return handleErrors(response.data.error);
      } else if (response.status === "requires_action" ||response.data?.intent_status === "requires_action") {
        // Use Stripe.js to handle the required next action
        const {
          error,
          paymentIntent
        } = await stripe.handleNextAction({
          clientSecret: response.client_secret||response.data?.client_secret
        });

        if (error) {
          // Show error from Stripe.js in payment form
          return handleErrors(error.message);
          // Notify.create({type: 'negative', message: error.message, closeBtn:true})
        } else {
          // Actions handled, show success message
          Notify.create({type: 'positive', message: "Payment successful", closeBtn:true})
           await store.clearCart();
        }
      } else {
        // No actions needed, show success message
          Notify.create({type: 'positive', message: "Payment successful", closeBtn:true})
         await store.clearCart();

      }
    }


    return{
      elements,
      paymentElement,
      handleSubmit,
      errors, processing
    }
  },
})
</script>
