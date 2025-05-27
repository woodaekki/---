<template>
  <div class="wrapper">
    <div class="article-info" v-if="article">
      <div class="title-row">
        <span class="article-title-text">{{ article.title }}</span>
        <span class="article-category">[{{ getCategoryLabel(article.category) }}]</span>
        <RouterLink :to="{name: 'article'}" class="back-link">목록</RouterLink>
      </div>
      <div class="article-content">
        {{ article.content }}
      </div>
    </div>
    <div v-else class="loading-message">고정된 게시글을 불러오는 중입니다...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useArticleStore } from '@/stores/articles'

const route = useRoute()
const store = useArticleStore()
const article = ref(null)

const getCategoryLabel = (category) => {
  switch (category) {
    case 0: return '공지사항'
    case 1: return '정보공유'
    case 2: return '자유게시판'
    default: return '기타'
  }
}

onMounted(() => {
  axios.get(`${store.API_URL}/api/v3/fixed_articles/${route.params.id}/`)
    .then(res => {
      article.value = res.data
    })
    .catch(err => {
      console.error('고정글 불러오기 실패:', err)
      article.value = {
        title: '불러오기 실패',
        content: '해당 게시글을 불러올 수 없습니다.',
        category: -1
      }
    })
})
</script>

<style scoped>
.wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 48px;
  font-family: 'Noto Sans KR', sans-serif;
  color: #222;
}

.article-info {
  padding-top: 48px;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 12px;
}

.article-title-text {
  font-size: 28px;
  font-weight: 600;
  word-break: break-word;
}

.article-category {
  font-size: 16px;
  color: #666;
}

.back-link {
  margin-left: auto;
  font-size: 14px;
  padding: 10px 24px;
  border-radius: 6px;
  background-color: #2563eb;
  color: white;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.back-link:hover {
  background-color: #1d4ed8;
}

.article-content {
  font-size: 19px;
  line-height: 2.2;
  padding: 36px 0;
  white-space: pre-wrap;
  border-bottom: 1px solid #d4d4d4;
  min-height: 500px;
}
</style>
