<template>

    <div class="flex justify-between self-start items-start row tw-static q-layout-padding col ">

          <q-card class="col-xs-12" :class="isCartEmpty?'col-md-8':'col-md-8'">
        <q-card-section v-if="!isCartEmpty">
          <div v-for="(product, id) in cart" :key="id">
            <q-card-section v-for="item in product.items" :key="item" class="column items-start justify-between ">

              <div v-for="i in item" :key="i.id" class="flex  tw-gap-2 items-center">
                <q-img v-if="!isTopping(product.items,item,i)" :src="i.cover_image" class="tw-rounded-2xl tw-h-20 tw-w-20" />

                <div :class="isTopping(product.items,item,i)?'flex tw-justify-between tw-min-w-[300px] ':''">
                  <div class="tw-text-md">{{i.name}}</div>
                  <div class="tw-text-sm">${{i.price}}</div>
                </div>
              </div>


              <q-card-actions class="self-end ">

                <div class="flex items-center q-ma-sm   rounded-borders container ">
                      <div class="text-h6 q-pa-lg">Quantity {{product.quantity}}</div>
                      <q-btn-group class="column" >
                        <q-btn size="sm" icon="add" dense flat @click.prevent="product.quantity++" />
                        <q-btn size="sm" icon="remove" dense flat @click.prevent="product.quantity > 1? product.quantity--:null"/>
                      </q-btn-group>
                </div>
                <q-btn icon="edit" @click="handleEdit(item, id)" color="primary" v-if="item[0].tags.includes('pizza')"/>
                <q-btn icon="delete" color="red" @click="removeFromCart(id)"/>
              </q-card-actions>


            </q-card-section>
          </div>

        <ProductModal :model-value="showEditModal" :editing="true"  action-text="Update"
                      :editing-items="itemToEdit" @hide-modal="showEditModal=false"/>
        </q-card-section>


        <q-card-section v-else class="text-center">
          <p class="tw-text-xl">Cart is empty, awaiting your delicious choices</p>
          <q-btn unelevated  color="primary" :to="{name:'Menu'}" label="Go Shopping" />
        </q-card-section>
      </q-card>

      <q-card class="flex-container  self-start tw-sticky tw-top-20 col-xs-12 col-md-3 q-mt-xs " v-if="!isCartEmpty">
        <q-card-section class="column justify-around   tw-min-h-[300px]">
          <q-toolbar-title>Subtotal ${{cartTotal}}</q-toolbar-title>
          <CouponComponent/>
          <q-btn @click.prevent="handleCheckout" dense color="primary" :disable="cartTotal<=0">Checkout</q-btn>
        </q-card-section>
      </q-card>
    </div>
</template>


<script>
import {computed, defineComponent, onMounted, ref, watch} from 'vue'
import {useShopStore} from "stores/shop";
import {storeToRefs} from "pinia";
import {useRouter} from "vue-router";
import CouponComponent from "components/shop/CouponComponent.vue";
import ProductModal from "components/shop/ProductModal.vue";


export default defineComponent({
  name: "CartComponent",
  components: {ProductModal, CouponComponent},
  emits:['showModal'],
  async setup(){
    let store = useShopStore();
    const router = useRouter()
    let cartTotal = ref(0);
    const { cart } = storeToRefs(store)
    const { order } = storeToRefs(store)
    const qtyRules =[ val => (val && val >= 1)];
    const isCartEmpty = computed(()=>{
      return Object.keys(cart.value).length === 0
    })

    let itemToEdit = ref({});

    const handleEdit = (productItems, id)=>{
      showEditModal.value = true;
      let temp = {};
      temp[id]= productItems;
      itemToEdit.value = temp;
      // console.log('prod', productItems)
    }
    let isTopping = (items, item, i)=>{
      return items[0].length > 1 && i.name!=item[0]?.name;
    };

    let showEditModal = ref(false);
    const removeFromCart=(prod_id)=>{
      delete cart.value[prod_id];
      if(isCartEmpty.value) {
        cartTotal.value = 0;
        if(order.value)
          order.value = {};
      }
    }
    const handleCheckout = async ()=>{
      // adds it to server session cart
      // and creates an order
      // and creates a stripe payment obj
      // await store.postToApiCart({"product_list": transformObjectToCartApiStructure(cart.value)})
      await store.postToApiCart({"product_list": store.flatCartProducts})
    }

    onMounted(()=>{
      // window.cart = cart.value
      if(!isCartEmpty.value){
        calculateCartDues()
      }
    })
    const calculateCartDues = ()=>{
      let total = Number(Object.values(cart.value).flatMap(({items, quantity})=> ({items, quantity}))
        .map(({items, quantity})=>Object.values(items).flat().map(x=>x.price).reduce((a,b)=>Number(a)+Number(b))*quantity)
        .reduce((acc,v)=>acc+v))?.toFixed(2)
      cartTotal.value = total || 0;
    };

    watch(cart.value,(value)=>{
      if(Object.keys(value).length)
      calculateCartDues();
    },{deep:true});

    return{
      cart,
      isCartEmpty,
      removeFromCart,
      cartTotal,
      handleCheckout,qtyRules,
      isTopping,showEditModal, handleEdit, itemToEdit
    }

  }
})
</script>



<style scoped>

</style>
