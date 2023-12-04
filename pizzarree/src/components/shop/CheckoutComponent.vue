
<template>
  <form id="checkout-form" @submit="handleSubmit">
    <div id="payment-methods"></div>
    <div id="link-authentication-element" />
    <button type="submit" class="tw-bg-blue-500 tw-hover:tw-bg-blue-700 tw-text-white tw-font-bold tw-py-2 tw-px-4 tw-rounded-full">Pay Now</button>
  </form>
</template>

<script>
import {defineComponent, onMounted} from 'vue'
import {loadStripe} from '@stripe/stripe-js';
import {useShopStore} from "stores/shop";
import {storeToRefs} from "pinia";
import {Notify} from "quasar";
import {api} from "boot/axios";
import {useRouter} from "vue-router";

export default defineComponent({
  name: "CheckoutComponent",
  async setup(){
    const store = useShopStore();
    let {order} = storeToRefs(store);
    const router = useRouter();
    onMounted(()=>{
      console.log(order.value.id)
        paymentElement.mount('#payment-methods')
        // linkAuthenticationElement.mount("#link-authentication-element");
    })
    const stripe = await loadStripe('pk_test_RUZqAN8CkTK39VGr7FuIxPWE');


    var elements = await stripe.elements({
        mode: 'payment',
        // amount: 9999,
        amount: Math.round(order.value.total_cost.toFixed(2)*100),
        currency: 'usd',
        paymentMethodCreation: 'manual',
    });
  const paymentElement = await elements.create('payment',{
      layout: {
        type: 'tabs',
      },
  });
    const handleSubmit = async (e) => {
      e.preventDefault();
      elements.submit().then((res)=>{
      }).catch(e=> Notify.create({type: 'negative', message: e.message, closeBtn:true}))

       stripe.createPaymentMethod({
        elements,
        params: {
          billing_details: {
            address:{},
            name:'guest-user',
            email:order.value.email,
            phone:order.value.phone
          }
        }
      }).then(async (res)=>{

        let server_res = await api.post(`api/v1/shop/payment/checkout/${order.value.id}/`,
          {paymentMethodId:res.paymentMethod.id});

        await handleServerResponse(server_res);
        // post it to the server res.paymentMethod
       }).catch(e=> Notify.create({type: 'negative', message: e.message, closeBtn:true}))
    }

    const handleServerResponse = async (response) => {
      if (response.error) {
        // Show error from server on payment form
        Notify.create({type: 'negative', message: response.error.message, closeBtn:true})
      } else if (response.status === "requires_action") {
        // Use Stripe.js to handle the required next action
        const {
          error,
          paymentIntent
        } = await stripe.handleNextAction({
          clientSecret: response.client_secret
        });

        if (error) {
          // Show error from Stripe.js in payment form
          Notify.create({type: 'negative', message: error.message, closeBtn:true})
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
      handleSubmit
    }
  },
})
</script>
