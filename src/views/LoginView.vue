<template>
  <div class="login">
    <h1>登录</h1>
    <el-form :model="form" @submit.prevent="handleLogin" label-width="80px">
      <el-form-item label="用户名" required>
        <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item label="密码" required>
        <el-input v-model="form.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">登录</el-button>
      </el-form-item>
    </el-form>
    <p>还没有账号？<router-link to="/register">立即注册</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { login } from '../api/user'

const router = useRouter()
const userStore = useUserStore()
const form = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  try {
    // 调用登录API
    const response = await login(form.value.username, form.value.password)
    // 存储token和用户信息
    userStore.setToken(response.access_token)
    userStore.setUser({
      id: 1, // 这里应该从API响应中获取
      username: form.value.username,
      email: '' // 这里应该从API响应中获取
    })
    // 登录成功后跳转到游戏页面
    router.push('/game')
  } catch (error) {
    console.error('登录失败:', error)
    alert('登录失败，请检查用户名和密码')
  }
}
</script>

<style scoped>
.login {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 30px;
}

p {
  margin-top: 20px;
}

router-link {
  color: #4CAF50;
  text-decoration: none;
}

router-link:hover {
  text-decoration: underline;
}
</style>