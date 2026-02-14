<template>
  <div class="register">
    <h1>注册</h1>
    <el-form :model="form" @submit.prevent="handleRegister" label-width="80px">
      <el-form-item label="用户名" required>
        <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" required>
        <el-input v-model="form.email" type="email" placeholder="请输入邮箱"></el-input>
      </el-form-item>
      <el-form-item label="密码" required>
        <el-input v-model="form.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" required>
        <el-input v-model="form.confirmPassword" type="password" placeholder="请确认密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">注册</el-button>
      </el-form-item>
    </el-form>
    <p>已有账号？<router-link to="/login">立即登录</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../api/user'

const router = useRouter()
const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  try {
    // 验证密码是否一致
    if (form.value.password !== form.value.confirmPassword) {
      alert('两次输入的密码不一致，请重新输入')
      return
    }
    
    // 调用注册API
    await register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
    })
    
    // 注册成功后跳转到登录页面
    alert('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    console.error('注册失败:', error)
    alert('注册失败，请检查输入信息')
  }
}
</script>

<style scoped>
.register {
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

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
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