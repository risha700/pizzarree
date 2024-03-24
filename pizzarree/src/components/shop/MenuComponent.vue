<template>
  <div  v-if="products && products.length" >
    <div class="col-md-1">
      <h6 class="text-capitalize">{{header_title}}</h6>
    </div>
    <div class="flex tw-gap-4 justify-md-start">
      <template v-for="product in products" :key="product.id"  >
        <ProductCard :product="product" @show-modal="showProductDetails" ></ProductCard>
      </template>
    </div>
    <ProductModal :model-value="showModal" :product="chosenProduct" @hide-modal="hideHandler"/>
  </div>
</template>

<script>
import {capitalize, defineComponent, reactive, ref} from 'vue'
import ProductCard from "components/shop/ProductCard.vue";
import ProductModal from "components/shop/ProductModal.vue";
export default defineComponent({
  name: "MenuComponent",
  methods: {capitalize},
  components: {ProductModal, ProductCard},
  props:['products','header_title'],
  async setup(){
    let showModal = ref(false);
    let chosenProduct = ref({});
    function showProductDetails(evt){
      showModal.value = true;
      chosenProduct.value = evt;
      // console.log(Object.assign({}, evt), "showProductDetails")
    }
    function hideHandler(evt){
      showModal.value = evt;
      chosenProduct.value = {};
    }

    return{
      showProductDetails,
      showModal,
      chosenProduct,hideHandler
    }


  }
})
</script>



<style scoped>

</style>
