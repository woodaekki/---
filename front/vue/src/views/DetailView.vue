<template>
  <div class="wrapper">
    <div v-if="article" class="article-info">
      <div class="title-row">
        <span class="article-title-text">{{ article.title }}</span>
        <span class="article-category">
          [{{ getCategoryLabel(article.category) }}]
        </span>
        <span class="article-time"> | </span>
        <span class="article-time"> {{ formatDate(article.created_at) }}</span>
        <button v-if="article.user === accountStore.username" class="change-btn" @click="changeArticle">
          수정
        </button>
        <button v-if="article.user === accountStore.username" class="delete-btn" @click="deleteArticle">
          삭제
        </button>
      </div>
      <div class="article-content">{{ article.content }}</div>
    </div>

    <div class="review-section">
      <form @submit.prevent="submitReview" class="comment-form">
        <div class="comment-flex">
          <div class="comment-box">
            <textarea v-model="reviewContent" placeholder="댓글을 입력하세요" class="comment-textarea"></textarea>
            <div class="comment-actions">
              <button type="submit" :disabled="!reviewContent.trim()">등록</button>
            </div>
          </div>
        </div>
      </form>

      <ReviewItem :reviews="reviews" />
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'
import ReviewItem from '@/components/ReviewItem.vue'

const accountStore = useAccountStore()
const store = useArticleStore()
const route = useRoute()
const router = useRouter()

const article = ref(null)
const reviewContent = ref('')
const reviews = ref([])

const profanityList = ref([])

const getCategoryLabel = (category) => {
  if (category === 0) return '공지사항'
  if (category === 1) return '정보공유'
  if (category === 2) return '자유게시판'
  return '기타'
}

function maskProfanity(text) {
  let result = text
  profanityList.value.forEach(word => {
    const regex = new RegExp(word, 'gi')
    result = result.replace(regex, '*'.repeat(word.length))
  })
  return result
}

onMounted(async () => {
  if (!accountStore.token) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const query = await fetch('/profanity.json')
    profanityList.value = await query.json()
  } catch (e) {
    console.error('비속어 리스트 로딩 실패:', e)
  }

  // 게시글 불러오기
  try {
    const res = await axios.get(`${store.API_URL}/api/v3/articles/${route.params.id}/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
    article.value = res.data
    reviews.value = res.data.reviews
  } catch (err) {
    console.error('게시글 불러오기 실패:', err)
    alert('인증이 만료되었거나 접근 권한이 없습니다.')
    router.push({ name: 'login' })
  }
})

const deleteArticle = () => {
  if (!confirm('정말 이 게시글을 삭제하시겠습니까?')) return

  axios.delete(`${store.API_URL}/api/v3/articles/${route.params.id}/`, {
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then(() => {
      store.articles = store.articles.filter(a => a.id !== Number(route.params.id))
      alert('게시글이 삭제되었습니다.')
      router.push({ name: 'article' })
    })
    .catch(err => {
      console.error('게시글 삭제 실패:', err)
      alert('삭제에 실패했습니다.')
    })
}

const submitReview = () => {
  const maskedReview = maskProfanity(reviewContent.value)

  axios({
    method: 'post',
    url: `${store.API_URL}/api/v3/articles/${route.params.id}/reviews/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
    data: {
      content: maskedReview
    }
  })
    .then(() => {
      reviewContent.value = ''
    })
    .catch(err => {
      console.error('댓글 등록 실패:', err)
      alert('댓글 등록 중 오류가 발생했습니다.')
    })
    .finally(() => {
      axios.get(`${store.API_URL}/api/v3/articles/${route.params.id}/`, {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
        .then(res => {
          article.value = res.data
          reviews.value = res.data.reviews
        })
        .catch(err => {
          console.error('게시글 재조회 실패:', err)
        })
    })
}

const formatDate = (datetime) => {
  const date = new Date(datetime)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

const changeArticle = () => {
  router.push({ name: 'edit', params: { id: route.params.id }, query: {
    title: article.value.title,
    content: article.value.content,
    category: article.value.category
  } })
}
</script>

<style scoped>
.wrapper {
  max-width: 1080px;
  margin: 0 auto;
  padding: 60px 32px;
  font-family: 'Noto Sans KR', sans-serif;
  color: #222;
  box-sizing: border-box;
}

.article-info {
  padding-top: 48px;
}

.title-row {
  display: flex;
  align-items: flex-end;
  gap: 14px;
  margin-bottom: 24px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}

.article-title-text {
  font-size: 28px;
  font-weight: 700;
  word-break: break-word;
}

.article-category {
  font-size: 16px;
  color: #666;
}

.article-time {
  margin-left: 12px;
  font-size: 15px;
  color: #888;
}

.article-content {
  font-size: 20px;
  line-height: 2.2;
  padding: 40px 0;
  white-space: pre-wrap;
  border-bottom: 1px solid #e0e0e0;
  min-height: 520px;
  margin-bottom: 48px;
}

.review-section {
  margin-top: 0;
}

form {
  width: 100%;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

textarea {
  width: 100%;
  min-height: 140px;
  padding: 16px 20px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 10px;
  resize: vertical;
  line-height: 1.8;
  outline: none;
}

button[type="submit"] {
  margin-top: 8px;
  align-self: flex-end;
  padding: 12px 20px;
  font-size: 14px;
  background-color: #2f80ed;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button[type="submit"]:hover {
  background-color: #1a73e8;
}

.change-btn,
.delete-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-left: 8px;
}
</style>