<template>
  <v-app-bar app>
    <v-btn
    class="navbutton"
    style="float:left"
    color="pink"
    dark
    @click.stop="drawer = !drawer"
    >
    <i class="mdi mdi-menu"></i>
    </v-btn>
    <v-row class="nav">
      <v-col style="float:left">

        <p class="display-1 pa-2">🍜</p>
      </v-col>
      <v-col style="float:middle; text-align:center">
        <v-btn @click="goHome" text x-large color="primary"><h2>홈</h2></v-btn>
        <v-btn @click="goplanner" text x-large color="primary"><h2>플래너</h2></v-btn>
        <v-btn text x-large color="primary"><h2>탐색</h2></v-btn>
      </v-col>
      <v-col style="float:right; text-align:right">
        <div v-if="$store.state.isLogin==false">
          <v-btn @click.stop="$store.state.dialog = true" text x-large="" color="error"><h2>로그인</h2></v-btn>
        </div>
        <div v-else>
          <v-btn @click="$store.dispatch('logout')" text x-large="" color="error"><h2>로그아웃</h2></v-btn>
        </div>
        <v-dialog
          background-color='black'
          v-model="$store.state.dialog"
          z-index="3"
          overlay-opacity="1"
          max-width="700px"
          min-heigth="700px"><LoginModal />
        </v-dialog>
      </v-col>
    </v-row>
    <v-navigation-drawer
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

  </v-app-bar>
  
</template>

<script>
import {mapState, mapActions} from "vuex"
import LoginModal from "./appbar/LoginModal"
import router from "../../router"
export default {
  name: "AppBar",
  components: {
    LoginModal,
  },
  data(){
    return{
      drawer:false,
      dialog : false,
      links: [
      {
        to: "/",
        icon: "mdi-home",
        text: "Home"
      },
      {
        to: "/search",
        icon: "mdi-card-search",
        text: "플래너"
      },
      {
        to: "/signup",
        icon: "mdi-account-multiple-plus",
        text: "탐색"
      },
      {
        to: "/login",
        icon: "mdi-account-multiple-plus",
        text: "로그인"
      }
    ]

    }
  },
  methods: {
    goHome(){
      router.push({name:"home"})
    },
    goplanner() {
      router.push({name:"planner"})
    },
    Modaloff(val){
      console.log(val)
      this.dialog = val
    }
  },

}
</script>

<style lang="scss" scoped>
.navbutton {
  @media screen and (min-width: 1000px) {
  display:none;
  }
}
.nav {
  @media screen and (max-width: 1000px) {
  display:none;
  }
}
</style>