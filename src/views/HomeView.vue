<template>
  <div class="home">
    <h1>首页</h1>
    <p>欢迎来到角色扮演游戏的首页！</p>
    <router-link to="/login">登录</router-link>
    <br>
    <router-link to="/register">注册</router-link>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
  margin-bottom: 30px;
}

router-link {
  display: inline-block;
  margin: 10px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

router-link:hover {
  background-color: #45a049;
}
</style>