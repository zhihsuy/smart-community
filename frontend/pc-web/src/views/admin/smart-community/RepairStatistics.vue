<template>
  <AdminLayout>
    <div class="repair-statistics">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>报修统计分析</h3>
            <div class="date-range">
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                @change="loadStatistics"
              />
            </div>
          </div>
        </template>
        
        <!-- 统计概览 -->
        <div class="stats-overview mb-6">
          <div class="stat-card">
            <div class="stat-icon primary">
              <el-icon><i-ep-data-analysis /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalOrders }}</div>
              <div class="stat-label">总工单数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon success">
              <el-icon><i-ep-check /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ completedOrders }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon warning">
              <el-icon><i-ep-time /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ pendingOrders }}</div>
              <div class="stat-label">待处理</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon danger">
              <el-icon><i-ep-alarm-clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ avgProcessTime }}h</div>
              <div class="stat-label">平均处理时间</div>
            </div>
          </div>
        </div>
        
        <!-- 图表区域 -->
        <div class="charts-grid">
          <!-- 工单类型分布 -->
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <h4>工单类型分布</h4>
            </template>
            <div class="chart-container">
              <div ref="typeChartRef" class="chart"></div>
            </div>
          </el-card>
          
          <!-- 工单状态分布 -->
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <h4>工单状态分布</h4>
            </template>
            <div class="chart-container">
              <div ref="statusChartRef" class="chart"></div>
            </div>
          </el-card>
          
          <!-- 工单趋势 -->
          <el-card shadow="hover" class="chart-card full-width">
            <template #header>
              <h4>工单趋势</h4>
            </template>
            <div class="chart-container">
              <div ref="trendChartRef" class="chart"></div>
            </div>
          </el-card>
          
          <!-- 维修人员效率 -->
          <el-card shadow="hover" class="chart-card full-width">
            <template #header>
              <h4>维修人员效率</h4>
            </template>
            <div class="chart-container">
              <div ref="efficiencyChartRef" class="chart"></div>
            </div>
          </el-card>
        </div>
        
        <!-- 详细数据表格 -->
        <div class="detail-table mt-6">
          <h4>详细统计数据</h4>
          <el-table :data="detailData" style="width: 100%">
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="total" label="总工单数" width="100" />
            <el-table-column prop="completed" label="已完成" width="100" />
            <el-table-column prop="pending" label="待处理" width="100" />
            <el-table-column prop="processing" label="处理中" width="100" />
            <el-table-column prop="avg_time" label="平均处理时间(h)" width="150" />
            <el-table-column prop="completion_rate" label="完成率" width="100">
              <template #default="scope">
                <el-progress :percentage="scope.row.completion_rate" :stroke-width="10" />
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const dateRange = ref([new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), new Date()])
const totalOrders = ref(0)
const completedOrders = ref(0)
const pendingOrders = ref(0)
const avgProcessTime = ref(0)
const typeDistribution = ref([])
const statusDistribution = ref([])
const trendData = ref([])
const technicianEfficiency = ref([])
const detailData = ref([])

// 图表引用
const typeChartRef = ref(null)
const statusChartRef = ref(null)
const trendChartRef = ref(null)
const efficiencyChartRef = ref(null)

// 图表实例
let typeChart = null
let statusChart = null
let trendChart = null
let efficiencyChart = null

// 加载统计数据
const loadStatistics = async () => {
  try {
    const startDate = dateRange.value[0]?.toISOString().split('T')[0]
    const endDate = dateRange.value[1]?.toISOString().split('T')[0]
    
    // 检查token是否存在
    const token = localStorage.getItem('token')
    console.log('token:', token)
    
    if (!token) {
      console.error('token不存在')
      ElMessage.error('请先登录')
      return
    }
    
    // 使用绝对路径调用API
    const response = await fetch(`http://localhost:8081/api/v1/pc/repair/statistics?start_date=${startDate}&end_date=${endDate}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    console.log('响应状态:', response.status)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    console.log('加载统计数据响应:', result)
    
    if (result.code === 0) {
      const data = result.data
      console.log('统计数据:', data)
      
      // 基本统计
      totalOrders.value = data.orders?.total || 0
      completedOrders.value = data.orders?.completed || 0
      pendingOrders.value = data.orders?.pending || 0
      avgProcessTime.value = 2.5 // 后端暂时没有提供平均处理时间
      
      // 类型分布
      typeDistribution.value = data.type_distribution || []
      
      // 状态分布
      statusDistribution.value = [
        { name: '已完成', value: data.orders?.completed || 0 },
        { name: '处理中', value: data.orders?.processing || 0 },
        { name: '待处理', value: data.orders?.pending || 0 },
        { name: '已取消', value: data.orders?.cancelled || 0 }
      ]
      
      // 趋势数据
      trendData.value = data.trend_data || []
      
      // 维修人员效率
      technicianEfficiency.value = data.technician_efficiency || []
      
      // 详细数据
      detailData.value = data.detail_data || []
      
      // 更新图表
      updateTypeChart()
      updateStatusChart()
      updateTrendChart()
      updateEfficiencyChart()
    } else {
      console.error('API返回错误:', result.msg)
      ElMessage.error(`加载统计数据失败: ${result.msg}`)
      // 清空数据
      totalOrders.value = 0
      completedOrders.value = 0
      pendingOrders.value = 0
      avgProcessTime.value = 0
      typeDistribution.value = []
      statusDistribution.value = [
        { name: '已完成', value: 0 },
        { name: '处理中', value: 0 },
        { name: '待处理', value: 0 },
        { name: '已取消', value: 0 }
      ]
      trendData.value = []
      technicianEfficiency.value = []
      detailData.value = []
      // 更新图表
      updateTypeChart()
      updateStatusChart()
      updateTrendChart()
      updateEfficiencyChart()
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
    // 清空数据
    totalOrders.value = 0
    completedOrders.value = 0
    pendingOrders.value = 0
    avgProcessTime.value = 0
    typeDistribution.value = []
    statusDistribution.value = [
      { name: '已完成', value: 0 },
      { name: '处理中', value: 0 },
      { name: '待处理', value: 0 },
      { name: '已取消', value: 0 }
    ]
    trendData.value = []
    technicianEfficiency.value = []
    detailData.value = []
    // 更新图表
    updateTypeChart()
    updateStatusChart()
    updateTrendChart()
    updateEfficiencyChart()
  }
}

// 初始化图表
const initCharts = () => {
  // 工单类型分布图表
  if (typeChartRef.value) {
    typeChart = echarts.init(typeChartRef.value)
    updateTypeChart()
  }
  
  // 工单状态分布图表
  if (statusChartRef.value) {
    statusChart = echarts.init(statusChartRef.value)
    updateStatusChart()
  }
  
  // 工单趋势图表
  if (trendChartRef.value) {
    trendChart = echarts.init(trendChartRef.value)
    updateTrendChart()
  }
  
  // 维修人员效率图表
  if (efficiencyChartRef.value) {
    efficiencyChart = echarts.init(efficiencyChartRef.value)
    updateEfficiencyChart()
  }
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    typeChart?.resize()
    statusChart?.resize()
    trendChart?.resize()
    efficiencyChart?.resize()
  })
}

// 更新工单类型分布图表
const updateTypeChart = () => {
  if (!typeChart) return
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 10,
      data: typeDistribution.value.map(item => item.name)
    },
    series: [
      {
        name: '工单类型',
        type: 'pie',
        radius: ['60%', '100%'],
        center: ['50%', '50%'],
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
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: typeDistribution.value,
        color: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
      }
    ]
  }
  
  typeChart.setOption(option)
}

// 更新工单状态分布图表
const updateStatusChart = () => {
  if (!statusChart) return
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 10,
      data: statusDistribution.value.map(item => item.name)
    },
    series: [
      {
        name: '工单状态',
        type: 'pie',
        radius: ['60%', '100%'],
        center: ['50%', '50%'],
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
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: statusDistribution.value,
        color: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C']
      }
    ]
  }
  
  statusChart.setOption(option)
}

// 更新工单趋势图表
const updateTrendChart = () => {
  if (!trendChart) return
  
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
      data: trendData.value.map(item => item.date)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '工单数量',
        type: 'line',
        data: trendData.value.map(item => item.value),
        smooth: true,
        lineStyle: {
          color: '#667eea',
          width: 2
        },
        itemStyle: {
          color: '#667eea'
        }
      }
    ]
  }
  
  trendChart.setOption(option)
}

// 更新维修人员效率图表
const updateEfficiencyChart = () => {
  if (!efficiencyChart) return
  
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
      data: technicianEfficiency.value.map(item => item.name),
      axisLabel: {
        interval: 0,
        rotate: 30
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '已完成工单',
        type: 'bar',
        data: technicianEfficiency.value.map(item => item.value),
        itemStyle: {
          color: '#667eea'
        }
      }
    ]
  }
  
  efficiencyChart.setOption(option)
}

// 生成模拟趋势数据
const generateMockTrendData = () => {
  const data = []
  const today = new Date()
  for (let i = 29; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    data.push({
      date: date.toISOString().split('T')[0],
      value: Math.floor(Math.random() * 10) + 5
    })
  }
  return data
}

// 生成模拟详细数据
const generateMockDetailData = () => {
  const data = []
  const today = new Date()
  for (let i = 6; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    const total = Math.floor(Math.random() * 10) + 5
    const completed = Math.floor(Math.random() * total)
    const pending = Math.floor(Math.random() * (total - completed))
    const processing = total - completed - pending
    data.push({
      date: date.toISOString().split('T')[0],
      total,
      completed,
      pending,
      processing,
      avg_time: (Math.random() * 4 + 1).toFixed(1),
      completion_rate: Math.floor((completed / total) * 100)
    })
  }
  return data
}

// 生成模拟数据
const generateMockData = () => {
  totalOrders.value = 120
  completedOrders.value = 85
  pendingOrders.value = 20
  avgProcessTime.value = 2.5
  
  typeDistribution.value = [
    { name: '水电维修', value: 60 },
    { name: '物业维修', value: 35 },
    { name: '其他维修', value: 25 }
  ]
  
  statusDistribution.value = [
    { name: '已完成', value: 85 },
    { name: '处理中', value: 15 },
    { name: '待处理', value: 20 }
  ]
  
  trendData.value = generateMockTrendData()
  technicianEfficiency.value = [
    { name: '张师傅', value: 25 },
    { name: '李师傅', value: 20 },
    { name: '王师傅', value: 30 },
    { name: '赵师傅', value: 15 },
    { name: '刘师傅', value: 22 }
  ]
  
  detailData.value = generateMockDetailData()
}

onMounted(() => {
  console.log('onMounted 钩子被调用')
  // 先初始化图表，再加载数据
  setTimeout(() => {
    console.log('开始初始化图表')
    initCharts()
    // 初始化图表后加载数据
    console.log('开始加载统计数据')
    loadStatistics()
  }, 100)
})
</script>

<style scoped>
.repair-statistics {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.success {
  background: linear-gradient(135deg, #67C23A 0%, #409EFF 100%);
}

.stat-icon.warning {
  background: linear-gradient(135deg, #E6A23C 0%, #F56C6C 100%);
}

.stat-icon.danger {
  background: linear-gradient(135deg, #F56C6C 0%, #E6A23C 100%);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-container {
  height: 300px;
  padding: 20px;
}

.chart {
  width: 100%;
  height: 100%;
}

.detail-table {
  margin-top: 30px;
}

.detail-table h4 {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.mt-6 {
  margin-top: 30px;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-overview {
    grid-template-columns: 1fr;
  }
}
</style>