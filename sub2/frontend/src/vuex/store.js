import Vue from "vue";
import Vuex from "vuex";
import router from "../routes.js";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userinfo:null, //db로부터 얻어온 정보가 여기에 저장(회원정보)
        isLogin:false,
        isLoginError:false
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
            sessionStorage.removeItem('access_token')
        },
        
    },
    actions: {
        //로그인을 시도
        login({dispatch}, loginObj){ //커밋으로 mutations 실행
            let form = new FormData()
            form.append('email', loginObj.email)
            form.append('password',loginObj.password)
            // 로그인 -> 토큰반환
            axios.post("", form)
            .then(res=>{
                //성공시 token:블라블라(유저 id를 받아옴)
                //토큰을 헤더에 포함시켜서 유저정보를 요청
                //let token = res.data.token;
                if(res.data.data!="failed"){ //로그인 성공
                    let token = res.data.data
                    //토큰을 로컬스토리지에 저장
                    sessionStorage.setItem("access_token", token)
                    dispatch("getMemberInfo") //액션은 디스패치로 불러온다.
                }
                else {
                    sessionStorage.removeItem('access_token')
                    alert("아이디 혹은 비밀번호를 확인해주세요.")
                }
            })
            
            .catch(error=>{
                alert("이메일과 비밀번호를 확인하세요!")
                console.log(error)
            })
        },

        getMemberInfo({commit}){
            let token = sessionStorage.getItem("access_token")
            
            //로컬 스토리지에 저장되어 있는 토큰을 불러온다.
            let form = new FormData()
            form.append('access_token', token)
            if(token!=null){
              // 반환된 토큰을 가지고 유저 정보를 가져와 저장(멤버 정보 반환)
                axios.post("", form)
                    .then(response=>{
                        let userinfo = {
                            email : response.data.object.email,
                            gender : response.data.object.gender,
                            birth_year : response.data.object.birth_year,
                            nickName : response.data.object.nickname,
                        }
                        commit('loginsuccess',userinfo);
                      
                        if(router.history.current.name=='Login'){
                            router.push({name:"Home"}).catch((any) =>{});
                        }
                    })
                    .catch(error=>{
                        sessionStorage.removeItem('access_token')
                        alert("이메일과 비밀번호를 확인하세요!")
                        console.log(error)
                    })
              
            }
        }
         
    }, 
})