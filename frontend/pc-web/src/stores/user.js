import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = '/v1/pc'

export const useUserStore = defineStore('user', {
  state: () => ({
    isLoggedIn: false,
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
    token: localStorage.getItem('token') || '',
    refreshToken: localStorage.getItem('refreshToken') || ''
  }),
  
  getters: {
    userInfoData: (state) => state.userInfo,
    getToken: (state) => state.token
  },
  
  actions: {
    // 登录
    async login(phone, password) {
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/login`, {
          phone,
          password,
          platformType: 'pc'
        })
        
        if (response.data.code === 0) {
          const { token, refreshToken, userInfo } = response.data.data
          this.token = token
          this.refreshToken = refreshToken
          this.userInfo = userInfo
          this.isLoggedIn = true
          
          // 存储到本地
          localStorage.setItem('token', token)
          localStorage.setItem('refreshToken', refreshToken)
          localStorage.setItem('userInfo', JSON.stringify(userInfo))
          
          // 设置请求头
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
          
          return true
        }
        return false
      } catch (error) {
        console.error('登录失败:', error)
        return false
      }
    },
    
    // 注册
    async register(phone, password, code) {
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/register`, {
          phone,
          password,
          code,
          platformType: 'pc'
        })
        
        return response.data.code === 0
      } catch (error) {
        console.error('注册失败:', error)
        return false
      }
    },
    
    // 退出登录
    logout() {
      this.token = ''
      this.refreshToken = ''
      this.userInfo = {}
      this.isLoggedIn = false
      
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('userInfo')
      
      delete axios.defaults.headers.common['Authorization']
    },
    
    // 刷新token
    async refreshToken() {
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refreshToken: this.refreshToken,
          platformType: 'pc'
        })
        
        if (response.data.code === 0) {
          const { token, refreshToken } = response.data.data
          this.token = token
          this.refreshToken = refreshToken
          
          localStorage.setItem('token', token)
          localStorage.setItem('refreshToken', refreshToken)
          
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
          
          return true
        }
        return false
      } catch (error) {
        console.error('刷新token失败:', error)
        this.logout()
        return false
      }
    },
    
    // 获取用户信息
    async getUserInfo() {
      try {
        const response = await axios.get(`${API_BASE_URL}/user/info`)
        
        if (response.data.code === 0) {
          this.userInfo = response.data.data
          localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
          return this.userInfo
        }
        return null
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return null
      }
    },
    
    // 初始化登录状态
    initLoginState() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        this.isLoggedIn = true
        this.getUserInfo()
      }
    },
    
    // 设置用户信息（用于模拟登录）
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      this.isLoggedIn = true
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    
    // 设置token（用于模拟登录）
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },
    
    // 设置refreshToken
    setRefreshToken(refreshToken) {
      this.refreshToken = refreshToken
      localStorage.setItem('refreshToken', refreshToken)
    }
  }
})