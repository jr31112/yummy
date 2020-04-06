<template>
  <v-app-bar id="app-toolbar" app flat color="white lighten-1">
    <v-container class="fill-height">
      <v-row
        align="center"
        justify="center"
      >
      <v-btn
        color="pink"
        dark
        @click="clickNavi"
      >
        Toggle
        </v-btn>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
import { EventBus } from '../main.js'
export default {

  data: () => ({
    drawer: false,
    responsive: false,
    isNavi: false,
  }),

  methods: {
    clickNavi: function() {
      EventBus.$emit('toggle', this.drawer)
    }
      
    }
}

</script>
