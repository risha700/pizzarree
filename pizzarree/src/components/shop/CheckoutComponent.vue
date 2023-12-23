
<template>
  <q-page-container class="q-pa-lg flex  items-start tw-gap-10">
    <q-card class="q-pa-lg tw-flex-auto">
      <div class="text-h6 tw-border-b-2 tw-border-dashed tw-mb-2"> Order# {{order.id}} Summary</div>

      <template v-for="(product, id) in store.cart" :key="id">
        <template v-for="item in product.items" :key="item.id+id">
            <template v-for="nestedItem in item" :key="nestedItem.id">
              <div class="flex justify-between items-center content-between"
                   :class="nestedItem.name === item[0].name?'tw-min-w-[300px]':'row inline wrap q-ml-lg text-italic'">
                <div>{{nestedItem.name}}</div>
                <div v-if="nestedItem.name === item[0].name">{{product.quantity}}x</div>
              </div>
            </template>
        </template>
      </template>
      <div class="tw-border-solid tw-border-t-2 column justify-start tw-my-4 ">
        <div class="text-h5 tw-text-green-400 " v-if="order.discount_value">Discounts {{order.discount_value}}</div>
        <div class="text-h5 tw-mt-2">Total {{order.total_cost}}</div>
      </div>
    </q-card>
    <q-card class="q-pa-lg tw-flex-auto">
      <q-banner rounded v-if="errors"  class="text-white bg-red q-mb-lg">
        {{errors}}
      </q-banner>
      <q-form class="column" @submit.prevent="handleSubmit" >
        <div  ref="paymentElement"></div>
        <q-btn type="submit" align="center" color="secondary" stretch label="Pay Now" class="q-mt-lg" :disable="processing"/>
      </q-form>
    </q-card>

  </q-page-container>

</template>

<script>
import {defineComponent, onMounted, reactive, ref} from 'vue'
import {loadStripe} from '@stripe/stripe-js';
import {useShopStore} from "stores/shop";
import {storeToRefs} from "pinia";
import {Dark, Notify} from "quasar";
import {api} from "boot/axios";
import {useRouter} from "vue-router";
const STRIPE_KEY = process.env.VUE_STRIPE_PUBLISHABLE_KEY;

export default defineComponent({
  name: "CheckoutComponent",
  async setup(){
    const store = useShopStore();
    let {order} = storeToRefs(store);
    const router = useRouter();
    const errors = ref(null);
    const processing = ref(false);
    const paymentElement = ref(null);
    const handleErrors = (err)=>errors.value = err;
    let elements;
    let stripe;

    onMounted(async ()=>{

        if(order.value.id)
          stripe = await loadStripe(STRIPE_KEY, {
                // stripeAccount: '{{CONNECTED_STRIPE_ACCOUNT_ID}}',
          });

        elements = await stripe.elements({
            mode: 'payment',
            amount: Math.round(order.value.total_cost?.toFixed(2)*100),
            currency: 'usd',
            paymentMethodCreation: 'manual',
            appearance:{theme:Dark.isActive?'night':'stripe'},
        });
        const paymentElements = await elements.create('payment',{
            layout: {
              type: 'tabs',
            },
        });

        paymentElements.mount(paymentElement.value)

        store.stripe = stripe;
        store.elements = elements;

        // const linkAuthenticationElement = elements.create("linkAuthentication");
        // linkAuthenticationElement.mount("#link-authentication-element");
    })


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
      // process payment on the server
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

    if(!order.value.id){
      await router.push({name:'Menu'});
      errors.value = 'seems that your cart is empty!'
      return {errors, handleSubmit, processing, store}
    }


    return{
      handleSubmit,
      errors, processing,
      order,store, paymentElement
    }
  },
})
</script>
