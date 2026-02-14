import axios from 'axios'
import { useUserStore } from '../stores/user'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://localhost:8000/api', // 后端API地址
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    // 如果有token，添加到请求头
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  error => {
    // 处理请求错误
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 直接返回响应数据
    return response.data
  },
  error => {
    // 处理响应错误
    console.error('响应错误:', error)
    
    // 处理401错误（未授权）
    if (error.response && error.response.status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      // 跳转到登录页
      window.location.href = '/login'
    }
    
    // 提取错误信息
    const errorMessage = error.response?.data?.message || error.message || '未知错误'
    
    return Promise.reject(new Error(errorMessage))
  }
)

export default service