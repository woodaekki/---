<template>
  <div class="outer">
    <div class="wrapper">
      <div class="detail-container">
        <h1 class="page-title">영상 상세 페이지</h1>
        <hr class="line" />

        <div v-if="video">
          <div class="video-section">
            <iframe
              :src="`https://www.youtube.com/embed/${video.id}`"
              frameborder="0"
              allowfullscreen
            ></iframe>
          </div>

          <div class="info-section">
            <h3 class="video-title">{{ video.snippet.title }}</h3>
            <p class="video-channel"><strong>채널:</strong> {{ video.snippet.channelTitle }}</p>

            <div class="description-box">
              <h4>📄 영상 설명</h4>
              <p :class="{ clamped: !expanded }">
                {{ video.snippet.description }}
              </p>
              <button class="toggle-btn" @click="expanded = !expanded">
                {{ expanded ? '간략히 보기 ▲' : '자세히 보기 ▼' }}
              </button>
            </div>
          </div>
        </div>

        <div v-else>
          <p>동영상 정보를 불러오는 중입니다...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const videoId = route.params.id
const video = ref(null)
const expanded = ref(false)

const API_KEY = import.meta.env.VITE_API_KEY

const fetchVideoDetail = async () => {
  try {
    const res = await axios.get('https://www.googleapis.com/youtube/v3/videos', {
      params: {
        part: 'snippet',
        id: videoId,
        key: API_KEY
      }
    })

    if (res.data.items && res.data.items.length > 0) {
      video.value = res.data.items[0]
    }
  } catch (error) {
    console.error('영상 정보 불러오기 실패:', error)
  }
}

onMounted(() => {
  fetchVideoDetail()
})
</script>

<style scoped>
.outer {
  display: flex;
  justify-content: center;
  min-height: 100vh;
}

.wrapper {
  background-color: #d8d8d8a8;
  max-width: 1200px;
  width: 100%;
  padding: 40px 0;
  box-sizing: border-box;
}

.detail-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 24px;
  font-family: 'Noto Sans KR', sans-serif;
  color: #0f0f0f;
}

.page-title {
  font-size: 26px;
  font-weight: 700;
  margin-top: 50px;
  margin-bottom: 10px;
}

.line {
  border: 1px solid #949090;
  margin-bottom: 15px;
}

.video-section {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 40px;
}

.video-section iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
  border: none;
  display: block;
}

.info-section {
  background-color: #fafafa;
  border: 1px solid #d1d0d0;
  border-radius: 12px;
  padding: 24px;
}

.video-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 8px;
}

.video-channel {
  font-size: 14px;
  color: #606060;
  margin-bottom: 24px;
}

.description-box {
  border-top: 1px solid #d1d0d0;
  padding-top: 16px;
}

.description-box h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.description-box p {
  font-size: 15px;
  color: #404040;
  line-height: 1.7;
  white-space: pre-wrap;
  margin-bottom: 10px;
  transition: max-height 0.3s ease;
}

.description-box p.clamped {
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.toggle-btn {
  background-color: #ffffff;
  border: 1px solid #d1d0d0;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  background-color: #f1f1f1;
  border-color: #999;
}
</style>