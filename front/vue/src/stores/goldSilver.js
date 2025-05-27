// stores/goldSilver.js

import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useGoldSilverStore = defineStore('goldSilver', () => {
  const goldPrices = ref([])
  const silverPrices = ref([])
  const labels = ref([])

  const API_URL = 'http://127.0.0.1:8000'

  const getGoldAndSilverPrices = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v4/gold_prices/`
    }).then(res1 => {
      goldPrices.value = res1.data.map(item => item.close)
      labels.value = res1.data.map(item => item.date)

      axios({
        method: 'get',
        url: `${API_URL}/api/v4/silver_prices`
      }).then(res2 => {
        silverPrices.value = res2.data.map(item => item.close)
      }).catch(err => console.log('은 가격 오류:', err))
    }).catch(err => console.log('금 가격 오류:', err))
  }

  return {
    goldPrices,
    silverPrices,
    labels,
    API_URL,
    getGoldAndSilverPrices
  }
}, { persist: true })
