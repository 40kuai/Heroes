<template>
  <div class="ranking">
    <h1>排行榜</h1>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <!-- 错误信息 -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadRanking" class="retry-btn">重试</button>
    </div>
    
    <div v-else>
      <!-- 排行榜类型选择 -->
      <div class="ranking-tabs">
        <button 
          v-for="tab in rankingTabs" 
          :key="tab.value"
          :class="['tab-btn', { active: activeTab === tab.value }]"
          @click="activeTab = tab.value; loadRanking()"
        >
          {{ tab.label }}
        </button>
      </div>
      
      <!-- 个人排名 -->
      <div v-if="personalRank" class="personal-rank">
        <h3>个人排名</h3>
        <p>你的{{ activeTab === 'level' ? '等级' : '战力' }}排名: <span class="rank-number">{{ personalRank }}</span></p>
      </div>
      
      <!-- 排行榜列表 -->
      <div class="ranking-list">
        <h2>{{ activeTab === 'level' ? '等级排行榜' : '战力排行榜' }}</h2>
        <div v-if="ranking.length === 0" class="no-ranking">
          <p>排行榜数据为空，快来提升你的{{ activeTab === 'level' ? '等级' : '战力' }}吧！</p>
        </div>
        <table v-else class="ranking-table">
          <thead>
            <tr>
              <th>排名</th>
              <th>角色名称</th>
              <th>玩家名称</th>
              <th>等级</th>
              <th>战力</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in ranking" :key="item.character_id" :class="{ 'personal-item': item.user_id === currentUserId }">
              <td>{{ item.rank }}</td>
              <td>{{ item.character_name }}</td>
              <td>{{ item.username }}</td>
              <td>{{ item.level }}</td>
              <td>{{ item.power }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getLevelRanking, getPowerRanking } from '../api/user'

const activeTab = ref('level')
const ranking = ref([])
const personalRank = ref(null)
const loading = ref(false)
const error = ref(null)
const currentUserId = ref(null)

const rankingTabs = [
  { label: '等级排行', value: 'level' },
  { label: '战力排行', value: 'power' }
]

onMounted(() => {
  loadRanking()
  // 从本地存储获取当前用户ID
  const userInfo = JSON.parse(localStorage.getItem('userInfo'))
  if (userInfo) {
    currentUserId.value = userInfo.id
  }
})

const loadRanking = async () => {
  loading.value = true
  error.value = null
  try {
    let response
    if (activeTab.value === 'level') {
      response = await getLevelRanking()
    } else {
      response = await getPowerRanking()
    }
    ranking.value = response.ranking
    personalRank.value = response.personal_rank
  } catch (err) {
    error.value = '获取排行榜数据失败: ' + err.message
    console.error('获取排行榜数据失败:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.ranking {
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

h2 {
  font-size: 1.5em;
  margin-bottom: 20px;
  color: #4CAF50;
}

.loading,
.error,
.no-ranking,
.personal-rank {
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

.retry-btn {
  margin-top: 10px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
}

.retry-btn:hover {
  background-color: #45a049;
}

.no-ranking {
  background-color: #f5f5f5;
}

/* 排行榜标签 */
.ranking-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: center;
}

.tab-btn {
  padding: 10px 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f5f5f5;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background-color: #e0e0e0;
}

.tab-btn.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

/* 个人排名 */
.personal-rank {
  background-color: #fff8e1;
  color: #ff6f00;
  font-weight: bold;
  margin-bottom: 30px;
  text-align: left;
}

.rank-number {
  font-size: 1.5em;
  color: #ff6f00;
}

/* 排行榜列表 */
.ranking-list {
  margin-top: 20px;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.ranking-table th,
.ranking-table td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

.ranking-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.ranking-table tr:hover {
  background-color: #f5f5f5;
}

.ranking-table tr.personal-item {
  background-color: #e3f2fd;
  font-weight: bold;
}
</style>
