<template>
  <SuspenseWithErrors>
    <div class="q-gutter-y-md ">
      <q-tabs
            v-model="tab"
            class="tw-sticky tw-top-10"
            active-color="primary"
            indicator-color="primary"
            align="justify"
            narrow-indicator
          >
            <q-tab name="all" label="All Products" />
            <q-tab v-for="t in tab_panels" :key="t.name" :name="t.name" :label="t.label"  />
          </q-tabs>
          <q-tab-panels v-model="tab" animated>
            <q-tab-panel name="all">
                <MenuComponent v-for="t in tab_panels" :key="t.name" :products="shopStore.products[t.name]" :header_title="t.name" />
            </q-tab-panel>
            <q-tab-panel v-for="t in tab_panels" :key="t.name" :name="t.name">
              <MenuComponent :products="shopStore.products[t.name]"/>
            </q-tab-panel>
          </q-tab-panels>


    </div>
  </SuspenseWithErrors>
</template>

<script>
import {defineComponent, onMounted, ref} from 'vue'
import MenuComponent from "components/shop/MenuComponent.vue";
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";
import {api} from "boot/axios";
import {useShopStore} from "stores/shop";
import {useRoute, useRouter} from "vue-router";
const products_url = "api/v1/shop/products";
const tab_panels = [
  {name:"pizzas",label:"Pizzas"},
  {name:"drinks",label:"Drinks"},
  {name:"deserts",label:"Deserts"},
  {name:"sides",label:"Sides"},
]
export default defineComponent({
  name: "MenuPage",
  components:{SuspenseWithErrors, MenuComponent},
  async setup(){
    const shopStore = useShopStore()
    const router = useRouter();
    const route = useRoute();
    const tab = ref("all")
    onMounted(async()=>{
      await shopStore.retrieveProducts(products_url);
      await shopStore.setupCustomerOrderEmail();
    })
    return{
      shopStore,tab,tab_panels
    }

  }
})
</script>



<style scoped>

</style>
