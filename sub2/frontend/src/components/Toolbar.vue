<template>
  <v-app-bar id="app-toolbar" app flat color="white lighten-1">
    <button @click="clickNavi">
      asdasdadassddsadasdd
    </button>
    
    <v-spacer />
  </v-app-bar>
</template>

<script>
export default {

  data: () => ({
    responsive: false,
    isNavi: false,
  }),

  methods: {
    clickNavi() {
      this.isNavi = !this.isNavi
      this.$emit('child',this.isNavi)
    }
  }
}
</script>
