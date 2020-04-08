<template>
  <v-container style="background:white;">
    <v-row>
      <v-col>
        <v-text-field label="이메일 주소 입력"
          v-model="email"
          @keyup.enter="login({email, password})"
          style="color:blue; border:none;"
          id="email"></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field label="비밀번호 입력"
          v-model="password"
          type="password"
          id="password"
          @keyup.enter="login({email, password1, password2})"
          style="color:blue"></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field label="비밀번호 확인"
          v-model="email"
          @keyup.enter="login({email, password1, password2})"
          style="color:blue; border:none;"
          id="email"></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <button @click="login({email, password})">로 그 인</button>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {mapState, mapActions} from "vuex"
export default {
    name: "loginModal",
    created() {
        if(sessionStorage.access_token){
            alert("로그인에 성공하셨습니다.")
            this.$store.dispatch('getMemberInfo')
        }
    },
    computed:{
        ...mapState(["isLogin","isLoginError"])
    },
    methods: {
        ...mapActions(["login"]),
    },
    data: () => {
        return {
            email: '',
            password: '',
            birth_year:'',
            gender:'',
            nickname:'',
            access_token: '',
        }
    }
}
</script>

<style>

</style>