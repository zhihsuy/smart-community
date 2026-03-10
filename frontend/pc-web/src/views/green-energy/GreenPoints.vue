<template>
  <div class="green-points">
    <div class="page-header">
      <h1>🎯 绿色积分系统</h1>
      <p>通过环保行为获得积分，兑换丰富奖励</p>
    </div>

    <div class="content-section">
      <!-- 积分概览 -->
      <div class="points-overview">
        <div class="overview-card">
          <div class="overview-icon">🏆</div>
          <div class="overview-info">
            <div class="overview-value">{{ userPoints.total }}</div>
            <div class="overview-label">总积分</div>
          </div>
        </div>
        <div class="overview-card">
          <div class="overview-icon">📈</div>
          <div class="overview-info">
            <div class="overview-value">{{ userPoints.available }}</div>
            <div class="overview-label">可用积分</div>
          </div>
        </div>
        <div class="overview-card">
          <div class="overview-icon">🎁</div>
          <div class="overview-info">
            <div class="overview-value">{{ userPoints.redeemed }}</div>
            <div class="overview-label">已兑换积分</div>
          </div>
        </div>
        <div class="overview-card">
          <div class="overview-icon">⭐</div>
          <div class="overview-info">
            <div class="overview-value">{{ userPoints.level }}</div>
            <div class="overview-label">环保等级</div>
          </div>
        </div>
      </div>

      <!-- 积分获取方式 -->
      <div class="points-earn-section">
        <h3>📊 积分获取方式</h3>
        <div class="earn-grid">
          <div 
            v-for="item in earnWays" 
            :key="item.id"
            class="earn-card"
          >
            <div class="earn-icon">{{ item.icon }}</div>
            <h4>{{ item.title }}</h4>
            <p>{{ item.description }}</p>
            <div class="earn-points">+{{ item.points }} 积分</div>
          </div>
        </div>
      </div>

      <!-- 积分商城 -->
      <div class="points-mall-section">
        <h3>🛍️ 积分商城</h3>
        <div class="mall-filters">
          <el-select
            v-model="selectedCategory"
            placeholder="按分类筛选"
            @change="filterRewards"
          >
            <el-option label="全部" value="all" />
            <el-option label="实物奖品" value="physical" />
            <el-option label="虚拟奖品" value="virtual" />
            <el-option label="优惠券" value="coupon" />
            <el-option label="服务" value="service" />
          </el-select>
          <el-select
            v-model="pointsRange"
            placeholder="按积分范围筛选"
            @change="filterRewards"
          >
            <el-option label="全部" value="all" />
            <el-option label="0-1000" value="0-1000" />
            <el-option label="1000-5000" value="1000-5000" />
            <el-option label="5000+" value="5000+" />
          </el-select>
        </div>

        <div class="rewards-grid">
          <div 
            v-for="reward in filteredRewards" 
            :key="reward.id"
            class="reward-card"
            @click="viewRewardDetail(reward)"
          >
            <div class="reward-image">
              <div class="image-placeholder">{{ reward.icon }}</div>
            </div>
            <div class="reward-info">
              <h4 class="reward-name">{{ reward.name }}</h4>
              <p class="reward-description">{{ reward.description.substring(0, 60) }}...</p>
              <div class="reward-price">
                <span class="price-points">{{ reward.points }} 积分</span>
                <span class="price-stock" v-if="reward.stock > 0">库存: {{ reward.stock }}</span>
                <span class="price-stock out-of-stock" v-else>已售罄</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 积分记录 -->
      <div class="points-history-section">
        <h3>📋 积分记录</h3>
        <el-table :data="pointsHistory" style="width: 100%">
          <el-table-column prop="date" label="日期" width="180" />
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="points" label="积分" width="120" />
          <el-table-column prop="type" label="类型" width="100" />
        </el-table>
      </div>

      <!-- 奖励详情对话框 -->
      <el-dialog
        v-model="showRewardDetail"
        :title="selectedReward.name"
        width="600px"
      >
        <div class="reward-detail">
          <div class="reward-detail-image">
            <div class="image-placeholder">{{ selectedReward.icon }}</div>
          </div>
          <div class="reward-detail-info">
            <h4 class="reward-name">{{ selectedReward.name }}</h4>
            <p class="reward-description">{{ selectedReward.description }}</p>
            <div class="reward-price">
              <span class="price-points">{{ selectedReward.points }} 积分</span>
              <span class="price-stock" v-if="selectedReward.stock > 0">库存: {{ selectedReward.stock }}</span>
              <span class="price-stock out-of-stock" v-else>已售罄</span>
            </div>
            <div class="reward-category">
              <span class="category-label">分类:</span>
              <span class="category-value">{{ getCategoryName(selectedReward.category) }}</span>
            </div>
            <div class="reward-expiry" v-if="selectedReward.expiryDate">
              <span class="expiry-label">有效期:</span>
              <span class="expiry-value">{{ selectedReward.expiryDate }}</span>
            </div>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showRewardDetail = false">关闭</el-button>
            <el-button 
              type="primary" 
              @click="redeemReward" 
              :disabled="selectedReward.stock <= 0 || userPoints.available < selectedReward.points"
            >
              兑换
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const userPoints = ref({
  total: 2500,
  available: 1800,
  redeemed: 700,
  level: 3
})

const selectedCategory = ref('all')
const pointsRange = ref('all')
const showRewardDetail = ref(false)
const selectedReward = ref({})

const earnWays = ref([
  {
    id: 1,
    icon: '♻️',
    title: '垃圾分类',
    description: '正确分类垃圾并投放到指定垃圾桶',
    points: 5
  },
  {
    id: 2,
    icon: '🚲',
    title: '绿色出行',
    description: '使用公共交通、自行车或步行出行',
    points: 10
  },
  {
    id: 3,
    icon: '💡',
    title: '节能行为',
    description: '关闭不必要的电器，合理使用空调',
    points: 8
  },
  {
    id: 4,
    icon: '🌱',
    title: '参与环保活动',
    description: '参加社区组织的环保活动',
    points: 20
  },
  {
    id: 5,
    icon: '📝',
    title: '分享环保知识',
    description: '在社区论坛分享环保知识和经验',
    points: 15
  },
  {
    id: 6,
    icon: '🛒',
    title: '绿色购物',
    description: '购买环保产品，减少一次性用品使用',
    points: 12
  }
])

const rewards = ref([
  {
    id: 1,
    name: '环保购物袋',
    description: '可重复使用的环保购物袋，减少塑料袋使用',
    icon: '🛍️',
    points: 500,
    category: 'physical',
    stock: 50,
    expiryDate: '2026-12-31'
  },
  {
    id: 2,
    name: 'LED节能灯泡',
    description: '节能LED灯泡，比传统灯泡节能80%以上',
    icon: '💡',
    points: 300,
    category: 'physical',
    stock: 30,
    expiryDate: '2026-12-31'
  },
  {
    id: 3,
    name: '环保电子书',
    description: '环保主题电子书，了解更多环保知识',
    icon: '📚',
    points: 200,
    category: 'virtual',
    stock: 100,
    expiryDate: '2026-12-31'
  },
  {
    id: 4,
    name: '绿色出行优惠券',
    description: '公共交通优惠券，鼓励绿色出行',
    icon: '🚌',
    points: 150,
    category: 'coupon',
    stock: 200,
    expiryDate: '2026-06-30'
  },
  {
    id: 5,
    name: '环保讲座门票',
    description: '免费参加环保主题讲座',
    icon: '🎫',
    points: 800,
    category: 'service',
    stock: 20,
    expiryDate: '2026-04-30'
  },
  {
    id: 6,
    name: '有机蔬菜礼盒',
    description: '新鲜有机蔬菜礼盒，健康又环保',
    icon: '🥬',
    points: 1200,
    category: 'physical',
    stock: 10,
    expiryDate: '2026-03-31'
  }
])

const pointsHistory = ref([
  { date: '2026-03-01', description: '参与社区绿化活动', points: '+20', type: '获得' },
  { date: '2026-02-28', description: '兑换环保购物袋', points: '-500', type: '兑换' },
  { date: '2026-02-25', description: '绿色出行', points: '+10', type: '获得' },
  { date: '2026-02-20', description: '垃圾分类', points: '+5', type: '获得' },
  { date: '2026-02-15', description: '分享环保知识', points: '+15', type: '获得' },
  { date: '2026-02-10', description: '绿色购物', points: '+12', type: '获得' }
])

const filteredRewards = computed(() => {
  let result = [...rewards.value]
  
  // 按分类筛选
  if (selectedCategory.value !== 'all') {
    result = result.filter(reward => reward.category === selectedCategory.value)
  }
  
  // 按积分范围筛选
  if (pointsRange.value !== 'all') {
    const [min, max] = pointsRange.value.split('-')
    if (max) {
      result = result.filter(reward => reward.points >= parseInt(min) && reward.points <= parseInt(max))
    } else {
      result = result.filter(reward => reward.points >= parseInt(min))
    }
  }
  
  return result
})

const filterRewards = () => {
  // 筛选逻辑已在computed属性中处理
}

const viewRewardDetail = (reward) => {
  selectedReward.value = { ...reward }
  showRewardDetail.value = true
}

const redeemReward = () => {
  if (selectedReward.value.stock <= 0 || userPoints.value.available < selectedReward.value.points) {
    return
  }
  
  // 扣除积分
  userPoints.value.available -= selectedReward.value.points
  userPoints.value.redeemed += selectedReward.value.points
  
  // 减少库存
  selectedReward.value.stock--
  const index = rewards.value.findIndex(r => r.id === selectedReward.value.id)
  if (index !== -1) {
    rewards.value[index].stock--
  }
  
  // 添加积分记录
  pointsHistory.value.unshift({
    date: new Date().toISOString().split('T')[0],
    description: `兑换${selectedReward.value.name}`,
    points: `-${selectedReward.value.points}`,
    type: '兑换'
  })
  
  // 关闭对话框
  showRewardDetail.value = false
  
  // 显示成功提示
  alert('兑换成功！')
}

const getCategoryName = (category) => {
  const categoryMap = {
    'physical': '实物奖品',
    'virtual': '虚拟奖品',
    'coupon': '优惠券',
    'service': '服务'
  }
  return categoryMap[category] || '其他'
}
</script>

<style scoped>
.green-points {
  min-height: 100vh;
  background: #f8fafc;
}

.page-header {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
}

.page-header h1 {
  font-size: 36px;
  margin-bottom: 10px;
  font-weight: 600;
}

.page-header p {
  font-size: 18px;
  opacity: 0.9;
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.points-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.overview-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.overview-icon {
  font-size: 48px;
  flex-shrink: 0;
}

.overview-info {
  flex: 1;
}

.overview-value {
  font-size: 32px;
  font-weight: 600;
  color: #10b981;
  margin-bottom: 5px;
}

.overview-label {
  font-size: 14px;
  color: #666;
}

.points-earn-section {
  margin-bottom: 60px;
}

.points-earn-section h3 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #10b981;
}

.earn-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.earn-card {
  background: white;
  border-radius: 8px;
  padding: 25px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.earn-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.earn-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.earn-card h4 {
  font-size: 16px;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.earn-card p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 15px;
}

.earn-points {
  font-size: 18px;
  font-weight: 600;
  color: #10b981;
}

.points-mall-section {
  margin-bottom: 60px;
}

.points-mall-section h3 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #10b981;
}

.mall-filters {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.rewards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.reward-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.reward-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.reward-image {
  height: 200px;
  background: #f0fdf4;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder {
  font-size: 64px;
}

.reward-info {
  padding: 20px;
}

.reward-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.reward-description {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 15px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.reward-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-points {
  font-size: 18px;
  font-weight: 600;
  color: #10b981;
}

.price-stock {
  font-size: 14px;
  color: #666;
}

.price-stock.out-of-stock {
  color: #ef4444;
}

.points-history-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.points-history-section h3 {
  text-align: center;
  font-size: 20px;
  margin-bottom: 20px;
  color: #10b981;
}

.reward-detail {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.reward-detail-image {
  flex: 1;
  min-width: 150px;
  height: 200px;
  background: #f0fdf4;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.reward-detail-info {
  flex: 2;
}

.reward-detail-info .reward-name {
  font-size: 20px;
  margin-bottom: 15px;
}

.reward-detail-info .reward-description {
  margin-bottom: 20px;
  overflow: visible;
  display: block;
}

.reward-category {
  display: flex;
  margin-bottom: 10px;
}

.category-label {
  width: 80px;
  font-size: 14px;
  color: #666;
}

.category-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.reward-expiry {
  display: flex;
  margin-bottom: 10px;
}

.expiry-label {
  width: 80px;
  font-size: 14px;
  color: #666;
}

.expiry-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

@media (max-width: 768px) {
  .page-header {
    padding: 40px 20px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .content-section {
    padding: 20px;
  }
  
  .points-overview {
    grid-template-columns: 1fr;
  }
  
  .earn-grid {
    grid-template-columns: 1fr;
  }
  
  .mall-filters {
    flex-direction: column;
  }
  
  .rewards-grid {
    grid-template-columns: 1fr;
  }
  
  .reward-detail {
    flex-direction: column;
  }
  
  .reward-detail-image {
    width: 100%;
  }
  
  .points-history-section {
    padding: 20px;
  }
}
</style>