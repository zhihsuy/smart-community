<template>
  <AdminLayout>
    <div class="utility-usage">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>用量数据监控</h3>
            <div class="date-range">
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                @change="loadUsageData"
              />
            </div>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="表具类型">
              <el-select v-model="searchForm.meter_type" placeholder="选择表具类型">
                <el-option label="电表" value="electric" />
                <el-option label="水表" value="water" />
                <el-option label="燃气表" value="gas" />
              </el-select>
            </el-form-item>
            <el-form-item label="楼栋">
              <el-select v-model="searchForm.building_id" placeholder="选择楼栋">
                <el-option 
                  v-for="building in buildings" 
                  :key="building.id" 
                  :label="building.name" 
                  :value="building.id" 
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchUsage">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <!-- 统计概览 -->
        <div class="stats-overview mb-6">
          <div class="stat-card">
            <div class="stat-icon primary">
              <el-icon><Setting /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalElectric }}</div>
              <div class="stat-label">总用电量 (kWh)</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon success">
              <el-icon><House /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalWater }}</div>
              <div class="stat-label">总用水量 (m³)</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon warning">
              <el-icon><Star /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalGas }}</div>
              <div class="stat-label">总用气量 (m³)</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon danger">
              <el-icon><Notification /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ alertCount }}</div>
              <div class="stat-label">异常预警</div>
            </div>
          </div>
        </div>
        
        <!-- 图表区域 -->
        <div class="charts-grid">
          <!-- 用电量趋势 -->
          <el-card shadow="hover" class="chart-card full-width">
            <template #header>
              <h4>用电量趋势</h4>
            </template>
            <div class="chart-container" ref="electricChartRef"></div>
          </el-card>
          
          <!-- 用水量趋势 -->
          <el-card shadow="hover" class="chart-card full-width">
            <template #header>
              <h4>用水量趋势</h4>
            </template>
            <div class="chart-container" ref="waterChartRef"></div>
          </el-card>
        </div>
        
        <!-- 详细数据表格 -->
        <div class="detail-table mt-6">
          <h4>详细用量数据</h4>
          <div class="table-container">
            <el-table :data="usageData" style="width: 100%">
              <el-table-column prop="id" label="记录ID" width="60" />
              <el-table-column prop="meter_code" label="表具编号" width="120" />
              <el-table-column prop="meter_type" label="表具类型" width="100">
                <template #default="scope">
                  <el-tag :type="getMeterTypeTag(scope.row.meter_type)">
                    {{ getMeterTypeText(scope.row.meter_type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="building_name" label="所属楼栋" width="140" />
              <el-table-column prop="unit" label="单元" width="80" />
              <el-table-column prop="room_number" label="房间号" width="80" />
              <el-table-column prop="previous_reading" label="上次读数" width="100" />
              <el-table-column prop="current_reading" label="当前读数" width="100" />
              <el-table-column prop="usage" label="用量" width="80" />
              <el-table-column prop="reading_date" label="抄表日期" width="140" />
            </el-table>
          </div>
          
          <div class="pagination" v-if="total > 0">
            <el-pagination
              v-model:current-page="page"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              :total="total"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </div>
      </el-card>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import { ElMessage } from 'element-plus'
import { Setting, House, Star, Notification } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const dateRange = ref([new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), new Date()])
const buildings = ref([])
const usageData = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  meter_type: '',
  building_id: ''
})

// 当前用户信息
const currentUser = ref(null)

// 统计数据
const totalElectric = ref(0)
const totalWater = ref(0)
const totalGas = ref(0)
const alertCount = ref(0)

// 趋势数据
const electricTrend = ref([])
const waterTrend = ref([])

// 图表引用
const electricChartRef = ref(null)
const waterChartRef = ref(null)
let electricChart = null
let waterChart = null

// 获取当前登录用户信息
const getCurrentUser = () => {
  try {
    // 尝试从 userInfo 获取用户信息
    const userStr = localStorage.getItem('userInfo')
    if (userStr) {
      currentUser.value = JSON.parse(userStr)
      console.log('当前用户:', currentUser.value)
    } else {
      console.warn('未找到用户信息，请检查登录状态')
    }
  } catch (error) {
    console.error('获取当前用户信息失败:', error)
  }
}

// 获取表具类型文本
const getMeterTypeText = (type) => {
  const types = {
    'electric': '电表',
    'water': '水表',
    'gas': '燃气表'
  }
  return types[type] || type
}

// 获取表具类型标签样式
const getMeterTypeTag = (type) => {
  const tags = {
    'electric': 'primary',
    'water': 'success',
    'gas': 'warning'
  }
  return tags[type] || 'default'
}

// 加载楼栋列表
const loadBuildings = async () => {
  try {
    const response = await fetch('/api/v1/pc/building/list')
    const result = await response.json()
    if (result.code === 0) {
      buildings.value = result.data
    }
  } catch (error) {
    console.error('加载楼栋列表失败:', error)
  }
}

// 加载用量数据
const loadUsageData = async () => {
  try {
    const startDate = dateRange.value[0]?.toISOString().split('T')[0]
    const endDate = dateRange.value[1]?.toISOString().split('T')[0]
    const params = new URLSearchParams()
    
    // 添加当前用户ID，只加载当前用户的数据
    if (currentUser.value && currentUser.value.id) {
      params.append('user_id', currentUser.value.id)
      console.log('加载用户ID的数据:', currentUser.value.id)
    }
    
    if (searchForm.value.meter_type) params.append('meter_type', searchForm.value.meter_type)
    if (searchForm.value.building_id) params.append('building_id', searchForm.value.building_id)
    params.append('start_date', startDate)
    params.append('end_date', endDate)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`/api/v1/pc/utility/usage?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      const data = result.data
      // 处理数据，确保数值类型正确
      usageData.value = (data.list || []).map(item => ({
        ...item,
        previous_reading: parseFloat(item.previous_reading) || 0,
        current_reading: parseFloat(item.current_reading) || 0,
        usage: parseFloat(item.usage_amount) || 0
      }))
      total.value = data.total || 0
      
      // 统计数据
      if (data.total_electric !== undefined) {
        totalElectric.value = data.total_electric || 0
        totalWater.value = data.total_water || 0
        totalGas.value = data.total_gas || 0
        alertCount.value = data.alert_count || 0
      } else {
        // 如果没有提供统计数据，基于列表计算
        calculateStats()
      }
      
      // 趋势数据
      console.log('Electric Trend Data:', data.electric_trend)
      console.log('Water Trend Data:', data.water_trend)
      electricTrend.value = data.electric_trend || []
      waterTrend.value = data.water_trend || []
      
      // 更新图表
      nextTick(() => {
        updateCharts()
      })
    } else {
      ElMessage.error(result.msg || '加载用量数据失败')
    }
  } catch (error) {
    console.error('加载用量数据失败:', error)
    ElMessage.error('加载用量数据失败')
  }
}

// 加载表具列表用于关联数据
const loadMeters = async () => {
  try {
    const response = await fetch('/api/v1/pc/utility/meters', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      return result.data
    }
    return []
  } catch (error) {
    console.error('加载表具列表失败:', error)
    return []
  }
}

// 搜索用量数据
const searchUsage = () => {
  page.value = 1
  loadUsageData()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    meter_type: '',
    building_id: ''
  }
  page.value = 1
  loadUsageData()
}

// 生成模拟趋势数据
const generateMockTrendData = (type) => {
  const data = []
  const today = new Date()
  for (let i = 29; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    data.push({
      date: date.toISOString().split('T')[0],
      value: Math.floor(Math.random() * 10) + (type === 'electric' ? 5 : 2)
    })
  }
  return data
}

// 初始化图表
const initCharts = () => {
  if (electricChartRef.value) {
    electricChart = echarts.init(electricChartRef.value)
  }
  if (waterChartRef.value) {
    waterChart = echarts.init(waterChartRef.value)
  }
  updateCharts()
}

// 更新图表
const updateCharts = () => {
  if (electricChart) {
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
        data: electricTrend.value.map(item => item.date),
        axisLabel: {
          interval: 4, // 每隔4个标签显示一个
          rotate: 45
        }
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '用电量',
          type: 'bar',
          data: electricTrend.value.map(item => item.value),
          itemStyle: {
            color: '#667eea'
          }
        }
      ]
    }
    electricChart.setOption(option)
  }
  
  if (waterChart) {
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
        data: waterTrend.value.map(item => item.date),
        axisLabel: {
          interval: 4, // 每隔4个标签显示一个
          rotate: 45
        }
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '用水量',
          type: 'bar',
          data: waterTrend.value.map(item => item.value),
          itemStyle: {
            color: '#4facfe'
          }
        }
      ]
    }
    waterChart.setOption(option)
  }
}

// 监听窗口大小变化
window.addEventListener('resize', () => {
  electricChart?.resize()
  waterChart?.resize()
})

// 计算统计数据
const calculateStats = () => {
  let electric = 0
  let water = 0
  let gas = 0
  let alerts = 0
  
  usageData.value.forEach(item => {
    const usage = parseFloat(item.usage) || 0
    switch (item.meter_type) {
      case 'electric':
        electric += usage
        break
      case 'water':
        water += usage
        break
      case 'gas':
        gas += usage
        break
    }
    // 模拟异常预警检测
    if (usage > 50) {
      alerts++
    }
  })
  
  totalElectric.value = Math.round(electric * 100) / 100
  totalWater.value = Math.round(water * 100) / 100
  totalGas.value = Math.round(gas * 100) / 100
  alertCount.value = alerts
}

// 生成模拟数据
const generateMockData = async () => {
  try {
    // 尝试加载表具列表
    const meters = await loadMeters()
    
    // 生成用量数据
    const mockUsageData = []
    
    // 如果有表具数据，基于表具生成用量数据
    if (meters && meters.length > 0) {
      meters.forEach((meter, index) => {
        // 为每个表具生成用量数据
        const meterType = meter.meter_type || 'electric'
        const baseReading = Math.floor(Math.random() * 1000) + 100
        const usage = Math.floor(Math.random() * 50) + 10
        
        mockUsageData.push({
          id: index + 1,
          meter_code: meter.meter_no || `M${index + 1}`,
          meter_type: meterType,
          building_name: meter.building_name || '1号楼',
          unit: meter.unit || '1',
          room_number: meter.room_number || `${index + 1}01`,
          previous_reading: baseReading,
          current_reading: baseReading + usage,
          usage: usage,
          reading_date: '2026-03-01'
        })
      })
    } else {
      // 如果没有表具数据，生成默认数据
      mockUsageData.push(
        {
          id: 1,
          meter_code: 'E1001',
          meter_type: 'electric',
          building_name: '1号楼',
          unit: '1',
          room_number: '101',
          previous_reading: 1250,
          current_reading: 1320,
          usage: 70,
          reading_date: '2026-03-01'
        },
        {
          id: 2,
          meter_code: 'W1001',
          meter_type: 'water',
          building_name: '1号楼',
          unit: '1',
          room_number: '101',
          previous_reading: 320,
          current_reading: 350,
          usage: 30,
          reading_date: '2026-03-01'
        },
        {
          id: 3,
          meter_code: 'G1001',
          meter_type: 'gas',
          building_name: '1号楼',
          unit: '1',
          room_number: '101',
          previous_reading: 150,
          current_reading: 180,
          usage: 30,
          reading_date: '2026-03-01'
        },
        {
          id: 4,
          meter_code: 'E1002',
          meter_type: 'electric',
          building_name: '1号楼',
          unit: '1',
          room_number: '102',
          previous_reading: 800,
          current_reading: 850,
          usage: 50,
          reading_date: '2026-03-01'
        },
        {
          id: 5,
          meter_code: 'W1002',
          meter_type: 'water',
          building_name: '1号楼',
          unit: '1',
          room_number: '102',
          previous_reading: 200,
          current_reading: 220,
          usage: 20,
          reading_date: '2026-03-01'
        }
      )
    }
    
    usageData.value = mockUsageData
    total.value = mockUsageData.length
    
    // 计算统计数据
    calculateStats()
    
    // 生成趋势数据
    electricTrend.value = generateMockTrendData('electric')
    waterTrend.value = generateMockTrendData('water')
  } catch (error) {
    console.error('生成模拟数据失败:', error)
    // 即使失败也要生成默认数据
    const defaultData = [
      {
        id: 1,
        meter_code: 'E1001',
        meter_type: 'electric',
        building_name: '1号楼',
        unit: '1',
        room_number: '101',
        previous_reading: 1250,
        current_reading: 1320,
        usage: 70,
        reading_date: '2026-03-01'
      },
      {
        id: 2,
        meter_code: 'W1001',
        meter_type: 'water',
        building_name: '1号楼',
        unit: '1',
        room_number: '101',
        previous_reading: 320,
        current_reading: 350,
        usage: 30,
        reading_date: '2026-03-01'
      }
    ]
    usageData.value = defaultData
    total.value = defaultData.length
    calculateStats()
    electricTrend.value = generateMockTrendData('electric')
    waterTrend.value = generateMockTrendData('water')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadUsageData()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadUsageData()
}

onMounted(async () => {
  // 获取当前用户信息
  getCurrentUser()
  
  await loadBuildings()
  await loadUsageData()
  
  // 初始化图表
  nextTick(() => {
    initCharts()
  })
})
</script>

<style scoped>
.utility-usage {
  padding: 0;
  width: 100%;
  box-sizing: border-box;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.search-filter {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow-x: auto;
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
  grid-template-columns: 1fr;
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

.detail-table {
  margin-top: 30px;
}

.detail-table h4 {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
  width: 100%;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.mt-6 {
  margin-top: 30px;
}

/* 响应式样式 */
@media (max-width: 1200px) {
  .el-table {
    font-size: 13px;
  }
  
  .el-table-column {
    white-space: nowrap;
  }
  
  .chart-container {
    height: 250px;
    padding: 15px;
  }
  
  .stats-overview {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

@media (max-width: 992px) {
  .search-filter {
    padding: 15px;
  }
  
  .el-form-item {
    margin-right: 10px;
  }
  
  .el-input {
    width: 120px;
  }
  
  .el-select {
    width: 120px;
  }
  
  .stat-card {
    padding: 15px;
    gap: 15px;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .stat-value {
    font-size: 24px;
  }
  
  .chart-container {
    height: 200px;
  }
  
  .el-table-column {
    width: auto !important;
    min-width: 80px;
  }
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .el-form {
    flex-wrap: wrap;
  }
  
  .el-form-item {
    margin-right: 15px;
    margin-bottom: 10px;
  }
  
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .el-table {
    font-size: 12px;
  }
  
  .el-table-column {
    width: auto !important;
    min-width: 60px;
  }
  
  .chart-container {
    height: 180px;
    padding: 10px;
  }
  
  .table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .el-button {
    padding: 0 8px;
    font-size: 12px;
  }
  
  .el-button .el-icon {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .search-filter {
    padding: 10px;
  }
  
  .el-form-item {
    margin-right: 10px;
    margin-bottom: 8px;
  }
  
  .el-input {
    width: 100px;
  }
  
  .el-select {
    width: 100px;
  }
  
  .stat-card {
    padding: 10px;
    gap: 10px;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .stat-label {
    font-size: 12px;
  }
  
  .chart-container {
    height: 150px;
    padding: 5px;
  }
  
  .el-table {
    font-size: 11px;
  }
  
  .el-table-column {
    min-width: 50px;
  }
}
</style>