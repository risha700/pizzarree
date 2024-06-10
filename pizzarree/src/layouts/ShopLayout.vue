<template>
  <q-layout view="hHh Lpr fFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Pizzarree Shop
        </q-toolbar-title>
<!--Cart-->
<!--        <div>Quasar v{{ $q.version }}</div>-->
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :mini="true"
      :breakpoint="10"
    >

      <q-list padding >
          <q-item clickable v-for="link in linksList" :key="link.title" :to="{ name: link.link }"
                  active-class="text-secondary"
                  exact  v-ripple>


              <q-badge color="secondary" floating transparent multi-line rounded align="middle"
                       v-if=" link.title.toLowerCase()==='cart' && cartCount > 0">
                {{cartCount}}
              </q-badge>

            <q-item-section v-if="link.icon" avatar >
              <div class="tw-flex tw-flex-col tw-items-center">
                  <q-icon :name="link.icon" size="2rem" />
                  <span class="tw-text-xs">{{link.title}}</span>
              </div>
            </q-item-section>
          </q-item>
      </q-list>
    </q-drawer>
     <q-footer elevated>
        <q-toolbar>
          <q-toolbar-title class="text-center">All rights reserved</q-toolbar-title>
        </q-toolbar>
      </q-footer>

    <q-page-container>
      <SuspenseWithErrors>
        <router-view />
      </SuspenseWithErrors>
    </q-page-container>
  </q-layout>
</template>

<script>
import {defineComponent, onMounted, ref, watch} from 'vue'
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";
import {useShopStore} from "stores/shop";

const linksList = [
  {
    title: 'Home',
    caption: '',
    icon: 'home',
    link: 'Home'
  },
    {
    title: 'Shop',
    caption: 'shop',
    icon: 'store',
    link: 'Menu'
  },
  {
    title: 'Cart',
    caption: 'cart',
    icon: 'shopping_cart',
    link: 'Cart'
  },

]

export default defineComponent({
  name: 'ShopLayout',
  components: {SuspenseWithErrors},
  setup () {
    const leftDrawerOpen = ref(false)
    const shopStore = useShopStore()
    let currentCart = shopStore.getCart;
    let cartCount = ref(shopStore.getCartItemsCount);
    watch([currentCart],(_)=>{
      cartCount.value = shopStore.getCartItemsCount;
    } )

    return {
      linksList,
      cartCount,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
