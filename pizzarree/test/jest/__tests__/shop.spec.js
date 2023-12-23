import { describe, jest, expect, test, afterEach, beforeEach } from "@jest/globals";
import { installQuasarPlugin } from "@quasar/quasar-app-extension-testing-unit-jest";
import { DOMWrapper, flushPromises, mount } from "@vue/test-utils";
import App from "src/App";
import {mountRouteSuspense, mountSuspense, router, setupUtils} from "app/test/utils";
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

describe("Shop", () => {
  let wrapper;
  let shopStore;
  let push = jest.spyOn(router, "push");
  let api_get = jest.spyOn(api, "get");
  let api_post = jest.spyOn(api, "post");
  let api_patch = jest.spyOn(api, "patch");
  let api_put = jest.spyOn(api, "put");
  let documentWrapper= new DOMWrapper(document.body)
  // const  mockedStripe = jest.requireActual('@stripe/stripe-js');
  // let loadTestStripe = jest.spyOn(mockedStripe, 'loadStripe')
  // loadTestStripe.mockResolvedValue({
  //   ...mockedStripe,
  //   _api_key: 'pk_test_RUZqAN8CkTK39VGr7FuIxPWE',
  //   _createPaymentMethod: jest.fn(),
  //   elements:()=>{
  //     return{
  //          default:jest.fn(),
  //         create: jest.fn()
  //     }
  //   }
  // })
  beforeEach(async () => {
    wrapper = await mountRouteSuspense(App,{
      shallow:false,

      });

    shopStore = useShopStore();
    // jest.resetAllMocks();

  });
  afterEach(async () => {
    // jest.restoreAllMocks()
    // shopStore?.$reset();
    // router.options.history.destroy(); // this doesnt reset router you need to create new instance
    // await router.isReady();
  });

  test("renders menu page with products", async () => {
    push({ name: "Menu" });
    api_get.mockResolvedValue({status:200, data:mockProductsList})
    await flushPromises();
    expect(api_get).toHaveBeenCalledTimes(1)
    expect(router.currentRoute.value.name).toEqual("Menu");
    let page = await wrapper.find(".q-page-container");
    expect(page.html()).not.toBe("");
    expect(page.html()).toContain(mockProductsList.results[0].name)
  });

  test("user can view memu page", async () => {
    // I have a menu
    push({ name: "Menu" });
    await flushPromises();
    expect(router.currentRoute.value.name).toEqual("Menu");
  });

  test("user can choose item from menu", async () => {

    push({ name: "Menu" });
    await flushPromises();

    expect(router.currentRoute.value.name).toEqual("Menu");
    // I have products in the store
    expect(shopStore.products).not.toBe({});
    let any_prod_img = await wrapper.findAll('img')[0]; // margreta pizza
    await any_prod_img.trigger('click');
    await flushPromises();
    // I have a popup product modal
    let product_card = await wrapper.getComponent(ProductCard);
    expect(product_card.emitted()).toHaveProperty('showModal')

    let menu = await wrapper.getComponent(MenuComponent);
    expect(menu.vm.showModal).toBeTruthy();
    // expect(menu.vm.chosenProduct).toEqual(mockProductsList.results[3]);
    let product_modal = await wrapper.findComponent(ProductModal);
    expect(product_card.vm.product).toEqual(menu.vm.chosenProduct)
    expect(product_modal.vm.modelValue).toBeTruthy();
    expect(product_modal.vm.currentPassedProduct).toEqual(product_modal.vm.product)


    expect(product_modal.vm.myPizza.length).toBe(1)
    expect(documentWrapper.html()).toContain('q-dialog')
    let radios = documentWrapper.findAll('.q-radio ')
    radios.forEach(x=>x.trigger('click')) // choose all
    await flushPromises();
    expect(product_modal.vm.myPizza.length).toBe(radios.length);
    //
    let modal_btns = documentWrapper.findAll("button");
    let add_to_order = modal_btns.filter(m=>m.text().includes("Add"))[0]
    await add_to_order.trigger("click");
    await flushPromises();
    expect(product_modal.emitted()).toHaveProperty('hideModal');
    expect(shopStore.cart[Object.keys(shopStore.cart)[0]].items).toContain(product_modal.vm.myPizza)

  });

  test("user can view cart", async () => {
    // I have a cart with a pizza
    push({ name: "Cart" });
    await flushPromises();
    // console.log(shopStore.cart)
    let cart_component = wrapper.getComponent(CartComponent);
    expect(router.currentRoute.value.name).toEqual("Cart");
    expect(Number(cart_component.vm.cartTotal)).toEqual(18.36)
    // console.log(wrapper.html())
    expect(wrapper.html()).toContain("Margreta");
  });
  test("user can edit item in cart", async () => {
    // I have a cart with a pizza
    push({ name: "Cart" });
    await flushPromises();
    let cart_component = wrapper.getComponent(CartComponent);
    let btns = cart_component.findAll("button");
    let editBtn =  btns.find(b=>b.html().includes('edit'));
    // remove the order item
    editBtn.trigger('click');
    await flushPromises();

    let radios = documentWrapper.findAll('.q-radio ')

    expect(documentWrapper.html()).toContain(' role="dialog"')
    // need to test the toppings

  });

    test("user can remove from cart", async () => {
    // I have a cart with a pizza
    push({ name: "Cart" });
    await flushPromises();
    let cart_component = wrapper.getComponent(CartComponent);
    let btns = cart_component.findAll("button");
    let removeBtn =  btns.find(b=>b.html().includes('delete'));
    // remove the order item
    removeBtn.trigger('click');
    await flushPromises();

    expect(wrapper.html()).toContain("Shopping")
    let checkoutBtn =  btns.find(b=>b.html().includes('Checkout'));
    // expect(checkoutBtn.html()).toContain('disabled=""')
    expect(checkoutBtn.attributes()).toHaveProperty('disabled')
    expect(Number(cart_component.vm.cartTotal)).toEqual(0)
  });

  test('user can checkout a cart', async ()=>{
    // visit menu page
    push({ name: "Menu" });
    expect(shopStore.products).not.toBe({});
    await flushPromises();
    // click the image for product modal
    let any_prod_img = await wrapper.findAll('img')[0]; // margreta pizza
    await any_prod_img.trigger('click');
    // adjust size and crust
    let radios = documentWrapper.findAll('.q-radio ')
    radios.forEach(x=>x.trigger('click')) // choose all
    await flushPromises();
    // finding add to cart btn
    let modal_btns = documentWrapper.findAll("button");
    let add_to_order = modal_btns.filter(m=>m.text().includes("Add"))[0]
    await add_to_order.trigger("click");
    // go to cart
    push({name:'Cart'})
    await flushPromises()
    let cart_component = await wrapper.getComponent(CartComponent)
    expect(Number(cart_component.vm.cartTotal)).toEqual(18.36)
    expect(cart_component.vm.isCartEmpty).toBeFalsy();

    let checkout_btn = wrapper.findAll('button').filter(b=>b.text().includes('Checkout'))[0]
    expect(checkout_btn.attributes()).not.toHaveProperty('disabled');
    api_get.mockResolvedValue({status:200, data:mockCartDetail})
    api_post.mockResolvedValue({status:201, message:"Cart Updated"})

    await checkout_btn.trigger('click');

    api_post.mockResolvedValue({status:201, data:mockSuccessfulOrderPayload})


    await flushPromises();
    expect(router.currentRoute.value.name).toEqual("Checkout");

  });

  // test('can load stripe form', async ()=>{
  //
  //   await flushPromises();
  //
  //   expect(router.currentRoute.value.name).toEqual("Checkout");
  //   const checkout_comp = wrapper.findComponent(checkoutPage)
  //   // wrapper = await mountRouteSuspense(checkoutPage,{  attachTo:document.body})
  //   await flushPromises();
  //   await checkout_comp.vm.$nextTick()
  //    console.log(await checkout_comp.html())
  // });




});
