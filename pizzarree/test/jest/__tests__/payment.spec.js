/**
 * @jest-environment jsdom
 */
import { describe, jest, expect, test, beforeEach } from "@jest/globals";
import {installQuasarPlugin} from "@quasar/quasar-app-extension-testing-unit-jest";
import {DOMWrapper, flushPromises} from "@vue/test-utils";
import App from "src/App";
import {mountRouteSuspense, setupUtils,} from "app/test/utils";
import {useShopStore} from "stores/shop";
import {Dark, Notify} from "quasar";
import {nextTick} from "vue";
import {fireEvent, waitFor} from "@testing-library/dom";
import '@testing-library/dom'
import checkoutComponent from "components/shop/CheckoutComponent.vue";
import {loadStripe} from "@stripe/stripe-js";


installQuasarPlugin({plugins:{Notify, Dark}});
setupUtils();
require('jest-fetch-mock').enableMocks()
//
const  mockedStripe = jest.requireActual('@stripe/stripe-js');
let loadTestStripe = jest.spyOn(mockedStripe, 'loadStripe')


describe("Payment", () => {
  let wrapper;
  let shopStore;
  let documentWrapper = new DOMWrapper(document.body);


  beforeEach(async () => {

    let meta_elm = document.createElement('meta');
    meta_elm.httpEquiv ="Content-Security-Policy";
    meta_elm.content="default-src *; style-src 'self' *.stripe.com 'unsafe-inline'; script-src * 'self' 'unsafe-inline' localhost:* *.stripe.com 'unsafe-eval'; img-src 'self' data localhost:* *.stripe.com 'unsafe-inline';";
    document.querySelector('head').prepend( meta_elm)
    // global.fetch.resetMocks()
    // global.fetch.doMock()
    jest.useFakeTimers()
    wrapper = await mountRouteSuspense(App, {attachTo:document.body});
    shopStore = useShopStore();

    await nextTick();
  });
  afterEach(async () => {
     jest.useRealTimers()
  });

  test('it renders checkout elements',async()=>{

    shopStore.cart = {
    "drink_6gk7ui": {
        "items": [
            [
                {
                    "id": 8,
                    "tags": [
                        "drink"
                    ],
                    "name": "Coke",
                    "slug": "coke",
                    "type": "SALE",
                    "price": "2.99",
                    "stock": 1000,
                    "description": "",
                    "published": true,
                    "featured": false,
                    "info": {},
                    "created": "2023-12-03T10:19:15.436000Z",
                    "updated": "2023-12-10T00:48:17.280000Z",
                    "cover_image": "https://localhost:8000/media/uploads/products/dpz-coke.png"
                }
            ]
        ],
        "quantity": 2
    },
    "desert_ra1s6": {
        "items": [
            [
                {
                    "id": 22,
                    "tags": [
                        "desert"
                    ],
                    "name": "Lava Cake",
                    "slug": "lava-cake",
                    "type": "SALE",
                    "price": "5.99",
                    "stock": 10000,
                    "description": "",
                    "published": true,
                    "featured": false,
                    "info": {},
                    "created": "2023-12-03T10:31:24.574000Z",
                    "updated": "2023-12-04T14:40:01.096000Z",
                    "cover_image": "https://localhost:8000/media/uploads/products/dessert.png"
                }
            ]
        ],
        "quantity": 2
    }
};
    shopStore.order = {
    "id": 64,
    "email": "1703204772853_guest@test.net",
    "phone": null,
    "updated": "2023-12-22T00:37:58.302981Z",
    "created": "2023-12-22T00:37:58.302955Z",
    "total_cost": 17.96,
    "paid": false,
    "discount_value": 0,
    "coupon": null,
    "items": [
        {
            "id": 1402,
            "price": "2.99",
            "product": {
                "id": 8,
                "slug": "coke",
                "name": "Coke",
                "cover_image": "https://localhost:8000/media/uploads/products/dpz-coke.png",
                "stock": 1000,
                "price": "2.99"
            },
            "quantity": 2,
            "order": 64
        },
        {
            "id": 1403,
            "price": "5.99",
            "product": {
                "id": 22,
                "slug": "lava-cake",
                "name": "Lava Cake",
                "cover_image": "https://localhost:8000/media/uploads/products/dessert.png",
                "stock": 10000,
                "price": "5.99"
            },
            "quantity": 2,
            "order": 64
        }
    ],
    "status": [
        "PENDING",
        "pending"
    ],
    "payment_method": null,
    "identifier": "028c1cfa-7460-4938-82f2-b1f7b95a22db",
    "billing_address": null,
    "shipping_address": null
};


    let checkout_wrapper = await mountRouteSuspense(checkoutComponent, {attachTo:document.body})
    let checkout_comp = await checkout_wrapper.findComponent(checkoutComponent)
    // await router.push({name:'Checkout'})

    await flushPromises();
    await nextTick()
    expect(document.head.outerHTML).toContain('stripe')

    // expect(loadTestStripe).toBeCalled();
    // const script = document.querySelector('script');
    // console.log(script.src)
    // try {
    //   fireEvent.load(script)
    // }catch (e){
    //   console.log('err loading script', e)
    // }
    jest.advanceTimersByTime(3000)
    // it should if stripe script define window.Stripe
    // expect(checkout_wrapper.get('form').html()).toContain('StripeElement');
  return expect(Promise.resolve(loadStripe)).resolves.toBe(loadTestStripe);

    // console.log(window.document.head.outerHTML)
  })

});

