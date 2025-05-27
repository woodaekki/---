// stores/accounts.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const router = useRouter()
  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'

  const token = ref(localStorage.getItem('token') || '')  
  const username = ref(localStorage.getItem('username') || '')
  const userId = ref(localStorage.getItem('userId') || '')

  const signUp = ({ username, password1, password2 }) => {
    axios.post(`${ACCOUNT_API_URL}/signup/`, {
      username, password1, password2
    })
      .then(() => {
        console.log('성공')
        router.push({ name: 'login' })
      })
      .catch(err => console.log(err.response.data))
  }

const logIn = ({ username: id, password }) => {
  axios.post(`${ACCOUNT_API_URL}/login/`, {
    username: id,
    password
  })
    .then(res => {
      const tokenValue = res.data.key
      localStorage.setItem('token', tokenValue)
      localStorage.setItem('username', id)
      token.value = tokenValue
      username.value = id

      return axios.get(`${ACCOUNT_API_URL}/user/`, {
        headers: {
          Authorization: `Token ${tokenValue}`
        }
      })
    })
    .then(res => {
      userId.value = res.data.pk || res.data.id
      localStorage.setItem('userId', userId.value)
      router.push({ name: 'home' })
    })
    .catch(err => {
      console.error('실패')
    })
}


  const logOut = () => {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')  
    router.push({ name: 'home' })
  }

  const isLogin = computed(() => !!token.value)

  return {
    token,
    username,
    isLogin,
    signUp,
    logIn,
    logOut,
    userId
  }
})
