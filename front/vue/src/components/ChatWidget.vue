<template>
  <div class="chatbox">
    <div class="chatbox-header">
      <span class="title"> MONEYKEY-NEKO</span>
      <button class="close-btn" @click="$emit('close')">×</button>
    </div>
    <div class="chatbox-body">
      <ChatbotView />
    </div>
  </div>
</template>

<script setup>
import ChatbotView from '@/components/ChatbotView.vue'
</script>

<style scoped>
.chatbox {
  position: fixed;
  bottom: 100px;
  right: 24px;
  width: 380px;
  height: 560px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 2000;
  border: 1px solid #e5e7eb;
}

.chatbox-header {
  background: linear-gradient(135deg, #4f86f7, #007aff);
  color: white;
  padding: 14px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 20px;
  color: white;
  cursor: pointer;
  padding: 0 6px;
  transition: transform 0.2s ease;
}

.close-btn:hover {
  transform: rotate(90deg);
}

.chatbox-body {
  flex: 1;
  overflow: hidden;
  background-color: #fdfdfd;
}
</style>
