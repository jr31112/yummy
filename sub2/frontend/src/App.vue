<template>
  <v-app id="app">
    <toolbar />
    <Drawer></Drawer>
    <route-view />
    <go-top />
  </v-app>
</template>

<script>
import Drawer from "@/components/Drawer";
import Toolbar from "@/components/Toolbar";
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";

export default {
  components: {
    Drawer,
    Toolbar,
    RouteView,
    GoTop
  },
  data:() => {
    return {
      isNavi: false
    }
  },
  methods: {
    updateNavi(drawer) {
      this.isNavi = drawer;
    },
  }
};
</script>
