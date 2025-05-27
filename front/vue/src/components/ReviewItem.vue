<!-- ReviewItem.vue -->

<template>
  <div>
    <ul v-if="localReviews.length > 0">
      <li v-for="review in localReviews" :key="review.id">
        <div class="review-meta">
          {{ review.user }} | {{ formatDate(review.created_at) }}
          <!-- localStorage는 모든 값을 문자열(string)로 저장!!! -->
          <button v-if="review.user === accountStore.username" class="delete-btn"
            @click="deleteReview(review.id)">삭제</button>
        </div>
        <div class="review-content">{{ review.content }}</div>
      </li>
    </ul>
    <p v-else>댓글이 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useArticleStore } from '@/stores/articles'

const props = defineProps({
  reviews: {
    type: Array,
    required: true
  }
})

const route = useRoute()
const accountStore = useAccountStore()
const store = useArticleStore()
const localReviews = ref([...props.reviews])

// props가 바뀔 때 localReviews도 함께 갱신
watch(() => props.reviews, (newVal) => {
  localReviews.value = [...newVal]
})

// 댓글 삭제 후 목록 재조회
const deleteReview = (reviewId) => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  axios.delete(`${store.API_URL}/api/v3/articles/${route.params.id}/reviews/${reviewId}/`, {
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then(() => {
      return axios.get(`${store.API_URL}/api/v3/articles/${route.params.id}/`, {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
    })
    .then(res => {
      localReviews.value = res.data.reviews
    })
    .catch(err => {
      console.error('댓글 삭제 또는 재조회 실패:', err)
      alert('댓글 삭제 중 문제가 발생했습니다.')
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
</script>


<style scoped>
div {
  font-family: 'Noto Sans KR', sans-serif;
  color: #222;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  padding: 16px 0;
  border-bottom: 1px solid #e5e5e5;
}

.review-meta {
  font-size: 13px;
  color: #888;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
}

.review-content {
  font-size: 16px;
  line-height: 1.8;
  white-space: pre-wrap;
}

.delete-btn {
  margin-left: 8px;
  background: none;
  color: #888;
  border: none;
  font-size: 12px;
  cursor: pointer;
  padding: 0;
}

p {
  margin: 6px 0;
}
</style>