<template>
  <AdminLayout>
    <div class="admin-dashboard">
      <!-- 欢迎区域 -->
      <div class="welcome-section">
        <div class="welcome-content">
          <div class="welcome-info">
            <h2 class="welcome-title">下午好，欢迎登录</h2>
            <p class="welcome-desc">一站式智能管理解决方案，提高管理效率</p>
            <button class="welcome-btn">
              <span>📈</span>
              <span>查看完整数据</span>
            </button>
          </div>
          <div class="welcome-illustration">
            <div class="illustration-content">
              <div class="illustration-icon">👩‍💻</div>
              <div class="illustration-elements">
                <div class="element element-1">📊</div>
                <div class="element element-2">💡</div>
                <div class="element element-3">🎯</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 今日核心指标 -->
      <div class="core-metrics">
        <h3 class="section-title">今日核心指标</h3>
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">今日进出人次</span>
              <span class="metric-trend up">+12.3%</span>
            </div>
            <div class="metric-value">{{ stats.todayAccess || 156 }}</div>
            <div class="metric-compare">同比昨日</div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">今日报修工单</span>
              <span class="metric-trend up">+8.7%</span>
            </div>
            <div class="metric-value">{{ stats.todayRepairs || 8 }}</div>
            <div class="metric-compare">同比昨日</div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">待处理事项</span>
              <span class="metric-trend down">-5.2%</span>
            </div>
            <div class="metric-value">{{ stats.pendingTasks || 23 }}</div>
            <div class="metric-compare">同比昨日</div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">费用收缴率</span>
              <span class="metric-trend up">+3.5%</span>
            </div>
            <div class="metric-value">{{ stats.paymentRate || '87.5%' }}</div>
            <div class="metric-compare">同比上月</div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">设备在线率</span>
              <span class="metric-trend up">+1.2%</span>
            </div>
            <div class="metric-value">{{ stats.deviceOnlineRate || '98.7%' }}</div>
            <div class="metric-compare">同比昨日</div>
          </div>
        </div>
      </div>

      <!-- 社区数据统计 -->
      <div class="stats-grid">
        <div class="stat-section">
          <div class="stat-header">
            <h3 class="section-title">社区进出统计</h3>
            <div class="stat-value large">{{ stats.totalAccess || '1,256,789' }}</div>
          </div>
          <div class="traffic-chart">
            <div class="traffic-item">
              <div class="traffic-circle blue">
                <div class="circle-percentage">65%</div>
              </div>
              <div class="traffic-info">
                <div class="traffic-label">居民进出</div>
                <div class="traffic-value">{{ stats.residentAccess || '816,913' }}</div>
              </div>
            </div>
            <div class="traffic-item">
              <div class="traffic-circle green">
                <div class="circle-percentage">25%</div>
              </div>
              <div class="traffic-info">
                <div class="traffic-label">访客进出</div>
                <div class="traffic-value">{{ stats.visitorAccess || '314,197' }}</div>
              </div>
            </div>
            <div class="traffic-item">
              <div class="traffic-circle gray">
                <div class="circle-percentage">10%</div>
              </div>
              <div class="traffic-info">
                <div class="traffic-label">其他进出</div>
                <div class="traffic-value">{{ stats.otherAccess || '125,679' }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 月度数据趋势 -->
        <div class="stat-section">
          <div class="stat-header">
            <h3 class="section-title">月度报修趋势</h3>
            <div class="date-selector">
              <span>最近一个月</span>
              <span class="selector-arrow">▼</span>
            </div>
          </div>
          <div class="trend-chart">
            <div class="chart-placeholder">
              <div class="chart-bars">
                <div class="bar" style="height: 60%"></div>
                <div class="bar" style="height: 45%"></div>
                <div class="bar" style="height: 70%"></div>
                <div class="bar" style="height: 50%"></div>
                <div class="bar" style="height: 80%"></div>
                <div class="bar" style="height: 65%"></div>
                <div class="bar" style="height: 90%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 社区待办与满意度 -->
      <div class="stats-grid">
        <div class="stat-section">
          <div class="stat-header">
            <h3 class="section-title">社区待办事项</h3>
          </div>
          <div class="alerts-list">
            <div class="alert-item warning">
              <div class="alert-icon">⚠️</div>
              <div class="alert-content">
                <div class="alert-title">未出账单达3期以上</div>
                <div class="alert-desc">请及时处理，避免影响信用</div>
              </div>
            </div>
            <div class="alert-item info">
              <div class="alert-icon">ℹ️</div>
              <div class="alert-content">
                <div class="alert-title">设备维护</div>
                <div class="alert-desc">5号楼电梯需要定期维护，请安排技术人员</div>
              </div>
            </div>
            <div class="alert-item danger">
              <div class="alert-icon">🚨</div>
              <div class="alert-content">
                <div class="alert-title">紧急报修</div>
                <div class="alert-desc">3号楼2单元水管漏水，需要紧急处理</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 社区满意度 -->
        <div class="stat-section">
          <div class="stat-header">
            <h3 class="section-title">社区满意度</h3>
          </div>
          <div class="satisfaction-card">
            <div class="satisfaction-score">4.8<span>/5.0</span></div>
            <div class="satisfaction-stars">⭐⭐⭐⭐⭐</div>
            <div class="satisfaction-desc">本月满意度 4.8/5.0</div>
            <div class="satisfaction-tip">继续保持优质服务</div>
          </div>
        </div>
      </div>

      <!-- 监控管理数据 -->
      <div class="monitoring-stats">
        <h3 class="section-title">监控管理数据</h3>
        <div class="monitoring-stats-grid">
          <!-- 左侧饼状图 -->
          <div class="monitoring-chart-section">
            <div class="chart-container">
              <div class="pie-chart">
                <div class="pie-chart-inner">
                  <div class="pie-chart-segment online" :style="{ '--percentage': onlinePercentage }" v-if="onlinePercentage > 0"></div>
                  <div class="pie-chart-segment offline" :style="{ '--percentage': offlinePercentage }" v-if="offlinePercentage > 0"></div>
                  <div class="pie-chart-center">
                    <div class="center-percentage">{{ Math.round((onlinePercentage / 100) * 100) }}%</div>
                    <div class="center-label">在线率</div>
                  </div>
                </div>
              </div>
              <div class="chart-legend">
                <div class="legend-item">
                  <div class="legend-color online"></div>
                  <span>在线设备 ({{ stats.onlineDevices || 14 }})</span>
                </div>
                <div class="legend-item">
                  <div class="legend-color offline"></div>
                  <span>离线设备 ({{ offlineDevices }})</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 右侧数据详情 -->
          <div class="monitoring-details">
            <div class="monitoring-detail-item">
              <div class="detail-icon total">
                <el-icon><i-ep-video-camera /></el-icon>
              </div>
              <div class="detail-content">
                <div class="detail-value">{{ stats.monitoringDevices || 16 }}</div>
                <div class="detail-label">监控设备总数</div>
              </div>
            </div>
            <div class="monitoring-detail-item">
              <div class="detail-icon online">
                <el-icon><i-ep-check /></el-icon>
              </div>
              <div class="detail-content">
                <div class="detail-value">{{ stats.onlineDevices || 14 }}</div>
                <div class="detail-label">在线设备</div>
              </div>
            </div>
            <div class="monitoring-detail-item">
              <div class="detail-icon offline">
                <el-icon><i-ep-close /></el-icon>
              </div>
              <div class="detail-content">
                <div class="detail-value">{{ offlineDevices }}</div>
                <div class="detail-label">离线设备</div>
              </div>
            </div>
            <div class="monitoring-detail-item">
              <div class="detail-icon alert">
                <el-icon><i-ep-warning /></el-icon>
              </div>
              <div class="detail-content">
                <div class="detail-value">{{ stats.alertCount || 3 }}</div>
                <div class="detail-label">预警数量</div>
              </div>
            </div>
            <div class="monitoring-detail-item">
              <div class="detail-icon request">
                <el-icon><i-ep-document /></el-icon>
              </div>
              <div class="detail-content">
                <div class="detail-value">{{ stats.pendingRequests || 2 }}</div>
                <div class="detail-label">待审批申请</div>
              </div>
            </div>
            <div class="monitoring-action">
              <button @click="goToPage('/admin/monitoring')" class="action-button">
                <el-icon><i-ep-setting /></el-icon>
                <span>管理监控系统</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 智慧社区管理数据 -->
      <div class="smart-community-stats">
        <h3 class="section-title">智慧社区管理数据</h3>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon primary">
              <el-icon><i-ep-lock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.accessDevices || 24 }}</div>
              <div class="stat-label">门禁设备</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/access-control/devices')" class="action-link">管理</button>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon success">
              <el-icon><i-ep-notebook /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.accessRecords || 156 }}</div>
              <div class="stat-label">今日进出</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/access-control/records')" class="action-link">查看</button>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon warning">
              <el-icon><i-ep-tools /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pendingRepairs || 8 }}</div>
              <div class="stat-label">待修工单</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/repair/orders')" class="action-link">处理</button>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon danger">
              <el-icon><i-ep-message /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.activeNotices || 5 }}</div>
              <div class="stat-label">公告通知</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/notices')" class="action-link">管理</button>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon info">
              <el-icon><i-ep-water /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.utilityMeters || 120 }}</div>
              <div class="stat-label">智能表具</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/utility/meters')" class="action-link">管理</button>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon primary">
              <el-icon><i-ep-money /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pendingPayments || 15 }}</div>
              <div class="stat-label">待缴费用</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/payment')" class="action-link">管理</button>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon success">
              <el-icon><i-ep-car /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.freeParkings || 12 }}</div>
              <div class="stat-label">空闲车位</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/parking')" class="action-link">管理</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="quick-actions">
        <h3 class="section-title">快捷操作</h3>
        <div class="action-grid">
          <button @click="goToPage('/admin/access-control/devices')" class="action-btn primary">
            <span class="action-icon">🔒</span>
            <span class="action-text">智能门禁管理</span>
          </button>
          <button @click="goToPage('/admin/repair/orders')" class="action-btn warning">
            <span class="action-icon">🔧</span>
            <span class="action-text">物业报修管理</span>
          </button>
          <button @click="goToPage('/admin/notices')" class="action-btn success">
            <span class="action-icon">📢</span>
            <span class="action-text">公告通知管理</span>
          </button>
          <button @click="goToPage('/admin/utility/meters')" class="action-btn info">
            <span class="action-icon">💡</span>
            <span class="action-text">智能水电管理</span>
          </button>
          <button @click="goToPage('/admin/payment')" class="action-btn primary">
            <span class="action-icon">💰</span>
            <span class="action-text">费用缴纳管理</span>
          </button>
          <button @click="goToPage('/admin/parking')" class="action-btn warning">
            <span class="action-icon">🚗</span>
            <span class="action-text">智能停车管理</span>
          </button>
          <button @click="goToPage('/admin/locker')" class="action-btn success">
            <span class="action-icon">📦</span>
            <span class="action-text">快递柜管理</span>
          </button>
          <button @click="goToPage('/admin/visitor')" class="action-btn info">
            <span class="action-icon">👤</span>
            <span class="action-text">访客管理</span>
          </button>
          <button @click="goToPage('/admin/monitoring')" class="action-btn warning">
            <span class="action-icon">📹</span>
            <span class="action-text">监控管理</span>
          </button>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from '@/components/AdminLayout.vue'

const router = useRouter()
const stats = ref({
  userCount: 0,
  merchantCount: 0,
  goodsCount: 0,
  reviewCount: 0,
  buildingCount: 0,
  pendingMerchantCount: 0,
  todayUV: 67,
  yesterdayUV: 569,
  newUsers: 45,
  weekUV: 366,
  monthUV: 5639,
  totalTraffic: '601,986,875',
  // 智慧社区核心指标
  todayAccess: 156,
  todayRepairs: 8,
  pendingTasks: 23,
  paymentRate: '87.5%',
  deviceOnlineRate: '98.7%',
  // 智慧社区统计数据
  accessDevices: 24,
  accessRecords: 156,
  pendingRepairs: 8,
  totalRepairs: 45,
  activeNotices: 5,
  totalNotices: 23,
  utilityMeters: 120,
  pendingPayments: 15,
  totalParkings: 50,
  freeParkings: 12,
  // 监控管理数据
  monitoringDevices: 16,
  onlineDevices: 14,
  alertCount: 3,
  pendingRequests: 2,
  // 社区进出统计
  totalAccess: '1,256,789',
  residentAccess: 816913,
  visitorAccess: 314197,
  otherAccess: 125679,
  // 社区满意度
  satisfactionScore: 4.8,
  satisfactionLevel: '优秀'
})

const goToPage = (path) => {
  router.push(path)
}

// 计算属性
const onlineDevices = computed(() => {
  return stats.value.onlineDevices || 14
})

const totalDevices = computed(() => {
  return stats.value.monitoringDevices || 16
})

const offlineDevices = computed(() => {
  return totalDevices.value - onlineDevices.value
})

const onlinePercentage = computed(() => {
  if (totalDevices.value === 0) return 0
  return (onlineDevices.value / totalDevices.value) * 100
})

const offlinePercentage = computed(() => {
  return 100 - onlinePercentage.value
})

const loadStats = async () => {
  try {
    const response = await fetch('/api/v1/admin/stats', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      stats.value = { ...stats.value, ...(result.data || {}) }
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.admin-dashboard {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 欢迎区域 */
.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 40px;
  color: white;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  margin-bottom: 16px;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.welcome-info {
  flex: 1;
}

.welcome-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 12px 0;
  line-height: 1.2;
}

.welcome-desc {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.welcome-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.welcome-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.welcome-illustration {
  flex-shrink: 0;
  position: relative;
}

.illustration-content {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.illustration-icon {
  font-size: 48px;
  z-index: 2;
}

.illustration-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.element {
  position: absolute;
  font-size: 20px;
  animation: float 3s ease-in-out infinite;
}

.element-1 {
  top: 10px;
  left: 10px;
  animation-delay: 0s;
}

.element-2 {
  bottom: 10px;
  right: 10px;
  animation-delay: 1s;
}

.element-3 {
  top: 50%;
  right: 10px;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 核心指标 */
.core-metrics {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.metric-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: white;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 14px;
  color: #606266;
  font-weight: 400;
}

.metric-trend {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 10px;
}

.metric-trend.up {
  color: #67c23a;
  background: #f0f9eb;
}

.metric-trend.down {
  color: #f56c6c;
  background: #fef0f0;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.metric-compare {
  font-size: 12px;
  color: #909399;
}

/* 统计网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.stat-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.stat-value.large {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin: 0;
}

.date-selector {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #f5f7fa;
  border-radius: 6px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s ease;
}

.date-selector:hover {
  background: #e4e7ed;
}

.selector-arrow {
  font-size: 10px;
  color: #909399;
}

/* 流量图表 */
.traffic-chart {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.traffic-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.traffic-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
}

.traffic-circle.blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.traffic-circle.green {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
}

.traffic-circle.gray {
  background: linear-gradient(135deg, #909399 0%, #c0c4cc 100%);
  color: white;
}

.circle-percentage {
  font-size: 12px;
  font-weight: bold;
}

.traffic-info {
  flex: 1;
}

.traffic-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 4px;
}

.traffic-value {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

/* 趋势图表 */
.trend-chart {
  height: 200px;
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 20px 0;
}

.chart-placeholder {
  flex: 1;
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  width: 100%;
}

.bar {
  flex: 1;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px 4px 0 0;
  transition: all 0.3s ease;
  min-height: 20px;
}

.bar:hover {
  opacity: 0.8;
  transform: translateY(-2px);
}

/* 系统提示 */
.system-alerts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.alert-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.alert-item:hover {
  background: #e4e7ed;
  transform: translateY(-2px);
}

.alert-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.alert-desc {
  font-size: 12px;
  color: #606266;
}

/* 社区满意度卡片 */
.satisfaction-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 30px;
  color: white;
  text-align: center;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.satisfaction-score {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 12px;
}

.satisfaction-score span {
  font-size: 24px;
  font-weight: normal;
  opacity: 0.8;
}

.satisfaction-stars {
  font-size: 24px;
  margin-bottom: 16px;
  letter-spacing: 4px;
}

.satisfaction-desc {
  font-size: 16px;
  margin-bottom: 8px;
  opacity: 0.9;
}

.satisfaction-tip {
  font-size: 14px;
  opacity: 0.8;
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 16px;
  border-radius: 20px;
  margin-top: 8px;
}

/* 智慧社区管理数据 */
.smart-community-stats {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
}

.smart-community-stats .stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid #e4e7ed;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: white;
  border-color: #667eea;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.stat-icon.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.success {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
}

.stat-icon.warning {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
  color: white;
}

.stat-icon.danger {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  color: white;
}

.stat-icon.info {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.stat-action {
  flex-shrink: 0;
}

.action-link {
  padding: 6px 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-link:hover {
  background: #764ba2;
  transform: translateY(-1px);
}

/* 快捷操作 */
.quick-actions {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  font-size: 14px;
  font-weight: 500;
}

.action-icon {
  font-size: 32px;
}

.action-text {
  text-align: center;
  line-height: 1.4;
}

.action-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #f56c6c;
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: bold;
  min-width: 20px;
  text-align: center;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.warning {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
  color: white;
}

.action-btn.success {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
}

.action-btn.info {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
}

.action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* 监控管理数据 */
.monitoring-stats {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
}

.monitoring-stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: center;
}

.monitoring-chart-section {
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-container {
  text-align: center;
}

.pie-chart {
  width: 200px;
  height: 200px;
  margin: 0 auto 20px;
}

.pie-chart-inner {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #f5f7fa;
  overflow: hidden;
}

.pie-chart-segment {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transform-origin: center;
  clip-path: polygon(50% 50%, 50% 0%, 100% 0%, 100% 100%, 50% 100%);
}

.pie-chart-segment.online {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  transform: rotate(calc((var(--percentage) / 100) * 360deg));
}

.pie-chart-segment.offline {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  transform: rotate(180deg);
  clip-path: polygon(50% 50%, 50% 100%, 0% 100%, 0% 0%, 50% 0%);
}

.pie-chart-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 140px;
  height: 140px;
  background: white;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.center-percentage {
  font-size: 32px;
  font-weight: bold;
  color: #67c23a;
  margin-bottom: 4px;
}

.center-label {
  font-size: 14px;
  color: #606266;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.legend-color.online {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.legend-color.offline {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
}

.monitoring-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.monitoring-detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid #e4e7ed;
}

.monitoring-detail-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: white;
  border-color: #667eea;
}

.detail-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.detail-icon.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.detail-icon.online {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
}

.detail-icon.offline {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
  color: white;
}

.detail-icon.alert {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
  color: white;
}

.detail-icon.request {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
}

.detail-content {
  flex: 1;
}

.detail-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.detail-label {
  font-size: 12px;
  color: #606266;
}

.monitoring-action {
  grid-column: 1 / -1;
  margin-top: 8px;
}

.action-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .welcome-content {
    flex-direction: column;
    text-align: center;
    gap: 30px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .system-alerts {
    grid-template-columns: 1fr;
  }
  
  .monitoring-stats-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .monitoring-details {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .welcome-section {
    padding: 30px 20px;
  }
  
  .welcome-title {
    font-size: 24px;
  }
  
  .core-metrics,
  .stat-section,
  .alert-section,
  .quick-actions,
  .smart-community-stats {
    padding: 20px;
  }
  
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .smart-community-stats .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .action-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .action-btn {
    padding: 20px;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    padding: 16px;
  }
  
  .stat-info {
    text-align: center;
  }
  
  .stat-action {
    margin-top: 8px;
  }
  
  .satisfaction-card {
    padding: 20px;
  }
  
  .satisfaction-score {
    font-size: 36px;
  }
  
  .satisfaction-stars {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .smart-community-stats .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .welcome-section {
    padding: 20px 16px;
  }
  
  .welcome-title {
    font-size: 20px;
  }
  
  .core-metrics,
  .stat-section,
  .alert-section,
  .quick-actions,
  .smart-community-stats {
    padding: 16px;
  }
  
  .section-title {
    font-size: 16px;
  }
  
  .metric-value {
    font-size: 20px;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .stat-value.large {
    font-size: 24px;
  }
  
  .stat-card {
    padding: 12px;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
}
</style>
