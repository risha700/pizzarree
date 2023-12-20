import { describe, jest, expect, test, afterEach, beforeEach } from "@jest/globals";
import { installQuasarPlugin } from "@quasar/quasar-app-extension-testing-unit-jest";
import { DOMWrapper, flushPromises, mount } from "@vue/test-utils";
import App from "src/App";
import {mountRouteSuspense, mountSuspense, router, setupUtils, testStore} from "app/test/utils";
import {useShopStore} from "stores/shop";
import { api } from "src/boot/axios";
import CartComponent from "components/shop/CartComponent.vue";
import MenuComponent from "components/shop/MenuComponent.vue";
import ProductCard from "components/shop/ProductCard.vue";

import ProductModal from "components/shop/ProductModal.vue";
import {Dark, Notify} from "quasar";
import {loadStripe, Stripe} from "@stripe/stripe-js";
import checkoutComponent from "components/shop/CheckoutComponent.vue";
import CheckoutPage from "pages/shop/CheckoutPage.vue";
import CheckoutComponent from "components/shop/CheckoutComponent.vue";
import checkoutPage from "pages/shop/CheckoutPage.vue";
import {nextTick} from "vue";



installQuasarPlugin({plugins:{Notify, Dark}});
setupUtils();




let mockProductsList = {
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 23,
            "tags": [
                "drink"
            ],
            "name": "Orange Juice",
            "slug": "orange-juice",
            "type": "SALE",
            "price": "2.99",
            "stock": 1000,
            "description": "",
            "published": true,
            "featured": false,
            "info": {},
            "created": "2023-12-04T21:34:17.037000Z",
            "updated": "2023-12-10T00:51:00.480000Z",
            "cover_image": "https://localhost:8000/media/uploads/products/build_vLPb96I.png"
        },
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
        },
        {
            "id": 21,
            "tags": [
                "crust"
            ],
            "name": "Brooklyn Crust",
            "slug": "brooklyn-crust",
            "type": "SALE",
            "price": "2.58",
            "stock": 10000,
            "description": "",
            "published": true,
            "featured": false,
            "info": {},
            "created": "2023-12-03T10:30:32.477000Z",
            "updated": "2023-12-10T07:44:44.151000Z",
            "cover_image": "https://localhost:8000/media/uploads/products/BK_PA3zy7k.png"
        },
      {
            "id": 33,
            "tags": [
                "size"
            ],
            "name": "XL",
            "slug": "xl",
            "type": "SALE",
            "price": "2.58",
            "stock": 10000,
            "description": "",
            "published": true,
            "featured": false,
            "info": {},
            "created": "2023-12-03T10:30:32.477000Z",
            "updated": "2023-12-10T07:44:44.151000Z",
            "cover_image": "https://localhost:8000/media/uploads/products/size.png"
        },
        {
            "id": 20,
            "tags": [
                "crust"
            ],
            "name": "Hand Tossed",
            "slug": "hand-tossed",
            "type": "SALE",
            "price": "3.79",
            "stock": 10000,
            "description": "",
            "published": true,
            "featured": false,
            "info": {},
            "created": "2023-12-03T10:30:08.496000Z",
            "updated": "2023-12-04T14:39:55.256000Z",
            "cover_image": "https://localhost:8000/media/uploads/products/HANDTOSS.png"
        },
        {
            "id": 19,
            "tags": [
                "pizza"
            ],
            "name": "Margreta",
            "slug": "margreta",
            "type": "SALE",
            "price": "11.99",
            "stock": 10000,
            "description": "",
            "published": true,
            "featured": false,
            "info": {},
            "created": "2023-12-03T10:29:42.852000Z",
            "updated": "2023-12-04T14:39:52.397000Z",
            "cover_image": "https://localhost:8000/media/uploads/products/pizza.png"
        }
    ]
}
let mockCartDetail ={
    "cart": [
        {
            "quantity": 1,
            "price": 11.99,
            "product": {
                "id": 5,
                "slug": "pizza-margreta",
                "name": "Pizza Margreta",
                "cover_image": "/media/uploads/products/pizza_margreta.png",
                "stock": 100,
                "price": "11.99"
            },
            "total_price": 11.99
        },
        {
            "quantity": 1,
            "price": 2.58,
            "product": {
                "id": 15,
                "slug": "xlarge",
                "name": "XLarge",
                "cover_image": null,
                "stock": 10000,
                "price": "2.58"
            },
            "total_price": 2.58
        },
        {
            "quantity": 1,
            "price": 3.79,
            "product": {
                "id": 20,
                "slug": "hand-tossed",
                "name": "Hand Tossed",
                "cover_image": "/media/uploads/products/BK_PA3zy7k.png",
                "stock": 10000,
                "price": "3.79"
            },
            "total_price": 3.79
        },
    ]
}
let mockSuccessfulOrderPayload = {
    "id": 58,
    "email": "1702455162613_guest@test.net",
    "phone": null,
    "updated": "2023-12-14T02:10:46.696063Z",
    "created": "2023-12-14T02:05:01.993567Z",
    "total_cost": 18.36,
    "paid": false,
    "discount_value": 0,
    "coupon": null,
    "items": [
        {
            "id": 1086,
            "price": "11.99",
            "product": {
                "id": 5,
                "slug": "pizza-margreta",
                "name": "Pizza Margreta",
                "cover_image": "https://localhost:8000/media/uploads/products/pizza_margreta.png",
                "stock": 100,
                "price": "11.99"
            },
            "quantity": 1,
            "order": 58
        },
        {
            "id": 1087,
            "price": "2.58",
            "product": {
                "id": 15,
                "slug": "xlarge",
                "name": "XLarge",
                "cover_image": null,
                "stock": 10000,
                "price": "2.58"
            },
            "quantity": 1,
            "order": 58
        },
        {
            "id": 1088,
            "price": "3.79",
            "product": {
                "id": 20,
                "slug": "hand-tossed",
                "name": "Hand Tossed",
                "cover_image": "https://localhost:8000/media/uploads/products/HANDTOSS.png",
                "stock": 10000,
                "price": "3.79"
            },
            "quantity": 1,
            "order": 58
        }
    ],
    "status": "('PENDING', 'pending')",
    "payment_method": null,
    "identifier": "7c4b7d35-3046-412f-9876-b0a7b46ab73f",
    "billing_address": null,
    "shipping_address": null
}

describe("Payment", () => {
  let wrapper;
  let shopStore;
  let push = jest.spyOn(router, "push");
  let api_get = jest.spyOn(api, "get");
  let api_post = jest.spyOn(api, "post");
  let api_patch = jest.spyOn(api, "patch");
  let api_put = jest.spyOn(api, "put");
  // const  mockedStripe = jest.requireActual('@stripe/stripe-js');
  // let loadTestStripe = jest.spyOn(mockedStripe, 'loadStripe')

  let documentWrapper = new DOMWrapper(document.body)

  beforeEach(async () => {
    wrapper = await mountRouteSuspense(App);
    shopStore = useShopStore();
    await nextTick();
  });

  test('it shows checkout form',async()=>{

    api_get.mockResolvedValueOnce({status:200, data:mockProductsList})
    push({name:'Menu'})
    await nextTick()

    api_get.mockResolvedValueOnce({status:200, data:mockCartDetail})
    api_post.mockResolvedValueOnce({status:201, message:"Cart Updated"})
    push({name:'Cart'})
    await nextTick()
    await flushPromises()
    // push({name:'Checkout'})
    // await nextTick()
    // await flushPromises()
    // let cart_component = wrapper.getComponent(CheckoutPage);

    //
    // api_post.mockResolvedValueOnce({status:201, data:mockSuccessfulOrderPayload})
    await nextTick()
   await console.log(wrapper.text())

  });
  test.skip('can load stripe', async () => {
     const mockElement = () => ({
      mount: jest.fn(),
      destroy: jest.fn(),
      on: jest.fn(),
      update: jest.fn(),
    })

    const mockElements = () => {
      const elements = {};
      return {
              create: jest.fn((type) => {
              elements[type] = mockElement();
              return elements[type];
            }),
            getElement: jest.fn((type) => {
              return elements[type] || null;
            }),
          }
      }

    const mockedStripe = () => ({
      elements: jest.fn(() => mockElements()),
      createToken: jest.fn(),
      loadScript: jest.fn(),
      loadStripe: jest.fn(),
      createSource: jest.fn(),
      createPaymentMethod: jest.fn(),
      confirmCardPayment: jest.fn(),
      confirmCardSetup: jest.fn(),
      paymentRequest: jest.fn(),
      _registerWrapper: jest.fn(),
    })
    const mockStripe = jest.requireActual('@stripe/stripe-js')

    jest.mock('@stripe/stripe-js', () => {

      return ({
        ...mockStripe,
        elements: () => {
          return mockElements
        },
        createPaymentMethod: () => {
          return mockedStripe
        },
      })
    })


    });
});
