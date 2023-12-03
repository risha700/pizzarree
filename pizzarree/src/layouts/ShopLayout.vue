<template>
  <q-layout view="lHh Lpr lFf">
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
    >
      <q-list>
        <q-item-label
          header
        >
          Menu
        </q-item-label>

        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <SuspenseWithErrors>
        <router-view />
      </SuspenseWithErrors>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/partials/EssentialLink.vue'
import SuspenseWithErrors from "components/partials/SuspenseWithErrors.vue";

const linksList = [
  {
    title: 'Home',
    caption: '',
    icon: 'Home',
    link: 'Home'
  },
    {
    title: 'Shop',
    caption: 'shop',
    icon: 'store',
    link: 'Menu'
  },
  {
    title: 'Checkout',
    caption: 'pay your order',
    icon: 'shopping_cart',
    link: 'Checkout'
  },

]

export default defineComponent({
  name: 'ShopLayout',
  components:{SuspenseWithErrors, EssentialLink},
  setup () {
    const leftDrawerOpen = ref(false)

    return {
      linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
