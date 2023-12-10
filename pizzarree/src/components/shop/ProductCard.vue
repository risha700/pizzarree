<template>
    <q-card class="my-card" v-if="product" >
       <q-img :src="product.cover_image" height="100px" @click="handleCustomize(product)"/>

      <q-card-section class="">
        <div class="text-h6">{{product.name}}</div>
        <div class="text-subtitle2">${{product.price}}</div>
      </q-card-section>
      <q-card-actions align="around">
        <q-btn flat @click="straightToCart(product)" >Add To Cart</q-btn>
        <q-btn @click="handleCustomize(product)" flat>Customize</q-btn>
      </q-card-actions>
    </q-card>
</template>


<script>
import {defineComponent} from 'vue'
import {useShopStore} from "stores/shop";

export default defineComponent({
  name: "ProductCard",
  props:['product'],
  emits:['showModal'],
  setup(props, {emit}){

    const store = useShopStore();
    const handleCustomize = (evt)=>{
      emit('showModal',evt);
      // console.log(evt)
    };

    async function straightToCart(product){
      if(product.tags.includes('pizza')){
          emit('showModal',product);
          return;
      }
        let rid = props.product.tags[0]+"_"+(Math.random() + 1).toString(36).substring(7);
        await store.addToLocalCart(rid, [product])
    }

    return{
      handleCustomize,
      straightToCart
    }

  }
})
</script>



<style scoped>

</style>
