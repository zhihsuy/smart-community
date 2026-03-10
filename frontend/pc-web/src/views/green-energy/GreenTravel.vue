<template>
  <div class="green-travel">
    <div class="page-header">
      <h1>🚲 绿色出行规划</h1>
      <p>规划环保出行路线，减少碳排放</p>
    </div>

    <div class="content-section">
      <!-- 路线规划表单 -->
      <div class="route-planning-card">
        <h3>📍 路线规划</h3>
        
        <div class="route-form">
          <div class="form-row">
            <div class="form-group">
              <label>起点</label>
              <el-input v-model="routePlan.startPoint" placeholder="请输入起点地址" />
            </div>
            <div class="form-group">
              <label>终点</label>
              <el-input v-model="routePlan.endPoint" placeholder="请输入终点地址" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>出发时间</label>
              <el-date-picker
                v-model="routePlan.departureTime"
                type="datetime"
                placeholder="选择出发时间"
                class="w-full"
              />
            </div>
            <div class="form-group">
              <label>出行方式</label>
              <el-select v-model="routePlan.travelMode" placeholder="请选择出行方式" class="w-full">
                <el-option label="步行" value="walk" />
                <el-option label="自行车" value="bicycle" />
                <el-option label="公共交通" value="public" />
                <el-option label="私家车" value="car" />
                <el-option label="混合方式" value="mixed" />
              </el-select>
            </div>
          </div>

          <div class="form-actions">
            <el-button type="primary" @click="planRoute" :loading="planning">
              <el-icon><Location /></el-icon>
              规划路线
            </el-button>
            <el-button @click="resetForm">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </div>
        </div>
      </div>

      <!-- 路线规划结果 -->
      <div v-if="routeResult" class="route-result-section">
        <div class="result-grid">
          <!-- 地图区域 -->
          <div class="map-area">
            <div class="map-placeholder">
              <div class="map-icon">🗺️</div>
              <p>地图区域</p>
              <p class="map-info">{{ routePlan.startPoint }} → {{ routePlan.endPoint }}</p>
            </div>
          </div>

          <!-- 路线信息 -->
          <div class="route-info">
            <h4>📋 路线信息</h4>
            <div class="info-grid">
              <div class="info-item">
                <div class="info-icon">📏</div>
                <div class="info-content">
                  <div class="info-label">总距离</div>
                  <div class="info-value">{{ routeResult.distance }} 公里</div>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon">⏱️</div>
                <div class="info-content">
                  <div class="info-label">预计时间</div>
                  <div class="info-value">{{ routeResult.duration }} 分钟</div>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon">💰</div>
                <div class="info-content">
                  <div class="info-label">预计费用</div>
                  <div class="info-value">¥{{ routeResult.cost }}</div>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon">🌱</div>
                <div class="info-content">
                  <div class="info-label">碳排放</div>
                  <div class="info-value eco-friendly">{{ routeResult.carbonEmission }} kg CO₂</div>
                </div>
              </div>
            </div>

            <div class="route-details">
              <h5>路线详情</h5>
              <div class="detail-list">
                <div 
                  v-for="(step, index) in routeResult.steps" 
                  :key="index"
                  class="detail-item"
                >
                  <div class="step-number">{{ index + 1 }}</div>
                  <div class="step-content">
                    <div class="step-action">{{ step.action }}</div>
                    <div class="step-info">{{ step.info }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 出行方式比较 -->
        <div class="comparison-section">
          <h4>🔄 出行方式比较</h4>
          <div class="comparison-grid">
            <div 
              v-for="mode in travelModes" 
              :key="mode.id"
              class="comparison-card"
              :class="{ recommended: mode.recommended }"
            >
              <div class="comparison-header">
                <div class="mode-icon">{{ mode.icon }}</div>
                <h5>{{ mode.name }}</h5>
                <span v-if="mode.recommended" class="recommended-badge">推荐</span>
              </div>
              <div class="comparison-content">
                <div class="comparison-item">
                  <span class="comparison-label">时间</span>
                  <span class="comparison-value">{{ mode.duration }} 分钟</span>
                </div>
                <div class="comparison-item">
                  <span class="comparison-label">费用</span>
                  <span class="comparison-value">¥{{ mode.cost }}</span>
                </div>
                <div class="comparison-item">
                  <span class="comparison-label">碳排放</span>
                  <span class="comparison-value" :class="mode.carbonClass">{{ mode.carbonEmission }} kg CO₂</span>
                </div>
                <div class="comparison-item">
                  <span class="comparison-label">健康指数</span>
                  <span class="comparison-value">{{ mode.healthIndex }} ⭐</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 环保建议 -->
        <div class="eco-tips-section">
          <h4>💡 环保出行建议</h4>
          <div class="tips-list">
            <div 
              v-for="(tip, index) in ecoTips" 
              :key="index"
              class="tip-item"
            >
              <div class="tip-icon">{{ tip.icon }}</div>
              <div class="tip-content">
                <h5>{{ tip.title }}</h5>
                <p>{{ tip.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 常用路线 -->
      <div class="saved-routes-section">
        <h3>📌 常用路线</h3>
        <div class="saved-routes-list">
          <div 
            v-for="(route, index) in savedRoutes" 
            :key="index"
            class="saved-route-item"
            @click="useSavedRoute(route)"
          >
            <div class="route-info">
              <div class="route-start-end">
                <span class="route-point">{{ route.startPoint }}</span>
                <span class="route-arrow">→</span>
                <span class="route-point">{{ route.endPoint }}</span>
              </div>
              <div class="route-details">
                <span class="route-detail">{{ route.distance }} 公里</span>
                <span class="route-detail">{{ route.duration }} 分钟</span>
                <span class="route-detail">{{ route.travelMode }}</span>
              </div>
            </div>
            <div class="route-actions">
              <el-button type="primary" size="small">
                使用
              </el-button>
              <el-button type="danger" size="small" @click.stop="deleteSavedRoute(index)">
                删除
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Location, Refresh } from '@element-plus/icons-vue'

const planning = ref(false)
const routePlan = ref({
  startPoint: '',
  endPoint: '',
  departureTime: null,
  travelMode: 'public'
})

const routeResult = ref(null)

const travelModes = ref([
  {
    id: 'walk',
    name: '步行',
    icon: '🚶',
    duration: 45,
    cost: 0,
    carbonEmission: 0,
    healthIndex: 5,
    carbonClass: 'excellent',
    recommended: false
  },
  {
    id: 'bicycle',
    name: '自行车',
    icon: '🚲',
    duration: 20,
    cost: 0,
    carbonEmission: 0,
    healthIndex: 4,
    carbonClass: 'excellent',
    recommended: true
  },
  {
    id: 'public',
    name: '公共交通',
    icon: '🚌',
    duration: 30,
    cost: 3,
    carbonEmission: 0.5,
    healthIndex: 3,
    carbonClass: 'good',
    recommended: false
  },
  {
    id: 'car',
    name: '私家车',
    icon: '🚗',
    duration: 15,
    cost: 15,
    carbonEmission: 2.5,
    healthIndex: 1,
    carbonClass: 'poor',
    recommended: false
  }
])

const ecoTips = ref([
  {
    icon: '🚲',
    title: '优先选择绿色出行方式',
    description: '在短途出行时，优先选择步行或自行车。这不仅环保，还有益于身体健康。'
  },
  {
    icon: '🚌',
    title: '充分利用公共交通',
    description: '中长途出行时，选择公共交通可以显著减少碳排放，同时节省停车费用。'
  },
  {
    icon: '🚗',
    title: '拼车出行',
    description: '如果必须使用私家车，可以尝试拼车，减少车辆使用数量和碳排放。'
  },
  {
    icon: '📱',
    title: '使用导航软件',
    description: '使用智能导航软件，选择最优路线，避免拥堵，减少不必要的绕行。'
  }
])

const savedRoutes = ref([
  {
    startPoint: '社区中心',
    endPoint: '地铁站',
    distance: 1.5,
    duration: 10,
    travelMode: '自行车'
  },
  {
    startPoint: '家',
    endPoint: '公司',
    distance: 8.5,
    duration: 35,
    travelMode: '公共交通'
  }
])

const planRoute = () => {
  if (!routePlan.value.startPoint || !routePlan.value.endPoint) {
    alert('请输入起点和终点')
    return
  }

  planning.value = true

  // 模拟路线规划
  setTimeout(() => {
    routeResult.value = {
      distance: 8.5,
      duration: 35,
      cost: 3,
      carbonEmission: 0.5,
      steps: [
        {
          action: '步行至公交站',
          info: '从起点步行至最近的公交站，约5分钟'
        },
        {
          action: '乘坐公交车',
          info: '乘坐123路公交车，经过8站，约25分钟'
        },
        {
          action: '步行至终点',
          info: '从公交站步行至终点，约5分钟'
        }
      ]
    }

    planning.value = false
  }, 1500)
}

const resetForm = () => {
  routePlan.value = {
    startPoint: '',
    endPoint: '',
    departureTime: null,
    travelMode: 'public'
  }
  routeResult.value = null
}

const useSavedRoute = (route) => {
  routePlan.value.startPoint = route.startPoint
  routePlan.value.endPoint = route.endPoint
  routePlan.value.travelMode = route.travelMode
  planRoute()
}

const deleteSavedRoute = (index) => {
  savedRoutes.value.splice(index, 1)
}
</script>

<style scoped>
.green-travel {
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

.route-planning-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
}

.route-planning-card h3 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 20px;
}

.route-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
}

.route-result-section {
  margin-bottom: 40px;
}

.result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.map-area {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.map-placeholder {
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f0fdf4;
  color: #666;
}

.map-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.map-info {
  font-size: 16px;
  font-weight: 500;
  color: #10b981;
}

.route-info {
  background: white;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.route-info h4 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 18px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
}

.info-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.info-value {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.info-value.eco-friendly {
  color: #10b981;
}

.route-details {
  margin-top: 25px;
}

.route-details h5 {
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
}

.detail-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #10b981;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-action {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.step-info {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.comparison-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.comparison-section h4 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 18px;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.comparison-card {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.comparison-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.comparison-card.recommended {
  border-color: #10b981;
  background: #f0fdf4;
}

.comparison-header {
  padding: 15px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
}

.mode-icon {
  font-size: 24px;
}

.comparison-header h5 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.recommended-badge {
  margin-left: auto;
  padding: 4px 12px;
  background: #10b981;
  color: white;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.comparison-content {
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comparison-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.comparison-label {
  color: #666;
}

.comparison-value {
  font-weight: 600;
  color: #333;
}

.comparison-value.excellent {
  color: #10b981;
}

.comparison-value.good {
  color: #3b82f6;
}

.comparison-value.poor {
  color: #ef4444;
}

.eco-tips-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.eco-tips-section h4 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 18px;
}

.tips-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
}

.tip-icon {
  font-size: 32px;
  flex-shrink: 0;
  color: #10b981;
}

.tip-content h5 {
  font-size: 16px;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.tip-content p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin: 0;
}

.saved-routes-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.saved-routes-section h3 {
  margin-bottom: 20px;
  color: #10b981;
  font-size: 20px;
}

.saved-routes-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.saved-route-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.saved-route-item:hover {
  background: #f0fdf4;
  transform: translateX(5px);
}

.route-info {
  flex: 1;
}

.route-start-end {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.route-point {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.route-arrow {
  color: #10b981;
  font-size: 18px;
}

.route-details {
  display: flex;
  gap: 15px;
}

.route-detail {
  font-size: 14px;
  color: #666;
}

.route-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
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
  
  .route-planning-card {
    padding: 20px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .result-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .comparison-grid {
    grid-template-columns: 1fr;
  }
  
  .tips-list {
    grid-template-columns: 1fr;
  }
  
  .saved-route-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .route-actions {
    width: 100%;
  }
}
</style>