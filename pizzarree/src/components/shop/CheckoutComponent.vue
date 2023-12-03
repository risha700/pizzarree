
<template>
  <form id="checkout-form" @submit="handleSubmit">
    <div id="payment-methods"></div>
    <div id="link-authentication-element" />
    <button type="submit">Pay Now</button>
  </form>
</template>

<script>
import {defineComponent, onMounted} from 'vue'
import {loadStripe} from '@stripe/stripe-js';

export default defineComponent({
  name: "CheckoutComponent",
  async setup(){
    onMounted(()=>{
        paymentElement.mount('#payment-methods')
        // linkAuthenticationElement.mount("#link-authentication-element");
    })
    const stripe = await loadStripe('pk_test_RUZqAN8CkTK39VGr7FuIxPWE');


    var elements = await stripe.elements({
        mode: 'payment',
        amount: 1099,
        currency: 'usd',
        paymentMethodCreation: 'manual',
    });
  const paymentElement = await elements.create('payment',{
      layout: {
        type: 'tabs',
        defaultCollapsed: false,
        radios: false,
        spacedAccordionItems: false
      },
      defaultValues:{
          name:'rs',
          email:'rs@mac.local'
        },

  });
    const handleSubmit = async (e) => {
      e.preventDefault();
      elements.submit().then((res)=>{
        console.log("submitted ", res)
        console.log(res.error)
      }).catch((e)=>console.log(e.message));

       stripe.createPaymentMethod({
        elements,
        params: {
          billing_details: {
            address:{},
            name:'rs',
            email:'rs@mac.local',
            phone:'+1615115723'
          }
        }
      }).then((res)=>console.log(res.paymentMethod)).catch(e=>console.log(e.message))

      // const { error } = await stripe.confirmPayment({
      //     elements,
      //     confirmParams: {
      //       return_url: `${window.location.origin}?=success`,
      //       // use_stripe_sdk:true
      //     },
      //   payment_method: paymentElement,
      //
      //
      //
      // });
    }

    return{
      elements,
      paymentElement,
      handleSubmit
    }
  },
})
</script>
