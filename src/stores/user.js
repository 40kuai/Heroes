import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: null,
    loading: false,
    error: null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    getUser: (state) => state.user
  },
  actions: {
    setUser(user) {
      this.user = user
    },
    setToken(token) {
      this.token = token
      // 将token存储到localStorage
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    setLoading(loading) {
      this.loading = loading
    },
    setError(error) {
      this.error = error
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    },
    // 初始化时从localStorage加载token
    initialize() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        // 这里可以添加验证token的逻辑
      }
    }
  }
})