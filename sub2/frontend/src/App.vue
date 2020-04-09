<template>
  <v-app id="app">
    <app-bar/>
    <route-view />
    <go-top />

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
    GoTop,
  },

  methods:{
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
