<template>
  <div class="social-container">
    <h1>社交系统</h1>
    
    <!-- 标签页导航 -->
    <div class="social-tabs">
      <button 
        v-for="tab in socialTabs" 
        :key="tab.value"
        @click="activeTab = tab.value"
        :class="['tab-btn', { active: activeTab === tab.value }]"
      >
        {{ tab.label }}
      </button>
    </div>
    
    <!-- 好友列表 -->
    <div v-if="activeTab === 'friends'" class="friends-section">
      <div class="friend-actions">
        <button @click="showAddFriendDialog = true" class="btn btn-primary">添加好友</button>
      </div>
      
      <div v-if="friends.length === 0" class="no-friends">
        <p>您还没有好友</p>
        <p>点击上方按钮添加好友</p>
      </div>
      <div v-else class="friend-list">
        <div v-for="friend in friends" :key="friend.id" class="friend-card">
          <div class="friend-info">
            <h3>{{ getFriendUsername(friend) }}</h3>
            <p>状态: {{ friend.status }}</p>
          </div>
          <div class="friend-actions">
            <button @click="startChat(friend)" class="btn btn-success">聊天</button>
            <button @click="blockFriend(friend)" class="btn btn-danger">拉黑</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 聊天界面 -->
    <div v-if="activeTab === 'chat'" class="chat-section">
      <div v-if="!selectedFriend" class="no-chat-selected">
        <p>请从好友列表中选择一个好友开始聊天</p>
      </div>
      <div v-else class="chat-container">
        <div class="chat-header">
          <h3>{{ getFriendUsername(selectedFriend) }}</h3>
        </div>
        <div class="chat-messages">
          <div 
            v-for="message in messages" 
            :key="message.id"
            :class="['message', { 'sent': message.sender_id === currentUser.id, 'received': message.receiver_id === currentUser.id }]"
          >
            <div class="message-content">{{ message.content }}</div>
            <div class="message-time">{{ formatTime(message.created_at) }}</div>
            <div v-if="message.receiver_id === currentUser.id" class="message-read" :class="{ 'read': message.is_read }">
              {{ message.is_read ? '已读' : '未读' }}
            </div>
          </div>
        </div>
        <div class="chat-input">
          <input 
            v-model="newMessage"
            type="text"
            placeholder="输入消息..."
            @keyup.enter="sendMessage"
          >
          <button @click="sendMessage" class="btn btn-primary">发送</button>
        </div>
      </div>
    </div>
    
    <!-- 添加好友对话框 -->
    <div v-if="showAddFriendDialog" class="dialog-overlay">
      <div class="dialog">
        <h3>添加好友</h3>
        <div class="dialog-content">
          <input 
            v-model="friendId"
            type="number"
            placeholder="输入好友用户ID"
          >
        </div>
        <div class="dialog-actions">
          <button @click="showAddFriendDialog = false" class="btn btn-secondary">取消</button>
          <button @click="addFriend" class="btn btn-primary">添加</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 响应式数据
const activeTab = ref('friends');
const friends = ref([]);
const messages = ref([]);
const selectedFriend = ref(null);
const newMessage = ref('');
const friendId = ref('');
const showAddFriendDialog = ref(false);
const currentUser = ref({ id: 1 }); // 假设当前用户ID为1

// 标签页配置
const socialTabs = [
  { label: '好友列表', value: 'friends' },
  { label: '聊天', value: 'chat' }
];

// 获取好友列表
const fetchFriends = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/friends/${currentUser.value.id}`);
    friends.value = response.data;
  } catch (error) {
    console.error('获取好友列表失败:', error);
  }
};

// 获取好友用户名（模拟）
const getFriendUsername = (friend) => {
  const friendUserId = friend.user_id === currentUser.value.id ? friend.friend_id : friend.user_id;
  return `用户${friendUserId}`;
};

// 添加好友
const addFriend = async () => {
  try {
    await axios.post('http://localhost:8000/friends/send', {
      user_id: currentUser.value.id,
      friend_id: friendId.value
    });
    showAddFriendDialog.value = false;
    friendId.value = '';
    fetchFriends();
    alert('好友请求发送成功');
  } catch (error) {
    console.error('发送好友请求失败:', error);
    alert('发送好友请求失败');
  }
};

// 拉黑好友
const blockFriend = async (friend) => {
  try {
    await axios.post('http://localhost:8000/friends/block', {
      user_id: currentUser.value.id,
      friend_id: friend.user_id === currentUser.value.id ? friend.friend_id : friend.user_id
    });
    fetchFriends();
    alert('好友已拉黑');
  } catch (error) {
    console.error('拉黑好友失败:', error);
    alert('拉黑好友失败');
  }
};

// 开始聊天
const startChat = (friend) => {
  selectedFriend.value = friend;
  activeTab.value = 'chat';
  fetchMessages();
};

// 获取聊天记录
const fetchMessages = async () => {
  if (!selectedFriend.value) return;
  
  try {
    const friendUserId = selectedFriend.value.user_id === currentUser.value.id 
      ? selectedFriend.value.friend_id 
      : selectedFriend.value.user_id;
    
    const response = await axios.get(`http://localhost:8000/messages/${currentUser.value.id}/${friendUserId}`);
    messages.value = response.data;
  } catch (error) {
    console.error('获取聊天记录失败:', error);
  }
};

// 发送消息
const sendMessage = async () => {
  if (!selectedFriend.value || !newMessage.value.trim()) return;
  
  try {
    const friendUserId = selectedFriend.value.user_id === currentUser.value.id 
      ? selectedFriend.value.friend_id 
      : selectedFriend.value.user_id;
    
    await axios.post('http://localhost:8000/messages/send', {
      sender_id: currentUser.value.id,
      receiver_id: friendUserId,
      content: newMessage.value
    });
    
    newMessage.value = '';
    fetchMessages();
  } catch (error) {
    console.error('发送消息失败:', error);
    alert('发送消息失败');
  }
};

// 格式化时间
const formatTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString();
};

// 组件挂载时获取好友列表
onMounted(() => {
  fetchFriends();
});
</script>

<style scoped>
.social-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.social-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.tab-btn {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  margin-right: 10px;
  border-bottom: 2px solid transparent;
}

.tab-btn.active {
  border-bottom: 2px solid #007bff;
  color: #007bff;
  font-weight: bold;
}

.friend-actions {
  margin-bottom: 20px;
}

.no-friends,
.no-chat-selected {
  text-align: center;
  padding: 40px 0;
  color: #666;
}

.friend-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.friend-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: #f9f9f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.friend-info h3 {
  margin: 0 0 5px 0;
}

.friend-info p {
  margin: 0;
  color: #666;
}

.chat-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  height: 600px;
  display: flex;
  flex-direction: column;
}

.chat-header {
  background: #f5f5f5;
  padding: 15px;
  border-bottom: 1px solid #ddd;
}

.chat-header h3 {
  margin: 0;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #f9f9f9;
}

.message {
  margin-bottom: 15px;
  max-width: 70%;
}

.message.sent {
  align-self: flex-end;
  margin-left: auto;
}

.message.received {
  align-self: flex-start;
}

.message-content {
  padding: 10px 15px;
  border-radius: 18px;
  background: #e3f2fd;
}

.message.sent .message-content {
  background: #dcf8c6;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  text-align: right;
}

.message-read {
  font-size: 12px;
  color: #007bff;
  margin-top: 3px;
  text-align: right;
}

.chat-input {
  padding: 15px;
  border-top: 1px solid #ddd;
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: white;
  border-radius: 8px;
  padding: 20px;
  width: 400px;
  max-width: 90%;
}

.dialog h3 {
  margin: 0 0 20px 0;
}

.dialog-content {
  margin-bottom: 20px;
}

.dialog-content input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}
</style>
