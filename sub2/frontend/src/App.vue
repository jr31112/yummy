<template>
  <v-app id="app">
    <header>
    <v-row class="toolbar">
      <v-col style="float:left">
        <p class="display-1 pa-2">🍜</p>
      </v-col>
      <v-col style="float:middle; text-align:center">
        <v-btn @click="home" text x-large color="primary"><h2>홈</h2></v-btn>
        <v-btn text x-large color="primary"><h2>플래너</h2></v-btn>
        <v-btn text x-large color="primary"><h2>탐색</h2></v-btn>
      </v-col>
      <v-col style="float:right; text-align:right">
        <v-btn @click="handleClickButton" text x-large="" color="error"><h2>로그인</h2></v-btn>
      </v-col>
    </v-row>
    </header>

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
    GoTop,
  },

  methods:{
    home(){
      var router = this.$router
      router.push({
        name:"home",
        params:{
        }
      })
    },
    login(){
      var router = this.$router
      router.push({
        name:"login",
        params:{
        }
      })
    },
    
  },
  data: () => ({
    dialog: false,
    email: '',
    password: '',
    birth_year:'',
    gender:'',
    nickname:'',
    access_token: '',
  }),
};
</script>

<style lang="scss" scoped>
.toolbar {
  height:70px; 
  position:fixed; 
  z-index:20;
  background-color:white;
  width:100%
}

</style>