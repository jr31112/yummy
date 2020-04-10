<template>
  <v-card>
    <v-tabs
      v-model="tab"
      background-color="transparent"
      color="basil"
      grow>
      <v-tab v-for="item in items" :key="item">
        {{ item }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item> 
        <v-card color="basil" flat>
          <v-container style="height:700px">
            <h3 class="form-title">회원가입</h3>
            <i class="fas fa-sign-in-alt"></i>
            <v-col>
              <v-text-field style="color:blue;" label="이메일" v-model="email" id="email"></v-text-field>
            </v-col>
            <v-col>
              <v-text-field style="color:blue;" label="비밀번호" type="password" v-model="password1" id="password1"></v-text-field>
            </v-col>
            <v-col>
              <v-text-field style="color:blue;" label="비밀번호 확인" type="password" v-model="password2" id="password2"></v-text-field>
            </v-col>
            <v-col>
              <v-text-field style="color:blue;" label="나이" v-model="birth_year" id="birth_year"></v-text-field>
            </v-col>
            <v-col>
              <v-text-field style="color:blue;" label="닉네임" v-model="nickname" id="nickname"></v-text-field>
            </v-col>
            <v-col>
              <v-text-field style="color:blue;" label="성별" v-model="gender" id="gender"></v-text-field>
            </v-col>
            <v-row>
              <v-col style="">
                <div class="text-xs-center">
                <v-btn @click="submit" round color="primary" dark>회원가입</v-btn>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-tab-item>

      <v-tab-item>
        <v-card>
          <v-container style="background:white; height:700px">
            <h3 class="form-title">로그인</h3>
            <v-row>
              <v-col>
                <v-text-field label="이메일 주소 입력"
                  v-model="email"
                  @keyup.enter="login({email, password1})"
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
                  @keyup.enter="login({email, password1})"
                  style="color:blue"></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-btn @click="login({email, password})" round color="primary" dark>로그인</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
import router from "../../../router";
import axios from 'axios'
import {mapState, mapActions} from "vuex"
import '../../../css/login.css'
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
        submit() {
          let form = new FormData()
          form.append('gender', this.gender)
          form.append('nickname', this.nickname)
          form.append('birth_year', this.birth_year)
          form.append('email', this.email)
          form.append('password1', this.password1)
          form.append('password2', this.password2)
          axios.post("http://127.0.0.1:8000/signup/", form)
          .then(Response => {
            this.$store.state.dialog = false
            var router = this.$router;
              router.push({
                name: "home",
                params: {
                }
              });
          })
          .catch(Error => {
              alert('이메일과 비밀번호를 확인하세요')
              console.log(Error)
          })
        }
    },
    data: () => {
        return {
          modal: false,
          tab: null,
          items: [
            'SignUp', 'Login'
          ],
          password:'',
          birth_year:'',
          email: '',
          password1: '',
          password2: '',
          nickname: '',
          gender:'',
          isSubmit: false,
          access_token: '',
        }
    }
}
</script>