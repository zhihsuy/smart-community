<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>垃圾分类统计</h1>
        <p>查看垃圾分类数据统计和分析</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card total" shadow="hover">
          <div class="stat-icon">
            <el-icon :size="36"><DataAnalysis /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.totalRecords || 0 }}</div>
            <div class="stat-label">总识别次数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card users" shadow="hover">
          <div class="stat-icon">
            <el-icon :size="36"><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.activeUsers || 0 }}</div>
            <div class="stat-label">活跃用户</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card accuracy" shadow="hover">
          <div class="stat-icon">
            <el-icon :size="36"><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.avgAccuracy || 0 }}%</div>
            <div class="stat-label">平均准确率</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card today" shadow="hover">
          <div class="stat-icon">
            <el-icon :size="36"><Calendar /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.todayCount || 0 }}</div>
            <div class="stat-label">今日识别</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>分类占比统计</span>
            </div>
          </template>
          <div class="pie-chart-container">
            <div class="pie-chart">
              <div class="pie-segment recyclable" :style="{ transform: `rotate(${getRotation('recyclable')}deg)` }"></div>
              <div class="pie-segment hazardous" :style="{ transform: `rotate(${getRotation('hazardous')}deg)` }"></div>
              <div class="pie-segment wet" :style="{ transform: `rotate(${getRotation('wet')}deg)` }"></div>
              <div class="pie-segment dry" :style="{ transform: `rotate(${getRotation('dry')}deg)` }"></div>
            </div>
            <div class="pie-legend">
              <div class="legend-item">
                <span class="legend-dot recyclable"></span>
                <span>可回收物</span>
                <span class="legend-value">{{ categoryStats.recyclable || 0 }} ({{ getPercentage('recyclable') }}%)</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot hazardous"></span>
                <span>有害垃圾</span>
                <span class="legend-value">{{ categoryStats.hazardous || 0 }} ({{ getPercentage('hazardous') }}%)</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot wet"></span>
                <span>湿垃圾</span>
                <span class="legend-value">{{ categoryStats.wet || 0 }} ({{ getPercentage('wet') }}%)</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot dry"></span>
                <span>干垃圾</span>
                <span class="legend-value">{{ categoryStats.dry || 0 }} ({{ getPercentage('dry') }}%)</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>识别趋势</span>
              <el-radio-group v-model="trendPeriod" size="small" @change="loadTrendData">
                <el-radio-button label="7d">近7天</el-radio-button>
                <el-radio-button label="30d">近30天</el-radio-button>
                <el-radio-button label="90d">近3月</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="trend-chart">
            <div class="chart-bars">
              <div v-for="(item, index) in trendData" :key="index" class="bar-item">
                <div class="bar" :style="{ height: getBarHeight(item.count) + '%' }">
                  <span class="bar-value">{{ item.count }}</span>
                </div>
                <span class="bar-label">{{ item.date }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户活跃度排行</span>
            </div>
          </template>
          <el-table :data="userRanking" style="width: 100%">
            <el-table-column type="index" label="排名" width="60" />
            <el-table-column prop="user_name" label="用户" width="120">
              <template #default="scope">
                <div class="user-info">
                  <el-avatar :size="24" style="margin-right: 8px;">{{ scope.row.user_name?.charAt(0) }}</el-avatar>
                  {{ scope.row.user_name }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="识别次数" width="100" />
            <el-table-column prop="accuracy" label="准确率" width="100">
              <template #default="scope">
                {{ scope.row.accuracy }}%
              </template>
            </el-table-column>
            <el-table-column prop="points" label="获得积分" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>热门物品排行</span>
            </div>
          </template>
          <el-table :data="itemRanking" style="width: 100%">
            <el-table-column type="index" label="排名" width="60" />
            <el-table-column prop="item_name" label="物品名称" min-width="150" />
            <el-table-column prop="category" label="分类" width="100">
              <template #default="scope">
                <el-tag :type="getCategoryType(scope.row.category)" size="small">
                  {{ getCategoryName(scope.row.category) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="识别次数" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="chart-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>时段分布统计</span>
        </div>
      </template>
      <div class="hourly-chart">
        <div class="hourly-bars">
          <div v-for="(item, index) in hourlyData" :key="index" class="hourly-item">
            <div class="hourly-bar" :style="{ height: (item.count / maxHourly * 100) + '%' }">
              <span class="hourly-value" v-if="item.count > 0">{{ item.count }}</span>
            </div>
            <span class="hourly-label">{{ item.hour }}时</span>
          </div>
        </div>
      </div>
    </el-card>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { DataAnalysis, User, CircleCheck, Calendar } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const trendPeriod = ref('7d')

const overview = ref({
  totalRecords: 12580,
  activeUsers: 3256,
  avgAccuracy: 96.5,
  todayCount: 156
})

const categoryStats = ref({
  recyclable: 4520,
  hazardous: 890,
  wet: 3560,
  dry: 3610
})

const trendData = ref([])
const userRanking = ref([])
const itemRanking = ref([])
const hourlyData = ref([])

const totalCategory = computed(() => {
  return categoryStats.value.recyclable + categoryStats.value.hazardous + 
         categoryStats.value.wet + categoryStats.value.dry
})

const maxHourly = computed(() => {
  return Math.max(...hourlyData.value.map(h => h.count), 1)
})

const getPercentage = (category) => {
  if (totalCategory.value === 0) return 0
  return ((categoryStats.value[category] / totalCategory.value) * 100).toFixed(1)
}

const getRotation = (category) => {
  const percentages = {
    recyclable: getPercentage('recyclable'),
    hazardous: getPercentage('hazardous'),
    wet: getPercentage('wet'),
    dry: getPercentage('dry')
  }
  let rotation = 0
  const cats = ['recyclable', 'hazardous', 'wet', 'dry']
  for (const cat of cats) {
    if (cat === category) break
    rotation += (percentages[cat] / 100) * 360
  }
  return rotation
}

const getBarHeight = (count) => {
  const max = Math.max(...trendData.value.map(t => t.count), 1)
  return (count / max) * 100
}

const getCategoryType = (category) => {
  const map = { 'recyclable': 'success', 'hazardous': 'danger', 'wet': 'warning', 'dry': 'info' }
  return map[category] || 'info'
}

const getCategoryName = (category) => {
  const map = { 'recyclable': '可回收物', 'hazardous': '有害垃圾', 'wet': '湿垃圾', 'dry': '干垃圾' }
  return map[category] || category
}

const loadTrendData = async () => {
  trendData.value = [
    { date: '03-04', count: 120 },
    { date: '03-05', count: 145 },
    { date: '03-06', count: 132 },
    { date: '03-07', count: 178 },
    { date: '03-08', count: 156 },
    { date: '03-09', count: 189 },
    { date: '03-10', count: 156 }
  ]
}

const loadStatistics = async () => {
  userRanking.value = [
    { user_name: '张三', count: 256, accuracy: 98.5, points: 1280 },
    { user_name: '李四', count: 198, accuracy: 97.2, points: 990 },
    { user_name: '王五', count: 176, accuracy: 96.8, points: 880 },
    { user_name: '赵六', count: 165, accuracy: 95.5, points: 825 },
    { user_name: '钱七', count: 152, accuracy: 94.3, points: 760 }
  ]

  itemRanking.value = [
    { item_name: '塑料饮料瓶', category: 'recyclable', count: 856 },
    { item_name: '剩饭剩菜', category: 'wet', count: 723 },
    { item_name: '餐巾纸', category: 'dry', count: 612 },
    { item_name: '废旧电池', category: 'hazardous', count: 458 },
    { item_name: '玻璃瓶', category: 'recyclable', count: 398 }
  ]

  hourlyData.value = Array.from({ length: 24 }, (_, i) => ({
    hour: i,
    count: Math.floor(Math.random() * 100) + (i >= 8 && i <= 20 ? 50 : 0)
  }))
}

onMounted(() => {
  loadTrendData()
  loadStatistics()
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

.stat-card {
  border-radius: 12px;
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

.stat-card.total .stat-icon { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-card.users .stat-icon { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.stat-card.accuracy .stat-icon { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-card.today .stat-icon { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.chart-card {
  border-radius: 12px;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pie-chart-container {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 20px;
}

.pie-chart {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(
    #67C23A 0deg 129.6deg,
    #F56C6C 129.6deg 155.2deg,
    #E6A23C 155.2deg 257.6deg,
    #909399 257.6deg 360deg
  );
  position: relative;
}

.pie-chart::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: white;
  border-radius: 50%;
}

.pie-legend {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.legend-dot.recyclable { background: #67C23A; }
.legend-dot.hazardous { background: #F56C6C; }
.legend-dot.wet { background: #E6A23C; }
.legend-dot.dry { background: #909399; }

.legend-value {
  margin-left: auto;
  font-weight: bold;
  color: #303133;
}

.trend-chart {
  padding: 20px;
  height: 250px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 200px;
  padding-top: 20px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 60px;
}

.bar {
  width: 30px;
  background: linear-gradient(180deg, #409EFF 0%, #79bbff 100%);
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: height 0.3s;
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

.user-info {
  display: flex;
  align-items: center;
}

.hourly-chart {
  padding: 20px;
}

.hourly-bars {
  display: flex;
  align-items: flex-end;
  height: 150px;
  gap: 4px;
}

.hourly-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hourly-bar {
  width: 100%;
  background: linear-gradient(180deg, #67C23A 0%, #95d475 100%);
  border-radius: 2px 2px 0 0;
  position: relative;
  min-height: 2px;
}

.hourly-value {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  color: #606266;
  white-space: nowrap;
}

.hourly-label {
  margin-top: 5px;
  font-size: 10px;
  color: #909399;
}
</style>
