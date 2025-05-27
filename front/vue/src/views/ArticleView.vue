<template>
  <div class="container">
    <h1>할 말이 머니</h1>

    <!-- 🔹 카테고리 탭 -->
    <div class="tab-buttons-wrapper">
      <div class="tab-buttons">
        <button :class="{ active: selectedCategory === null }" @click="selectCategory(null)">전체</button>
        <button :class="{ active: selectedCategory === 0 }" @click="selectCategory(0)">공지사항</button>
        <button :class="{ active: selectedCategory === 1 }" @click="selectCategory(1)">정보공유</button>
        <button :class="{ active: selectedCategory === 2 }" @click="selectCategory(2)">자유게시판</button>
      </div>
      <button @click="goToCreate" class="post-btn">글쓰기</button>
    </div>

    <div class="post-board" v-if="selectedCategory !== 2">
      <ul v-if="filteredFixedArticles.length">
        <li v-for="item in filteredFixedArticles" :key="item.id">
          <RouterLink :to="{ name: 'fixed-detail', params: { id: item.id } }" class="article-item fixed-article">
            <div class="meta">
              <span>{{ item.title }}</span>

            </div>
          </RouterLink>
        </li>
        
      </ul>
      <p v-else>해당 카테고리의 고정글이 없습니다.</p>
      <ArticleList :selectedCategory="selectedCategory" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useArticleStore } from '@/stores/articles'
import ArticleList from '@/components/ArticleList.vue'

const router = useRouter()
const account = useAccountStore()
const store = useArticleStore()

const selectedCategory = ref(null)
const fixedArticles = ref([])

const selectCategory = (value) => {
  selectedCategory.value = value
}

const goToCreate = () => {
  if (!account.isLogin) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
  } else {
    router.push({ name: 'create', query: { category: selectedCategory.value } })
  }
}

const filteredFixedArticles = computed(() => {
  if (selectedCategory.value === null) {
    return fixedArticles.value
  }
  return fixedArticles.value.filter(item => item.category === selectedCategory.value)
})

onMounted(() => {
  store.getArticles()

  axios.get(`${store.API_URL}/api/v3/fixed_articles/`)
    .then(res => {
      fixedArticles.value = res.data
    })
    .catch(err => console.error('고정글 불러오기 실패:', err))
})
</script>

<style>
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 48px 24px;
  background-color: #d8d8d8a8;
}

h1 {
  font-size: 28px;
  font-weight: 700;
  color: #2d2d2d;
  padding-left: 12px;
  margin-bottom: 32px;
  font-family: 'WooridaumB', sans-serif;
  border-left: 5px solid #38b2ac;
}

.tab-buttons-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.tab-buttons {
  display: flex;
  gap: 12px;
}

.tab-buttons button {
  padding: 8px 20px;
  font-size: 14px;
  border-radius: 20px;
  border: 1px solid #d1d5db;
  background-color: #f1f5f9;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.tab-buttons button.active {
  background-color: #9ca3af;
  color: white;
  border-color: #9ca3af;
}

.tab-buttons button:hover {
  background-color: #e5e7eb;
  color: #374151;
}

.post-board {
  background-color: #ffffffbe;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 32px 24px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.02);
  margin-bottom: 32px;
}

.post-btn {
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 500;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-right: 4px;
}

.post-btn:hover {
  background-color: #1d4ed8;
}

.article-item {
  display: block;
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
  text-decoration: none;
}

.article-item:last-child {
  border-bottom: none;
}

.meta {
  display: flex;
  font-family: Noto Sans KR;
  flex-direction: column;
  font-weight: 500;       
  font-size: 14px;        
  color: #374151;      
  margin-bottom: 4px;
}

.preview {
  font-size: 14px;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 600px;
}

.post-board ul {
  list-style: none;
  padding-left: 0;
}

.fixed-article {
  background-color: #b2bdc74d;
  padding: 14px 16px;
  margin-bottom: 8px;
  border-radius: 8px;
  position: relative;
}

.fixed-article .title {
  color: #1f2937;
  font-weight: 600;
}

.fixed-article .preview {
  color: #4b5563;
}

.fixed-article::before {
  content: '공지';
  position: absolute;
  top: 12px;
  right: 16px;
  background-color: #9ca3af;
  color: white;
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
}
</style>
