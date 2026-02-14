<template>
  <div class="task">
    <h1>任务系统</h1>
    <div class="task-tabs">
      <button @click="activeTab = 'available'" :class="{ active: activeTab === 'available' }">可接任务</button>
      <button @click="activeTab = 'inProgress'" :class="{ active: activeTab === 'inProgress' }">进行中</button>
      <button @click="activeTab = 'completed'" :class="{ active: activeTab === 'completed' }">已完成</button>
    </div>
    
    <!-- 可接任务 -->
    <div v-if="activeTab === 'available'" class="task-list">
      <h2>可接任务</h2>
      <div v-if="availableTasks.length === 0" class="no-tasks">
        <p>当前没有可接任务</p>
      </div>
      <div v-else class="tasks-grid">
        <div v-for="task in availableTasks" :key="task.id" class="task-card available">
          <h3>{{ task.title }}</h3>
          <p class="task-description">{{ task.description }}</p>
          <div class="task-details">
            <p>难度: {{ task.difficulty }}</p>
            <p>奖励经验: {{ task.rewardExp }}</p>
            <p>奖励金币: {{ task.rewardGold }}</p>
          </div>
          <button @click="acceptTask(task)" class="accept-btn">接取任务</button>
        </div>
      </div>
    </div>
    
    <!-- 进行中任务 -->
    <div v-if="activeTab === 'inProgress'" class="task-list">
      <h2>进行中任务</h2>
      <div v-if="inProgressTasks.length === 0" class="no-tasks">
        <p>当前没有进行中的任务</p>
      </div>
      <div v-else class="tasks-grid">
        <div v-for="task in inProgressTasks" :key="task.id" class="task-card in-progress">
          <h3>{{ task.title }}</h3>
          <p class="task-description">{{ task.description }}</p>
          <div class="task-details">
            <p>难度: {{ task.difficulty }}</p>
            <p>奖励经验: {{ task.rewardExp }}</p>
            <p>奖励金币: {{ task.rewardGold }}</p>
            <p>进度: {{ task.progress }}%</p>
          </div>
          <div class="task-actions">
            <button @click="updateTaskProgress(task)" class="progress-btn">更新进度</button>
            <button @click="completeTask(task)" class="complete-btn">完成任务</button>
            <button @click="abandonTask(task.id)" class="abandon-btn">放弃任务</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 已完成任务 -->
    <div v-if="activeTab === 'completed'" class="task-list">
      <h2>已完成任务</h2>
      <div v-if="completedTasks.length === 0" class="no-tasks">
        <p>当前没有已完成的任务</p>
      </div>
      <div v-else class="tasks-grid">
        <div v-for="task in completedTasks" :key="task.id" class="task-card completed">
          <h3>{{ task.title }}</h3>
          <p class="task-description">{{ task.description }}</p>
          <div class="task-details">
            <p>难度: {{ task.difficulty }}</p>
            <p>奖励经验: {{ task.rewardExp }}</p>
            <p>奖励金币: {{ task.rewardGold }}</p>
            <p>完成时间: {{ task.completedAt }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const activeTab = ref('available')

// 模拟任务数据
const tasks = ref([
  {
    id: 1,
    title: '新手引导',
    description: '完成游戏的新手引导任务，了解基本操作',
    difficulty: '简单',
    rewardExp: 100,
    rewardGold: 50,
    status: 'available',
    progress: 0
  },
  {
    id: 2,
    title: '击败怪物',
    description: '击败10只小怪，提升战斗经验',
    difficulty: '简单',
    rewardExp: 150,
    rewardGold: 80,
    status: 'available',
    progress: 0
  },
  {
    id: 3,
    title: '收集物品',
    description: '收集5个铁矿石和3个木材',
    difficulty: '中等',
    rewardExp: 200,
    rewardGold: 120,
    status: 'available',
    progress: 0
  }
])

const availableTasks = computed(() => {
  return tasks.value.filter(task => task.status === 'available')
})

const inProgressTasks = computed(() => {
  return tasks.value.filter(task => task.status === 'inProgress')
})

const completedTasks = computed(() => {
  return tasks.value.filter(task => task.status === 'completed')
})

const acceptTask = (task) => {
  task.status = 'inProgress'
  task.progress = 0
  alert(`已接取任务: ${task.title}`)
}

const updateTaskProgress = (task) => {
  if (task.progress < 100) {
    task.progress = Math.min(100, task.progress + 25)
    alert(`任务进度更新: ${task.title} - ${task.progress}%`)
  }
}

const completeTask = (task) => {
  task.status = 'completed'
  task.progress = 100
  task.completedAt = new Date().toLocaleString()
  alert(`任务完成: ${task.title}\n获得奖励: ${task.rewardExp}经验, ${task.rewardGold}金币`)
}

const abandonTask = (taskId) => {
  if (confirm('确定要放弃这个任务吗？')) {
    const task = tasks.value.find(t => t.id === taskId)
    if (task) {
      task.status = 'available'
      task.progress = 0
      alert('任务已放弃')
    }
  }
}

onMounted(() => {
  // 初始化任务数据
  console.log('任务系统初始化完成')
})
</script>

<style scoped>
.task {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 30px;
}

.task-tabs {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.task-tabs button {
  padding: 10px 30px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  background-color: #f0f0f0;
  transition: all 0.3s ease;
}

.task-tabs button.active {
  background-color: #4CAF50;
  color: white;
}

.task-tabs button:hover:not(.active) {
  background-color: #e0e0e0;
}

.task-list {
  margin-bottom: 40px;
}

.task-list h2 {
  margin-bottom: 20px;
  color: #4CAF50;
}

.no-tasks {
  background-color: #f5f5f5;
  padding: 40px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.no-tasks p {
  font-size: 1.2em;
  margin: 0;
}

.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.task-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: left;
}

.task-card.available {
  border-left: 4px solid #2196F3;
}

.task-card.in-progress {
  border-left: 4px solid #ff9800;
}

.task-card.completed {
  border-left: 4px solid #4CAF50;
  opacity: 0.8;
}

.task-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #2196F3;
}

.task-description {
  margin-bottom: 15px;
  font-size: 14px;
  line-height: 1.4;
}

.task-details {
  margin-bottom: 20px;
  font-size: 14px;
}

.task-details p {
  margin: 5px 0;
}

.task-actions {
  display: flex;
  gap: 10px;
}

.accept-btn,
.progress-btn,
.complete-btn,
.abandon-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.accept-btn {
  background-color: #4CAF50;
  color: white;
}

.accept-btn:hover {
  background-color: #45a049;
}

.progress-btn {
  background-color: #2196F3;
  color: white;
}

.progress-btn:hover {
  background-color: #0b7dda;
}

.complete-btn {
  background-color: #4CAF50;
  color: white;
}

.complete-btn:hover {
  background-color: #45a049;
}

.abandon-btn {
  background-color: #f44336;
  color: white;
}

.abandon-btn:hover {
  background-color: #da190b;
}
</style>