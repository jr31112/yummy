<template>
<div>
<div style="margin:100px"></div>
<v-container style="background-image: url('https://pixabay.com/get/54e1d4444953ac14f6da8c7dda293277113cd6e2524c704c7d2978d69f4cc75f_1280.jpg'); background-size:cover">
  <v-row>
    <v-col>
      <v-hover v-slot:default="{ hover }">
        <v-card
          class="mx-auto"
          color="grey lighten-4"
          max-width="500"
        >
          <v-img
            :aspect-ratio="16/9"
            src="https://cdn.pixabay.com/photo/2017/01/26/02/06/platter-2009590_960_720.jpg"
          >
            <v-expand-transition>
              <button>

              <div
                v-if="hover"
                class="d-flex transition-fast-in-fast-out orange darken-2 v-card--reveal display-3 white--text"
                style="height: 100%;"
              >
                샤샤샥
              </div>
              </button>
            </v-expand-transition>
          </v-img>
          <v-card-text
            class="pt-6"
            style="position: relative;"
          >
            <h5 class="display-1 font-weight-light orange--text mb-2">맛있겠다 ㅎㅎ</h5 >

          </v-card-text>
        </v-card>
      </v-hover>
    </v-col>
    <v-col>
      <v-hover v-slot:default="{ hover }">
        <v-card
          class="mx-auto"
          color="grey lighten-4"
          max-width="500"
        >
          <v-img
            :aspect-ratio="16/9"
            src="https://cdn.pixabay.com/photo/2015/07/11/23/02/plane-841441_960_720.jpg"
          >
            <v-expand-transition>
              <button>

              <div
                v-if="hover"
                class="d-flex transition-fast-in-fast-out orange darken-2 v-card--reveal display-3 white--text"
                style="height: 100%;"
              >
                계획 짜기
              </div>
              </button>
            </v-expand-transition>
          </v-img>
          <v-card-text
            class="pt-6"
            style="position: relative;"
          >
            <h5 class="display-1 font-weight-light orange--text mb-2">새 플래너 시작</h5 >

          </v-card-text>
        </v-card>
      </v-hover>
    </v-col>
  </v-row>
</v-container>

<!-- 유저 경로 -->
<h2 style="margin:3%">유저 추천 경로</h2>
<carousel :perPage=4 :autoplay='true' :loop='true' :autoplayHoverPause='true'>
  <slide v-for="item in list" v-bind:key="item.id">
     <v-card
    max-width="344"
    class="mx-auto"
    >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="headline">지역설명</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-img
      src='https://cdn.pixabay.com/photo/2014/04/02/14/09/world-map-306338_960_720.png'
      height="194"
    ></v-img>

    <v-card-text>
      경로설명
    </v-card-text>

    <v-card-actions>
      <v-btn
        text
        color="deep-purple accent-4"
      >
        스크랩
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-share-variant</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
  </slide>
</carousel>

<!-- 내경로  -->
<h2 style="margin:3%">내 경로</h2>
<v-spacer></v-spacer>
<div v-if="this.$store.state.isLogin">

<carousel :perPage=4 :autoplay='true' :loop='true' :autoplayHoverPause='true'>
  <slide v-for="item in list" v-bind:key="item.id">
     <v-card
    max-width="344"
    class="mx-auto"
    >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="headline">지역설명</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-img
      src='https://cdn.pixabay.com/photo/2014/04/02/14/09/world-map-306338_960_720.png'
      height="194"
    ></v-img>

    <v-card-text>
      경로설명
    </v-card-text>

    <v-card-actions>
      <v-btn
        text
        color="deep-purple accent-4"
      >
        스크랩
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-share-variant</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
  </slide>
</carousel>
</div>
<div v-else>
    <v-card
      class="mx-auto"
      color="grey lighten-4"
      max-width="500"
    >
      <v-img
        :aspect-ratio="16/9"
        src="https://cdn.pixabay.com/photo/2017/01/20/00/30/maldives-1993704_960_720.jpg"
      >
        <v-expand-transition>
          <button>

          <div
            class="d-flex transition-fast-in-fast-out blue darken-2 v-card--reveal display-3 white--text"
            style="height: 100%;"
          >
            로그인
          </div>
          </button>
        </v-expand-transition>
      </v-img>
      <v-card-text
        class="pt-6"
        style="position: relative;"
      >
        <h5 class="display-1 font-weight-light orange--text mb-2" style="text-align:center">로그인이 필요합니다</h5 >

      </v-card-text>
    </v-card>
</div>
</div>
</template>

<script>
import { Carousel, Slide } from 'vue-carousel';
export default {
  components: {
    Carousel,
    Slide
  },
  created() {
    console.log(this.$store.state.isLogin)
  },
  methods:{
    
    },
  data: () => {
    return {
        list:[
          {map: 'https://cdn.pixabay.com/photo/2014/04/02/14/09/world-map-306338_960_720.png'},
          {map: 'https://cdn.pixabay.com/photo/2014/04/02/14/09/world-map-306338_960_720.png'},
          {map: 'https://cdn.pixabay.com/photo/2014/04/02/14/09/world-map-306338_960_720.png'},
          {map: 'https://cdn.pixabay.com/photo/2014/04/02/14/09/world-map-306338_960_720.png'},
          {map: 'https://cdn.pixabay.com/photo/2014/04/02/14/09/world-map-306338_960_720.png'},
          {map: 'https://cdn.pixabay.com/photo/2014/04/02/14/09/world-map-306338_960_720.png'},
        ]
      }
  }

};
</script>
<style scoped>
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: .5;
  position: absolute;
  width: 100%;
}
</style>
