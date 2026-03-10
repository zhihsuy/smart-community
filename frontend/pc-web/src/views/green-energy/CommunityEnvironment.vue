<template>
  <div class="community-environment">
    <div class="page-header">
      <h1>🌿 环保数据监测</h1>
      <p>实时监测社区环境数据，关注环境质量</p>
    </div>

    <div class="content-section">
      <!-- 环境数据概览 -->
      <div class="data-overview">
        <div class="overview-card">
          <div class="overview-icon">🌬️</div>
          <div class="overview-info">
            <div class="overview-value">{{ airQuality.value }} <span class="unit">AQI</span></div>
            <div class="overview-label">空气质量</div>
            <div class="overview-status" :class="airQuality.status">{{ airQuality.statusText }}</div>
          </div>
        </div>
        <div class="overview-card">
          <div class="overview-icon">🔊</div>
          <div class="overview-info">
            <div class="overview-value">{{ noiseLevel.value }} <span class="unit">dB</span></div>
            <div class="overview-label">噪音水平</div>
            <div class="overview-status" :class="noiseLevel.status">{{ noiseLevel.statusText }}</div>
          </div>
        </div>
        <div class="overview-card">
          <div class="overview-icon">🌡️</div>
          <div class="overview-info">
            <div class="overview-value">{{ temperature.value }} <span class="unit">°C</span></div>
            <div class="overview-label">温度</div>
            <div class="overview-status" :class="temperature.status">{{ temperature.statusText }}</div>
          </div>
        </div>
        <div class="overview-card">
          <div class="overview-icon">💧</div>
          <div class="overview-info">
            <div class="overview-value">{{ humidity.value }} <span class="unit">%</span></div>
            <div class="overview-label">湿度</div>
            <div class="overview-status" :class="humidity.status">{{ humidity.statusText }}</div>
          </div>
        </div>
      </div>

      <!-- 数据趋势图表 -->
      <div class="charts-section">
        <div class="chart-card">
          <div class="chart-header">
            <h3>空气质量趋势</h3>
            <el-select v-model="timeRange" @change="updateCharts">
              <el-option label="今日" value="today" />
              <el-option label="本周" value="week" />
              <el-option label="本月" value="month" />
            </el-select>
          </div>
          <div class="chart-content">
            <canvas ref="airQualityChart"></canvas>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <h3>噪音水平趋势</h3>
          </div>
          <div class="chart-content">
            <canvas ref="noiseChart"></canvas>
          </div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <h3>温度湿度趋势</h3>
          </div>
          <div class="chart-content">
            <canvas ref="tempHumidityChart"></canvas>
          </div>
        </div>
      </div>

      <!-- 环境数据详情 -->
      <div class="data-details">
        <div class="detail-card">
          <div class="detail-header">
            <h3>🌬️ 空气质量详情</h3>
          </div>
          <div class="detail-content">
            <div class="detail-item">
              <div class="detail-label">PM2.5</div>
              <div class="detail-value">{{ airQualityDetails.pm25 }} μg/m³</div>
              <div class="detail-status" :class="getAirQualityStatus(airQualityDetails.pm25)">
                {{ getAirQualityStatusText(airQualityDetails.pm25) }}
              </div>
            </div>
            <div class="detail-item">
              <div class="detail-label">PM10</div>
              <div class="detail-value">{{ airQualityDetails.pm10 }} μg/m³</div>
              <div class="detail-status" :class="getAirQualityStatus(airQualityDetails.pm10)">
                {{ getAirQualityStatusText(airQualityDetails.pm10) }}
              </div>
            </div>
            <div class="detail-item">
              <div class="detail-label">SO₂</div>
              <div class="detail-value">{{ airQualityDetails.so2 }} μg/m³</div>
              <div class="detail-status" :class="getAirQualityStatus(airQualityDetails.so2)">
                {{ getAirQualityStatusText(airQualityDetails.so2) }}
              </div>
            </div>
            <div class="detail-item">
              <div class="detail-label">NO₂</div>
              <div class="detail-value">{{ airQualityDetails.no2 }} μg/m³</div>
              <div class="detail-status" :class="getAirQualityStatus(airQualityDetails.no2)">
                {{ getAirQualityStatusText(airQualityDetails.no2) }}
              </div>
            </div>
            <div class="detail-item">
              <div class="detail-label">O₃</div>
              <div class="detail-value">{{ airQualityDetails.o3 }} μg/m³</div>
              <div class="detail-status" :class="getAirQualityStatus(airQualityDetails.o3)">
                {{ getAirQualityStatusText(airQualityDetails.o3) }}
              </div>
            </div>
            <div class="detail-item">
              <div class="detail-label">CO</div>
              <div class="detail-value">{{ airQualityDetails.co }} mg/m³</div>
              <div class="detail-status" :class="getAirQualityStatus(airQualityDetails.co)">
                {{ getAirQualityStatusText(airQualityDetails.co) }}
              </div>
            </div>
          </div>
        </div>

        <div class="detail-card">
          <div class="detail-header">
            <h3>🌱 环保建议</h3>
          </div>
          <div class="detail-content">
            <div class="recommendation-item" v-for="(recommendation, index) in recommendations" :key="index">
              <div class="recommendation-icon">{{ recommendation.icon }}</div>
              <div class="recommendation-content">
                <h4>{{ recommendation.title }}</h4>
                <p>{{ recommendation.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

const timeRange = ref('today')
const airQualityChart = ref(null)
const noiseChart = ref(null)
const tempHumidityChart = ref(null)
const airQualityChartInstance = ref(null)
const noiseChartInstance = ref(null)
const tempHumidityChartInstance = ref(null)

// 空气质量数据
const airQuality = ref({
  value: 65,
  status: 'moderate',
  statusText: '良'
})

// 噪音水平数据
const noiseLevel = ref({
  value: 55,
  status: 'moderate',
  statusText: '中等'
})

// 温度数据
const temperature = ref({
  value: 22,
  status: 'good',
  statusText: '舒适'
})

// 湿度数据
const humidity = ref({
  value: 60,
  status: 'good',
  statusText: '适宜'
})

// 空气质量详情
const airQualityDetails = ref({
  pm25: 45,
  pm10: 70,
  so2: 15,
  no2: 30,
  o3: 80,
  co: 0.8
})

// 环保建议
const recommendations = ref([
  {
    icon: '🌿',
    title: '增加绿化',
    description: '在社区内增加绿植，提高空气质量，减少噪音污染。'
  },
  {
    icon: '🚲',
    title: '绿色出行',
    description: '鼓励居民使用公共交通、自行车或步行出行，减少汽车尾气排放。'
  },
  {
    icon: '💡',
    title: '节能减排',
    description: '使用节能电器，减少能源消耗，降低碳排放。'
  },
  {
    icon: '♻️',
    title: '垃圾分类',
    description: '积极参与垃圾分类，减少环境污染，提高资源利用效率。'
  }
])

// 模拟历史数据
const generateHistoricalData = (days) => {
  const labels = []
  const airQualityData = []
  const noiseData = []
  const temperatureData = []
  const humidityData = []
  
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    
    if (days === 1) {
      // 今日数据，按小时
      for (let j = 0; j < 24; j++) {
        labels.push(`${j}:00`)
        airQualityData.push(50 + Math.random() * 50)
        noiseData.push(45 + Math.random() * 20)
        temperatureData.push(18 + Math.random() * 8)
        humidityData.push(50 + Math.random() * 20)
      }
    } else if (days === 7) {
      // 本周数据，按天
      labels.push(`${date.getMonth() + 1}/${date.getDate()}`)
      airQualityData.push(50 + Math.random() * 50)
      noiseData.push(45 + Math.random() * 20)
      temperatureData.push(18 + Math.random() * 8)
      humidityData.push(50 + Math.random() * 20)
    } else {
      // 本月数据，按周
      labels.push(`第${Math.ceil((date.getDate() + 6) / 7)}周`)
      airQualityData.push(50 + Math.random() * 50)
      noiseData.push(45 + Math.random() * 20)
      temperatureData.push(18 + Math.random() * 8)
      humidityData.push(50 + Math.random() * 20)
    }
  }
  
  return {
    labels,
    airQualityData,
    noiseData,
    temperatureData,
    humidityData
  }
}

// 更新图表
const updateCharts = () => {
  let days = 1
  if (timeRange.value === 'week') {
    days = 7
  } else if (timeRange.value === 'month') {
    days = 30
  }
  
  const data = generateHistoricalData(days)
  
  // 更新空气质量图表
  if (airQualityChartInstance.value) {
    airQualityChartInstance.value.destroy()
  }
  
  if (airQualityChart.value) {
    airQualityChartInstance.value = new Chart(airQualityChart.value, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'AQI',
          data: data.airQualityData,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'AQI'
            }
          }
        }
      }
    })
  }
  
  // 更新噪音图表
  if (noiseChartInstance.value) {
    noiseChartInstance.value.destroy()
  }
  
  if (noiseChart.value) {
    noiseChartInstance.value = new Chart(noiseChart.value, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [{
          label: '噪音 (dB)',
          data: data.noiseData,
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'dB'
            }
          }
        }
      }
    })
  }
  
  // 更新温度湿度图表
  if (tempHumidityChartInstance.value) {
    tempHumidityChartInstance.value.destroy()
  }
  
  if (tempHumidityChart.value) {
    tempHumidityChartInstance.value = new Chart(tempHumidityChart.value, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: '温度 (°C)',
            data: data.temperatureData,
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            tension: 0.4,
            fill: true,
            yAxisID: 'y'
          },
          {
            label: '湿度 (%)',
            data: data.humidityData,
            borderColor: '#06b6d4',
            backgroundColor: 'rgba(6, 182, 212, 0.1)',
            tension: 0.4,
            fill: true,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top'
          }
        },
        scales: {
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: '温度 (°C)'
            }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: {
              display: true,
              text: '湿度 (%)'
            },
            grid: {
              drawOnChartArea: false
            }
          }
        }
      }
    })
  }
}

// 获取空气质量状态
const getAirQualityStatus = (value) => {
  if (value <= 35) {
    return 'good'
  } else if (value <= 75) {
    return 'moderate'
  } else if (value <= 115) {
    return 'unhealthy-sensitive'
  } else if (value <= 150) {
    return 'unhealthy'
  } else {
    return 'very-unhealthy'
  }
}

// 获取空气质量状态文本
const getAirQualityStatusText = (value) => {
  if (value <= 35) {
    return '优'
  } else if (value <= 75) {
    return '良'
  } else if (value <= 115) {
    return '轻度污染'
  } else if (value <= 150) {
    return '中度污染'
  } else {
    return '重度污染'
  }
}

onMounted(() => {
  updateCharts()
})

watch(timeRange, () => {
  updateCharts()
})
</script>

<style scoped>
.community-environment {
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

.data-overview {
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

.overview-value .unit {
  font-size: 16px;
  color: #666;
  font-weight: normal;
}

.overview-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.overview-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
  font-weight: 500;
}

.overview-status.good {
  background: #d1fae5;
  color: #065f46;
}

.overview-status.moderate {
  background: #fef3c7;
  color: #92400e;
}

.overview-status.unhealthy-sensitive {
  background: #fee2e2;
  color: #b91c1c;
}

.overview-status.unhealthy {
  background: #fecaca;
  color: #991b1b;
}

.overview-status.very-unhealthy {
  background: #fca5a5;
  color: #7f1d1d;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.chart-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chart-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.chart-content {
  padding: 20px;
  height: 300px;
}

.data-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
}

.detail-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.detail-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.detail-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.detail-content {
  padding: 20px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f3f4f6;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 14px;
  color: #666;
}

.detail-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.detail-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px 0;
  border-bottom: 1px solid #f3f4f6;
}

.recommendation-item:last-child {
  border-bottom: none;
}

.recommendation-icon {
  font-size: 24px;
  flex-shrink: 0;
  margin-top: 5px;
}

.recommendation-content h4 {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.recommendation-content p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin: 0;
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
  
  .data-overview {
    grid-template-columns: 1fr;
  }
  
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .chart-content {
    height: 250px;
  }
  
  .data-details {
    grid-template-columns: 1fr;
  }
  
  .detail-card {
    margin-bottom: 20px;
  }
}
</style>