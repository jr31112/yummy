import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import infiniteScroll from "vue-infinite-scroll";
import router from "./router";
import store from "./vuex/store";
import Vuex from 'vuex'
import axios from 'axios'

export const EventBus = new Vue()
Vue.use(Vuex)
Vue.prototype.$Axios = axios;

Vue.config.productionTip = false;
Vue.use(infiniteScroll);
new Vue({
  vuetify,
  router,
  store,
  beforeCreate() {
    this.$store.dispatch('getMemberInfo')
},
  render: h => h(App)
}).$mount("#app");
