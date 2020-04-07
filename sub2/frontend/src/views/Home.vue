<template>
  <v-container style="padding:0;">
    <header >
      <video autoplay muted loop id="myVideo">
      <source src="https://storage.coverr.co/videos/coverr-grilled-hen-1568039522040?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IjExNDMyN0NEOTRCMUFCMTFERTE3IiwiaWF0IjoxNTg2MjI0MDE4fQ.TSQ-jh-G1HzQcCSoL2t1ong3o0TTSfauWs7w-snLidc" type="video/mp4">
    </video>
    </header>
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
<style scoped>
#myVideo {
  top:0;
  right: 0;
  bottom: 0;
  width: 100%; 
  max-height: 500px;
  object-fit: cover;
}
</style>