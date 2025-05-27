<template>
  <div class="container">
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle" class="form">
      <div class="form-group">
        <label for="title">제목</label>
        <input type="text" id="title" v-model.trim="title" />
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
        <textarea id="content" v-model.trim="content"></textarea>
      </div>

      <button type="submit" class="submit-btn">등록</button>
    </form>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import { useAccountStore } from '@/stores/accounts'

const store = useArticleStore()
const accountStore = useAccountStore()
const router = useRouter()
const route = useRoute()

const title = ref('')
const content = ref('')
const category = ref('')
const profanityList = ref([])

onMounted(async () => {
  const queryCategory = route.query.category
  if (queryCategory !== undefined && !isNaN(queryCategory)) {
    category.value = Number(queryCategory)
  }

  // 욕설 JSON 불러오기
  const res = await fetch('/profanity.json')  // public 폴더에 있어야 함
  profanityList.value = await res.json()
})

function maskProfanity(text) {
  let result = text
  profanityList.value.forEach(word => {
    const pattern = new RegExp(word, 'gi')
    result = result.replace(pattern, '*'.repeat(word.length))
  })
  return result
}

const createArticle = () => {
  if (category.value === '') {
    alert('카테고리를 선택해주세요.')
    return
  }

  // 제목과 내용에 대해 욕설 필터링 적용
  const maskedTitle = maskProfanity(title.value)
  const maskedContent = maskProfanity(content.value)

  axios({
    method: 'post',
    url: `${store.API_URL}/api/v3/articles/`,
    headers: {
      Authorization: `Token ${accountStore.token}`
    },
    data: {
      title: maskedTitle,
      content: maskedContent,
      category: category.value
    },
  })
    .then(() => {
      router.push({ name: 'article' })
    })
    .catch(err => console.log(err))
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

select {
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  background-color: #fff;
  transition: border-color 0.2s ease;
  appearance: none; /* 기본 브라우저 스타일 제거 */
  background-image: url("data:image/svg+xml,%3Csvg fill='gray' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px 16px;
}

select:focus {
  border-color: #2f80ed;
}

/* 선택 박스 주변의 마진 조정 */
.form-group select {
  margin-top: 4px;
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
