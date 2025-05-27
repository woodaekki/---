<template>
  <div class="home-container">
    <img src="../assets/mainpage.png" alt="메인 이미지" class="bg-img" />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const goToLogin = () => {
  router.push({ name: 'product' })
}
</script>

<style scoped>
.home-container {
  height: calc(100vh - 60px);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.bg-img {
  height: 100%;
  width: auto;
  object-fit: contain;
  display: block;
}
</style>
