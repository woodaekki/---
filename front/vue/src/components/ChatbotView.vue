<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index">
        <div v-if="msg.sender === 'MONEYKEY-NEKO'" class="message left">
          <p class="sender">{{ msg.sender }}</p>
          <div class="bubble">{{ msg.text }}</div>
        </div>
        <div v-else class="message right">
          <div class="bubble">{{ msg.text }}</div>
        </div>
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="input"
        @keyup.enter="sendMessage"
        placeholder="메시지를 입력하세요"
        class="input-box"
      />
      <button @click="sendMessage" class="send-button">보내기</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const input = ref('')
const messages = ref([])
const accountStore = useAccountStore()
const router = useRouter()

const sendMessage = function () {
  if (!accountStore.isLogin) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  if (!input.value.trim()) return

  messages.value.push({ sender: '', text: input.value })

  axios.post('http://127.0.0.1:8000/api/v5/', {
    message: input.value
  }, {
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  }).then(res => {
    messages.value.push({ sender: 'MONEYKEY-NEKO', text: res.data.response })
  })

  input.value = ''
}
</script>

<style scoped>
.chat-container {
  width: 100%;
  height: 100%;
  padding: 16px;
  border-radius: 16px;
  background-color: #fefefe;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  background-color: #f3f4f6;
  gap: 10px;
}

.message {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.left {
  align-items: flex-start;
}

.right {
  align-items: flex-end;
}

.sender {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 2px;
  color: #666;
}

.bubble {
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
  word-break: break-word;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  max-width: 80%;
}

.left .bubble {
  background-color: #ffffff;
  border-bottom-left-radius: 4px;
}

.right .bubble {
  background-color: #4f86f7;
  color: #fff;
  border-bottom-right-radius: 4px;
  margin-left: auto;
}

.input-area {
  display: flex;
  padding: 14px 16px;
  border-top: 1px solid #e2e8f0;
  background-color: #fff;
}

.input-box {
  flex: 1;
  padding: 10px 14px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 20px;
  outline: none;
  margin-right: 8px;
}

.send-button {
  background-color: #4f86f7;
  color: white;
  border: none;
  padding: 10px 18px;
  font-size: 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.send-button:hover {
  background-color: #397ae3;
}
</style>
