import { defineStore } from "pinia";
import { api } from "src/boot/axios";
import {Notify} from "quasar";


export const useShopStore = defineStore("shop", {
  state: () => ({
    products:{
      pizzas:{},
      toppings:{},
      drinks:{},
      deserts:{},
      sides:{},
      sizes:{},
      crusts:{},
    },
    cart: {},
    checkout:{},
    order:{}

  }),
  persist: {
    beforeRestore: (ctx) => {
      // console.log(`about to restore '${ctx.store.$id}'`);
    },
    key:'shop'
  },
  getters: {
    getCart: (state) => {
      return state.cart
    },
  },
  actions: {
    async clearCart(){
      this.cart = {};
      this.order = {};
      await this.router.push({name:"Done", query:{message: 'Order Successful', level:'success'}})
    },
    async postToApiCart(data, url) {
      api.defaults.withCredentials = true

      await api
        .post(url, data)
        .then(async (response) => {
          // sanity check to retrieve the server cart and compare it
          await this.createOrder('api/v1/shop/orders/')
        })
      .catch(e=> Notify.create({type: 'negative', message: e.response?.data?.detail, closeBtn:true}))
    },
    async getCartApi(url){
      api.defaults.withCredentials = true
      await api.get(url)
        .then((data)=>console.log(data))
        .catch(e=> Notify.create({type: 'negative', message: e.response.data.detail, closeBtn:true}))
    },
    async createOrder(url) {
      api.defaults.withCredentials = true
      await api
        .post(url, {"email":"ahbox@outlook.com"})
        .then(async ({data}) => {

          Object.assign(this.order, data);
          await this.router.push({name:"Checkout"})
        })
        .catch(e=> Notify.create({type: 'negative', message: e.message, closeBtn:true}))
    },
    async addToLocalCart(id, products){
      this.cart[id] = [products]
    },
   async retrieveProducts(url){
      let response = await api.get(url);
      let all_products = response.data.results;
      this.products.drinks = all_products.filter((m)=>m.tags.includes('drink'))
     this.products.pizzas = all_products.filter((m)=>m.tags.includes('pizza'))
     this.products.deserts = all_products.filter((m)=>m.tags.includes('desert'))
     this.products.toppings = all_products.filter((m)=>m.tags.includes('topping'))
     this.products.sides = all_products.filter((m)=>m.tags.includes('side'))
     this.products.sizes = all_products.filter((m)=>m.tags.includes('size'))
     this.products.crusts = all_products.filter((m)=>m.tags.includes('crust'))
   }
  },
});
