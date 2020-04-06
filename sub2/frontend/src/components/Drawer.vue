<template>
  <!-- <v-navigation-drawer
    id="app-drawer"
    v-model="inputValue"
    app
    dark
    floating
    persistent
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
        <button @click="$store.dispatch('logout')">
          로그아웃
        </button>
      </v-list>
    </v-layout>
  </v-navigation-drawer> -->
   <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary
    >
      <v-list-item>
        <v-list-item-avatar>
          <v-img src="https://randomuser.me/api/portraits/men/78.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>John Leider</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense>

        <v-list-item
          v-for="item in links"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import { EventBus } from '../main';

export default {
  created: function() {
    console.log('asd')
    EventBus.$on('toggle', function(value){
    this.drawer = value;
    });
  },
  data: () => ({
    drawer:true,
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


  methods: {
  }
};
</script>
