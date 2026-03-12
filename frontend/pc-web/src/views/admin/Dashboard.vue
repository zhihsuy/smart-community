<template>
  <AdminLayout>
    <div class="admin-dashboard">
      <!-- 欢迎区域 -->
      <div class="welcome-section">
        <div class="welcome-content">
          <div class="welcome-info">
            <h2 class="welcome-title">下午好，欢迎登录</h2>
            <p class="welcome-desc">一站式智能管理解决方案，提高管理效率</p>
            <button class="welcome-btn" @click="refreshData">
              <span>📈</span>
              <span>刷新数据</span>
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

      <!-- 时间范围筛选 -->
      <div class="time-filter">
        <el-radio-group v-model="timeRange" @change="handleTimeRangeChange" size="large">
          <el-radio-button label="today">今日</el-radio-button>
          <el-radio-button label="week">本周</el-radio-button>
          <el-radio-button label="month">本月</el-radio-button>
        </el-radio-group>
        <div class="last-update" v-if="lastUpdateTime">
          最后更新: {{ lastUpdateTime }}
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
            <div class="metric-value">{{ overviewStats.todayAccessCount || 156 }}</div>
            <div class="metric-compare">同比昨日</div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">今日报修工单</span>
              <span class="metric-trend up">+8.7%</span>
            </div>
            <div class="metric-value">{{ overviewStats.todayRepairCount || 8 }}</div>
            <div class="metric-compare">同比昨日</div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">待处理事项</span>
              <span class="metric-trend down">-5.2%</span>
            </div>
            <div class="metric-value">{{ overviewStats.pendingComplaintCount || 23 }}</div>
            <div class="metric-compare">同比昨日</div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">待缴费用</span>
              <span class="metric-trend up">+3.5%</span>
            </div>
            <div class="metric-value">{{ overviewStats.pendingPaymentCount || 15 }}</div>
            <div class="metric-compare">同比上月</div>
          </div>
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-label">设备在线率</span>
              <span class="metric-trend up">+1.2%</span>
            </div>
            <div class="metric-value">{{ deviceOnlineRate }}%</div>
            <div class="metric-compare">同比昨日</div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="charts-grid">
        <!-- 用户增长趋势 -->
        <div class="chart-section">
          <div class="chart-header">
            <h3 class="section-title">用户增长趋势</h3>
            <div class="chart-legend">
              <span class="legend-item"><span class="legend-color user"></span>新增用户</span>
            </div>
          </div>
          <div ref="userTrendChart" class="chart-container"></div>
        </div>

        <!-- 报修趋势 -->
        <div class="chart-section">
          <div class="chart-header">
            <h3 class="section-title">报修趋势</h3>
            <div class="chart-legend">
              <span class="legend-item"><span class="legend-color repair"></span>报修数量</span>
            </div>
          </div>
          <div ref="repairTrendChart" class="chart-container"></div>
        </div>

        <!-- 门禁进出趋势 -->
        <div class="chart-section">
          <div class="chart-header">
            <h3 class="section-title">门禁进出趋势</h3>
            <div class="chart-legend">
              <span class="legend-item"><span class="legend-color access"></span>进出人次</span>
            </div>
          </div>
          <div ref="accessTrendChart" class="chart-container"></div>
        </div>

        <!-- 费用统计 -->
        <div class="chart-section">
          <div class="chart-header">
            <h3 class="section-title">费用统计</h3>
            <div class="chart-legend">
              <span class="legend-item"><span class="legend-color payment"></span>费用金额</span>
            </div>
          </div>
          <div ref="paymentChart" class="chart-container"></div>
        </div>
      </div>

      <!-- 报修状态分布 -->
      <div class="stats-grid">
        <div class="stat-section">
          <div class="stat-header">
            <h3 class="section-title">报修状态分布</h3>
          </div>
          <div ref="repairStatusChart" class="chart-container"></div>
        </div>

        <!-- 费用类型分布 -->
        <div class="stat-section">
          <div class="stat-header">
            <h3 class="section-title">费用类型分布</h3>
          </div>
          <div ref="paymentTypeChart" class="chart-container"></div>
        </div>
      </div>

      <!-- 水电使用趋势 -->
      <div class="chart-section full-width">
        <div class="chart-header">
          <h3 class="section-title">水电使用趋势</h3>
          <div class="chart-legend">
            <span class="legend-item"><span class="legend-color water"></span>水费</span>
            <span class="legend-item"><span class="legend-color electricity"></span>电费</span>
          </div>
        </div>
        <div ref="utilityChart" class="chart-container"></div>
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
              <div class="stat-value">{{ overviewStats.accessDeviceCount || 24 }}</div>
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
              <div class="stat-value">{{ overviewStats.todayAccessCount || 156 }}</div>
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
              <div class="stat-value">{{ overviewStats.todayRepairCount || 8 }}</div>
              <div class="stat-label">今日报修</div>
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
              <div class="stat-value">{{ overviewStats.activeNoticeCount || 5 }}</div>
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
              <div class="stat-value">{{ overviewStats.utilityCount || 120 }}</div>
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
              <div class="stat-value">{{ overviewStats.pendingPaymentCount || 15 }}</div>
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
              <div class="stat-value">{{ overviewStats.freeParkingCount || 12 }}</div>
              <div class="stat-label">空闲车位</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/parking')" class="action-link">管理</button>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon warning">
              <el-icon><i-ep-video-camera /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ overviewStats.onlineMonitoringCount || 14 }}</div>
              <div class="stat-label">在线监控</div>
            </div>
            <div class="stat-action">
              <button @click="goToPage('/admin/monitoring')" class="action-link">管理</button>
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
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import AdminLayout from '@/components/AdminLayout.vue'

const router = useRouter()

const timeRange = ref('week')
const lastUpdateTime = ref('')
const overviewStats = ref({
  userCount: 0,
  newUserCount: 0,
  buildingCount: 0,
  activityCount: 0,
  repairCount: 0,
  todayRepairCount: 0,
  accessDeviceCount: 0,
  todayAccessCount: 0,
  monitoringCount: 0,
  onlineMonitoringCount: 0,
  utilityCount: 0,
  parkingCount: 0,
  freeParkingCount: 0,
  noticeCount: 0,
  activeNoticeCount: 0,
  lockerCount: 0,
  pendingPaymentCount: 0,
  complaintCount: 0,
  pendingComplaintCount: 0,
  visitorCount: 0
})

const userTrendChart = ref(null)
const repairTrendChart = ref(null)
const accessTrendChart = ref(null)
const paymentChart = ref(null)
const repairStatusChart = ref(null)
const paymentTypeChart = ref(null)
const utilityChart = ref(null)

let userTrendChartInstance = null
let repairTrendChartInstance = null
let accessTrendChartInstance = null
let paymentChartInstance = null
let repairStatusChartInstance = null
let paymentTypeChartInstance = null
let utilityChartInstance = null

const deviceOnlineRate = computed(() => {
  if (overviewStats.value.monitoringCount === 0) return 0
  return ((overviewStats.value.onlineMonitoringCount / overviewStats.value.monitoringCount) * 100).toFixed(1)
})

const goToPage = (path) => {
  router.push(path)
}

const initCharts = () => {
  initUserTrendChart()
  initRepairTrendChart()
  initAccessTrendChart()
  initPaymentChart()
  initRepairStatusChart()
  initPaymentTypeChart()
  initUtilityChart()
}

const initUserTrendChart = () => {
  if (!userTrendChart.value) return
  userTrendChartInstance = echarts.init(userTrendChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: '新增用户',
      type: 'line',
      smooth: true,
      data: [],
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
          { offset: 1, color: 'rgba(102, 126, 234, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#667eea',
        width: 3
      },
      itemStyle: {
        color: '#667eea'
      }
    }]
  }
  userTrendChartInstance.setOption(option)
}

const initRepairTrendChart = () => {
  if (!repairTrendChart.value) return
  repairTrendChartInstance = echarts.init(repairTrendChart.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: '报修数量',
      type: 'bar',
      data: [],
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#e6a23c' },
          { offset: 1, color: '#ebb563' }
        ]),
        borderRadius: [4, 4, 0, 0]
      }
    }]
  }
  repairTrendChartInstance.setOption(option)
}

const initAccessTrendChart = () => {
  if (!accessTrendChart.value) return
  accessTrendChartInstance = echarts.init(accessTrendChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: '进出人次',
      type: 'line',
      smooth: true,
      data: [],
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(103, 194, 58, 0.3)' },
          { offset: 1, color: 'rgba(103, 194, 58, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#67c23a',
        width: 3
      },
      itemStyle: {
        color: '#67c23a'
      }
    }]
  }
  accessTrendChartInstance.setOption(option)
}

const initPaymentChart = () => {
  if (!paymentChart.value) return
  paymentChartInstance = echarts.init(paymentChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      name: '费用金额',
      type: 'line',
      smooth: true,
      data: [],
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
          { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
        ])
      },
      lineStyle: {
        color: '#409eff',
        width: 3
      },
      itemStyle: {
        color: '#409eff'
      }
    }]
  }
  paymentChartInstance.setOption(option)
}

const initRepairStatusChart = () => {
  if (!repairStatusChart.value) return
  repairStatusChartInstance = echarts.init(repairStatusChart.value)
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [{
      name: '报修状态',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: []
    }]
  }
  repairStatusChartInstance.setOption(option)
}

const initPaymentTypeChart = () => {
  if (!paymentTypeChart.value) return
  paymentTypeChartInstance = echarts.init(paymentTypeChart.value)
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [{
      name: '费用类型',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: []
    }]
  }
  paymentTypeChartInstance.setOption(option)
}

const initUtilityChart = () => {
  if (!utilityChart.value) return
  utilityChartInstance = echarts.init(utilityChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['水费', '电费']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '水费',
        type: 'line',
        smooth: true,
        data: [],
        lineStyle: {
          color: '#409eff',
          width: 3
        },
        itemStyle: {
          color: '#409eff'
        }
      },
      {
        name: '电费',
        type: 'line',
        smooth: true,
        data: [],
        lineStyle: {
          color: '#67c23a',
          width: 3
        },
        itemStyle: {
          color: '#67c23a'
        }
      }
    ]
  }
  utilityChartInstance.setOption(option)
}

const loadOverviewStats = async () => {
  try {
    const response = await fetch(`/api/v1/admin/stats/overview?range=${timeRange.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      overviewStats.value = { ...overviewStats.value, ...(result.data || {}) }
    }
  } catch (error) {
    console.error('加载概览统计数据失败:', error)
  }
}

const loadUserTrend = async () => {
  try {
    const response = await fetch(`/api/v1/admin/stats/user-trend?range=${timeRange.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0 && userTrendChartInstance) {
      userTrendChartInstance.setOption({
        xAxis: {
          data: result.data.labels
        },
        series: [{
          data: result.data.values
        }]
      })
    }
  } catch (error) {
    console.error('加载用户增长趋势失败:', error)
  }
}

const loadRepairTrend = async () => {
  try {
    const response = await fetch(`/api/v1/admin/stats/repair-trend?range=${timeRange.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0 && repairTrendChartInstance) {
      repairTrendChartInstance.setOption({
        xAxis: {
          data: result.data.labels
        },
        series: [{
          data: result.data.values
        }]
      })
    }
  } catch (error) {
    console.error('加载报修趋势失败:', error)
  }
}

const loadAccessTrend = async () => {
  try {
    const response = await fetch(`/api/v1/admin/stats/access-trend?range=${timeRange.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0 && accessTrendChartInstance) {
      accessTrendChartInstance.setOption({
        xAxis: {
          data: result.data.labels
        },
        series: [{
          data: result.data.values
        }]
      })
    }
  } catch (error) {
    console.error('加载门禁进出趋势失败:', error)
  }
}

const loadPaymentStats = async () => {
  try {
    const response = await fetch(`/api/v1/admin/stats/payment-stats?range=${timeRange.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      if (paymentChartInstance) {
        paymentChartInstance.setOption({
          xAxis: {
            data: result.data.type.labels
          },
          series: [{
            data: result.data.type.values
          }]
        })
      }
      if (paymentTypeChartInstance) {
        paymentTypeChartInstance.setOption({
          series: [{
            data: result.data.type.labels.map((label, index) => ({
              name: label,
              value: result.data.type.values[index]
            }))
          }]
        })
      }
    }
  } catch (error) {
    console.error('加载费用统计失败:', error)
  }
}

const loadRepairStatus = async () => {
  try {
    const response = await fetch('/api/v1/admin/stats/repair-status', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0 && repairStatusChartInstance) {
      repairStatusChartInstance.setOption({
        series: [{
          data: result.data.labels.map((label, index) => ({
            name: label,
            value: result.data.values[index]
          }))
        }]
      })
    }
  } catch (error) {
    console.error('加载报修状态分布失败:', error)
  }
}

const loadUtilityTrend = async () => {
  try {
    const response = await fetch(`/api/v1/admin/stats/utility-trend?range=${timeRange.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0 && utilityChartInstance) {
      utilityChartInstance.setOption({
        xAxis: {
          data: result.data.water.labels
        },
        series: [
          {
            data: result.data.water.values
          },
          {
            data: result.data.electricity.values
          }
        ]
      })
    }
  } catch (error) {
    console.error('加载水电使用趋势失败:', error)
  }
}

const refreshData = async () => {
  await Promise.all([
    loadOverviewStats(),
    loadUserTrend(),
    loadRepairTrend(),
    loadAccessTrend(),
    loadPaymentStats(),
    loadRepairStatus(),
    loadUtilityTrend()
  ])
  lastUpdateTime.value = new Date().toLocaleTimeString()
}

const handleTimeRangeChange = () => {
  refreshData()
}

const handleResize = () => {
  userTrendChartInstance?.resize()
  repairTrendChartInstance?.resize()
  accessTrendChartInstance?.resize()
  paymentChartInstance?.resize()
  repairStatusChartInstance?.resize()
  paymentTypeChartInstance?.resize()
  utilityChartInstance?.resize()
}

onMounted(async () => {
  await nextTick()
  initCharts()
  await refreshData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  userTrendChartInstance?.dispose()
  repairTrendChartInstance?.dispose()
  accessTrendChartInstance?.dispose()
  paymentChartInstance?.dispose()
  repairStatusChartInstance?.dispose()
  paymentTypeChartInstance?.dispose()
  utilityChartInstance?.dispose()
  window.removeEventListener('resize', handleResize)
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
  font-size: 64px;
}

.illustration-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.element {
  position: absolute;
  font-size: 24px;
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

/* 时间筛选 */
.time-filter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.last-update {
  font-size: 14px;
  color: #909399;
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

/* 图表区域 */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.chart-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.chart-section.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-color.user {
  background: #667eea;
}

.legend-color.repair {
  background: #e6a23c;
}

.legend-color.access {
  background: #67c23a;
}

.legend-color.payment {
  background: #409eff;
}

.legend-color.water {
  background: #409eff;
}

.legend-color.electricity {
  background: #67c23a;
}

.chart-container {
  height: 300px;
  width: 100%;
}

/* 统计区域 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.stat-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
  grid-template-columns: repeat(4, 1fr);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
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
  color: white;
}

.stat-icon.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.success {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.stat-icon.warning {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
}

.stat-icon.danger {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
}

.stat-icon.info {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
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
  font-size: 12px;
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
  border-radius: 4px;
  font-size: 12px;
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
  grid-template-columns: repeat(3, 1fr);
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
}

.action-icon {
  font-size: 32px;
}

.action-text {
  font-size: 14px;
  font-weight: 500;
  color: white;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.action-btn.warning {
  background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
}

.action-btn.success {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.action-btn.info {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
}

.action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .welcome-content {
    flex-direction: column;
    text-align: center;
    gap: 30px;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
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
}

@media (max-width: 768px) {
  .welcome-section {
    padding: 30px 20px;
  }
  
  .welcome-title {
    font-size: 24px;
  }
  
  .core-metrics,
  .chart-section,
  .stat-section,
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
  
  .chart-container {
    height: 250px;
  }
  
  .smart-community-stats .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
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
  
  .chart-container {
    height: 200px;
  }
}
</style>
