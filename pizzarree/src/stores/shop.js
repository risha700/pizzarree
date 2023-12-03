import { defineStore } from "pinia";
import { api } from "src/boot/axios";

export const useShopStore = defineStore("shop", {
  state: () => ({
    products:{},
    cart: {},
    checkout:{}
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
    async addToCart(form, url) {
      await form
        .post(url)
        .then((data) => {
          this.cart = data;
        })
        .catch((e) => e);
    },

  },
});
