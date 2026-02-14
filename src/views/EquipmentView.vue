<template>
  <div class="equipment">
    <h1>装备管理</h1>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <!-- 错误信息 -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadEquipmentList" class="retry-btn">重试</button>
    </div>
    
    <div v-else>
      <!-- 装备列表 -->
      <div class="equipment-section">
        <h2>装备列表</h2>
        <div v-if="equipmentList.length === 0" class="no-equipment">
          <p>还没有装备，快来创建装备吧！</p>
          <button @click="showCreateForm = true" class="create-btn">创建装备</button>
        </div>
        <div v-else class="equipment-grid">
          <div v-for="equipment in equipmentList" :key="equipment.id" class="equipment-card">
            <h3>{{ equipment.name }}</h3>
            <p>类型: {{ equipment.type }}</p>
            <p>等级: {{ equipment.level }}</p>
            <p>稀有度: {{ equipment.rarity }}</p>
            
            <!-- 属性加成 -->
            <div class="equipment-attributes">
              <h4>属性加成</h4>
              <div class="attribute-row">
                <span>攻击力: {{ equipment.attack }}</span>
                <span>防御力: {{ equipment.defense }}</span>
              </div>
              <div class="attribute-row">
                <span>力量: {{ equipment.strength }}</span>
                <span>敏捷: {{ equipment.agility }}</span>
              </div>
              <div class="attribute-row">
                <span>智力: {{ equipment.intelligence }}</span>
                <span>体力: {{ equipment.vitality }}</span>
              </div>
            </div>
            
            <div class="equipment-actions">
              <button @click="selectEquipment(equipment)" class="select-btn">选择</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 角色装备 -->
      <div class="character-equipment-section">
        <h2>角色装备</h2>
        <div v-if="characters.length === 0" class="no-characters">
          <p>还没有角色，快去创建角色吧！</p>
          <router-link to="/character" class="create-link">创建角色</router-link>
        </div>
        <div v-else>
          <select v-model="selectedCharacterId" @change="loadCharacterEquipment" class="character-select">
            <option value="">选择角色</option>
            <option v-for="character in characters" :key="character.id" :value="character.id">
              {{ character.name }} (等级: {{ character.level }})
            </option>
          </select>
          
          <div v-if="selectedCharacterId" class="character-equipment">
            <h3>{{ getCharacterName(selectedCharacterId) }}的装备</h3>
            <div v-if="characterEquipment.length === 0" class="no-equipment">
              <p>角色还没有穿戴装备，快去为角色穿戴装备吧！</p>
            </div>
            <div v-else class="equipment-slots">
              <div v-for="slot in characterEquipment" :key="slot.id" class="equipment-slot">
                <h4>{{ slot.slot_type }}</h4>
                <div class="slot-equipment">
                  <h5>{{ slot.equipment.name }}</h5>
                  <p>等级: {{ slot.equipment.level }}</p>
                  <p>稀有度: {{ slot.equipment.rarity }}</p>
                  <button @click="unequipItem(slot.id)" class="unequip-btn">卸下</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 穿戴装备 -->
      <div v-if="selectedCharacterId && selectedEquipment" class="equip-section">
        <h2>穿戴装备</h2>
        <div class="equip-form">
          <h3>角色: {{ getCharacterName(selectedCharacterId) }}</h3>
          <h3>装备: {{ selectedEquipment.name }}</h3>
          <div class="slot-selection">
            <label>选择槽位:</label>
            <select v-model="selectedSlotType">
              <option value="武器">武器</option>
              <option value="头盔">头盔</option>
              <option value="胸甲">胸甲</option>
              <option value="手套">手套</option>
              <option value="靴子">靴子</option>
              <option value="饰品1">饰品1</option>
              <option value="饰品2">饰品2</option>
            </select>
          </div>
          <button @click="equipItem" class="equip-btn">穿戴装备</button>
        </div>
      </div>
    </div>
    
    <!-- 创建装备表单 -->
    <div v-if="showCreateForm" class="equipment-form">
      <h2>创建装备</h2>
      <form @submit.prevent="saveEquipment">
        <div class="form-group">
          <label>装备名称:</label>
          <input v-model="form.name" type="text" required>
        </div>
        <div class="form-group">
          <label>装备类型:</label>
          <select v-model="form.type" required>
            <option value="武器">武器</option>
            <option value="头盔">头盔</option>
            <option value="胸甲">胸甲</option>
            <option value="手套">手套</option>
            <option value="靴子">靴子</option>
            <option value="饰品">饰品</option>
          </select>
        </div>
        <div class="form-group">
          <label>装备等级:</label>
          <input v-model.number="form.level" type="number" min="1" required>
        </div>
        <div class="form-group">
          <label>稀有度:</label>
          <select v-model="form.rarity" required>
            <option value="普通">普通</option>
            <option value="优秀">优秀</option>
            <option value="稀有">稀有</option>
            <option value="史诗">史诗</option>
            <option value="传说">传说</option>
          </select>
        </div>
        
        <!-- 属性加成 -->
        <div class="form-group">
          <label>攻击力:</label>
          <input v-model.number="form.attack" type="number" min="0">
        </div>
        <div class="form-group">
          <label>防御力:</label>
          <input v-model.number="form.defense" type="number" min="0">
        </div>
        <div class="form-group">
          <label>力量:</label>
          <input v-model.number="form.strength" type="number" min="0">
        </div>
        <div class="form-group">
          <label>敏捷:</label>
          <input v-model.number="form.agility" type="number" min="0">
        </div>
        <div class="form-group">
          <label>智力:</label>
          <input v-model.number="form.intelligence" type="number" min="0">
        </div>
        <div class="form-group">
          <label>体力:</label>
          <input v-model.number="form.vitality" type="number" min="0">
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
import { useRouter } from 'vue-router'
import { getEquipmentList, createEquipment as createEquipmentApi, equipEquipment as equipEquipmentApi, unequipEquipment as unequipEquipmentApi, getCharacterEquipment as getCharacterEquipmentApi } from '../api/user'
import { getCharacters } from '../api/user'

const router = useRouter()
const showCreateForm = ref(false)
const form = ref({
  name: '',
  type: '武器',
  level: 1,
  rarity: '普通',
  attack: 0,
  defense: 0,
  strength: 0,
  agility: 0,
  intelligence: 0,
  vitality: 0
})
const equipmentList = ref([])
const characters = ref([])
const characterEquipment = ref([])
const selectedCharacterId = ref('')
const selectedEquipment = ref(null)
const selectedSlotType = ref('武器')
const loading = ref(false)
const error = ref(null)

onMounted(() => {
  loadEquipmentList()
  loadCharacters()
})

const loadEquipmentList = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await getEquipmentList()
    equipmentList.value = response
  } catch (err) {
    error.value = '获取装备列表失败: ' + err.message
    console.error('获取装备列表失败:', err)
  } finally {
    loading.value = false
  }
}

const loadCharacters = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await getCharacters()
    characters.value = response
  } catch (err) {
    error.value = '获取角色列表失败: ' + err.message
    console.error('获取角色列表失败:', err)
  } finally {
    loading.value = false
  }
}

const loadCharacterEquipment = async () => {
  if (!selectedCharacterId.value) {
    characterEquipment.value = []
    return
  }
  
  loading.value = true
  error.value = null
  try {
    const response = await getCharacterEquipmentApi(selectedCharacterId.value)
    characterEquipment.value = response
  } catch (err) {
    error.value = '获取角色装备失败: ' + err.message
    console.error('获取角色装备失败:', err)
  } finally {
    loading.value = false
  }
}

const selectEquipment = (equipment) => {
  selectedEquipment.value = equipment
}

const getCharacterName = (characterId) => {
  const character = characters.value.find(c => c.id === characterId)
  return character ? character.name : ''
}

const saveEquipment = async () => {
  loading.value = true
  error.value = null
  try {
    await createEquipmentApi(form.value)
    showCreateForm.value = false
    await loadEquipmentList()
  } catch (err) {
    error.value = '创建装备失败: ' + err.message
    console.error('创建装备失败:', err)
  } finally {
    loading.value = false
  }
}

const equipItem = async () => {
  if (!selectedCharacterId.value || !selectedEquipment.value) {
    alert('请选择角色和装备')
    return
  }
  
  loading.value = true
  error.value = null
  try {
    await equipEquipmentApi({
      character_id: selectedCharacterId.value,
      equipment_id: selectedEquipment.value.id,
      slot_type: selectedSlotType.value
    })
    await loadCharacterEquipment()
    alert('装备穿戴成功')
  } catch (err) {
    error.value = '穿戴装备失败: ' + err.message
    console.error('穿戴装备失败:', err)
  } finally {
    loading.value = false
  }
}

const unequipItem = async (slotId) => {
  loading.value = true
  error.value = null
  try {
    await unequipEquipmentApi(slotId)
    await loadCharacterEquipment()
    alert('装备卸下成功')
  } catch (err) {
    error.value = '卸下装备失败: ' + err.message
    console.error('卸下装备失败:', err)
  } finally {
    loading.value = false
  }
}

const cancelForm = () => {
  showCreateForm.value = false
  form.value = {
    name: '',
    type: '武器',
    level: 1,
    rarity: '普通',
    attack: 0,
    defense: 0,
    strength: 0,
    agility: 0,
    intelligence: 0,
    vitality: 0
  }
}
</script>

<style scoped>
.equipment {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  max-width: 1200px;
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
.no-equipment,
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

.no-equipment,
.no-characters {
  background-color: #f5f5f5;
}

.create-btn,
.create-link {
  margin-top: 10px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.create-btn:hover,
.create-link:hover {
  background-color: #45a049;
}

.equipment-section,
.character-equipment-section {
  margin-bottom: 40px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.equipment-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: left;
}

.equipment-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #2196F3;
}

.equipment-card p {
  margin: 5px 0;
}

.equipment-attributes {
  margin: 15px 0;
}

.equipment-attributes h4 {
  margin: 10px 0 5px 0;
  color: #555;
  font-size: 14px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

.attribute-row {
  display: flex;
  justify-content: space-between;
  margin: 3px 0;
  font-size: 13px;
  color: #666;
}

.equipment-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.select-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #2196F3;
  color: white;
  cursor: pointer;
}

.select-btn:hover {
  background-color: #0b7dda;
}

.character-select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  margin-bottom: 20px;
}

.character-equipment {
  margin-top: 20px;
}

.equipment-slots {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.equipment-slot {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.equipment-slot h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #555;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

.slot-equipment {
  margin-top: 10px;
}

.slot-equipment h5 {
  margin: 0 0 5px 0;
  color: #2196F3;
}

.slot-equipment p {
  margin: 3px 0;
  font-size: 13px;
  color: #666;
}

.unequip-btn {
  margin-top: 10px;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  background-color: #f44336;
  color: white;
  cursor: pointer;
  font-size: 13px;
}

.unequip-btn:hover {
  background-color: #da190b;
}

.equip-section {
  margin-top: 40px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.equip-form {
  max-width: 500px;
  margin: 0 auto;
  text-align: left;
}

.slot-selection {
  margin: 15px 0;
}

.slot-selection label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.slot-selection select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.equip-btn {
  margin-top: 20px;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
  font-size: 16px;
}

.equip-btn:hover {
  background-color: #45a049;
}

.equipment-form {
  background-color: #f5f5f5;
  padding: 30px;
  border-radius: 8px;
  margin-top: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  text-align: left;
}

.equipment-form h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #4CAF50;
}

.form-group {
  margin-bottom: 15px;
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

.save-btn,
.cancel-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.save-btn {
  background-color: #4CAF50;
  color: white;
}

.save-btn:hover {
  background-color: #45a049;
}

.cancel-btn {
  background-color: #9e9e9e;
  color: white;
}

.cancel-btn:hover {
  background-color: #757575;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
