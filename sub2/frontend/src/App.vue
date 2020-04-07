<template>
  <v-app id="app"> 
    <header style="height:400px">
      <v-btn
        color="pink"
        dark
        @click.stop="drawer = !drawer"
      >
      <i class="mdi mdi-menu"></i>
      </v-btn>
    </header>

  <v-navigation-drawer
    style="z-index:21"
    id="app-drawer"
    v-model="drawer"
    app
    white
    floating
    absolute
    temporary
    mobile-break-point="900"
    width="250" 
  >
  
    <v-layout column>
      <v-list rounded>
        <v-list-item
          v-for="(link, i) in links"
          :key="i"
          :to="link.to"
          active-class="blue lighten-1 white--text"
          class="v-list-item ma-3"
        >
          <v-list-item-action>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-title v-text="link.text" />
        </v-list-item>
        <v-list-item
          active-class="blue lighten-1 white--text"
          class="v-list-item ma-3"
        >
        <button 
          @click="$store.dispatch('logout')">
          <v-icon class="mdi mdi-logout"></v-icon>
          로그아웃
        </button>
        </v-list-item>
      </v-list>
    </v-layout>
  </v-navigation-drawer>
    <route-view />
    <go-top />
  </v-app>
</template>

<script>
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";
import '../src/css/app.css'
export default {
  components: {
    RouteView,
    GoTop
  },
  methods:{

  },
  data: () => ({
    drawer:false,
    links: [
      {
        to: "/",
        icon: "mdi-home",
        text: "Home"
      },
      {
        to: "/search",
        icon: "mdi-card-search",
        text: "맛집 검색"
      },
      {
        to: "/signup",
        icon: "mdi-account-multiple-plus",
        text: "회원가입"
      },
      {
        to: "/login",
        icon: "mdi-account-multiple-plus",
        text: "로그인"
      }
    ]
  }),
};
</script>
<style lang="scss" scoped>
header {
  height:400px; 
  position:fixed; 
  z-index:20;
  top:10px
}

</style>