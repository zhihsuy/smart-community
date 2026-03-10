<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>环保数据监测</h1>
        <p>监测社区环境数据，包括空气质量、水质和噪音等</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card air" shadow="hover">
          <div class="stat-icon">
            <el-icon :size="32"><Sunny /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ airQuality.aqi || '--' }}</div>
            <div class="stat-label">空气质量指数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card noise" shadow="hover">
          <div class="stat-icon">
            <el-icon :size="32"><Mic /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ noise.level || '--' }} dB</div>
            <div class="stat-label">噪音水平</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card water" shadow="hover">
          <div class="stat-icon">
            <el-icon :size="32"><Coffee /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ water.quality || '--' }}</div>
            <div class="stat-label">水质等级</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card temp" shadow="hover">
          <div class="stat-icon">
            <el-icon :size="32"><Thermometer /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ temperature.value || '--' }}°C</div>
            <div class="stat-label">环境温度</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>实时监测数据</span>
              <el-radio-group v-model="monitorType" size="small" @change="loadMonitorData">
                <el-radio-button label="air">空气质量</el-radio-button>
                <el-radio-button label="noise">噪音</el-radio-button>
                <el-radio-button label="water">水质</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="monitor-chart">
            <div class="chart-bars">
              <div v-for="(item, index) in monitorData" :key="index" class="bar-item">
                <div class="bar" :style="{ height: getBarHeight(item.value) + '%', background: getBarColor(item.value) }">
                  <span class="bar-value">{{ item.value }}</span>
                </div>
                <span class="bar-label">{{ item.time }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <span>监测站点状态</span>
          </template>
          <div class="station-list">
            <div v-for="station in stations" :key="station.id" class="station-item">
              <div class="station-info">
                <span class="station-name">{{ station.name }}</span>
                <el-tag :type="station.status === 'online' ? 'success' : 'danger'" size="small">
                  {{ station.status === 'online' ? '在线' : '离线' }}
                </el-tag>
              </div>
              <div class="station-data">
                <span>AQI: {{ station.aqi }}</span>
                <span>温度: {{ station.temp }}°C</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card class="detail-card">
          <template #header>
            <span>空气质量详情</span>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="AQI指数">{{ airQuality.aqi }}</el-descriptions-item>
            <el-descriptions-item label="空气质量">{{ airQuality.level }}</el-descriptions-item>
            <el-descriptions-item label="PM2.5">{{ airQuality.pm25 }} μg/m³</el-descriptions-item>
            <el-descriptions-item label="PM10">{{ airQuality.pm10 }} μg/m³</el-descriptions-item>
            <el-descriptions-item label="SO2">{{ airQuality.so2 }} μg/m³</el-descriptions-item>
            <el-descriptions-item label="NO2">{{ airQuality.no2 }} μg/m³</el-descriptions-item>
            <el-descriptions-item label="CO">{{ airQuality.co }} mg/m³</el-descriptions-item>
            <el-descriptions-item label="O3">{{ airQuality.o3 }} μg/m³</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="detail-card">
          <template #header>
            <span>水质监测详情</span>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="水质等级">{{ water.quality }}</el-descriptions-item>
            <el-descriptions-item label="pH值">{{ water.ph }}</el-descriptions-item>
            <el-descriptions-item label="溶解氧">{{ water.dissolvedOxygen }} mg/L</el-descriptions-item>
            <el-descriptions-item label="浊度">{{ water.turbidity }} NTU</el-descriptions-item>
            <el-descriptions-item label="电导率">{{ water.conductivity }} μS/cm</el-descriptions-item>
            <el-descriptions-item label="水温">{{ water.temperature }}°C</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="alert-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>预警信息</span>
          <el-button type="primary" size="small" @click="loadAlerts">刷新</el-button>
        </div>
      </template>
      <el-table :data="alerts" style="width: 100%">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="type" label="预警类型" width="120">
          <template #default="scope">
            <el-tag :type="getAlertType(scope.row.level)" size="small">
              {{ scope.row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="station" label="监测站点" width="150" />
        <el-table-column prop="message" label="预警内容" min-width="200" />
        <el-table-column prop="value" label="监测值" width="100" />
        <el-table-column prop="threshold" label="阈值" width="100" />
        <el-table-column prop="time" label="预警时间" width="160" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'danger' : 'success'" size="small">
              {{ scope.row.status === 'active' ? '进行中' : '已恢复' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="handleAlert(scope.row)" v-if="scope.row.status === 'active'">处理</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Sunny, Mic, Coffee, Thermometer } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const monitorType = ref('air')

const airQuality = ref({
  aqi: 65,
  level: '良',
  pm25: 45,
  pm10: 78,
  so2: 12,
  no2: 35,
  co: 0.8,
  o3: 89
})

const noise = ref({
  level: 52
})

const water = ref({
  quality: 'II类',
  ph: 7.2,
  dissolvedOxygen: 8.5,
  turbidity: 2.3,
  conductivity: 450,
  temperature: 18
})

const temperature = ref({
  value: 22
})

const monitorData = ref([])
const stations = ref([])
const alerts = ref([])

const loadMonitorData = () => {
  if (monitorType.value === 'air') {
    monitorData.value = [
      { time: '00:00', value: 45 },
      { time: '04:00', value: 38 },
      { time: '08:00', value: 65 },
      { time: '12:00', value: 78 },
      { time: '16:00', value: 72 },
      { time: '20:00', value: 58 },
      { time: '现在', value: 65 }
    ]
  } else if (monitorType.value === 'noise') {
    monitorData.value = [
      { time: '00:00', value: 35 },
      { time: '04:00', value: 32 },
      { time: '08:00', value: 58 },
      { time: '12:00', value: 62 },
      { time: '16:00', value: 55 },
      { time: '20:00', value: 48 },
      { time: '现在', value: 52 }
    ]
  } else {
    monitorData.value = [
      { time: '00:00', value: 7.1 },
      { time: '04:00', value: 7.0 },
      { time: '08:00', value: 7.2 },
      { time: '12:00', value: 7.3 },
      { time: '16:00', value: 7.2 },
      { time: '20:00', value: 7.2 },
      { time: '现在', value: 7.2 }
    ]
  }
}

const loadStations = () => {
  stations.value = [
    { id: 1, name: '社区中心站', status: 'online', aqi: 65, temp: 22 },
    { id: 2, name: '东门监测站', status: 'online', aqi: 58, temp: 21 },
    { id: 3, name: '西门监测站', status: 'online', aqi: 72, temp: 23 },
    { id: 4, name: '公园监测站', status: 'offline', aqi: '--', temp: '--' }
  ]
}

const loadAlerts = () => {
  alerts.value = [
    { id: 1, type: '空气质量', level: 'warning', station: '西门监测站', message: 'PM2.5浓度超标', value: '85 μg/m³', threshold: '75 μg/m³', time: '2024-01-15 14:30:00', status: 'active' },
    { id: 2, type: '噪音', level: 'info', station: '东门监测站', message: '噪音水平偏高', value: '68 dB', threshold: '65 dB', time: '2024-01-15 12:00:00', status: 'recovered' }
  ]
}

const getBarHeight = (value) => {
  const max = Math.max(...monitorData.value.map(d => d.value), 1)
  return (value / max) * 100
}

const getBarColor = (value) => {
  if (monitorType.value === 'air') {
    if (value <= 50) return 'linear-gradient(180deg, #67C23A 0%, #95d475 100%)'
    if (value <= 100) return 'linear-gradient(180deg, #E6A23C 0%, #f5d442 100%)'
    return 'linear-gradient(180deg, #F56C6C 0%, #fab6b6 100%)'
  }
  return 'linear-gradient(180deg, #409EFF 0%, #79bbff 100%)'
}

const getAlertType = (level) => {
  const map = { 'warning': 'warning', 'danger': 'danger', 'info': 'info' }
  return map[level] || 'info'
}

const handleAlert = (alert) => {
  ElMessage.success('预警已处理')
  alert.status = 'recovered'
}

onMounted(() => {
  loadMonitorData()
  loadStations()
  loadAlerts()
})
</script>

<style scoped>
.admin-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 24px;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-card.air .stat-icon { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-card.noise .stat-icon { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.stat-card.water .stat-icon { background: linear-gradient(135deg, #409EFF 0%, #79bbff 100%); }
.stat-card.temp .stat-icon { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.chart-card, .info-card, .detail-card, .alert-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.monitor-chart {
  height: 250px;
  padding: 20px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 200px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.bar {
  width: 40px;
  border-radius: 4px 4px 0 0;
  position: relative;
  min-height: 5px;
}

.bar-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  color: #606266;
}

.bar-label {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.station-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.station-item {
  padding: 15px;
  background: #F5F7FA;
  border-radius: 8px;
}

.station-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.station-name {
  font-weight: bold;
  color: #303133;
}

.station-data {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: #606266;
}
</style>
