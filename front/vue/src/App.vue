<!-- App.vue -->

<template>
  <header class="navbar">
    <div class="navbar-left">
      <RouterLink :to="{ name: 'home' }" class="nav-item">MONEYKEY-NEKO</RouterLink>
    </div>

    <div class="navbar-center">
      <RouterLink :to="{ name: 'product' }" class="nav-item">예적금 비교</RouterLink>
       <RouterLink :to="{ name: 'recommend' }" class="nav-item">맞춤상품 추천</RouterLink>
      <RouterLink :to="{ name: 'stock' }" class="nav-item">주식정보</RouterLink>
      <RouterLink :to="{ name: 'gold_and_silver' }" class="nav-item">현물상품</RouterLink>
      <RouterLink :to="{ name: 'map' }" class="nav-item">은행지도</RouterLink>
      <RouterLink :to="{ name: 'article' }" class="nav-item">게시판</RouterLink>
    </div>

    <div class="navbar-right">
      <template v-if="accountStore.isLogin">
        <span @click="goToProfile" class="nav-item" style="cursor: pointer">
          {{ accountStore.username }}님
        </span>
        <button @click="accountStore.logOut" class="nav-item btn btn-outline-secondary btn-sm">로그아웃</button>
      </template>
      <template v-else>
        <RouterLink :to="{ name: 'signup' }" class="nav-item">회원가입</RouterLink>
        <RouterLink :to="{ name: 'login' }" class="nav-item">로그인</RouterLink>
      </template>
    </div>
  </header>

  <main>
    <RouterView />
  </main>

  <button @click="showChat = !showChat" class="chatbot-button">
    <img :src="icon" alt="챗봇 아이콘" class="chatbot-icon" />
  </button>

  <ChatWidget v-if="showChat" @close="showChat = false" />
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'
import icon from '@/assets/icon.png'
import ChatWidget from '@/components/ChatWidget.vue'
import axios from 'axios'

const showChat = ref(false)
const accountStore = useAccountStore()
const router = useRouter()

const goToProfile = () => {
  axios.get('http://127.0.0.1:8000/api/v1/profile/my_profile/', {
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then(() => {
      router.push({ name: 'final-userprofile', params: { id: accountStore.userId } })
    })
    .catch(() => {
      router.push({ name: 'userprofile' })
    })
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 32px;
  background-color: white;
  border-bottom: 1px solid #eaeaea;
  font-size: 20px;
  font-family: 'WooridaumB', sans-serif;
}

.navbar-center .nav-item {
  padding: 11px;
}

.navbar-left,
.navbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.navbar-left .nav-item {
  font-family: 'WooridaumB', sans-serif;
  font-size: 20px;
}

.navbar-right .nav-item {
  font-family: 'WooridaumB', sans-serif;
  font-size: 15px;
}

.nav-item {
  margin: 0 4px;
  text-decoration: none;
  color: #111;
  font-weight: 500;
}

.nav-item:hover {
  color: #2f80ed;
}

button.nav-item {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 6px 10px;
}

.chatbot-button {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 72px;
  height: 72px;
  background-color: #ffffff;
  border-radius: 50%;
  border: 0.5px solid #bdb8b8d7;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.10); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  transition: transform 0.2s ease-in-out;
}


.chatbot-button:hover {
  transform: scale(1.1) rotate(-3deg);
}

.chatbot-button img {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.chatbot-icon {
  width: 64px;
  height: 64px;
  object-fit: contain;
  display: block;
}

</style>

