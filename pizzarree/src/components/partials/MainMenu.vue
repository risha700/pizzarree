<template>
  <q-list v-if="children && children.length">
    <q-expansion-item
      dense-toggle
      expand-separator
      :icon="icon"
      :label="capitalize($t(title))"
      :caption="capitalize($t(caption))"
      :to="link"
      default-opened
    >
      <q-item
        v-for="child in children"
        :key="child.link"
        clickable
        :to="{ name: child.link }"
        exact
        :inset-level="1"
      >
        <q-item-section v-if="child.icon" avatar>
          <q-icon :name="child.icon" />
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ capitalize($t(child.title)) }}</q-item-label>
          <q-item-label caption>{{
            capitalize($t(child.caption))
          }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-expansion-item>
  </q-list>

  <q-item clickable :to="{ name: link }" exact v-else>
    <q-item-section v-if="icon" avatar>
      <q-icon :name="icon" />
    </q-item-section>
    <q-item-section>
      <q-item-label>{{ capitalize($t(title)) }}</q-item-label>
      <q-item-label caption>{{ capitalize($t(caption)) }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";
import { format } from "quasar";

export default defineComponent({
  name: "MainMenu",
  props: {
    title: {
      type: String,
      required: true,
    },

    caption: {
      type: String,
      default: "",
    },

    link: {
      type: String,
      default: "#",
    },

    icon: {
      type: String,
      default: "",
    },
    children: {
      type: Array,
      default: () => [],
    },
  },

  setup() {
    const { capitalize } = format;
    return { capitalize };
  },
});
</script>
