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
          Pizzarree Shop - User Area
        </q-toolbar-title>

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
          v-for="link in essentialLinks"
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
    icon: 'home',
    link: 'Home'
  },
  {
    title: 'Shop',
    caption: 'Start Ordering',
    icon: 'store',
    link: 'Menu'
  },


]

export default defineComponent({
  name: 'UserLayout',
  components: {SuspenseWithErrors, EssentialLink},
  setup () {
    const leftDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
