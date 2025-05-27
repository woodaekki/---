<template>
  <div class="container">
    <h1>게시글 수정</h1>
    <form @submit.prevent="updateArticle" class="form">
      <div class="form-group">
        <label for="title">제목</label>
        <input type="text" id="title" v-model="title" />
      </div>

      <div class="form-group">
        <label for="category">카테고리</label>
        <select id="category" v-model.number="category">
          <option disabled value="">-- 카테고리 선택 --</option>
          <option :value="0">공지사항</option>
          <option :value="1">정보공유</option>
          <option :value="2">자유게시판</option>
        </select>
      </div>

      <div class="form-group">
        <label for="content">내용</label>
        <textarea id="content" v-model="content"></textarea>
      </div>

      <button type="submit" class="submit-btn">수정 완료</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useArticleStore } from '@/stores/articles'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const store = useArticleStore()

const title = ref('')
const content = ref('')
const category = ref('')
const profanityList = ref([])

onMounted(async () => {
  const query = await fetch('/profanity.json')
  profanityList.value = await query.json()

  axios.get(`${store.API_URL}/api/v3/articles/${route.params.id}/`, {
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then(res => {
      title.value = res.data.title
      content.value = res.data.content
      category.value = res.data.category
    })
    .catch(err => {
      console.error('불러오기 실패:', err)
      alert('로그인이 필요한 기능입니다.')
      router.push({ name: 'login' })
    })
})

function maskProfanity(text) {
  let result = text
  profanityList.value.forEach(word => {
    const regex = new RegExp(word, 'gi')
    result = result.replace(regex, '*'.repeat(word.length))
  })
  return result
}

const updateArticle = () => {
  if (category.value === '') {
    alert('카테고리를 선택해주세요.')
    return
  }

  const maskedTitle = maskProfanity(title.value)
  const maskedContent = maskProfanity(content.value)

  axios.put(`${store.API_URL}/api/v3/articles/${route.params.id}/`, {
    title: maskedTitle,
    content: maskedContent,
    category: category.value
  }, {
    headers: {
      Authorization: `Token ${accountStore.token}`
    }
  })
    .then(() => {
      alert('게시글이 수정되었습니다.')
      router.push({ name: 'detail', params: { id: route.params.id } })
    })
    .catch(err => {
      console.error('수정 실패:', err)
      alert('수정에 실패했습니다.')
    })
}
</script>


<style scoped>
.container {
  max-width: 760px;
  margin: 0 auto;
  padding: 40px 24px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

h1 {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 32px;
  color: #212529;
  border-left: 4px solid #0a857aa1;
  padding-left: 12px;
}

.form {
  display: flex;
  flex-direction: column;
  min-height: 700px;
  gap: 24px;
  background-color: #fff;
  padding: 32px;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 15px;
  font-weight: 500;
  color: #495057;
}

input[type="text"],
textarea {
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  background-color: #fff;
  transition: border-color 0.2s ease;
}

input[type="text"]:focus,
textarea:focus {
  border-color: #2f80ed;
}

textarea {
  height: 360px;
  resize: vertical;
}

.submit-btn {
  align-self: flex-end;
  padding: 10px 22px;
  font-size: 15px;
  font-weight: 500;
  background-color: #2f80ed;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-btn:hover {
  background-color: #1a73e8;
  color: #fff;
}
</style>
