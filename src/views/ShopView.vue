<template>
  <div class="shop-container">
    <h1>商城系统</h1>
    
    <!-- 标签页导航 -->
    <div class="shop-tabs">
      <button 
        v-for="tab in shopTabs" 
        :key="tab.value"
        @click="activeTab = tab.value"
        :class="['tab-btn', { active: activeTab === tab.value }]"
      >
        {{ tab.label }}
      </button>
    </div>
    
    <!-- 商品列表 -->
    <div v-if="activeTab === 'products'" class="products-section">
      <div v-if="products.length === 0" class="no-products">
        <p>当前没有商品</p>
      </div>
      <div v-else class="product-list">
        <div v-for="product in products" :key="product.id" class="product-card">
          <div class="product-header">
            <h3>{{ product.name }}</h3>
            <span class="product-price">{{ product.price }} {{ product.currency }}</span>
          </div>
          <div class="product-content">
            <p class="product-description">{{ product.description }}</p>
            <div class="product-info">
              <p>类型: {{ getProductTypeLabel(product.type) }}</p>
              <p>数量: {{ product.quantity }}</p>
              <p>等级要求: {{ product.level_requirement }}</p>
            </div>
          </div>
          <div class="product-actions">
            <button 
              @click="buyProduct(product)" 
              :disabled="!canBuyProduct(product)"
              class="btn btn-primary"
            >
              {{ canBuyProduct(product) ? '购买' : '等级不足' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 充值界面 -->
    <div v-if="activeTab === 'recharge'" class="recharge-section">
      <div class="recharge-form">
        <h3>货币充值</h3>
        <div class="form-group">
          <label for="recharge-amount">充值金额</label>
          <input 
            v-model="rechargeAmount"
            type="number"
            id="recharge-amount"
            placeholder="输入充值金额"
            min="0"
            step="1"
          >
        </div>
        <div class="form-group">
          <label for="recharge-currency">货币类型</label>
          <select v-model="rechargeCurrency" id="recharge-currency">
            <option value="diamond">钻石</option>
            <option value="gold">金币</option>
          </select>
        </div>
        <button @click="recharge" class="btn btn-success">确认充值</button>
      </div>
    </div>
    
    <!-- 订单记录 -->
    <div v-if="activeTab === 'orders'" class="orders-section">
      <div v-if="orders.length === 0" class="no-orders">
        <p>暂无订单记录</p>
      </div>
      <div v-else class="order-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <h4>订单 #{{ order.id }}</h4>
            <span :class="['order-status', order.payment_status]">{{ getPaymentStatusLabel(order.payment_status) }}</span>
          </div>
          <div class="order-content">
            <p>商品: {{ getProductName(order.product_id) }}</p>
            <p>数量: {{ order.quantity }}</p>
            <p>总价: {{ order.total_price }} {{ order.currency }}</p>
            <p>创建时间: {{ formatTime(order.created_at) }}</p>
          </div>
          <div class="order-actions">
            <button 
              v-if="order.payment_status === 'pending'"
              @click="payOrder(order.id)"
              class="btn btn-warning"
            >
              支付
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// 响应式数据
const activeTab = ref('products');
const products = ref([]);
const orders = ref([]);
const rechargeAmount = ref(0);
const rechargeCurrency = ref('diamond');
const currentUser = ref({ id: 1, level: 1 }); // 假设当前用户ID为1，等级为1

// 标签页配置
const shopTabs = [
  { label: '商品列表', value: 'products' },
  { label: '充值中心', value: 'recharge' },
  { label: '订单记录', value: 'orders' }
];

// 获取商品列表
const fetchProducts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/products');
    products.value = response.data;
  } catch (error) {
    console.error('获取商品列表失败:', error);
  }
};

// 获取用户订单
const fetchOrders = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/orders/${currentUser.value.id}`);
    orders.value = response.data;
  } catch (error) {
    console.error('获取订单列表失败:', error);
  }
};

// 获取商品类型标签
const getProductTypeLabel = (type) => {
  const typeMap = {
    'item': '物品',
    'currency': '货币',
    'special': '特殊'
  };
  return typeMap[type] || type;
};

// 获取支付状态标签
const getPaymentStatusLabel = (status) => {
  const statusMap = {
    'pending': '待支付',
    'completed': '已完成',
    'failed': '失败'
  };
  return statusMap[status] || status;
};

// 获取商品名称
const getProductName = (productId) => {
  const product = products.value.find(p => p.id === productId);
  return product ? product.name : `商品${productId}`;
};

// 检查是否可以购买商品
const canBuyProduct = (product) => {
  return currentUser.value.level >= product.level_requirement;
};

// 购买商品
const buyProduct = async (product) => {
  try {
    await axios.post('http://localhost:8000/orders', {
      user_id: currentUser.value.id,
      product_id: product.id,
      quantity: 1
    });
    alert('购买成功');
    fetchOrders();
  } catch (error) {
    console.error('购买商品失败:', error);
    alert('购买商品失败');
  }
};

// 支付订单
const payOrder = async (orderId) => {
  try {
    await axios.post(`http://localhost:8000/orders/${orderId}/pay`);
    alert('支付成功');
    fetchOrders();
  } catch (error) {
    console.error('支付订单失败:', error);
    alert('支付订单失败');
  }
};

// 充值
const recharge = async () => {
  if (rechargeAmount.value <= 0) {
    alert('请输入有效的充值金额');
    return;
  }
  
  try {
    await axios.post('http://localhost:8000/recharge', {
      user_id: currentUser.value.id,
      amount: rechargeAmount.value,
      currency: rechargeCurrency.value
    });
    alert('充值成功');
    rechargeAmount.value = 0;
    fetchOrders();
  } catch (error) {
    console.error('充值失败:', error);
    alert('充值失败');
  }
};

// 格式化时间
const formatTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

// 组件挂载时获取数据
onMounted(() => {
  fetchProducts();
  fetchOrders();
});
</script>

<style scoped>
.shop-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.shop-tabs {
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

.no-products,
.no-orders {
  text-align: center;
  padding: 40px 0;
  color: #666;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background: #f9f9f9;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.product-header h3 {
  margin: 0;
}

.product-price {
  font-size: 18px;
  font-weight: bold;
  color: #007bff;
}

.product-description {
  margin-bottom: 15px;
  color: #666;
}

.product-info {
  margin-bottom: 20px;
}

.product-info p {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

.product-actions {
  text-align: right;
}

.recharge-section {
  max-width: 500px;
  margin: 0 auto;
}

.recharge-form {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 30px;
}

.recharge-form h3 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
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

.order-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.order-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background: #f9f9f9;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.order-header h4 {
  margin: 0;
}

.order-status {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
}

.order-status.pending {
  background: #ffc107;
  color: #212529;
}

.order-status.completed {
  background: #28a745;
  color: white;
}

.order-status.failed {
  background: #dc3545;
  color: white;
}

.order-content p {
  margin: 8px 0;
  font-size: 14px;
  color: #555;
}

.order-actions {
  margin-top: 15px;
  text-align: right;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0069d9;
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background: #e0a800;
}
</style>
