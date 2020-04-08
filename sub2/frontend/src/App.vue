<template>
  <v-app id="app">
    <app-bar/>
    <route-view />
    <go-top />
      <v-row justify="center">

    <v-dialog
      v-model="dialog"
      max-width="500"
    >
      <v-card>
        <v-card-title class="headline">Use Google's location service?</v-card-title>

        <v-card-text>
          Let Google help apps determine location. This means sending anonymous location data to Google, even when no apps are running.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Disagree
          </v-btn>

          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Agree
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
  </v-app>
</template>

<script>
import AppBar from "@/components/header/AppBar"
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";
import '../src/css/app.css'
export default {
  components: {
    AppBar,
    RouteView,
    GoTop
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