import Vue from "vue";
import Vuex from "vuex";
import router from "../router";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userinfo:null, //db로부터 얻어온 정보가 여기에 저장(회원정보)
        isLogin:false,
        isLoginError:false,
        email:'',
        gender:'',
        birth_year:'',
        nickname:'',
        dialog:false
    },
    mutations: {
        loginsuccess(state, payload){
            state.isLogin = true
            state.isLoginError = false
            state.userinfo = payload
        },

        loginError(state){
            state.isLogin = false
            state.isLoginError = true
        },
        logout(state){
            state.isLogin = false
            state.isLoginError = false
            state.userinfo = null
            localStorage.removeItem('access_token')
        },
        
    },
    actions: {
        //로그인을 시도
        login({dispatch}, loginObj){ //커밋으로 mutations 실행
            var form = new FormData()
            form.append('email', loginObj.email)
            form.append('password', loginObj.password)
            // 로그인 -> 토큰반환
            axios.post("http://127.0.0.1:8000/login/", form)
            .then(response=>{
                //let token = res.data.token;
                if(response.data.token){ //로그인 성공
                    this.state.dialog = false
                    let token = response.data.token
                    //토큰을 로컬스토리지에 저장 

                    this.state.email = response.data.user.email
                    this.state.gender = response.data.user.gender,
                    this.state.birth_year = response.data.user.birth_year,
                    this.state.nickname = response.data.user.nickname,

                    localStorage.setItem("access_token", token)
                    // dispatch("getMemberInfo") //액션은 디스패치로 불러온다.
                    dispatch("getMemberInfo")
                }
  
                else {
                    localStorage.removeItem('access_token')
                    alert("아이디 혹은 비밀번호를 확인해주세요.")
                }
            })
            
            .catch(error=>{
                console.log(error)
            })
        },
        logout({commit}){
            commit("logout")
            router.push({name:"home"})
        },

        getMemberInfo({commit}){
            let token = localStorage.getItem("access_token")
            if(token){

                //로컬 스토리지에 저장되어 있는 토큰을 불러온다.
                // 반환된 토큰을 가지고 유저 정보를 가져와 저장(멤버 정보 반환)
                let userinfo = {
                    email : this.state.email,
                    nickname : this.state.nickname,
                    gender : this.state.gender,
                    birth_year : this.state.birth_year,
                }
                
                commit('loginsuccess',userinfo);
                var router = this.$router;
                    router.push({
                        name: "home",
                        params: {
                        }
                    });
                
            }
            
        } 
    }, 
})