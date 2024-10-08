import { defineStore } from "pinia";
import { api } from "src/boot/axios";
import {Notify} from "quasar";
import {useAuthStore} from "stores/auth";


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
    order:{},
    customer_email:null

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
    getCartItemsCount: (state) => {
      let count = 0;
      Object.values(state.cart).forEach((item)=>{
        count += item?.quantity||0;
      })
      return count;
    },
    hasCurrentPendingOrder:(state)=>{
      // TODO: add  condition on user email
      return Object.keys(state.order).length > 0 && Object.hasOwnProperty(state.order, 'id') ;
    },
    AuthUser: (state)=>{
      const user = useAuthStore();
      return user
    },
    flatCartProducts:(state)=>{
      return Object.values(state.cart).flatMap(
      ({items, quantity})=> ({items, quantity})).map(
        ({items, quantity})=>Object.values(items).flat().map(x=>[{id:x.id, quantity}]))
        .flat().flatMap(x=>x)

    }
  },
  actions: {

    async clearCart(){
      this.cart = {};
      this.order = {};
      await this.router.push({name:"Done", query:{message: 'Order Successful', level:'success'}})
    },

    async serverCartSanityCheck(){
      let active_session_cart_items= await api.get('api/v1/shop/cart/details/');
      let transformedCartItems = active_session_cart_items.data.cart.flatMap((p)=>({id: p.product.id, quantity:p.quantity}))
      const sameObj = JSON.stringify(this.flatCartProducts.sort()) === JSON.stringify(transformedCartItems.sort())
      const cartIsDirty = Object.keys(active_session_cart_items.data).length !== 0;
      if (cartIsDirty && !sameObj){
          await api.post('api/v1/shop/cart/clear/');
      }
      return sameObj;
    },

    async postToApiCart(data, url="api/v1/shop/cart/add/") {
      api.defaults.withCredentials = true
      //todo: sanity check for adjusted active session orders
      let sameCart = await this.serverCartSanityCheck();

      if(sameCart){
        // assumes we have order in storage
          await this.router.push({name:"Checkout"})
          return;
      }

      await api
        .post(url, data) // add to cart
        .then(async (response) => {
            await this.createOrUpdateOrder();
        })
      .catch(e=> Notify.create({type: 'negative', message: e.response?.data?.detail, closeBtn:true}))
    },
    async getCartApi(url){
      api.defaults.withCredentials = true
      await api.get(url)
        .then((data)=>console.log(data))
        .catch(e=> Notify.create({type: 'negative', message: e.response.data.detail, closeBtn:true}))
    },
    async createOrUpdateOrder(redirects=true) {
      api.defaults.withCredentials = true
      let url;
      let method;
      if(this.hasCurrentPendingOrder){
        url = `api/v1/shop/orders/${this.order.id}/`;
        method = 'put';
      }else{
        url = 'api/v1/shop/orders/';
        method = 'post';
      }
      await api[method](url, {"email":this.customer_email})
        .then(async ({data}) => {
          Object.assign(this.order, data);
          if(redirects)
          await this.router.push({name:"Checkout"})
        })
        .catch(e=> {
          console.log(e.message)
          Notify.create({type: 'negative', message: e.message, closeBtn: true});
        })
    },
    async addToLocalCart(id, products){
      // adding to local cart
      const comparer= (x)=>JSON.stringify(Object.values(x))
      let duplicate=false;
      let idx = id;
      for (const cartItemId in this.cart) {
        if(comparer(this.cart[cartItemId].items.flat().sort())=== comparer(products.sort())){
            duplicate = true;
            idx = cartItemId;
        }
      }
      if(duplicate){
        this.cart[idx].quantity +=1;
      }else{
        this.cart[idx]  = {items:[products], quantity:1}

      }
        // this.cart[id] = [products]

    },
   async retrieveProducts(url='api/v1/shop/products'){
      let response = await api.get(url);
      let all_products = response.data.results;
      this.products.drinks = all_products.filter((m)=>m.tags.includes('drink'))
      this.products.pizzas = all_products.filter((m)=>m.tags.includes('pizza'))
      this.products.deserts = all_products.filter((m)=>m.tags.includes('desert'))
      this.products.toppings = all_products.filter((m)=>m.tags.includes('topping'))
      this.products.sides = all_products.filter((m)=>m.tags.includes('side'))
      this.products.sizes = all_products.filter((m)=>m.tags.includes('size'))
      this.products.crusts = all_products.filter((m)=>m.tags.includes('crust'))
   },
   async setupCustomerOrderEmail(){
      if(this.AuthUser.isAuthenticated){
        this.customer_email = this.AuthUser.authUser.email;
      }
      else if(this.customer_email == null){
          // Todo: make it more unique
        // this.customer_email = Date.now()+'_guest@'+window.location.host;
        this.customer_email = Date.now()+'_guest@test.net';
      }
   },

  },
});
