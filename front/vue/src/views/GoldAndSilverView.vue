<template>
  <div class="content-wrapper">
    <nav class="banner-img-box ">
      <img src="../assets/gold_silver_banner.png" alt="#">
    </nav>

    <h1 class="price">{{ title }} 시세</h1>

    <div class="tab">
      <button @click="type = 'gold'" :class="{ active: type === 'gold' }">금</button>
      <button @click="type = 'silver'" :class="{ active: type === 'silver' }">은</button>
    </div>

    <div class="date-picker">
      <label>시작일</label>
      <input type="date" v-model="startDate" />
      <label>종료일</label>
      <input type="date" v-model="endDate" />
    </div>

    <div v-if="chartDataAvailable" class="chart-container">
      <Line :data="chart" :options="option" />
    </div>
    <div v-else>
      <p>선택된 조건에 해당하는 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useGoldSilverStore } from '@/stores/goldSilver'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const store = useGoldSilverStore()
store.getGoldAndSilverPrices()

const type = ref('gold')
const startDate = ref('2023-01-01')
const endDate = ref('2023-06-30')

function formatDate(dateStr) {
  return dateStr.slice(0, 10)
}

const title = computed(function () {
  return type.value === 'gold' ? '금' : '은'
})

const chartDataAvailable = computed(function () {
  for (let i = 0; i < store.labels.length; i++) {
    const d = store.labels[i]
    if (d >= startDate.value && d <= endDate.value) {
      return true
    }
  }
  return false
})

const chart = computed(function () {
  const x = []
  const y = []

  for (let i = 0; i < store.labels.length; i++) {
    const d = store.labels[i]
    if (d >= startDate.value && d <= endDate.value) {
      x.push(formatDate(d))
      if (type.value === 'gold') {
        y.push(store.goldPrices[i])
      } else {
        y.push(store.silverPrices[i])
      }
    }
  }

  return {
    labels: x,
    datasets: [
      {
        label: title.value + ' 시세',
        data: y,
        borderWidth: 2,
        borderColor: type.value === 'gold' ? '#f1c40f' : '#95a5a6',
        tension: 0.3
      }
    ]
  }
})

const option = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      title: {
        display: true,
        text: '날짜'
      }
    },
    y: {
      title: {
        display: true,
        text: '가격 (USD)'
      }
    }
  }
}
</script>

<style scoped>
.content-wrapper {
  max-width: 1200px;  
  margin: 0 auto;
  padding: 10px 10px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  box-sizing: border-box;
  background-color: #dfdfdfd0;
  height: 100vh;
}

.banner-img-box {
  width: 100%;
  overflow: hidden;
  position: relative;
  max-height: 400px;
}

.banner-img-box img {
  width: 100%;
  height: 100%;
  object-fit: cover; 
  display: block;
  margin: 0 auto;
}

.chart-container {
  background: white;
  padding: 0.1px;
  width: 100%;
  position: relative;
  box-sizing: border-box;
}

.price {
  font-size: 30px;
  font-weight: 700;
  color: #1f2937;
  padding-left: 12px;
  border-left: 5px solid #38b2ac;
  margin-top: 35px;
  margin-bottom: 26px;
  font-family: 'WooridaumB', sans-serif;
}

.tab {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.tab button {
  padding: 10px 20px;
  font-size: 16px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.tab button:hover {
  background: #f0f0f0;
}

.tab button.active {
  background: #333;
  color: white;
  border-color: #333;
}

.date-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 20px;
  align-items: center;
}

.date-picker label {
  font-size: 15px;
  font-weight: 500;
}

.date-picker input {
  padding: 8px 12px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: white;
  box-sizing: border-box;
}

canvas {
  width: 100% !important;
  height: auto !important;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 40px 20px;
  }

  h1 {
    font-size: 24px;
    margin-bottom: 28px;
  }

  .tab button {
    font-size: 14px;
    padding: 8px 14px;
  }

  .chart-container {
    padding: 20px;
    height: 400px;
  }

  .date-picker {
    flex-direction: column;
    align-items: flex-start;
  }

  .date-picker input {
    width: 100%;
  }
}
</style>