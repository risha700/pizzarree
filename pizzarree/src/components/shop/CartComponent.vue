<template>

    <div class="flex  justify-between  self-start items-start row tw-static q-layout-padding col">

      <q-card class=" col-sm-12 col-md-9">
        <q-card-section v-if="!isCartEmpty">
          <div v-for="(items, id) in cart" :key="id">

            <q-card-actions v-for="item in items" :key="item" class="flex row justify-between content-between items-center  ">
              <div v-for="i in item" :key="i.id" class="flex tw-gap-2 items-center  ">
                <q-img :src="i.cover_image" class="tw-rounded-2xl tw-h-20 tw-w-20" v-if="!i.tags.includes('crust')" />
                <div class="">
                  <div class="tw-text-md">{{i.name}}</div>
                  <div class="tw-text-sm">${{i.price}}</div>
                </div>
              </div>

              <q-card-actions class="">
                  <q-btn icon="edit" color="primary"/>
                  <q-btn icon="delete" color="red" @click="removeFromCart(id)"/>
              </q-card-actions>
            </q-card-actions>

          </div>


        </q-card-section>


        <q-card-section v-else class="flex flex-center column tw-min-h-[300px] tw-p-10">
          <p class="tw-text-xl">Cart is empty, awaiting your delicious choices</p>
          <q-btn :to="{name:'Menu'}" dense color="primary">Go Shopping</q-btn>
        </q-card-section>
      </q-card>

      <q-card class="flex-container self-start tw-sticky  tw-top-20">
        <q-card-section>
          <q-toolbar-title>You Total ${{cartTotal}}</q-toolbar-title>
          <q-btn @click.prevent="handleCheckout" dense color="primary"  style="width: 150px">Checkout</q-btn>
        </q-card-section>
      </q-card>
    </div>
</template>


<script>
import {computed, defineComponent, onMounted, ref, watch} from 'vue'
import {useShopStore} from "stores/shop";
import {storeToRefs} from "pinia";
import {useRouter} from "vue-router";
const cart_url = "api/v1/shop/cart/add/";

export default defineComponent({
  name: "CartComponent",
  async setup(){
    let store = useShopStore();
    const router = useRouter()
    let cartTotal = ref(0);
    const { cart } = storeToRefs(store)
    const isCartEmpty = computed(()=>{
      return Object.keys(cart.value).length === 0
    })

    const removeFromCart=(prod_id)=>{
      delete cart.value[prod_id];
      if(!isCartEmpty.value)
      calculateCartDues()
    }
    const handleCheckout = async ()=>{
      window.cart = cart.value
      let data = Object.values(cart.value)?.flatMap(x=>x).flat().flatMap(x=>[{"id":x.id}])

      // await store.postToApiCart({"product_list":data}, cart_url)
      await store.postToApiCart({"product_list":data}, cart_url)
    }
    onMounted(()=>{if(!isCartEmpty.value)calculateCartDues();})
    const calculateCartDues = ()=>{
      cartTotal.value = Object.values(cart.value)?.flatMap(x=>x).flat().map(x=>x.price).reduce((a,b)=>Number(a)+Number(b)).toFixed(2)
    };


    return{
      cart,
      isCartEmpty,
      removeFromCart,
      cartTotal,
      handleCheckout
    }

  }
})
</script>



<style scoped>

</style>
