<template>
  <div class="character">
    <h1>角色管理</h1>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <!-- 错误信息 -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadCharacters" class="retry-btn">重试</button>
    </div>
    
    <div v-else>
      <!-- 角色数量限制 -->
      <div class="character-limit">
        <p>角色数量: {{ characterCount }}/{{ characterLimit }}</p>
      </div>
      
      <!-- 无角色时 -->
      <div v-if="characters.length === 0" class="no-characters">
        <p>您还没有创建角色，快来创建第一个角色吧！</p>
        <button @click="showCreateForm = true" class="create-btn" :disabled="characterCount >= characterLimit">创建角色</button>
      </div>
      
      <!-- 角色列表 -->
      <div v-else class="character-list">
        <h2>我的角色</h2>
        <div class="characters-grid">
          <div v-for="character in characters" :key="character.id" class="character-card">
            <h3>{{ character.name }}</h3>
            <p>等级: {{ character.level }}</p>
            <p>职业: {{ character.class_type || character.class }}</p>
            <p>经验值: {{ character.exp }}/{{ character.nextLevelExp || 1000 }}</p>
            
            <!-- 基础属性 -->
            <div class="attributes">
              <h4>基础属性</h4>
              <div class="attribute-row">
                <span>力量: {{ character.strength || 0 }}</span>
                <span>敏捷: {{ character.agility || 0 }}</span>
              </div>
              <div class="attribute-row">
                <span>智力: {{ character.intelligence || 0 }}</span>
                <span>体力: {{ character.vitality || 0 }}</span>
              </div>
            </div>
            
            <!-- 衍生属性 -->
            <div class="derived-attributes">
              <h4>衍生属性</h4>
              <div class="attribute-row">
                <span>生命值: {{ character.hp || 0 }}</span>
                <span>魔法值: {{ character.mp || 0 }}</span>
              </div>
              <div class="attribute-row">
                <span>攻击力: {{ character.attack || 0 }}</span>
                <span>防御力: {{ character.defense || 0 }}</span>
              </div>
            </div>
            
            <div class="character-actions">
              <button @click="selectCharacter(character)" class="select-btn">选择</button>
              <button @click="editCharacter(character)" class="edit-btn">编辑</button>
              <button @click="deleteCharacter(character.id)" class="delete-btn">删除</button>
            </div>
          </div>
        </div>
        <button @click="showCreateForm = true" class="create-btn" :disabled="characterCount >= characterLimit">创建新角色</button>
      </div>
    </div>
    
    <!-- 创建角色表单 -->
    <div v-if="showCreateForm" class="character-form">
      <h2>{{ editingCharacter ? '编辑角色' : '创建角色' }}</h2>
      <form @submit.prevent="saveCharacter">
        <div class="form-group">
          <label>角色名称:</label>
          <input v-model="form.name" type="text" required>
        </div>
        <div class="form-group">
          <label>职业:</label>
          <select v-model="form.class" required>
            <option value="战士">战士</option>
            <option value="法师">法师</option>
            <option value="射手">射手</option>
            <option value="刺客">刺客</option>
          </select>
        </div>
        <div class="form-actions">
          <button type="submit" class="save-btn" :disabled="loading">保存</button>
          <button type="button" @click="cancelForm" class="cancel-btn" :disabled="loading">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCharacterStore } from '../stores/character'
import { getCharacters, createCharacter as createCharacterApi, updateCharacter as updateCharacterApi, deleteCharacter as deleteCharacterApi, getCharacterCount } from '../api/user'

const characterStore = useCharacterStore()
const showCreateForm = ref(false)
const editingCharacter = ref(null)
const form = ref({
  name: '',
  class: '战士'
})
const characters = ref([])
const loading = ref(false)
const error = ref(null)
const characterCount = ref(0)
const characterLimit = ref(3)

onMounted(() => {
  loadCharacters()
  checkCharacterCount()
})

const loadCharacters = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await getCharacters()
    characters.value = response
    characterStore.setCharacters(response)
  } catch (err) {
    error.value = '获取角色列表失败: ' + err.message
    console.error('获取角色列表失败:', err)
  } finally {
    loading.value = false
  }
}

const checkCharacterCount = async () => {
  try {
    const response = await getCharacterCount()
    characterCount.value = response.count
    characterLimit.value = response.limit
  } catch (err) {
    console.error('获取角色数量失败:', err)
  }
}

const selectCharacter = (character) => {
  characterStore.selectCharacter(character.id)
  alert(`已选择角色: ${character.name}`)
}

const createCharacter = () => {
  if (characterCount.value >= characterLimit.value) {
    alert(`每个用户最多只能创建${characterLimit.value}个角色`)
    return
  }
  editingCharacter.value = null
  form.value = {
    name: '',
    class: '战士'
  }
  showCreateForm.value = true
}

const editCharacter = (character) => {
  editingCharacter.value = character
  form.value = {
    name: character.name,
    class: character.class
  }
  showCreateForm.value = true
}

const saveCharacter = async () => {
  loading.value = true
  error.value = null
  try {
    if (editingCharacter.value) {
      // 更新角色
      await updateCharacterApi(editingCharacter.value.id, { name: form.value.name })
    } else {
      // 创建角色
      await createCharacterApi({
        name: form.value.name,
        class_type: form.value.class
      })
    }
    showCreateForm.value = false
    await loadCharacters()
    await checkCharacterCount()
  } catch (err) {
    error.value = '保存角色失败: ' + err.message
    console.error('保存角色失败:', err)
  } finally {
    loading.value = false
  }
}

const deleteCharacter = async (characterId) => {
  if (confirm('确定要删除这个角色吗？')) {
    loading.value = true
    error.value = null
    try {
      await deleteCharacterApi(characterId)
      await loadCharacters()
      await checkCharacterCount()
    } catch (err) {
      error.value = '删除角色失败: ' + err.message
      console.error('删除角色失败:', err)
    } finally {
      loading.value = false
    }
  }
}

const cancelForm = () => {
  showCreateForm.value = false
  editingCharacter.value = null
}
</script>

<style scoped>
.character {
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

.loading,
.error,
.character-limit {
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

.character-limit {
  background-color: #fff8e1;
  color: #ff6f00;
  font-weight: bold;
  margin-bottom: 30px;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.no-characters {
  background-color: #f5f5f5;
  padding: 40px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.no-characters p {
  font-size: 1.2em;
  margin-bottom: 20px;
}

.character-list {
  margin-bottom: 30px;
}

.character-list h2 {
  margin-bottom: 20px;
  color: #4CAF50;
}

.characters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.character-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.character-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #2196F3;
}

.character-card p {
  margin: 5px 0;
}

.character-card h4 {
  margin: 10px 0 5px 0;
  color: #555;
  font-size: 14px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

.attributes,
.derived-attributes {
  margin: 10px 0;
  text-align: left;
}

.attribute-row {
  display: flex;
  justify-content: space-between;
  margin: 3px 0;
  font-size: 13px;
  color: #666;
}

.attribute-row span {
  flex: 1;
  text-align: center;
}

.character-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.character-form {
  background-color: #f5f5f5;
  padding: 30px;
  border-radius: 8px;
  margin-top: 30px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.character-form h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #4CAF50;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.create-btn,
.select-btn,
.edit-btn,
.delete-btn,
.save-btn,
.cancel-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.create-btn,
.save-btn {
  background-color: #4CAF50;
  color: white;
}

.create-btn:hover,
.save-btn:hover {
  background-color: #45a049;
}

.select-btn {
  background-color: #2196F3;
  color: white;
}

.select-btn:hover {
  background-color: #0b7dda;
}

.edit-btn {
  background-color: #ff9800;
  color: white;
}

.edit-btn:hover {
  background-color: #e68a00;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}

.delete-btn:hover {
  background-color: #da190b;
}

.cancel-btn {
  background-color: #9e9e9e;
  color: white;
}

.cancel-btn:hover {
  background-color: #757575;
}
</style>