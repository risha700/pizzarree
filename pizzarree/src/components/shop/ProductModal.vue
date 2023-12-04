<template>
    <q-dialog :model-value="modelValue" @update:model-value="handleModelChanged" persistent @show="handleBeforeShow" >

      <q-card v-if="product" class="tw-min-w-[70%] tw-min-h-full row tw-static">

        <q-card class="left col-md-8 ">
          <q-toolbar>
            <q-avatar>
              <img :src="product.cover_image">
            </q-avatar>
            <q-toolbar-title><span class="text-weight-bold">{{product.name}}</span></q-toolbar-title>

          </q-toolbar>
          <div v-if="product.tags.includes('pizza')">
            <q-card-section class="flex items-stretch align-center column">
              <p class="tw-font-medium">Size:</p>
              <div class="q-gutter-sm">
                <q-radio v-model="selectedSize" v-for="sz in shopStore.products.sizes"
                            :key="sz.name" :val="sz"  :label="sz.name">
                  <q-icon :name="'img:'+sz.cover_image" v-if="sz.cover_image" ></q-icon>
                  <span>${{sz.price}}</span>
                </q-radio>
              </div>

              </q-card-section>
              <q-card-section class="flex items-stretch align-center column">
                <p class="tw-font-medium">Crust:</p>
                <div class="q-gutter-sm">
                  <q-radio v-model="selectedCrust" v-for="crust in shopStore.products.crusts"
                              :key="crust.name" :val="crust"  :label="crust.name">
                    <q-icon :name="'img:'+crust.cover_image" ></q-icon>
                    <span>${{crust.price}}</span>
                  </q-radio>
                </div>

              </q-card-section>
              <q-card-section class="flex items-stretch align-center column">
                <p class="tw-font-medium">Toppings:</p>
                <div class="q-gutter-sm flex column">
                  <q-checkbox v-model="selectedToppings" v-for="topping in shopStore.products.toppings"
                              :key="topping.name" :val="topping"  :label="topping.name" >
                    <q-icon :name="'img:'+topping.cover_image" class="tw-h-20 tw-w-20"></q-icon>
                    <span>${{topping.price}}</span>
                  </q-checkbox>
                </div>

              </q-card-section>
            </div>
          </q-card>


        <q-card class="tw-bg-gray-500 col-md-4 col-sm-12 tw-sticky tw-top-0 self-start ">
            <q-card-actions align="between">
              <q-toolbar-title>My Pizza</q-toolbar-title>
              <q-btn flat round dense stack icon="close" v-close-popup >Discard</q-btn>

           </q-card-actions>
            <!-- selected pizza -->

            <q-card-section>
              <div v-for="item in myPizza" :key="item">
                <span v-if="item?.id">
                  <span v-text="item.name"></span>
                  <q-btn flat dense stack icon="remove" @click="clearTopping(item.name)" v-if="item.tags.includes('topping')"/>
                </span>
              </div>
            </q-card-section>

            <q-card-actions>
              <q-btn class="glossy" dense color="secondary" icon="add" label="Add To Order" @click="addToOrder" ></q-btn>

            </q-card-actions>
          </q-card>
        </q-card>
    </q-dialog>
</template>
<script>
import {defineComponent, onMounted, ref, watch} from 'vue'
import {useShopStore} from "stores/shop";
import {useQuasar} from "quasar";

export default defineComponent({
  name: "ProductModal",
  props:{
    product:{
      type:Object,
      default:()=>{}
    },
    showModal:{
      type:Boolean,
      default:false
    },
    modelValue:{
      type:Boolean,
      default:false,
    }
  },
  emits:['hideModal','update:model-value'],

  setup(props,{emit}){
    const shopStore = useShopStore();
    const $q = useQuasar()
    let isOpen = ref(true);
    let selectedToppings = ref([]);
    let selectedSize = ref(null)
    let selectedCrust = ref(null)
    let myPizza = ref([])

    const handleModelChanged = (v)=>{
      emit('hideModal', v);
    }
    function clearTopping(topping){
      let t_id = selectedToppings.value.findIndex((x)=>x.name==topping)
      selectedToppings.value.splice(t_id, 1)
      t_id = myPizza.value.findIndex((x)=>x.name==topping)
      myPizza.value.splice(t_id, 1)
    }
    async function addToOrder(){
      if((!selectedSize.value || !selectedCrust.value) && props.product.tags.includes('pizza')){
          $q.notify({
            type: 'warning',
            message: 'You need to select size and crust.',
            progress: true,
          })
        return;
      }
      let rid = props.product.tags[0]+"_"+(Math.random() + 1).toString(36).substring(7);

      await shopStore.addToLocalCart(rid, myPizza.value)
      emit('hideModal', false);
    }
    const handleBeforeShow = (e)=>{

      myPizza.value = [props.product]
    }
    watch([selectedSize,selectedCrust,selectedToppings],(val)=>{
      myPizza.value = val.flat();
      myPizza.value.unshift(props.product)

    });
    return{
      isOpen,
      handleModelChanged,
      selectedToppings,selectedSize,selectedCrust,
      myPizza,clearTopping,
      shopStore,addToOrder,handleBeforeShow
    }

  }
})
</script>

<style scoped>

</style>
