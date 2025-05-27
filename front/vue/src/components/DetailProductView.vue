<template>
  <div class="wrapper">
    <div class="page-background">
      <h1 class="page-title">예적금 상품 안내</h1>
      <div class="product-wrapper" v-if="product">
        <div class="product-card">
          <div class="header">
            <div class="name-box">
              <h2>{{ product.fin_prdt_nm }}</h2>
              <p class="bank-name">{{ product.kor_co_nm }}</p>
            </div>
            <div class="rate-box">
              <span class="rate-label">최고 연</span>
              <span class="rate-value">{{ product.highest_rate }}%</span>
              <div class="like-box-inline">
                <button class="like-button" @click="toggleLike">
                  {{ isLiked ? '♥ 관심 해제' : '♡ 관심 상품' }}
                </button>
              </div>
            </div>
          </div>
          <ul class="info-list">
            <li><strong>가입 방법</strong> | {{ product.join_way }}</li>
            <li><strong>우대 조건</strong> | {{ product.spcl_cnd }}</li>
            <li><strong>가입 대상</strong> | {{ product.join_member }}</li>
            <li><strong>최대 가입 한도</strong> | {{ Number(product.max_limit).toLocaleString() }}원</li>
            <li><strong>만기 후 이자율</strong> | {{ product.mtrt_int }}</li>
            <li><strong>기타</strong> {{ product.etc_note }}</li>
          </ul>
          <div v-if="options.length" class="option-section">
            <h3 class="option-title">금리 옵션 정보</h3>
            <div class="table-wrapper">
              <table class="option-table">
                <thead>
                  <tr>
                    <th>저축 기간 (개월)</th>
                    <th>금리 유형</th>
                    <th>기본 금리</th>
                    <th>최고 금리</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="opt in options" :key="opt.id">
                    <td>{{ opt.save_trm }}개월</td>
                    <td>{{ opt.intr_rate_type_nm }}</td>
                    <td>{{ opt.intr_rate }}%</td>
                    <td>{{ opt.intr_rate2 }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="router-links">
            <RouterLink :to="{ name: 'article' }">상품 Q&A</RouterLink>
            <RouterLink :to="{ name: 'stock' }">정보 검색</RouterLink>
            <RouterLink :to="{ name: 'product' }">목록으로</RouterLink>
          </div>
        </div>
      </div>
      <div v-else>
        <p>불러오는 중...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const props = defineProps(['type', 'id'])

const product = ref(null)
const options = ref([])
const isLiked = ref(false)

const accountStore = useAccountStore()
const token = accountStore.token

onMounted(async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/v2/load/${props.type}s/${props.id}/`)
    product.value = res.data

    const optionUrl =
      props.type === 'deposit'
        ? `http://127.0.0.1:8000/api/v2/deposit-product-options/${props.id}/`
        : `http://127.0.0.1:8000/api/v2/saving-product-options/${props.id}/`

    const optionRes = await axios.get(optionUrl)
    options.value = optionRes.data

    const profileRes = await axios.get('http://127.0.0.1:8000/api/v1/profile/my_profile/', {
      headers: { Authorization: `Token ${token}` }
    })

    const likedList =
      props.type === 'deposit'
        ? profileRes.data.liked_deposits
        : profileRes.data.liked_savings

    isLiked.value = likedList.includes(props.id)
  } catch (err) {
    console.error('상세 정보 요청 실패:', err)
  }
})

const toggleLike = async () => {
  const method = isLiked.value ? 'delete' : 'post'
  try {
    await axios({
      method,
      url: `http://127.0.0.1:8000/api/v1/profile/like-${props.type}/${props.id}/`,
      headers: { Authorization: `Token ${token}` }
    })
    isLiked.value = !isLiked.value
  } catch (err) {
    console.error('하트 처리 실패:', err)
    alert('관심상품 처리 중 오류가 발생했습니다.')
  }
}
</script>

<style scoped>
.wrapper {
  padding: 32px 24px;
  max-width: 1200px;
  margin: 0 auto;
  height: 100vh;
  background-color: #dbdadad0;
  padding: 120px 0;
}

.page-title {
  max-width: 960px;
  margin: 0 auto 24px;
  padding-left: 12px;
  font-size: 28px;
  font-weight: 700;
  color: black;
  border-left: 5px solid #38b2ac;
}

.product-wrapper {
  max-width: 960px;
  margin: 0 auto;
  padding: 40px 24px;
  background-color: #ffffff;
  font-family: 'Noto Sans KR', sans-serif;
  color: #1f2937;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.product-card {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.name-box h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 6px;
}

.bank-name {
  font-size: 15px;
  color: #6b7280;
}

.rate-box {
  text-align: right;
}

.rate-label {
  font-size: 14px;
  color: #6b7280;
}

.rate-value {
  font-size: 32px;
  font-weight: bold;
  color: #dc2626;
}

.like-box-inline {
  margin-top: 10px;
  text-align: right;
}

.like-button {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.like-button:hover {
  background-color: #1e40af;
}

.info-list {
  list-style: none;
  padding: 0;
  font-size: 15px;
  line-height: 1.8;
  color: #374151;
  border-top: 1px solid #e5e7eb;
  padding-top: 20px;
}

.info-list li {
  margin-bottom: 10px;
}

.option-section {
  margin-top: 16px;
}

.option-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

.table-wrapper {
  overflow-x: auto;
}

.option-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  font-size: 14px;
}

.option-table th,
.option-table td {
  border: 1px solid #d6d7d8;
  padding: 12px;
  white-space: nowrap;
}

.option-table th {
  background-color: #f9fafb;
  color: #1f2937;
  font-weight: 600;
}

.router-links {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 24px;
}

.router-links a {
  flex: 1;
  text-align: center;
  background-color: #e0e7ff;
  color: #1e3a8a;
  padding: 10px 16px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  border: 1px solid #c7d2fe;
  transition: background-color 0.2s;
}

.router-links a:hover {
  background-color: #c7d2fe;
}
</style>
