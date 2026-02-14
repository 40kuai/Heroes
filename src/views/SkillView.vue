<template>
  <div class="skill-container">
    <h1>技能管理</h1>
    
    <div class="character-selector">
      <h2>选择角色</h2>
      <select v-model="selectedCharacterId" @change="loadCharacterSkills">
        <option value="">-- 选择角色 --</option>
        <option v-for="character in characters" :key="character.id" :value="character.id">
          {{ character.name }} (等级: {{ character.level }})
        </option>
      </select>
    </div>

    <div v-if="selectedCharacterId" class="skill-management">
      <div class="character-skills">
        <h2>角色技能</h2>
        <div v-if="characterSkills.length === 0" class="no-skills">
          <p>该角色尚未学习任何技能</p>
        </div>
        <div v-else class="skill-list">
          <div v-for="characterSkill in characterSkills" :key="characterSkill.id" class="skill-card">
            <h3>{{ characterSkill.skill.name }} (等级: {{ characterSkill.skill_level }})</h3>
            <p>{{ characterSkill.skill.description }}</p>
            <div class="skill-stats">
              <p>类型: {{ characterSkill.skill.type }}</p>
              <p>稀有度: {{ characterSkill.skill.rarity }}</p>
              <p v-if="characterSkill.skill.base_damage > 0">基础伤害: {{ characterSkill.skill.base_damage }}</p>
              <p v-if="characterSkill.skill.base_defense > 0">基础防御: {{ characterSkill.skill.base_defense }}</p>
              <p v-if="characterSkill.skill.base_healing > 0">基础治疗: {{ characterSkill.skill.base_healing }}</p>
              <p>冷却时间: {{ characterSkill.skill.cooldown }}秒</p>
              <p>魔法消耗: {{ characterSkill.skill.mana_cost }}</p>
            </div>
            <div class="skill-actions">
              <button 
                @click="upgradeSkill(characterSkill.id)" 
                :disabled="characterSkill.skill_level >= getCharacterLevel()"
                class="btn btn-primary"
              >
                升级技能
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="available-skills">
        <h2>可用技能</h2>
        <div class="skill-list">
          <div v-for="skill in availableSkills" :key="skill.id" class="skill-card">
            <h3>{{ skill.name }}</h3>
            <p>{{ skill.description }}</p>
            <div class="skill-stats">
              <p>类型: {{ skill.type }}</p>
              <p>稀有度: {{ skill.rarity }}</p>
              <p v-if="skill.base_damage > 0">基础伤害: {{ skill.base_damage }}</p>
              <p v-if="skill.base_defense > 0">基础防御: {{ skill.base_defense }}</p>
              <p v-if="skill.base_healing > 0">基础治疗: {{ skill.base_healing }}</p>
              <p>冷却时间: {{ skill.cooldown }}秒</p>
              <p>魔法消耗: {{ skill.mana_cost }}</p>
              <p>需求等级: {{ skill.required_level }}</p>
            </div>
            <div class="skill-actions">
              <button 
                @click="learnSkill(skill.id)" 
                :disabled="!canLearnSkill(skill)"
                class="btn btn-success"
              >
                {{ canLearnSkill(skill) ? '学习技能' : '条件不足' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useCharacterStore } from '../stores/character';
import axios from '../utils/axios';

const characterStore = useCharacterStore();
const selectedCharacterId = ref('');
const characterSkills = ref([]);
const availableSkills = ref([]);
const characters = ref([]);

// 加载角色列表
const loadCharacters = async () => {
  try {
    const response = await axios.get('/characters');
    characters.value = response.data;
  } catch (error) {
    console.error('加载角色列表失败:', error);
  }
};

// 加载角色技能
const loadCharacterSkills = async () => {
  if (!selectedCharacterId.value) {
    characterSkills.value = [];
    return;
  }
  
  try {
    const response = await axios.get(`/characters/${selectedCharacterId.value}/skills`);
    characterSkills.value = response.data;
  } catch (error) {
    console.error('加载角色技能失败:', error);
    characterSkills.value = [];
  }
};

// 加载所有技能
const loadSkills = async () => {
  try {
    const response = await axios.get('/skills');
    availableSkills.value = response.data;
  } catch (error) {
    console.error('加载技能列表失败:', error);
    availableSkills.value = [];
  }
};

// 学习技能
const learnSkill = async (skillId) => {
  if (!selectedCharacterId.value) return;
  
  try {
    await axios.post(`/characters/${selectedCharacterId.value}/skills`, {
      skill_id: skillId
    });
    await loadCharacterSkills();
    alert('技能学习成功！');
  } catch (error) {
    console.error('学习技能失败:', error);
    alert(`学习技能失败: ${error.response?.data?.detail || '未知错误'}`);
  }
};

// 升级技能
const upgradeSkill = async (characterSkillId) => {
  try {
    await axios.post('/character-skills/upgrade', {
      character_skill_id: characterSkillId
    });
    await loadCharacterSkills();
    alert('技能升级成功！');
  } catch (error) {
    console.error('升级技能失败:', error);
    alert(`升级技能失败: ${error.response?.data?.detail || '未知错误'}`);
  }
};

// 检查是否可以学习技能
const canLearnSkill = (skill) => {
  if (!selectedCharacterId.value) return false;
  
  const character = characters.value.find(c => c.id === parseInt(selectedCharacterId.value));
  if (!character) return false;
  
  // 检查角色等级是否满足技能需求
  if (character.level < skill.required_level) return false;
  
  // 检查角色是否已经学习了该技能
  const hasLearned = characterSkills.value.some(cs => cs.skill.id === skill.id);
  if (hasLearned) return false;
  
  return true;
};

// 获取当前选择角色的等级
const getCharacterLevel = () => {
  if (!selectedCharacterId.value) return 0;
  
  const character = characters.value.find(c => c.id === parseInt(selectedCharacterId.value));
  return character ? character.level : 0;
};

// 初始化
onMounted(async () => {
  await loadCharacters();
  await loadSkills();
});
</script>

<style scoped>
.skill-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.character-selector {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.character-selector select {
  padding: 10px;
  font-size: 16px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.skill-management {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .skill-management {
    grid-template-columns: 1fr;
  }
}

.skill-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.skill-card {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: box-shadow 0.3s ease;
}

.skill-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.skill-stats {
  margin: 15px 0;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
}

.skill-stats p {
  margin: 5px 0;
  font-size: 14px;
}

.skill-actions {
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0069d9;
}

.btn-primary:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-success:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.no-skills {
  padding: 40px;
  text-align: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  color: #666;
}
</style>
