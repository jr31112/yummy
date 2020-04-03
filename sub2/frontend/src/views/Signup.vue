<template>
<v-app>
    <div class="user join">
        <div class="header" style="width:100%; height:40px">
            <p style="vertical-align: middle;padding: 8px 5px;float:left;">회원가입</p>
        </div>
        <br>
            <div style="width:50%">
                <v-text-field style="color:blue;" label="이메일" v-model="email" id="email"></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue" v-model="password1" label="비밀번호" type=password></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue"  v-model="password2" label="비밀번호 확인" type=password></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue;" label="성별" v-model="gender" id="gender"></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue" v-model="nickname" id="nickname" label="닉네임"></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue;" label="나이" v-model="birth_year" id="birth_year"></v-text-field>
            </div>
            <br>

            
        <div>
            <button @click="submit">
                회원가입
            </button>
        </div>                 
    </div>
</v-app>
</template>

<script>
import axios from 'axios'
    export default {
        data: () => {
            return {
                birth_year:'',
                email: '',
                password1: '',
                password2: '',
                nickname: '',
                gender:'',
                isSubmit: false,
            }
        },
        methods: {
            submit() {
                let form = new FormData()
                form.append('gender', this.gender)
                form.append('nickname', this.nickname)
                form.append('birth_year', this.birth_year)
                form.append('email', this.email)
                form.append('password1', this.password1)
                form.append('password2', this.password2)
                    
                axios.post("http://127.0.0.1:8000/rest-auth/registration/", form)
                .then(Response => {
                    var router = this.$router;
                            router.push({
                                name: "home",
                                params: {
                                    "email": this.email,
                                }
                            });
                })
                .catch(Error => {
                    alert('이메일과 비밀번호를 확인하세요')
                    console.log(Error)
                })
            }
        }

    }
</script>