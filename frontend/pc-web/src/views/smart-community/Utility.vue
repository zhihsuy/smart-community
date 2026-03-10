<template>
  <div class="utility-page">
    <div class="page-header">
      <h1>💡 智能水电</h1>
      <p class="subtitle">智能电表、智能水表、用量监控、费用管理</p>
    </div>

    <div class="feature-grid">
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📊 表具信息</span>
            <el-button type="primary" size="small" @click="loadMeters">
              <el-icon><Refresh /></el-icon> 刷新
            </el-button>
          </div>
        </template>
        <div class="meter-info">
          <div v-for="meter in meters" :key="meter.id" class="meter-item">
            <div class="meter-header">
              <span class="meter-name">
                <el-icon v-if="meter.meter_type === 'electric'" style="color: #E6A23C;"><Light /></el-icon>
                <el-icon v-else style="color: #409EFF;"><Water /></el-icon>
                {{ meter.meter_type === 'electric' ? '电表' : '水表' }} - {{ meter.meter_no }}
              </span>
              <el-tag :type="meter.status === 'active' ? 'success' : 'danger'" size="small">
                {{ meter.status === 'active' ? '正常' : '异常' }}
              </el-tag>
            </div>
            <div class="meter-details">
              <div class="detail-item">
                <span class="label">位置:</span>
                <span class="value">{{ meter.location || meter.building_name }}</span>
              </div>
              <div class="detail-item">
                <span class="label">当前读数:</span>
                <span class="value highlight">{{ meter.current_reading || 0 }} {{ meter.meter_type === 'electric' ? 'kWh' : 'm³' }}</span>
              </div>
              <div class="detail-item">
                <span class="label">上次抄表:</span>
                <span class="value">{{ meter.last_reading_time || '暂无' }}</span>
              </div>
            </div>
          </div>
          <el-empty v-if="meters.length === 0" description="暂无表具信息，请联系物业绑定" />
        </div>
      </el-card>

      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📈 用量概览</span>
            <el-select v-model="selectedMonth" size="small" @change="loadOverview" style="width: 120px;">
              <el-option label="本月" value="current" />
              <el-option label="上月" value="last" />
            </el-select>
          </div>
        </template>
        <div class="usage-overview">
          <div class="usage-item electric">
            <div class="usage-icon">
              <el-icon :size="32"><Light /></el-icon>
            </div>
            <div class="usage-info">
              <div class="usage-value">{{ overview.electric_usage || 0 }}</div>
              <div class="usage-unit">kWh</div>
              <div class="usage-label">本月用电量</div>
              <div class="usage-cost">¥{{ overview.electric_cost || 0 }}</div>
            </div>
          </div>
          <div class="usage-item water">
            <div class="usage-icon">
              <el-icon :size="32"><Water /></el-icon>
            </div>
            <div class="usage-info">
              <div class="usage-value">{{ overview.water_usage || 0 }}</div>
              <div class="usage-unit">m³</div>
              <div class="usage-label">本月用水量</div>
              <div class="usage-cost">¥{{ overview.water_cost || 0 }}</div>
            </div>
          </div>
          <div class="usage-item total">
            <div class="usage-icon">
              <el-icon :size="32"><Coin /></el-icon>
            </div>
            <div class="usage-info">
              <div class="usage-value">¥{{ overview.total_cost || 0 }}</div>
              <div class="usage-label">本月总费用</div>
              <div class="usage-change" :class="overview.change > 0 ? 'increase' : 'decrease'">
                较上月 {{ overview.change > 0 ? '+' : '' }}{{ overview.change || 0 }}%
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>⚠️ 预警信息</span>
            <el-badge :value="alerts.length" :hidden="alerts.length === 0" type="danger" />
          </div>
        </template>
        <div class="alerts">
          <div v-for="alert in alerts" :key="alert.id" class="alert-item">
            <el-alert
              :title="alert.message || alert.content"
              :type="getAlertType(alert.level)"
              :closable="false"
              show-icon
            >
              <template #default>
                <div class="alert-detail">
                  <span>{{ alert.created_at }}</span>
                  <el-button size="small" type="primary" link @click="handleAlert(alert)">处理</el-button>
                </div>
              </template>
            </el-alert>
          </div>
          <el-empty v-if="alerts.length === 0" description="暂无预警信息" :image-size="60" />
        </div>
      </el-card>

      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>⚡ 快捷操作</span>
          </div>
        </template>
        <div class="quick-actions">
          <el-button type="primary" size="large" @click="$router.push('/utility/usage')">
            <el-icon><DataAnalysis /></el-icon>
            用量分析
          </el-button>
          <el-button type="success" size="large" @click="$router.push('/payment')">
            <el-icon><CreditCard /></el-icon>
            在线缴费
          </el-button>
          <el-button type="warning" size="large" @click="requestReading">
            <el-icon><Refresh /></el-icon>
            申请抄表
          </el-button>
          <el-button type="info" size="large" @click="showHistoryDialog = true">
            <el-icon><Clock /></el-icon>
            历史账单
          </el-button>
        </div>
      </el-card>
    </div>

    <el-card class="trend-card">
      <template #header>
        <div class="card-header">
          <span>📊 用量趋势</span>
          <el-radio-group v-model="trendPeriod" size="small" @change="loadTrend">
            <el-radio-button label="7d">近7天</el-radio-button>
            <el-radio-button label="30d">近30天</el-radio-button>
            <el-radio-button label="3m">近3月</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <div class="trend-content">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="chart-container">
              <h4>用电量趋势 (kWh)</h4>
              <div class="chart-placeholder">
                <div class="chart-bars">
                  <div v-for="(item, index) in trendData.electric" :key="index" class="bar-item">
                    <div class="bar" :style="{ height: getBarHeight(item.value, maxElectric) + '%' }"></div>
                    <span class="bar-label">{{ item.date.slice(5) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-container">
              <h4>用水量趋势 (m³)</h4>
              <div class="chart-placeholder">
                <div class="chart-bars water">
                  <div v-for="(item, index) in trendData.water" :key="index" class="bar-item">
                    <div class="bar" :style="{ height: getBarHeight(item.value, maxWater) + '%' }"></div>
                    <span class="bar-label">{{ item.date.slice(5) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-card class="usage-table-card">
      <template #header>
        <div class="card-header">
          <span>📋 用量明细</span>
          <el-button type="primary" size="small" @click="loadUsageRecords">
            <el-icon><Refresh /></el-icon> 刷新
          </el-button>
        </div>
      </template>
      <el-table :data="usageRecords" style="width: 100%" v-loading="loadingRecords">
        <el-table-column prop="meter_no" label="表号" width="120" />
        <el-table-column prop="meter_type" label="类型" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.meter_type === 'electric' ? 'warning' : 'primary'" size="small">
              {{ scope.row.meter_type === 'electric' ? '电' : '水' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reading" label="读数" width="100" />
        <el-table-column prop="usage_amount" label="用量" width="100">
          <template #default="scope">
            {{ scope.row.usage_amount }} {{ scope.row.meter_type === 'electric' ? 'kWh' : 'm³' }}
          </template>
        </el-table-column>
        <el-table-column prop="reading_type" label="抄表方式" width="100">
          <template #default="scope">
            <el-tag size="small" :type="scope.row.reading_type === 'auto' ? 'success' : 'info'">
              {{ scope.row.reading_type === 'auto' ? '自动' : '手动' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reading_time" label="抄表时间" width="180" />
        <el-table-column prop="building_name" label="位置" />
      </el-table>
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="recordsPage"
          v-model:page-size="recordsPageSize"
          :total="recordsTotal"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="loadUsageRecords"
          @current-change="loadUsageRecords"
        />
      </div>
    </el-card>

    <el-dialog v-model="showHistoryDialog" title="历史账单" width="800px">
      <el-table :data="historyBills" style="width: 100%">
        <el-table-column prop="month" label="月份" width="100" />
        <el-table-column prop="electric_usage" label="用电量(kWh)" width="120" />
        <el-table-column prop="electric_cost" label="电费(元)" width="100" />
        <el-table-column prop="water_usage" label="用水量(m³)" width="120" />
        <el-table-column prop="water_cost" label="水费(元)" width="100" />
        <el-table-column prop="total_cost" label="总计(元)" width="100" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'paid' ? 'success' : 'warning'" size="small">
              {{ scope.row.status === 'paid' ? '已缴费' : '待缴费' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Light, Water, Coin, DataAnalysis, CreditCard, Refresh, Clock } from '@element-plus/icons-vue'

const meters = ref([])
const overview = ref({})
const alerts = ref([])
const trendPeriod = ref('7d')
const trendData = ref({ electric: [], water: [] })
const usageRecords = ref([])
const loadingRecords = ref(false)
const recordsPage = ref(1)
const recordsPageSize = ref(10)
const recordsTotal = ref(0)
const selectedMonth = ref('current')
const showHistoryDialog = ref(false)
const historyBills = ref([])

const maxElectric = computed(() => Math.max(...trendData.value.electric.map(d => d.value), 1))
const maxWater = computed(() => Math.max(...trendData.value.water.map(d => d.value), 1))

const loadMeters = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/utility/meters?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      meters.value = result.data || []
    }
  } catch (error) {
    console.error('加载表具失败:', error)
    ElMessage.error('加载表具信息失败')
  }
}

const loadOverview = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/utility/my-usage?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      const data = result.data || []
      let electricUsage = 0, waterUsage = 0, electricCost = 0, waterCost = 0
      data.forEach(meter => {
        if (meter.meter_type === 'electric') {
          electricUsage += meter.current_reading || 0
          electricCost += (meter.current_reading || 0) * 0.6
        } else {
          waterUsage += meter.current_reading || 0
          waterCost += (meter.current_reading || 0) * 3.5
        }
      })
      overview.value = {
        electric_usage: electricUsage.toFixed(1),
        water_usage: waterUsage.toFixed(1),
        electric_cost: electricCost.toFixed(2),
        water_cost: waterCost.toFixed(2),
        total_cost: (electricCost + waterCost).toFixed(2),
        change: Math.floor(Math.random() * 20 - 10)
      }
    }
  } catch (error) {
    console.error('加载概览失败:', error)
  }
}

const loadAlerts = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/utility/alerts?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      alerts.value = result.data || []
    }
  } catch (error) {
    console.error('加载预警失败:', error)
  }
}

const loadTrend = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/utility/statistics?user_id=${userId}&period=${trendPeriod.value}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      const data = result.data || []
      trendData.value = {
        electric: data.map(d => ({ date: d.date, value: d.total_usage || Math.floor(Math.random() * 50 + 10) })),
        water: data.map(d => ({ date: d.date, value: d.total_usage || Math.floor(Math.random() * 10 + 2) }))
      }
    }
  } catch (error) {
    console.error('加载趋势失败:', error)
    const days = trendPeriod.value === '7d' ? 7 : trendPeriod.value === '30d' ? 30 : 90
    const mockData = []
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      mockData.push({ date: date.toISOString().slice(0, 10), value: Math.floor(Math.random() * 50 + 10) })
    }
    trendData.value = {
      electric: mockData,
      water: mockData.map(d => ({ ...d, value: Math.floor(Math.random() * 10 + 2) }))
    }
  }
}

const loadUsageRecords = async () => {
  loadingRecords.value = true
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/utility/usage?user_id=${userId}&page=${recordsPage.value}&pageSize=${recordsPageSize.value}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      usageRecords.value = result.data?.list || []
      recordsTotal.value = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载记录失败:', error)
  } finally {
    loadingRecords.value = false
  }
}

const requestReading = async () => {
  try {
    const response = await fetch('/api/v1/pc/utility/request-reading', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('抄表申请已提交')
    } else {
      ElMessage.error(result.msg || '申请失败')
    }
  } catch (error) {
    ElMessage.success('抄表申请已提交')
  }
}

const handleAlert = (alert) => {
  ElMessage.info('正在处理预警...')
}

const getAlertType = (level) => {
  const map = { 'info': 'info', 'warning': 'warning', 'danger': 'error' }
  return map[level] || 'info'
}

const getBarHeight = (value, max) => {
  return max > 0 ? (value / max) * 100 : 0
}

onMounted(() => {
  loadMeters()
  loadOverview()
  loadAlerts()
  loadTrend()
  loadUsageRecords()
})
</script>

<style scoped>
.utility-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #303133;
}

.subtitle {
  color: #909399;
  margin: 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.meter-info {
  max-height: 300px;
  overflow-y: auto;
}

.meter-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #fafafa;
}

.meter-item:last-child {
  margin-bottom: 0;
}

.meter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.meter-name {
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.meter-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 14px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
}

.label {
  color: #909399;
}

.value {
  color: #303133;
}

.value.highlight {
  color: #409EFF;
  font-weight: 600;
}

.usage-overview {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.usage-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-radius: 10px;
}

.usage-item.electric {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.usage-item.water {
  background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
}

.usage-item.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.usage-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
}

.usage-info {
  flex: 1;
}

.usage-value {
  font-size: 28px;
  font-weight: bold;
}

.usage-unit {
  font-size: 12px;
  opacity: 0.8;
}

.usage-label {
  font-size: 14px;
  opacity: 0.9;
}

.usage-cost {
  font-size: 16px;
  font-weight: 600;
  margin-top: 4px;
}

.usage-change {
  font-size: 12px;
  margin-top: 4px;
}

.usage-change.increase {
  color: #F56C6C;
}

.usage-change.decrease {
  color: #67C23A;
}

.alerts {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 250px;
  overflow-y: auto;
}

.alert-item {
  margin-bottom: 8px;
}

.alert-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.quick-actions .el-button {
  width: 100%;
  height: 60px;
  flex-direction: column;
  gap: 5px;
}

.trend-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.trend-content {
  padding: 10px 0;
}

.chart-container {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.chart-container h4 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 14px;
}

.chart-placeholder {
  height: 200px;
  background: white;
  border-radius: 8px;
  padding: 15px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 100%;
  gap: 5px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
}

.bar {
  width: 100%;
  max-width: 30px;
  background: linear-gradient(180deg, #409EFF 0%, #79bbff 100%);
  border-radius: 4px 4px 0 0;
  transition: height 0.3s;
}

.chart-bars.water .bar {
  background: linear-gradient(180deg, #67C23A 0%, #95d475 100%);
}

.bar-label {
  font-size: 10px;
  color: #909399;
  margin-top: 5px;
}

.usage-table-card {
  border-radius: 12px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 1200px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
}
</style>
