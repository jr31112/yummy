<template>
<v-app>
    <div class="user join">
        <div class="header" style="width:100%; height:40px">
            <p style="vertical-align: middle;padding: 8px 5px;float:left;">회원가입</p>
        </div>
        <br>

            <div style="width:50%">
                <v-text-field style="color:blue;" label="ID" v-model="id" id="id" hide-details="auto"></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue" v-model="nickName" id="nickName" label="닉네임" hide-details="auto"></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue;" label="나이" v-model="age" id="age" hide-details="auto"></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue" v-model="password" label="비밀번호" type=password hide-details="auto"></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue"  v-model="passwordConfirm" label="비밀번호 확인" type=password hide-details="auto"></v-text-field>
            </div>
            <br>

            <div style="width:50%">
                <v-text-field style="color:blue;" label="이메일" v-model="email" id="email" hide-details="auto"></v-text-field>
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
    export default {
        data: () => {
            return {
                id:'',
                name: '',
                age:'',
                email: '',
                password: '',
                passwordConfirm: '',
                nickName: '',
                isSubmit: false,
            }
        },
        methods: {
            submit() {
                let form = new FormData()
                form.append('id', this.id)
                form.append('name', this.name)
                form.append('age', this.age)
                form.append('email', this.email)
                form.append('password', this.password)
                form.append('nickname', this.nickName)
                    
                axios.post("".form)
                .then(Response => {
                })
                .catch(Error => {
                  console.log(Error)
                })
            }
        }

    }
</script>