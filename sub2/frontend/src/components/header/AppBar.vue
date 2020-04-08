<template>
  <v-app-bar app>
    <v-row class="toolbar">
      <v-col style="float:left">
        <p class="display-1 pa-2">🍜</p>
      </v-col>
      <v-col style="float:middle; text-align:center">
        <v-btn @click="goHome" text x-large color="primary"><h2>홈</h2></v-btn>
        <v-btn text x-large color="primary"><h2>플래너</h2></v-btn>
        <v-btn text x-large color="primary"><h2>탐색</h2></v-btn>
      </v-col>
      <v-col style="float:right; text-align:right">
        <v-btn @click.stop="dialog = true" text x-large="" color="error"><h2>로그인</h2></v-btn>
        <v-dialog
          v-model="dialog"
          z-index="3"
          overlay-opacity="1"
          max-width="545px"><LoginModal />
        </v-dialog>
      </v-col>
    </v-row>
  </v-app-bar>
</template>

<script>
import LoginModal from "./appbar/LoginModal"
import router from "../../router"
export default {
  name: "AppBar",
  components: {
    LoginModal,
  },
  data(){
    return{
      dialog : false,
    }
  },
  methods: {
    goHome(){
      router.push({name:"home"})
    }
  },

}
</script>

<style>

</style>