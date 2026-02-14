<template>
  <div id="app">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-container">
        <router-link to="/" class="navbar-brand">游戏首页</router-link>
        <div class="navbar-menu">
          <router-link to="/user-info" class="navbar-item">个人信息</router-link>
          <router-link to="/character" class="navbar-item">角色管理</router-link>
          <router-link to="/level" class="navbar-item">等级管理</router-link>
          <router-link to="/equipment" class="navbar-item">装备管理</router-link>
          <router-link to="/ranking" class="navbar-item">排行榜</router-link>
          <router-link to="/task" class="navbar-item">任务</router-link>
          <router-link to="/battle" class="navbar-item">战斗</router-link>
          <router-link to="/login" class="navbar-item">登录</router-link>
          <router-link to="/register" class="navbar-item">注册</router-link>
        </div>
      </div>
    </nav>
    
    <!-- 主要内容 -->
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

/* 导航栏样式 */
.navbar {
  background-color: #2c3e50;
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.navbar-brand {
  font-size: 1.5em;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.navbar-menu {
  display: flex;
  gap: 15px;
}

.navbar-item {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.navbar-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* 主要内容样式 */
.main-content {
  margin-top: 80px;
  padding: 20px;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
}
</style>