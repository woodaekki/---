<template>
  <div class="page-wrapper">
    <div class="container-box">
      <h2 class="title">비디오 검색</h2>

      <div class="search-bar">
        <input v-model="query" placeholder="검색어를 입력하세요" @keyup.enter="searchVideos" />
        <button @click="searchVideos">검색</button>
      </div>

      <div v-if="videos.length > 0">
        <h3>검색 결과</h3>
        <ul class="video-list">
          <li v-for="video in videos" :key="video.id.videoId" class="video-row">
            <RouterLink :to="{ name: 'stock-detail', params: { id: video.id.videoId } }" class="video-row-link">
              <img :src="video.snippet.thumbnails.medium.url" class="video-thumb" />
              <div class="video-info">
                <h4 class="video-title">{{ video.snippet.title }}</h4>
                <p class="video-meta">{{ video.snippet.channelTitle }} · {{ video.snippet.publishedAt.slice(0, 10) }}</p>
              </div>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const query = ref('')
const videos = ref([])

const API_KEY = import.meta.env.VITE_API_KEY

function searchVideos() {
  axios.get('https://www.googleapis.com/youtube/v3/search', {
    params: {
      part: 'snippet',
      q: query.value,
      key: API_KEY,
      type: 'video',
      maxResults: 20
    }
  }).then(response => {
    videos.value = response.data.items
  }).catch(err => {
    console.error('유튜브 API 호출 실패:', err.response || err)
  })
}
</script>

<style scoped>
.page-wrapper {
  padding: 60px 20px;
  min-height: 100vh;
}

.container-box {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}


.title {
  font-size: 30px;
  font-weight: 700;
  font-family: 'WooridaumB', sans-serif;
  margin-top: 54px;
  margin-bottom: 36px;
  text-align: center;
  color: #111111;
}

.search-bar {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 40px;
}

input {
  padding: 12px 16px;
  flex: 1;
  max-width: 400px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
  background-color: #fff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input:focus {
  border-color: #2f80ed;
  box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.2);
}

button {
  padding: 12px 20px;
  font-size: 15px;
  font-weight: 600;
  background-color: #2f80ed;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #2b6fc8;
}

h3 {
  text-align: left;
  font-size: 20px;
  margin-top: 50px;
  margin-bottom: 20px;
  color: #111111;
}

.video-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 0;
  list-style: none;
}

.video-row {
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 16px;
}

.video-row-link {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  text-decoration: none;
  color: inherit;
  transition: background-color 0.2s ease;
  padding: 8px 4px;
  border-radius: 8px;
}

.video-row-link:hover {
  background-color: #f5f5f5;
}

.video-thumb {
  width: 160px;
  height: 90px;
  object-fit: cover;
  border-radius: 6px;
}

.video-info {
  flex: 1;
}

.video-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;
  color: #111111;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.video-meta {
  font-size: 13px;
  color: #555555;
}
</style>
