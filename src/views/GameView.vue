<template>
  <div class="game">
    <h1>游戏页面</h1>
    <p>欢迎来到角色扮演游戏！</p>
    <div class="game-info">
      <h2>玩家信息</h2>
      <p>用户名: {{ user.username }}</p>
      <button @click="handleLogout" class="logout-btn">退出登录</button>
    </div>
    <div class="game-features">
      <h2>游戏功能</h2>
      <div class="feature-grid">
        <router-link to="/user-info" class="feature-card">
          <h3>个人信息</h3>
          <p>查看和更新你的个人信息</p>
        </router-link>
        <router-link to="/character" class="feature-card">
          <h3>角色管理</h3>
          <p>创建、编辑和管理你的游戏角色</p>
        </router-link>
        <router-link to="/task" class="feature-card">
          <h3>任务系统</h3>
          <p>接受任务、完成任务获取奖励</p>
        </router-link>
        <router-link to="/battle" class="feature-card">
          <h3>战斗系统</h3>
          <p>与怪物战斗，提升你的战斗力</p>
        </router-link>
        <router-link to="/ranking" class="feature-card">
          <h3>排行榜</h3>
          <p>查看服务器排行榜，与其他玩家竞争</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user)

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.game {
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
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
  margin-bottom: 30px;
}

.game-info {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.game-info h2 {
  margin-top: 0;
  color: #4CAF50;
}

.logout-btn {
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

.logout-btn:hover {
  background-color: #da190b;
}

.game-features {
  margin-top: 30px;
}

.game-features h2 {
  margin-top: 0;
  color: #2196F3;
  margin-bottom: 20px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.feature-card {
  background-color: #f0f8ff;
  padding: 20px;
  border-radius: 8px;
  text-decoration: none;
  color: #2c3e50;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  background-color: #e3f2fd;
}

.feature-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #2196F3;
}

.feature-card p {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
}
</style>