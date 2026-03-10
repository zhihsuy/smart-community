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
              <el-icon><i-ep-lightning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalElectric }}</div>
              <div class="stat-label">总用电量 (kWh)</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon success">
              <el-icon><i-ep-water /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalWater }}</div>
              <div class="stat-label">总用水量 (m³)</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon warning">
              <el-icon><i-ep-fire /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ totalGas }}</div>
              <div class="stat-label">总用气量 (m³)</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon danger">
              <el-icon><i-ep-alarm /></el-icon>
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
            <div class="chart-container">
              <el-chart>
                <el-line-chart
                  :data="electricTrend"
                  x-field="date"
                  y-field="value"
                >
                  <el-line-series
                    :data="electricTrend"
                    :x-field="'date'"
                    :y-field="'value'"
                    smooth
                    :line-style="{ stroke: '#667eea', lineWidth: 2 }"
                    :point-style="{ fill: '#667eea', r: 4 }"
                  />
                  <el-chart-tooltip />
                  <el-chart-axis />
                </el-line-chart>
              </el-chart>
            </div>
          </el-card>
          
          <!-- 用水量趋势 -->
          <el-card shadow="hover" class="chart-card full-width">
            <template #header>
              <h4>用水量趋势</h4>
            </template>
            <div class="chart-container">
              <el-chart>
                <el-line-chart
                  :data="waterTrend"
                  x-field="date"
                  y-field="value"
                >
                  <el-line-series
                    :data="waterTrend"
                    :x-field="'date'"
                    :y-field="'value'"
                    smooth
                    :line-style="{ stroke: '#4facfe', lineWidth: 2 }"
                    :point-style="{ fill: '#4facfe', r: 4 }"
                  />
                  <el-chart-tooltip />
                  <el-chart-axis />
                </el-line-chart>
              </el-chart>
            </div>
          </el-card>
        </div>
        
        <!-- 详细数据表格 -->
        <div class="detail-table mt-6">
          <h4>详细用量数据</h4>
          <el-table :data="usageData" style="width: 100%">
            <el-table-column prop="id" label="记录ID" width="80" />
            <el-table-column prop="meter_code" label="表具编号" width="150" />
            <el-table-column prop="meter_type" label="表具类型" width="120">
              <template #default="scope">
                <el-tag :type="getMeterTypeTag(scope.row.meter_type)">
                  {{ getMeterTypeText(scope.row.meter_type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="building_name" label="所属楼栋" />
            <el-table-column prop="unit" label="单元" width="80" />
            <el-table-column prop="room_number" label="房间号" width="100" />
            <el-table-column prop="previous_reading" label="上次读数" width="120" />
            <el-table-column prop="current_reading" label="当前读数" width="120" />
            <el-table-column prop="usage" label="用量" width="100" />
            <el-table-column prop="reading_date" label="抄表日期" width="180" />
          </el-table>
          
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
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import { ElMessage } from 'element-plus'

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

// 统计数据
const totalElectric = ref(0)
const totalWater = ref(0)
const totalGas = ref(0)
const alertCount = ref(0)

// 趋势数据
const electricTrend = ref([])
const waterTrend = ref([])

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
    if (searchForm.value.meter_type) params.append('meter_type', searchForm.value.meter_type)
    if (searchForm.value.building_id) params.append('building_id', searchForm.value.building_id)
    params.append('start_date', startDate)
    params.append('end_date', endDate)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`/api/v1/admin/utility/usage?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      const data = result.data
      usageData.value = data.list
      total.value = data.total
      
      // 统计数据
      totalElectric.value = data.total_electric || 0
      totalWater.value = data.total_water || 0
      totalGas.value = data.total_gas || 0
      alertCount.value = data.alert_count || 0
      
      // 趋势数据
      electricTrend.value = data.electric_trend || generateMockTrendData('electric')
      waterTrend.value = data.water_trend || generateMockTrendData('water')
    }
  } catch (error) {
    console.error('加载用量数据失败:', error)
    ElMessage.error('加载用量数据失败')
    // 生成模拟数据
    generateMockData()
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

// 生成模拟数据
const generateMockData = () => {
  totalElectric.value = 1250
  totalWater.value = 320
  totalGas.value = 180
  alertCount.value = 5
  
  electricTrend.value = generateMockTrendData('electric')
  waterTrend.value = generateMockTrendData('water')
  
  usageData.value = [
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
  total.value = 2
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

onMounted(() => {
  loadBuildings()
  loadUsageData()
})
</script>

<style scoped>
.utility-usage {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-filter {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
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

.pagination {
  margin-top: 20px;
  text-align: right;
}

.mt-6 {
  margin-top: 30px;
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: 1fr;
  }
}
</style>