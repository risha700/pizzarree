<template>
    <q-dialog :model-value="modelValue" @update:model-value="handleModelChanged" @beforeShow="handleBeforeShow" :persistent="editing"  >

      <q-card v-if="currentPassedProduct" class="tw-min-w-[70%] tw-min-h-full row tw-static">

        <q-card class="left col-md-8 col-xs-12">
          <q-toolbar>
            <q-avatar>
              <img :src="currentPassedProduct.cover_image">
            </q-avatar>
            <q-toolbar-title><span class="text-weight-bold">{{currentPassedProduct.name}}</span></q-toolbar-title>

          </q-toolbar>
          <div v-if="currentPassedProduct.tags?.includes('pizza')">
            <q-card-section class="flex items-stretch align-center column">
              <p class="tw-font-medium">Size:</p>
              <div class="q-gutter-sm">
                <q-radio  v-model="selectedSize" v-for="sz in shopStore.products.sizes"
                            :key="sz.name" :val="sz"  :label="sz.name">
                  <q-icon :name="'img:'+sz.cover_image" v-if="sz.cover_image" ></q-icon>
                  <span>${{sz.price}}</span>
                </q-radio>
              </div>
              </q-card-section>
              <q-card-section class="flex items-stretch align-center column">
                <p class="tw-font-medium">Crust:</p>

                <div class="q-gutter-sm"  >
                  <q-radio v-model="selectedCrust" :val="crust" :label="crust.name" :name="crust.name"
                           v-for="crust in shopStore.products.crusts" :key="crust.id">
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


        <q-card class="tw-bg-gray-500 col-md-4 col-xs-12 tw-sticky tw-top-0 self-start ">
            <q-card-actions align="between">
              <q-toolbar-title>My Pizza</q-toolbar-title>
              <q-btn flat round dense stack icon="close" v-close-popup >Discard</q-btn>

           </q-card-actions>
            <!-- selected pizza -->

            <q-card-section>
              <div v-for="item in myPizza" :key="item">
                <span v-if="item?.id">
                  <span v-text="item?.name"></span>
                  <q-btn flat dense stack icon="remove" @click.prevent="clearTopping(item?.name)" v-if="item?.tags?.includes('topping')"/>

                </span>
              </div>
            </q-card-section>

            <q-card-actions>
              <q-btn class="glossy" dense color="secondary" icon="add" :label="actionText" @click="addToOrder" ></q-btn>

            </q-card-actions>
          </q-card>
        </q-card>
    </q-dialog>
</template>
<script>
import {defineComponent, ref, toRaw, watch} from 'vue'
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
      default:false,
      required: false
    },
    modelValue:{
      type:Boolean,
      default:false,
    },
    editing:{
      type:Boolean,
      default:false
    },
    editingItems:{
      type:Object,
      default:()=>{},
      required:false
    },
    actionText:{
      type:String,
      default:'Add to cart'
    }
  },
  emits:['hideModal','update:model-value'],
  setup(props,{emit}){
    const shopStore = useShopStore();
    const $q = useQuasar();

    let selectedToppings = ref([]);
    let selectedSize = ref(null);
    let selectedCrust = ref(null);
    let myPizza = ref([]);
    let currentPassedProduct = ref({});
    let currentPassedId = ref(null);
    const handleModelChanged = (v)=>{
      emit('hideModal', v);
      //reset mypiuzza
    }
    function clearTopping(topping){
      let t_id = selectedToppings.value.findIndex((x)=>x.name===topping)
      selectedToppings.value.splice(t_id, 1);
      let p_id = myPizza.value.findIndex((x)=>x?.name===topping);
      myPizza.value.splice(p_id, 1);
    }

    async function addToOrder(){
      let pizza_needs_size_n_crust = (!selectedSize.value || !selectedCrust.value)&&currentPassedProduct.value?.tags?.includes('pizza');
      if(pizza_needs_size_n_crust){
          $q.notify({
            type: 'warning',
            message: 'You need to select size and crust.',
            progress: true,
          })
        return;
      }
      let rid = currentPassedId.value?currentPassedId.value: props.product.tags[0]+"_"+(Math.random() + 1).toString(36).substring(7);
      await shopStore.addToLocalCart(rid, myPizza.value)
      $q.notify({
          type: 'positive',
          message: props.actionText,
          progress: true,
          // position:'top',
        })
      emit('hideModal', false);
    }
    function handleBeforeShow  (){

      if(props.editing && Object.keys(props.editingItems).length===1){ // editing one at a time
        currentPassedId.value = Object.keys(props.editingItems)[0];
        currentPassedProduct.value = Object.values(props.editingItems)[0][0];
        let toppings_holder =[];
        Object.values(props.editingItems).flat().forEach((item)=>{
          if (item.tags.includes('topping')){
            toppings_holder.push(shopStore.products.toppings.filter(x=>x.id===item.id)[0]);
          }else if(item.tags.includes('crust')){
            selectedCrust.value = shopStore.products.crusts.filter(x=>x.id===item.id)[0];
          }else if(item.tags.includes('size')){
            selectedSize.value = shopStore.products.sizes.filter(x=>x.id===item.id)[0];
          }
      });
        selectedToppings.value = [...new Set(toppings_holder)];
      }
      else{
        currentPassedProduct.value = props.product
      }

      myPizza.value = [ currentPassedProduct.value ];

    }
    watch([selectedSize,selectedCrust,selectedToppings],(val)=>{
      myPizza.value = val.flat();
      myPizza.value.unshift(currentPassedProduct.value)
    });

    return{
      handleModelChanged,
      selectedToppings,selectedSize,selectedCrust,
      myPizza,clearTopping,
      shopStore,
      addToOrder,
      handleBeforeShow,
      currentPassedProduct,
      currentPassedId
    }

  },


})
</script>

<style scoped>

</style>
