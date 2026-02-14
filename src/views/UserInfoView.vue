<template>
  <div class="user-info">
    <h1>个人信息管理</h1>
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    <div v-else class="info-content">
      <div class="info-section">
        <h2>基本信息</h2>
        <div class="info-item">
          <label>用户名:</label>
          <span>{{ user.username }}</span>
        </div>
        <div class="info-item">
          <label>邮箱:</label>
          <span>{{ user.email }}</span>
        </div>
      </div>
      
      <div class="update-section">
        <h2>更新信息</h2>
        <form @submit.prevent="handleUpdate" class="update-form">
          <div class="form-group">
            <label>新邮箱:</label>
            <input v-model="form.email" type="email" placeholder="输入新邮箱（可选）">
          </div>
          <div class="form-group">
            <label>新密码:</label>
            <input v-model="form.password" type="password" placeholder="输入新密码（可选）">
          </div>
          <div class="form-group">
            <label>确认新密码:</label>
            <input v-model="form.confirmPassword" type="password" placeholder="确认新密码">
          </div>
          <div class="form-actions">
            <button type="submit" class="update-btn">更新信息</button>
            <button type="button" @click="resetForm" class="reset-btn">重置</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserInfo, updateUserInfo as updateUserInfoApi } from '../api/user'

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const user = ref({})
const form = ref({
  email: '',
  password: '',
  confirmPassword: ''
})

onMounted(() => {
  loadUserInfo()
})

const loadUserInfo = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await getUserInfo()
    user.value = response
  } catch (err) {
    error.value = '获取用户信息失败: ' + err.message
    console.error('获取用户信息失败:', err)
  } finally {
    loading.value = false
  }
}

const handleUpdate = async () => {
  // 验证密码确认
  if (form.value.password && form.value.password !== form.value.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  loading.value = true
  error.value = null
  try {
    // 准备更新数据
    const updateData = {}
    if (form.value.email) {
      updateData.email = form.value.email
    }
    if (form.value.password) {
      updateData.password = form.value.password
    }
    
    // 调用API更新信息
    const response = await updateUserInfoApi(updateData)
    user.value = response
    alert('信息更新成功！')
    resetForm()
  } catch (err) {
    error.value = '更新信息失败: ' + err.message
    console.error('更新信息失败:', err)
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.value = {
    email: '',
    password: '',
    confirmPassword: ''
  }
}
</script>

<style scoped>
.user-info {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 30px;
}

h2 {
  font-size: 1.5em;
  margin-bottom: 20px;
  color: #4CAF50;
}

.loading,
.error {
  padding: 20px;
  margin: 20px 0;
  border-radius: 4px;
}

.loading {
  background-color: #e3f2fd;
  color: #1976d2;
}

.error {
  background-color: #ffebee;
  color: #d32f2f;
}

.info-content {
  background-color: #f9f9f9;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.info-section {
  margin-bottom: 40px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: left;
}

.info-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.info-item label {
  width: 100px;
  font-weight: bold;
  color: #555;
}

.info-item span {
  flex: 1;
  color: #333;
}

.update-section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: left;
}

.update-form {
  max-width: 500px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-actions {
  margin-top: 30px;
  display: flex;
  gap: 15px;
}

.update-btn,
.reset-btn {
  padding: 10px 25px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.update-btn {
  background-color: #4CAF50;
  color: white;
}

.update-btn:hover {
  background-color: #45a049;
}

.reset-btn {
  background-color: #9e9e9e;
  color: white;
}

.reset-btn:hover {
  background-color: #757575;
}
</style>