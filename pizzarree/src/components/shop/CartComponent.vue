<template>

    <div class="flex  justify-between self-start items-start row tw-static q-layout-padding col">

      <q-card class=" col-xs-12 col-md-8">
        <q-card-section v-if="!isCartEmpty">
          <div v-for="(items, id) in cart" :key="id">

            <q-card-actions v-for="item in items" :key="item" class="column items-start justify-between ">
              <div v-for="i in item" :key="id+i.id" class="flex  tw-gap-2 items-center   ">
                <q-img v-if="!isTopping(items,item,i)" :src="i.cover_image" class="tw-rounded-2xl tw-h-20 tw-w-20" />

                <div :class="isTopping(items,item,i)?'flex tw-justify-between tw-min-w-[300px] ':''">
                  <div class="tw-text-md">{{i.name}}</div>
                  <div class="tw-text-sm">${{i.price}}</div>
                </div>
              </div>

              <q-card-actions class="self-end">
                  <q-btn icon="edit" @click="handleEdit(item, id)" color="primary"/>
                  <q-btn icon="delete" color="red" @click="removeFromCart(id)"/>
              </q-card-actions>


            </q-card-actions>
          </div>

        <ProductModal :model-value="showEditModal" :editing="true"  action-text="Update"
                      :editing-items="itemToEdit" @hide-modal="showEditModal=false"/>
        </q-card-section>


        <q-card-section v-else class="flex flex-center column tw-min-h-[300px] tw-p-10">
          <p class="tw-text-xl">Cart is empty, awaiting your delicious choices</p>
          <q-btn :to="{name:'Menu'}" dense color="primary">Go Shopping</q-btn>
        </q-card-section>
      </q-card>

      <q-card class="flex-container  self-start tw-sticky tw-top-20 col-xs-12 col-md-3 q-mt-xs">
        <q-card-section class="column justify-around   tw-min-h-[300px]">
          <q-toolbar-title>Sub Total ${{cartTotal}}</q-toolbar-title>
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
      if(isCartEmpty.value) cartTotal.value = 0;
    }

    const transformObjectToCartApiStructure = (obj) => Object.values(obj)?.flatMap(x=>x).flat().flatMap(x=>[{"id":x.id}])

    const handleCheckout = async ()=>{
      // adds it to server session cart
      // and creates an order
      // and creates a stripe payment obj
      await store.postToApiCart({"product_list": transformObjectToCartApiStructure(cart.value)})
    }

    onMounted(()=>{
      // window.cart = cart.value
      if(!isCartEmpty.value){
        calculateCartDues()
      }
    })
    const calculateCartDues = ()=>{
      let total = Number(Object.values(cart.value)?.flatMap(x=>x).flat().map(x=>x.price)?.reduce((a,b)=>Number(a)+Number(b)))?.toFixed(2)
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
      handleCheckout,
      isTopping,showEditModal, handleEdit, itemToEdit
    }

  }
})
</script>



<style scoped>

</style>
