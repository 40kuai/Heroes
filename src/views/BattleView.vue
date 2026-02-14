<template>
  <div class="battle">
    <h1>战斗系统</h1>
    <div v-if="!inBattle" class="battle-prepare">
      <h2>选择对手</h2>
      <div class="enemy-list">
        <div v-for="enemy in enemies" :key="enemy.id" class="enemy-card">
          <h3>{{ enemy.name }}</h3>
          <p>等级: {{ enemy.level }}</p>
          <p>生命值: {{ enemy.health }}/{{ enemy.maxHealth }}</p>
          <p>攻击力: {{ enemy.attack }}</p>
          <p>防御力: {{ enemy.defense }}</p>
          <p>经验奖励: {{ enemy.expReward }}</p>
          <p>金币奖励: {{ enemy.goldReward }}</p>
          <button @click="startBattle(enemy)" class="battle-btn">开始战斗</button>
        </div>
      </div>
    </div>
    
    <div v-else class="battle-arena">
      <h2>战斗中</h2>
      <div class="battle-status">
        <div class="player-status">
          <h3>玩家</h3>
          <div class="health-bar">
            <div class="health-fill" :style="{ width: `${player.healthPercentage}%` }"></div>
          </div>
          <p>生命值: {{ player.health }}/{{ player.maxHealth }}</p>
          <p>攻击力: {{ player.attack }}</p>
          <p>防御力: {{ player.defense }}</p>
        </div>
        
        <div class="enemy-status">
          <h3>{{ currentEnemy.name }}</h3>
          <div class="health-bar enemy">
            <div class="health-fill enemy" :style="{ width: `${enemy.healthPercentage}%` }"></div>
          </div>
          <p>生命值: {{ currentEnemy.health }}/{{ currentEnemy.maxHealth }}</p>
          <p>攻击力: {{ currentEnemy.attack }}</p>
          <p>防御力: {{ currentEnemy.defense }}</p>
        </div>
      </div>
      
      <div class="battle-log">
        <h3>战斗日志</h3>
        <div class="log-content">
          <div v-for="(log, index) in battleLog" :key="index" class="log-entry">
            {{ log }}
          </div>
        </div>
      </div>
      
      <div class="battle-actions">
        <button @click="attack()" class="attack-btn">攻击</button>
        <button @click="defend()" class="defend-btn">防御</button>
        <button @click="useSkill()" class="skill-btn">技能</button>
        <button @click="flee()" class="flee-btn">逃跑</button>
      </div>
    </div>
    
    <!-- 战斗结果 -->
    <div v-if="battleResult" class="battle-result">
      <h2>{{ battleResult.victory ? '战斗胜利！' : '战斗失败！' }}</h2>
      <div v-if="battleResult.victory" class="rewards">
        <p>获得经验: {{ battleResult.expReward }}</p>
        <p>获得金币: {{ battleResult.goldReward }}</p>
      </div>
      <button @click="resetBattle" class="continue-btn">继续</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const inBattle = ref(false)
const currentEnemy = ref(null)
const battleLog = ref([])
const battleResult = ref(null)

// 玩家数据
const player = reactive({
  name: '玩家',
  level: 1,
  maxHealth: 100,
  health: 100,
  attack: 20,
  defense: 10
})

// 敌人数据
const enemies = ref([
  {
    id: 1,
    name: '小怪',
    level: 1,
    maxHealth: 50,
    health: 50,
    attack: 10,
    defense: 5,
    expReward: 50,
    goldReward: 20
  },
  {
    id: 2,
    name: '精英怪',
    level: 2,
    maxHealth: 100,
    health: 100,
    attack: 15,
    defense: 8,
    expReward: 100,
    goldReward: 40
  },
  {
    id: 3,
    name: 'Boss',
    level: 3,
    maxHealth: 200,
    health: 200,
    attack: 25,
    defense: 15,
    expReward: 200,
    goldReward: 100
  }
])

// 计算生命值百分比
const playerHealthPercentage = computed(() => {
  return Math.max(0, (player.health / player.maxHealth) * 100)
})

const enemyHealthPercentage = computed(() => {
  if (!currentEnemy.value) return 0
  return Math.max(0, (currentEnemy.value.health / currentEnemy.value.maxHealth) * 100)
})

// 开始战斗
const startBattle = (enemy) => {
  // 重置敌人状态
  currentEnemy.value = { ...enemy }
  // 重置玩家状态
  player.health = player.maxHealth
  // 清空战斗日志
  battleLog.value = []
  // 开始战斗
  inBattle.value = true
  battleResult.value = null
  battleLog.value.push(`战斗开始！你面对的是 ${currentEnemy.value.name}`)
}

// 攻击
const attack = () => {
  if (!currentEnemy.value) return
  
  // 玩家攻击
  const playerDamage = Math.max(1, player.attack - currentEnemy.value.defense / 2)
  currentEnemy.value.health -= playerDamage
  battleLog.value.push(`你对 ${currentEnemy.value.name} 造成了 ${playerDamage} 点伤害`)
  
  // 检查敌人是否死亡
  if (currentEnemy.value.health <= 0) {
    endBattle(true)
    return
  }
  
  // 敌人反击
  enemyAttack()
}

// 防御
const defend = () => {
  if (!currentEnemy.value) return
  
  battleLog.value.push('你选择了防御，减少受到的伤害')
  
  // 敌人攻击，但玩家防御
  const enemyDamage = Math.max(1, (currentEnemy.value.attack - player.defense / 2) / 2)
  player.health -= enemyDamage
  battleLog.value.push(`${currentEnemy.value.name} 对你造成了 ${enemyDamage} 点伤害（防御中）`)
  
  // 检查玩家是否死亡
  if (player.health <= 0) {
    endBattle(false)
  }
}

// 使用技能
const useSkill = () => {
  if (!currentEnemy.value) return
  
  // 技能伤害
  const skillDamage = player.attack * 1.5
  currentEnemy.value.health -= skillDamage
  battleLog.value.push(`你使用了技能，对 ${currentEnemy.value.name} 造成了 ${skillDamage} 点伤害`)
  
  // 检查敌人是否死亡
  if (currentEnemy.value.health <= 0) {
    endBattle(true)
    return
  }
  
  // 敌人反击
  enemyAttack()
}

// 逃跑
const flee = () => {
  if (!currentEnemy.value) return
  
  // 逃跑成功率
  const fleeSuccess = Math.random() > 0.3
  
  if (fleeSuccess) {
    battleLog.value.push('你成功逃跑了')
    inBattle.value = false
    currentEnemy.value = null
  } else {
    battleLog.value.push('逃跑失败！')
    // 敌人反击
    enemyAttack()
  }
}

// 敌人攻击
const enemyAttack = () => {
  if (!currentEnemy.value) return
  
  const enemyDamage = Math.max(1, currentEnemy.value.attack - player.defense / 2)
  player.health -= enemyDamage
  battleLog.value.push(`${currentEnemy.value.name} 对你造成了 ${enemyDamage} 点伤害`)
  
  // 检查玩家是否死亡
  if (player.health <= 0) {
    endBattle(false)
  }
}

// 结束战斗
const endBattle = (victory) => {
  inBattle.value = false
  
  if (victory) {
    battleLog.value.push(`战斗胜利！你击败了 ${currentEnemy.value.name}`)
    battleResult.value = {
      victory: true,
      expReward: currentEnemy.value.expReward,
      goldReward: currentEnemy.value.goldReward
    }
  } else {
    battleLog.value.push('战斗失败！你被击败了')
    battleResult.value = {
      victory: false
    }
  }
}

// 重置战斗
const resetBattle = () => {
  battleResult.value = null
  currentEnemy.value = null
  inBattle.value = false
  battleLog.value = []
}
</script>

<style scoped>
.battle {
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

.battle-prepare {
  margin-bottom: 40px;
}

.battle-prepare h2 {
  margin-bottom: 20px;
  color: #4CAF50;
}

.enemy-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.enemy-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: left;
  border-left: 4px solid #f44336;
}

.enemy-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #f44336;
}

.enemy-card p {
  margin: 5px 0;
  font-size: 14px;
}

.battle-btn {
  margin-top: 15px;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  background-color: #f44336;
  color: white;
  width: 100%;
}

.battle-btn:hover {
  background-color: #da190b;
}

.battle-arena {
  background-color: #f5f5f5;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.battle-arena h2 {
  margin-bottom: 20px;
  color: #ff9800;
}

.battle-status {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  gap: 20px;
}

.player-status,
.enemy-status {
  flex: 1;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.player-status h3,
.enemy-status h3 {
  margin-top: 0;
  margin-bottom: 15px;
}

.health-bar {
  width: 100%;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
}

.health-fill {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.5s ease;
}

.health-fill.enemy {
  background-color: #f44336;
}

.battle-log {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 30px;
  max-height: 200px;
  overflow-y: auto;
}

.battle-log h3 {
  margin-top: 0;
  margin-bottom: 15px;
}

.log-content {
  text-align: left;
}

.log-entry {
  margin: 5px 0;
  font-size: 14px;
}

.battle-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.attack-btn,
.defend-btn,
.skill-btn,
.flee-btn {
  padding: 15px 30px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.attack-btn {
  background-color: #f44336;
  color: white;
}

.attack-btn:hover {
  background-color: #da190b;
}

.defend-btn {
  background-color: #2196F3;
  color: white;
}

.defend-btn:hover {
  background-color: #0b7dda;
}

.skill-btn {
  background-color: #ff9800;
  color: white;
}

.skill-btn:hover {
  background-color: #e68a00;
}

.flee-btn {
  background-color: #9e9e9e;
  color: white;
}

.flee-btn:hover {
  background-color: #757575;
}

.battle-result {
  background-color: #f0f8ff;
  padding: 40px;
  border-radius: 8px;
  margin-top: 30px;
  text-align: center;
}

.battle-result h2 {
  margin-bottom: 20px;
  color: #4CAF50;
}

.rewards {
  margin-bottom: 30px;
}

.rewards p {
  font-size: 1.2em;
  margin: 10px 0;
}

.continue-btn {
  padding: 15px 40px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  transition: all 0.3s ease;
}

.continue-btn:hover {
  background-color: #45a049;
}
</style>