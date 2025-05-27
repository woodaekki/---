<template>
  <div class="map-search-container">
    <!-- 시도 선택 -->
    <div class="form-group">
      <label>시도:</label>
      <select v-model="sido">
        <option value="">선택하세요</option>
        <option v-for="(districts, city) in provinceData" :key="city" :value="city">
          {{ city }}
        </option>
      </select>
    </div>

    <!-- 군구 선택 -->
    <div class="form-group">
      <label>군구:</label>
      <select v-model="gungu">
        <option value="">선택하세요</option>
        <option v-if="sido" v-for="area in provinceData[sido]" :key="area" :value="area">
          {{ area }}
        </option>
      </select>
    </div>

    <!-- 은행 선택 -->
    <div class="form-group" v-if="searchType === 'bank'">
      <label>은행:</label>
      <select v-model="bank">
        <option value="">선택하세요</option>
        <option v-for="b in bankList" :key="b" :value="b">
          {{ b }}
        </option>
      </select>
    </div>

    <!-- 은행/ATM 선택 라디오 -->
    <div class="form-group radio-group">
      <label><input type="radio" value="bank" v-model="searchType" /> 은행</label>
      <label><input type="radio" value="atm" v-model="searchType" /> ATM</label>
    </div>

    <!-- 검색 버튼 -->
    <div class="form-group">
      <button @click="submitSearch">검색하기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'

const emit = defineEmits([
  'update-sido',
  'update-gungu',
  'update-bank',
  'update-search-type',
  'trigger-search'
])

const sido = ref('')
const gungu = ref('')
const bank = ref('')
const searchType = ref('bank')
const provinceData = ref({})
const bankList = ref([])

watch(searchType, val => emit('update-search-type', val))
watch(sido, val => {
  gungu.value = ''
  emit('update-sido', val)
})
watch(gungu, val => emit('update-gungu', val))
watch(bank, val => emit('update-bank', val))

function submitSearch() {
  emit('trigger-search')
}

onMounted(async () => {
  try {
    const [provinceRes, bankRes] = await Promise.all([
      axios.get('/districts_by_province.json'),
      axios.get('/banks_info.json')
    ])
    provinceData.value = provinceRes.data
    bankList.value = bankRes.data.offlineBanks || bankRes.data
  } catch (err) {
    console.error('데이터 로드 실패:', err)
  }
})
</script>

<style scoped>
.map-search-container {
  background: #fff;
  padding: 24px;
  border: 1px solid #dcdfe3;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 400px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.radio-group {
  flex-direction: row;
  gap: 16px;
  align-items: center;
}

.map-search-container label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.map-search-container select,
.map-search-container button {
  padding: 10px 12px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #c2c7cc;
  background-color: #ffffff;
  transition: 0.2s ease;
  box-shadow: none;
}

.map-search-container select:focus {
  border-color: #3b82f6;
  outline: none;
}

.map-search-container button {
  background-color: #2563eb;
  color: white;
  font-weight: 600;
  border: none;
  cursor: pointer;
  align-self: flex-start;
}

.map-search-container button:hover {
  background-color: #1d4ed8;
}
</style>
