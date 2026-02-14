<template>
  <div class="level">
    <h1>等级管理</h1>
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadCharactersLevel" class="retry-btn">重试</button>
    </div>
    <div v-else class="level-content">
      <h2>角色等级信息</h2>
      <div v-if="characters.length === 0" class="no-characters">
        <p>您还没有创建角色，快来创建角色吧！</p>
        <router-link to="/character" class="create-link">创建角色</router-link>
      </div>
      <div v-else class="characters-level">
        <div v-for="character in characters" :key="character.character_id" class="character-level-card">
          <h3>{{ character.name }}</h3>
          <div class="level-info">
            <p>等级: {{ character.level }}</p>
            <p>经验值: {{ character.exp }}/{{ character.next_level_exp }}</p>
            <div class="exp-bar">
              <div class="exp-fill" :style="{ width: `${character.exp_percentage}%` }"></div>
            </div>
            <p class="exp-percentage">{{ Math.round(character.exp_percentage) }}%</p>
          </div>
          
          <!-- 属性信息 -->
          <div class="character-attributes">
            <h4>角色属性</h4>
            <div class="attributes-grid">
              <div class="attribute-item">
                <span class="attribute-label">力量</span>
                <span class="attribute-value">{{ character.strength || 0 }}</span>
              </div>
              <div class="attribute-item">
                <span class="attribute-label">敏捷</span>
                <span class="attribute-value">{{ character.agility || 0 }}</span>
              </div>
              <div class="attribute-item">
                <span class="attribute-label">智力</span>
                <span class="attribute-value">{{ character.intelligence || 0 }}</span>
              </div>
              <div class="attribute-item">
                <span class="attribute-label">体力</span>
                <span class="attribute-value">{{ character.vitality || 0 }}</span>
              </div>
              <div class="attribute-item">
                <span class="attribute-label">生命值</span>
                <span class="attribute-value">{{ character.hp || 0 }}</span>
              </div>
              <div class="attribute-item">
                <span class="attribute-label">魔法值</span>
                <span class="attribute-value">{{ character.mp || 0 }}</span>
              </div>
              <div class="attribute-item">
                <span class="attribute-label">攻击力</span>
                <span class="attribute-value">{{ character.attack || 0 }}</span>
              </div>
              <div class="attribute-item">
                <span class="attribute-label">防御力</span>
                <span class="attribute-value">{{ character.defense || 0 }}</span>
              </div>
            </div>
          </div>
          
          <div class="level-actions">
            <button @click="testGainExp(character.character_id, 500)" class="gain-exp-btn">获取500经验</button>
            <button @click="testGainExp(character.character_id, 1000)" class="gain-exp-btn">获取1000经验</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCharactersLevel, gainExp } from '../api/user'

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const characters = ref([])

onMounted(() => {
  loadCharactersLevel()
})

const loadCharactersLevel = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await getCharactersLevel()
    characters.value = response.characters
  } catch (err) {
    error.value = '获取角色等级信息失败: ' + err.message
    console.error('获取角色等级信息失败:', err)
  } finally {
    loading.value = false
  }
}

const testGainExp = async (characterId, exp) => {
  loading.value = true
  error.value = null
  try {
    await gainExp(characterId, exp)
    alert(`成功获取 ${exp} 经验值！`)
    // 重新加载等级信息
    await loadCharactersLevel()
  } catch (err) {
    error.value = '获取经验值失败: ' + err.message
    console.error('获取经验值失败:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.level {
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
.error,
.no-characters {
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

.no-characters {
  background-color: #f5f5f5;
}

.create-link {
  display: inline-block;
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.create-link:hover {
  background-color: #45a049;
}

.characters-level {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.character-level-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: left;
}

.character-level-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #2196F3;
  text-align: center;
}

.level-info {
  margin-bottom: 20px;
}

.level-info p {
  margin: 5px 0;
}

.exp-bar {
  width: 100%;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  margin: 10px 0;
}

.exp-fill {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.5s ease;
  border-radius: 10px;
}

.exp-percentage {
  text-align: right;
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.character-attributes {
  margin: 20px 0;
}

.character-attributes h4 {
  margin: 0 0 10px 0;
  color: #555;
  font-size: 14px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

.attributes-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.attribute-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-size: 13px;
}

.attribute-label {
  color: #666;
}

.attribute-value {
  font-weight: bold;
  color: #333;
}

.level-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.gain-exp-btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #ff9800;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.gain-exp-btn:hover {
  background-color: #e68a00;
}
</style>