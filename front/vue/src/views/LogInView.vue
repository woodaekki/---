<!-- views/LogInView.vue -->
<template>
  <div>
    <h1>로그인 페이지</h1>
  </div>

  <div>
    <form @submit.prevent="onLogIn">
      <label for="username">아이디</label>
      <input type="text" id="username" v-model="username">

      <label for="password">비밀번호</label>
      <input type="password" id="password" v-model="password">

      <input type="submit" value="로그인" class="btn">
    </form>  
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'

const accountStore = useAccountStore()

const username = ref('')
const password = ref('')

const onLogIn = function () {
  const userInfo = {
    username: username.value,
    password: password.value
  }
  accountStore.logIn(userInfo)
}
</script>

<style scoped>
/* 로그인 페이지 스타일 */
form {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  background-color: #fff;
  padding: 48px 56px;
  border-radius: 14px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 28px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin: 64px 0 48px;
  font-size: 30px;
  font-weight: bold;
}

label {
  font-weight: 600;
  color: #333;
  font-size: 17px;
  margin-bottom: 10px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 16px 18px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.2s ease;
}

div {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.btn {
  background-color: #2f80ed;
  color: white;
  font-weight: bold;
  border: none;
  padding: 18px;
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  width: 100%;
}

.btn:hover {
  background-color: #1c6dd0;
}

</style>
