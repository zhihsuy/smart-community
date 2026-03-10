<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>绿色出行规划</h1>
        <p>管理绿色出行路线、交通方式和用户出行数据</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalTrips || 0 }}</div>
          <div class="stat-label">总出行次数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.greenTrips || 0 }}</div>
          <div class="stat-label">绿色出行</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.carbonSaved || 0 }} kg</div>
          <div class="stat-label">减少碳排放</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.activeUsers || 0 }}</div>
          <div class="stat-label">活跃用户</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="出行记录" name="trips">
          <div class="filter-bar">
            <el-select v-model="filterTransport" placeholder="交通方式" clearable style="width: 120px;" @change="loadTrips">
              <el-option label="步行" value="walk" />
              <el-option label="骑行" value="bike" />
              <el-option label="公交" value="bus" />
              <el-option label="地铁" value="subway" />
              <el-option label="私家车" value="car" />
            </el-select>
            <el-input v-model="searchKeyword" placeholder="搜索用户" style="width: 180px; margin-left: 10px;" clearable />
            <el-button type="primary" style="margin-left: 10px;" @click="loadTrips">查询</el-button>
          </div>

          <el-table :data="trips" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="user_name" label="用户" width="120">
              <template #default="scope">
                <div class="user-info">
                  <el-avatar :size="24">{{ scope.row.user_name?.charAt(0) }}</el-avatar>
                  <span style="margin-left: 8px;">{{ scope.row.user_name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="start_point" label="起点" min-width="150" />
            <el-table-column prop="end_point" label="终点" min-width="150" />
            <el-table-column prop="transport" label="交通方式" width="100">
              <template #default="scope">
                <el-tag :type="getTransportType(scope.row.transport)" size="small">
                  {{ getTransportName(scope.row.transport) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="distance" label="距离" width="100">
              <template #default="scope">
                {{ scope.row.distance }} km
              </template>
            </el-table-column>
            <el-table-column prop="duration" label="时长" width="100">
              <template #default="scope">
                {{ scope.row.duration }} min
              </template>
            </el-table-column>
            <el-table-column prop="carbon_saved" label="减少碳排放" width="120">
              <template #default="scope">
                <span class="carbon-value">{{ scope.row.carbon_saved || 0 }} kg</span>
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="出行时间" width="160" />
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewTrip(scope.row)">详情</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              :page-sizes="[10, 20, 50]"
              layout="total, sizes, prev, pager, next"
            />
          </div>
        </el-tab-pane>

        <el-tab-pane label="路线管理" name="routes">
          <div class="route-header">
            <h4>常用路线</h4>
            <el-button type="primary" @click="showAddRouteDialog = true">
              <el-icon><Plus /></el-icon> 添加路线
            </el-button>
          </div>

          <el-table :data="routes" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="路线名称" width="150" />
            <el-table-column prop="start_point" label="起点" min-width="150" />
            <el-table-column prop="end_point" label="终点" min-width="150" />
            <el-table-column prop="distance" label="距离" width="100">
              <template #default="scope">
                {{ scope.row.distance }} km
              </template>
            </el-table-column>
            <el-table-column prop="popularity" label="使用次数" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.status" @change="toggleRouteStatus(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editRoute(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteRoute(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="交通方式" name="transport">
          <div class="transport-header">
            <h4>交通方式配置</h4>
          </div>

          <el-table :data="transportOptions" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="交通方式" width="120" />
            <el-table-column prop="carbon_per_km" label="碳排放/km" width="120">
              <template #default="scope">
                {{ scope.row.carbon_per_km }} kg
              </template>
            </el-table-column>
            <el-table-column prop="speed" label="平均速度" width="100">
              <template #default="scope">
                {{ scope.row.speed }} km/h
              </template>
            </el-table-column>
            <el-table-column prop="price_per_km" label="费用/km" width="100">
              <template #default="scope">
                ¥{{ scope.row.price_per_km }}
              </template>
            </el-table-column>
            <el-table-column prop="is_green" label="绿色出行" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.is_green ? 'success' : 'info'" size="small">
                  {{ scope.row.is_green ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editTransport(scope.row)">编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="统计分析" name="statistics">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>出行方式分布</span>
                </template>
                <div class="transport-distribution">
                  <div class="pie-chart">
                    <div class="pie-segment walk" :style="{ transform: `rotate(${getPieRotation('walk')}deg)` }"></div>
                    <div class="pie-segment bike" :style="{ transform: `rotate(${getPieRotation('bike')}deg)` }"></div>
                    <div class="pie-segment bus" :style="{ transform: `rotate(${getPieRotation('bus')}deg)` }"></div>
                    <div class="pie-segment subway" :style="{ transform: `rotate(${getPieRotation('subway')}deg)` }"></div>
                    <div class="pie-segment car" :style="{ transform: `rotate(${getPieRotation('car')}deg)` }"></div>
                  </div>
                  <div class="pie-legend">
                    <div class="legend-item">
                      <span class="legend-dot walk"></span>
                      <span>步行</span>
                      <span class="legend-value">{{ transportStats.walk || 0 }}%</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-dot bike"></span>
                      <span>骑行</span>
                      <span class="legend-value">{{ transportStats.bike || 0 }}%</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-dot bus"></span>
                      <span>公交</span>
                      <span class="legend-value">{{ transportStats.bus || 0 }}%</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-dot subway"></span>
                      <span>地铁</span>
                      <span class="legend-value">{{ transportStats.subway || 0 }}%</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-dot car"></span>
                      <span>私家车</span>
                      <span class="legend-value">{{ transportStats.car || 0 }}%</span>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>碳排放趋势</span>
                </template>
                <div class="trend-chart">
                  <div class="chart-bars">
                    <div v-for="(item, index) in carbonTrend" :key="index" class="bar-item">
                      <div class="bar" :style="{ height: getBarHeight(item.carbon) + '%' }">
                        <span class="bar-value">{{ item.carbon }} kg</span>
                      </div>
                      <span class="bar-label">{{ item.week }}</span>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showAddRouteDialog" title="添加路线" width="500px">
      <el-form :model="routeForm" label-width="100px">
        <el-form-item label="路线名称">
          <el-input v-model="routeForm.name" placeholder="请输入路线名称" />
        </el-form-item>
        <el-form-item label="起点">
          <el-input v-model="routeForm.start_point" placeholder="请输入起点" />
        </el-form-item>
        <el-form-item label="终点">
          <el-input v-model="routeForm.end_point" placeholder="请输入终点" />
        </el-form-item>
        <el-form-item label="距离">
          <el-input-number v-model="routeForm.distance" :min="0.1" :step="0.1" />
          <span style="margin-left: 10px;">km</span>
        </el-form-item>
        <el-form-item label="推荐方式">
          <el-select v-model="routeForm.recommended_transport" style="width: 100%;">
            <el-option label="步行" value="walk" />
            <el-option label="骑行" value="bike" />
            <el-option label="公交" value="bus" />
            <el-option label="地铁" value="subway" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddRouteDialog = false">取消</el-button>
        <el-button type="primary" @click="saveRoute">保存</el-button>
      </template>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('trips')
const loading = ref(false)
const filterTransport = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddRouteDialog = ref(false)

const stats = ref({
  totalTrips: 5680,
  greenTrips: 4250,
  carbonSaved: 1250,
  activeUsers: 2890
})

const trips = ref([])
const routes = ref([])
const transportOptions = ref([])
const transportStats = ref({})
const carbonTrend = ref([])
const routeForm = ref({ name: '', start_point: '', end_point: '', distance: 0, recommended_transport: 'walk' })

const loadTrips = () => {
  trips.value = [
    { id: 1, user_name: '张三', start_point: '家', end_point: '公司', transport: 'subway', distance: 5.2, duration: 25, carbon_saved: 0.8, create_time: '2024-01-15 08:30:00' },
    { id: 2, user_name: '李四', start_point: '家', end_point: '超市', transport: 'walk', distance: 1.5, duration: 20, carbon_saved: 0.3, create_time: '2024-01-15 14:00:00' },
    { id: 3, user_name: '王五', start_point: '家', end_point: '公园', transport: 'bike', distance: 3.8, duration: 15, carbon_saved: 0.6, create_time: '2024-01-14 16:30:00' }
  ]
  total.value = 3
}

const loadRoutes = () => {
  routes.value = [
    { id: 1, name: '家到公司', start_point: '幸福小区', end_point: '科技园', distance: 5.2, popularity: 1256, status: true, recommended_transport: 'subway' },
    { id: 2, name: '家到超市', start_point: '幸福小区', end_point: '世纪超市', distance: 1.5, popularity: 890, status: true, recommended_transport: 'walk' },
    { id: 3, name: '家到公园', start_point: '幸福小区', end_point: '中央公园', distance: 3.8, popularity: 654, status: true, recommended_transport: 'bike' }
  ]
}

const loadTransportOptions = () => {
  transportOptions.value = [
    { id: 1, name: '步行', carbon_per_km: 0, speed: 4, price_per_km: 0, is_green: true },
    { id: 2, name: '骑行', carbon_per_km: 0, speed: 15, price_per_km: 0, is_green: true },
    { id: 3, name: '公交', carbon_per_km: 0.1, speed: 20, price_per_km: 2, is_green: true },
    { id: 4, name: '地铁', carbon_per_km: 0.05, speed: 30, price_per_km: 3, is_green: true },
    { id: 5, name: '私家车', carbon_per_km: 0.2, speed: 35, price_per_km: 1.5, is_green: false }
  ]
}

const loadStatistics = () => {
  transportStats.value = {
    walk: 25,
    bike: 20,
    bus: 15,
    subway: 30,
    car: 10
  }
  carbonTrend.value = [
    { week: '第1周', carbon: 120 },
    { week: '第2周', carbon: 110 },
    { week: '第3周', carbon: 95 },
    { week: '第4周', carbon: 80 },
    { week: '第5周', carbon: 70 }
  ]
}

const viewTrip = (trip) => {
  ElMessage.info('查看出行详情')
}

const saveRoute = () => {
  ElMessage.success('路线保存成功')
  showAddRouteDialog.value = false
  loadRoutes()
}

const editRoute = (route) => {
  routeForm.value = { ...route }
  showAddRouteDialog.value = true
}

const deleteRoute = async (route) => {
  try {
    await ElMessageBox.confirm('确定要删除该路线吗？', '提示', { type: 'warning' })
    ElMessage.success('路线删除成功')
    loadRoutes()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const toggleRouteStatus = (route) => {
  ElMessage.success(`路线已${route.status ? '启用' : '禁用'}`)
}

const editTransport = (transport) => {
  ElMessage.info('编辑交通方式')
}

const getTransportType = (transport) => {
  const map = { 'walk': 'success', 'bike': 'success', 'bus': 'success', 'subway': 'success', 'car': 'info' }
  return map[transport] || 'info'
}

const getTransportName = (transport) => {
  const map = { 'walk': '步行', 'bike': '骑行', 'bus': '公交', 'subway': '地铁', 'car': '私家车' }
  return map[transport] || transport
}

const getPieRotation = (transport) => {
  const order = ['walk', 'bike', 'bus', 'subway', 'car']
  let rotation = 0
  for (const t of order) {
    if (t === transport) break
    rotation += (transportStats.value[t] || 0) * 3.6
  }
  return rotation
}

const getBarHeight = (carbon) => {
  const max = Math.max(...carbonTrend.value.map(t => t.carbon), 1)
  return (carbon / max) * 100
}

onMounted(() => {
  loadTrips()
  loadRoutes()
  loadTransportOptions()
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
  text-align: center;
  border-radius: 8px;
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

.main-card {
  border-radius: 12px;
}

.filter-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.route-header, .transport-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.route-header h4, .transport-header h4 {
  margin: 0;
  font-size: 16px;
}

.carbon-value {
  color: #67C23A;
  font-weight: bold;
}

.transport-distribution {
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
    #67C23A 0deg 90deg,
    #409EFF 90deg 162deg,
    #E6A23C 162deg 216deg,
    #909399 216deg 324deg,
    #F56C6C 324deg 360deg
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

.legend-dot.walk { background: #67C23A; }
.legend-dot.bike { background: #409EFF; }
.legend-dot.bus { background: #E6A23C; }
.legend-dot.subway { background: #909399; }
.legend-dot.car { background: #F56C6C; }

.legend-value {
  margin-left: auto;
  font-weight: bold;
  color: #303133;
}

.trend-chart {
  height: 200px;
  padding: 20px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 150px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.bar {
  width: 30px;
  background: linear-gradient(180deg, #F56C6C 0%, #fab6b6 100%);
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
</style>
