<!-- views/SignUpView.vue -->
<template>
  <div class="signup-container">
    <h1>회원 가입 페이지</h1>

    <form @submit.prevent="onSignUp">
      <div class="form-group">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model="username">
      </div>

      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model="password1">
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="password2">
      </div>

      <input type="submit" value="회원가입" class="btn">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'

const accountStore = useAccountStore()

const username = ref('')
const password1 = ref('')
const password2 = ref('')

const onSignUp = function () {
  const userInfo = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }
  accountStore.signUp(userInfo)
}
</script>

<style scoped>
.signup-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 64px 24px; /* 상단 패딩을 약간 늘림 */
}

form {
  width: 100%;
  max-width: 800px;
  background-color: #fff;
  padding: 48px 56px; /* 좌우 padding을 살짝 넓힘 */
  border-radius: 14px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 28px; /* 각 항목 간 간격을 약간 더 넓힘 */
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 48px; /* 제목과 폼 간격 증가 */
  font-size: 30px;
  font-weight: bold;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px; /* label과 input 간 거리 증가 */
}

label {
  font-weight: 600;
  color: #333;
  font-size: 17px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 16px 18px; /* 인풋 내부 여백 증가 */
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.2s ease;
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
