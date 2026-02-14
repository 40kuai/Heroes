<template>
  <div class="task-container">
    <h1>任务管理</h1>
    
    <div class="character-selector">
      <h2>选择角色</h2>
      <select v-model="selectedCharacterId" @change="loadCharacterTasks">
        <option value="">-- 选择角色 --</option>
        <option v-for="character in characters" :key="character.id" :value="character.id">
          {{ character.name }} (等级: {{ character.level }})
        </option>
      </select>
    </div>

    <div v-if="selectedCharacterId" class="task-management">
      <div class="task-tabs">
        <button 
          v-for="tab in taskTabs" 
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="['tab-btn', { active: activeTab === tab.value }]"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="task-list">
        <div v-if="filteredTasks.length === 0" class="no-tasks">
          <p>当前没有任务</p>
        </div>
        <div v-else class="task-cards">
          <div v-for="characterTask in filteredTasks" :key="characterTask.id" class="task-card">
            <div class="task-header">
              <h3>{{ characterTask.task.name }}</h3>
              <span class="task-type">{{ getTaskTypeLabel(characterTask.task.type) }}</span>
              <span class="task-status">{{ getTaskStatusLabel(characterTask.status) }}</span>
            </div>
            <div class="task-content">
              <p class="task-description">{{ characterTask.task.description }}</p>
              <div class="task-rewards">
                <h4>奖励</h4>
                <ul>
                  <li v-if="characterTask.task.exp_reward > 0">经验值: {{ characterTask.task.exp_reward }}</li>
                  <li v-if="characterTask.task.gold_reward > 0">金币: {{ characterTask.task.gold_reward }}</li>
                  <li v-if="characterTask.task.item_reward">物品: {{ characterTask.task.item_reward }}</li>
                </ul>
              </div>
              <div class="task-progress">
                <h4>进度</h4>
                <div class="progress-bar">
                  <div 
                    class="progress-fill" 
                    :style="{ width: `${(characterTask.progress / characterTask.task.target_count) * 100}%` }"
                  ></div>
                </div>
                <p class="progress-text">{{ characterTask.progress }} / {{ characterTask.task.target_count }}</p>
              </div>
            </div>
            <div class="task-actions">
              <button 
                v-if="characterTask.status === 'available'"
                @click="acceptTask(characterTask.task.id)"
                class="btn btn-primary"
              >
                接取任务
              </button>
              <button 
                v-else-if="characterTask.status === 'accepted'"
                @click="updateTaskProgress(characterTask.id, characterTask.task.target_count)"
                class="btn btn-success"
              >
                完成任务
              </button>
              <button 
                v-else-if="characterTask.status === 'completed'"
                @click="claimReward(characterTask.task.id)"
                class="btn btn-warning"
              >
                领取奖励
              </button>
              <button 
                v-else-if="characterTask.status === 'rewarded'"
                disabled
                class="btn btn-secondary"
              >
                已领取奖励
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
const characterTasks = ref([]);
const characters = ref([]);
const activeTab = ref('all');

const taskTabs = [
  { label: '全部任务', value: 'all' },
  { label: '可接取', value: 'available' },
  { label: '进行中', value: 'accepted' },
  { label: '已完成', value: 'completed' },
  { label: '已领取', value: 'rewarded' }
];

// 加载角色列表
const loadCharacters = async () => {
  try {
    const response = await axios.get('/characters');
    characters.value = response.data;
  } catch (error) {
    console.error('加载角色列表失败:', error);
  }
};

// 加载角色任务
const loadCharacterTasks = async () => {
  if (!selectedCharacterId.value) {
    characterTasks.value = [];
    return;
  }
  
  try {
    const response = await axios.get(`/characters/${selectedCharacterId.value}/tasks`);
    characterTasks.value = response.data;
  } catch (error) {
    console.error('加载角色任务失败:', error);
    characterTasks.value = [];
  }
};

// 过滤任务
const filteredTasks = computed(() => {
  if (activeTab.value === 'all') {
    return characterTasks.value;
  }
  return characterTasks.value.filter(task => task.status === activeTab.value);
});

// 接取任务
const acceptTask = async (taskId) => {
  if (!selectedCharacterId.value) return;
  
  try {
    await axios.post(`/characters/${selectedCharacterId.value}/tasks/accept`, {
      task_id: taskId
    });
    await loadCharacterTasks();
    alert('任务接取成功！');
  } catch (error) {
    console.error('接取任务失败:', error);
    alert(`接取任务失败: ${error.response?.data?.detail || '未知错误'}`);
  }
};

// 更新任务进度
const updateTaskProgress = async (characterTaskId, progress) => {
  if (!selectedCharacterId.value) return;
  
  try {
    await axios.post(`/characters/${selectedCharacterId.value}/tasks/progress`, {
      character_task_id: characterTaskId,
      progress: progress
    });
    await loadCharacterTasks();
    alert('任务完成成功！');
  } catch (error) {
    console.error('更新任务进度失败:', error);
    alert(`更新任务进度失败: ${error.response?.data?.detail || '未知错误'}`);
  }
};

// 领取奖励
const claimReward = async (taskId) => {
  if (!selectedCharacterId.value) return;
  
  try {
    await axios.post(`/characters/${selectedCharacterId.value}/tasks/reward`, {
      task_id: taskId
    });
    await loadCharacterTasks();
    alert('奖励领取成功！');
  } catch (error) {
    console.error('领取奖励失败:', error);
    alert(`领取奖励失败: ${error.response?.data?.detail || '未知错误'}`);
  }
};

// 获取任务类型标签
const getTaskTypeLabel = (type) => {
  const typeMap = {
    'main': '主线任务',
    'daily': '日常任务',
    'side': '支线任务'
  };
  return typeMap[type] || type;
};

// 获取任务状态标签
const getTaskStatusLabel = (status) => {
  const statusMap = {
    'available': '可接取',
    'accepted': '进行中',
    'completed': '已完成',
    'rewarded': '已领取'
  };
  return statusMap[status] || status;
};

// 初始化
onMounted(async () => {
  await loadCharacters();
});
</script>

<style scoped>
.task-container {
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

.task-management {
  margin-top: 30px;
}

.task-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background-color: #f0f0f0;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background-color: #e0e0e0;
}

.tab-btn.active {
  background-color: #007bff;
  color: white;
}

.task-list {
  margin-top: 20px;
}

.task-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.task-card {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: box-shadow 0.3s ease;
}

.task-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.task-header h3 {
  margin: 0;
  font-size: 18px;
}

.task-type {
  padding: 4px 12px;
  background-color: #e7f3ff;
  color: #007bff;
  border-radius: 12px;
  font-size: 12px;
}

.task-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
}

.task-status[data-status="available"] {
  background-color: #e7f3ff;
  color: #007bff;
}

.task-status[data-status="accepted"] {
  background-color: #fff3cd;
  color: #856404;
}

.task-status[data-status="completed"] {
  background-color: #d4edda;
  color: #155724;
}

.task-status[data-status="rewarded"] {
  background-color: #f8d7da;
  color: #721c24;
}

.task-description {
  margin: 10px 0 15px;
  color: #666;
}

.task-rewards {
  margin-bottom: 15px;
}

.task-rewards h4 {
  margin: 0 0 8px;
  font-size: 14px;
  font-weight: 600;
}

.task-rewards ul {
  margin: 0;
  padding-left: 20px;
}

.task-rewards li {
  margin: 4px 0;
  font-size: 14px;
}

.task-progress {
  margin-bottom: 20px;
}

.task-progress h4 {
  margin: 0 0 8px;
  font-size: 14px;
  font-weight: 600;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background-color: #28a745;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  margin: 0;
  font-size: 14px;
  color: #666;
  text-align: right;
}

.task-actions {
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

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-warning {
  background-color: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background-color: #e0a800;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.no-tasks {
  padding: 40px;
  text-align: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  color: #666;
}

.no-tasks p {
  margin: 0;
  font-size: 16px;
}

@media (max-width: 768px) {
  .task-cards {
    grid-template-columns: 1fr;
  }
  
  .task-tabs {
    flex-wrap: wrap;
  }
  
  .tab-btn {
    padding: 8px 12px;
    font-size: 12px;
  }
}
</style>
