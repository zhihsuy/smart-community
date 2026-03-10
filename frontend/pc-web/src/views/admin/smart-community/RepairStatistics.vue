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
              <el-chart>
                <el-pie-chart
                  :data="typeDistribution"
                  :radius="[60, 100]"
                  center="50%, 50%"
                >
                  <el-pie-series
                    :data-key="'value'"
                    :name-key="'name'"
                    :color="['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']"
                  />
                  <el-chart-tooltip />
                </el-pie-chart>
              </el-chart>
            </div>
          </el-card>
          
          <!-- 工单状态分布 -->
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <h4>工单状态分布</h4>
            </template>
            <div class="chart-container">
              <el-chart>
                <el-pie-chart
                  :data="statusDistribution"
                  :radius="[60, 100]"
                  center="50%, 50%"
                >
                  <el-pie-series
                    :data-key="'value'"
                    :name-key="'name'"
                    :color="['#409EFF', '#67C23A', '#E6A23C', '#F56C6C']"
                  />
                  <el-chart-tooltip />
                </el-pie-chart>
              </el-chart>
            </div>
          </el-card>
          
          <!-- 工单趋势 -->
          <el-card shadow="hover" class="chart-card full-width">
            <template #header>
              <h4>工单趋势</h4>
            </template>
            <div class="chart-container">
              <el-chart>
                <el-line-chart
                  :data="trendData"
                  x-field="date"
                  y-field="value"
                >
                  <el-line-series
                    :data="trendData"
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
          
          <!-- 维修人员效率 -->
          <el-card shadow="hover" class="chart-card full-width">
            <template #header>
              <h4>维修人员效率</h4>
            </template>
            <div class="chart-container">
              <el-chart>
                <el-bar-chart
                  :data="technicianEfficiency"
                  x-field="name"
                  y-field="value"
                >
                  <el-bar-series
                    :data="technicianEfficiency"
                    :x-field="'name'"
                    :y-field="'value'"
                    :bar-style="{ fill: '#667eea' }"
                  />
                  <el-chart-tooltip />
                  <el-chart-axis />
                </el-bar-chart>
              </el-chart>
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
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import { ElMessage } from 'element-plus'

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

// 加载统计数据
const loadStatistics = async () => {
  try {
    const startDate = dateRange.value[0]?.toISOString().split('T')[0]
    const endDate = dateRange.value[1]?.toISOString().split('T')[0]
    
    const response = await fetch(`/api/v1/admin/repair/statistics?start_date=${startDate}&end_date=${endDate}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    const result = await response.json()
    if (result.code === 0) {
      const data = result.data
      
      // 基本统计
      totalOrders.value = data.total_orders || 0
      completedOrders.value = data.completed_orders || 0
      pendingOrders.value = data.pending_orders || 0
      avgProcessTime.value = data.avg_process_time || 0
      
      // 类型分布
      typeDistribution.value = data.type_distribution || [
        { name: '水电维修', value: 45 },
        { name: '物业维修', value: 30 },
        { name: '其他维修', value: 25 }
      ]
      
      // 状态分布
      statusDistribution.value = data.status_distribution || [
        { name: '已完成', value: 60 },
        { name: '处理中', value: 25 },
        { name: '待处理', value: 15 }
      ]
      
      // 趋势数据
      trendData.value = data.trend_data || generateMockTrendData()
      
      // 维修人员效率
      technicianEfficiency.value = data.technician_efficiency || [
        { name: '张师傅', value: 15 },
        { name: '李师傅', value: 12 },
        { name: '王师傅', value: 18 },
        { name: '赵师傅', value: 10 },
        { name: '刘师傅', value: 14 }
      ]
      
      // 详细数据
      detailData.value = data.detail_data || generateMockDetailData()
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
    // 生成模拟数据
    generateMockData()
  }
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
  loadStatistics()
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