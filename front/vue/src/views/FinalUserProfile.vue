<template>
  <div class="wrapper">
    <div class="profile-header">
      <h1>
        내 프로필
        <RouterLink :to="{ name: 'userprofile_edit' }" class="edit-btn">수정</RouterLink>
      </h1>
    </div>

    <div v-if="profile">
      <p class="userinfo"><strong>아이디:</strong> {{ profile.user }}</p>
      <p class="userinfo"><strong>닉네임:</strong> {{ profile.nickname }}</p>
      <p class="userinfo"><strong>이메일:</strong> {{ profile.email }}</p>
      <p class="userinfo"><strong>생년월일:</strong> {{ profile.birthdate }}</p>
      
      <p class="userinfo"><strong>자산:</strong> {{ profile.asset }}</p>
      <p class="userinfo"><strong>월급:</strong> {{ profile.salary }}</p>
    </div>
    <div v-else>
      <p>불러오는 중입니다...</p>
    </div>

    <hr>
    <h1 class="cart">내 관심 상품</h1>

    <section class="product-section">
      <h3>예금</h3>
      <div v-if="likedDepositProducts.length">
        <div
          v-for="item in likedDepositProducts"
          :key="item.fin_prdt_cd"
          class="product-line"
        >
          <span @click.prevent="goToDetail(item.fin_prdt_cd, 'deposit')">
            {{ item.fin_prdt_nm }} - {{ item.kor_co_nm }}
          </span>
          <button @click="toggleLike(item.fin_prdt_cd, 'deposit')">
            {{ profile.liked_deposits.includes(item.fin_prdt_cd) ? '🐾' : '🍚' }}
          </button>
        </div>
      </div>
      <p v-else>관심 등록한 예금 상품이 없습니다.</p>

      <div class="chart-wrapper">
        <canvas ref="depositChartRef"></canvas>
      </div>

      <h3 style="margin-top: 40px">적금</h3>
      <div v-if="likedSavingProducts.length">
        <div
          v-for="item in likedSavingProducts"
          :key="item.fin_prdt_cd"
          class="product-line"
        >
          <span @click.prevent="goToDetail(item.fin_prdt_cd, 'saving')">
            {{ item.fin_prdt_nm }} - {{ item.kor_co_nm }}
          </span>
          <button @click="toggleLike(item.fin_prdt_cd, 'saving')">
            {{ profile.liked_savings.includes(item.fin_prdt_cd) ? '🐾' : '🍚' }}
          </button>
        </div>
      </div>
      <p v-else>관심 등록한 적금 상품이 없습니다.</p>

      <div class="chart-wrapper">
        <canvas ref="savingChartRef"></canvas>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'
import { Chart, BarElement, CategoryScale, LinearScale } from 'chart.js'

Chart.register(BarElement, CategoryScale, LinearScale)

const router = useRouter()
const accountStore = useAccountStore()
const token = accountStore.token

const profile = ref(null)
const deposits = ref([])
const savings = ref([])

const depositChartRef = ref(null)
const savingChartRef = ref(null)
let depositChartInstance = null
let savingChartInstance = null

onMounted(function () {
  axios.get('http://127.0.0.1:8000/api/v1/profile/my_profile/', {
    headers: { Authorization: 'Token ' + token }
  }).then(function (res1) {
    profile.value = res1.data

    axios.get('http://127.0.0.1:8000/api/v2/load/deposits/')
    .then(function (res2) {
      deposits.value = res2.data

      axios.get('http://127.0.0.1:8000/api/v2/load/savings/')
      .then(function (res3) {
        savings.value = res3.data

        drawDepositChart()
        drawSavingChart()
      })
    })
  }).catch(function (err) {
    console.log('불러오기 실패:', err)
    alert('정보를 불러오는 데 실패했습니다.')
  })
})

const likedDepositProducts = computed(function () {
  const result = []
  if (profile.value && deposits.value.length > 0) {
    for (let i = 0; i < profile.value.liked_deposits.length; i++) {
      const code = profile.value.liked_deposits[i]
      for (let j = 0; j < deposits.value.length; j++) {
        if (deposits.value[j].fin_prdt_cd === code) {
          result.push(deposits.value[j])
          break
        }
      }
    }
  }
  return result
})

const likedSavingProducts = computed(function () {
  const result = []
  if (profile.value && savings.value.length > 0) {
    for (let i = 0; i < profile.value.liked_savings.length; i++) {
      const code = profile.value.liked_savings[i]
      for (let j = 0; j < savings.value.length; j++) {
        if (savings.value[j].fin_prdt_cd === code) {
          result.push(savings.value[j])
          break
        }
      }
    }
  }
  return result
})

function toggleLike(productCode, type) {
  const isDeposit = (type === 'deposit')
  const list = isDeposit ? profile.value.liked_deposits : profile.value.liked_savings

  let alreadyLiked = false
  for (let i = 0; i < list.length; i++) {
    if (list[i] === productCode) {
      alreadyLiked = true
      break
    }
  }

  const method = alreadyLiked ? 'delete' : 'post'

  axios({
    method: method,
    url: 'http://127.0.0.1:8000/api/v1/profile/like-' + type + '/' + productCode + '/',
    headers: { Authorization: 'Token ' + token }
  }).then(function () {
    if (alreadyLiked) {
      const newList = []
      for (let i = 0; i < list.length; i++) {
        if (list[i] !== productCode) {
          newList.push(list[i])
        }
      }
      if (isDeposit) {
        profile.value.liked_deposits = newList
      } else {
        profile.value.liked_savings = newList
      }
    } else {
      list.push(productCode)
    }

    if (isDeposit) {
      drawDepositChart()
    } else {
      drawSavingChart()
    }
  }).catch(function (err) {
    console.log('하트 처리 실패:', err)
    alert('관심상품 처리 중 오류가 발생했습니다.')
  })
}

function goToDetail(productCode, type) {
  router.push({ name: 'detailproduct', params: { type: type, id: productCode } })
}

function drawDepositChart() {
  if (!depositChartRef.value) return
  if (depositChartInstance) depositChartInstance.destroy()

  const labels = []
  const data = []
  const list = likedDepositProducts.value
  for (let i = 0; i < list.length; i++) {
    labels.push(list[i].fin_prdt_nm)
    data.push(list[i].highest_rate || 0)
  }

  depositChartInstance = new Chart(depositChartRef.value, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '예금 최고 금리(%)',
        data: data,
        backgroundColor: 'rgba(30, 64, 175, 0.5)',  
        borderColor: '#1e3a8a',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 2,
            callback: function(value) {
              return value.toFixed(2) + '%'
            }
          }
        }
      }
    }
  })
}

function drawSavingChart() {
  if (!savingChartRef.value) return
  if (savingChartInstance) savingChartInstance.destroy()

  const labels = []
  const data = []
  const list = likedSavingProducts.value
  for (let i = 0; i < list.length; i++) {
    labels.push(list[i].fin_prdt_nm)
    data.push(list[i].highest_rate || 0)
  }

  savingChartInstance = new Chart(savingChartRef.value, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '적금 최고 금리(%)',
        data: data,
        backgroundColor: 'rgba(30, 64, 175, 0.7)', // blue-700
        borderColor: '#1E40AF',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 2,
            callback: function(value) {
              return value.toFixed(2) + '%'
            }
          }
        }
      }
    }
  })
}

watch(likedDepositProducts, function () {
  drawDepositChart()
})

watch(likedSavingProducts, function () {
  drawSavingChart()
})
</script>

<style scoped>
.wrapper {
  max-width: 1000px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
  padding: 40px 24px;
  background-color: #d8d8d8a8;
  min-height: 100vh;
  color: #1f2937; 
  font-size: 16px;
  line-height: 1.6;
}

.profile-header h1 {
  display: inline-flex;
  align-items: center;
  font-size: 28px;
  color: #1e293b; 
  gap: 12px;
  margin-bottom: 32px;
}

.edit-btn {
  font-size: 14px;
  color: #6b7280; 
  background-color: transparent;
  border: 1px solid #d1d5db; 
  padding: 4px 10px;
  border-radius: 6px;
  text-decoration: none;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.edit-btn:hover {
  background-color: #e2e8f0; 
  color: #374151; 
}

.userinfo {
  font-size: 17px;
  margin-bottom: 8px;
}

h1 {
  font-size: 28px;
  margin-bottom: 32px;
  color: #1e293b;
}

h3 {
  margin-top: 32px;
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

hr {
  margin: 40px 0;
  border: 0;
  border-top: 1px solid #0000005e;
}

.cart {
  margin-bottom: 40px;
}

.product-section {
  margin-bottom: 40px;
}

.product-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #ced0d3;
  font-size: 15px;
}

.product-line span {
  color: #334155; 
  cursor: pointer;
}

.product-line span:hover {
  text-decoration: underline;
}

button {
  background-color: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.chart-wrapper {
  background-color: #ffffff;
  border: 1px solid #cbd5e1; 
  border-radius: 10px;
  padding: 24px;
  margin: 24px 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

canvas {
  width: 100% !important;
  height: 280px !important; 
}
</style>
