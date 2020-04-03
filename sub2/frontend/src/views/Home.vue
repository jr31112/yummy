<template>
  <v-container class="mt-5" fill-height>
    <v-card-text class="text-center">
      <button @click="goStore(a)">
      <h1>짜장면</h1>  
      </button>
      <br>
      <button @click="goStore(b)">
      <h1>국밥</h1>
      </button>
      <br>
      <p class="display-3 pa-2">🍜</p>
      <p class="display-2 pa-5">코딩도 식후경</p>
      <v-btn large color="blue lighten-1 white--text ma-5" rounded to="/search">검색하기</v-btn>
    </v-card-text>
  </v-container>
</template>

<script>
export default {
  methods:{
    goStore(StoreName){
      var router = this.$router
      router.push({
        name:"detail",
        params:{
          "StoreName": StoreName
        }
      })
    }
  },
  data: () => {
    return {
      a:"짜장면",
      b:"국밥",
    }
  }

};
</script>