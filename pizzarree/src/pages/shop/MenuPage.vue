<template>
  <SuspenseWithErrors>
      <q-tabs
            v-model="tab"
            class="tw-sticky tw-top-12 tw-z-10"
            :class="$q.dark.isActive?'tw-bg-gray-800':'tw-bg-white'"
            active-color="secondary"
            indicator-color="secondary"
            align="justify"
            narrow-indicator
            shrink>

            <q-tab name="all" label="All Products" />
            <q-tab v-for="t in tab_panels" :key="t.name" :name="t.name" :label="t.label"  />
      </q-tabs>

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="all">
            <MenuComponent v-for="t in tab_panels" :key="t.name" :products="shopStore.products[t.name]" :header_title="t.name" />
        </q-tab-panel>
        <q-tab-panel v-for="t in tab_panels" :key="t.name" :name="t.name">
            <MenuComponent :products="shopStore.products[t.name]" :header_title="t.name"/>
        </q-tab-panel>
      </q-tab-panels>
    </SuspenseWithErrors>


</template>

<script>
import {defineAsyncComponent, defineComponent, onMounted, ref} from 'vue'
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";
import {useShopStore} from "stores/shop";


const tab_panels = [
  {name:"pizzas",label:"Pizzas"},
  {name:"drinks",label:"Drinks"},
  {name:"deserts",label:"Deserts"},
  {name:"sides",label:"Sides"},
]
export default defineComponent({
  name: "MenuPage",
  components:{SuspenseWithErrors,
    MenuComponent: defineAsyncComponent(()=> import("components/shop/MenuComponent.vue")),
  },
    async setup(){
    const shopStore = useShopStore()
    const tab = ref("all")
    onMounted(async()=>{
      await shopStore.retrieveProducts();
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
