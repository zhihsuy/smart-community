<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>家居节能优化</h1>
        <p>管理家居节能方案、设备监控和节能数据</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalDevices || 0 }}</div>
          <div class="stat-label">智能设备</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.optimizedHomes || 0 }}</div>
          <div class="stat-label">优化家庭</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.energySaved || 0 }} kWh</div>
          <div class="stat-label">节约能源</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">¥{{ stats.costSaved || 0 }}</div>
          <div class="stat-label">节省费用</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="设备监控" name="devices">
          <div class="filter-bar">
            <el-select v-model="filterDeviceType" placeholder="设备类型" clearable style="width: 150px;" @change="loadDevices">
              <el-option label="空调" value="air conditioner" />
              <el-option label="照明" value="light" />
              <el-option label="热水器" value="water heater" />
              <el-option label="冰箱" value="refrigerator" />
              <el-option label="洗衣机" value="washing machine" />
            </el-select>
            <el-select v-model="filterStatus" placeholder="状态" clearable style="width: 120px; margin-left: 10px;" @change="loadDevices">
              <el-option label="在线" value="online" />
              <el-option label="离线" value="offline" />
            </el-select>
            <el-input v-model="searchKeyword" placeholder="搜索设备" style="width: 200px; margin-left: 10px;" clearable />
            <el-button type="primary" style="margin-left: 10px;" @click="loadDevices">查询</el-button>
          </div>

          <el-table :data="devices" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="设备名称" min-width="150" />
            <el-table-column prop="type" label="设备类型" width="120">
              <template #default="scope">
                <el-tag size="small">{{ getDeviceTypeName(scope.row.type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="home_address" label="家庭地址" min-width="150" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'online' ? 'success' : 'danger'">
                  {{ scope.row.status === 'online' ? '在线' : '离线' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="energy_consumption" label="能耗" width="120">
              <template #default="scope">
                {{ scope.row.energy_consumption }} kWh
              </template>
            </el-table-column>
            <el-table-column prop="last_active" label="最后活跃" width="160" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewDevice(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="controlDevice(scope.row)">控制</el-button>
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

        <el-tab-pane label="节能方案" name="plans">
          <div class="plan-header">
            <h4>节能方案管理</h4>
            <el-button type="primary" @click="showAddPlanDialog = true">
              <el-icon><Plus /></el-icon> 添加方案
            </el-button>
          </div>

          <el-table :data="plans" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="name" label="方案名称" width="180" />
            <el-table-column prop="type" label="方案类型" width="120">
              <template #default="scope">
                <el-tag :type="getPlanType(scope.row.type)" size="small">
                  {{ getPlanTypeName(scope.row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="energy_saving" label="节能效果" width="120">
              <template #default="scope">
                {{ scope.row.energy_saving }}%
              </template>
            </el-table-column>
            <el-table-column prop="cost" label="实施成本" width="100">
              <template #default="scope">
                ¥{{ scope.row.cost }}
              </template>
            </el-table-column>
            <el-table-column prop="popularity" label="使用次数" width="100" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewPlan(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="editPlan(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deletePlan(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="节能统计" name="statistics">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>设备能耗分布</span>
                </template>
                <div class="energy-distribution">
                  <div v-for="item in energyDistribution" :key="item.type" class="energy-item">
                    <div class="energy-info">
                      <span class="energy-name">{{ getDeviceTypeName(item.type) }}</span>
                      <span class="energy-value">{{ item.consumption }} kWh</span>
                    </div>
                    <el-progress :percentage="item.percentage" :stroke-width="10" />
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>节能趋势</span>
                </template>
                <div class="trend-chart">
                  <div class="chart-bars">
                    <div v-for="(item, index) in energyTrend" :key="index" class="bar-item">
                      <div class="bar" :style="{ height: getBarHeight(item.energy) + '%' }">
                        <span class="bar-value">{{ item.energy }} kWh</span>
                      </div>
                      <span class="bar-label">{{ item.month }}</span>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <el-tab-pane label="用户节能排行" name="ranking">
          <el-table :data="userRanking" style="width: 100%">
            <el-table-column prop="rank" label="排名" width="80">
              <template #default="scope">
                <div class="rank-number" :class="{ 'top3': scope.row.rank <= 3 }">
                  {{ scope.row.rank }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="user_name" label="用户" width="150">
              <template #default="scope">
                <div class="user-info">
                  <el-avatar :size="32">{{ scope.row.user_name?.charAt(0) }}</el-avatar>
                  <span style="margin-left: 10px;">{{ scope.row.user_name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="home_address" label="家庭地址" min-width="150" />
            <el-table-column prop="energy_saved" label="节能总量" width="120">
              <template #default="scope">
                <span class="energy-saved">{{ scope.row.energy_saved }} kWh</span>
              </template>
            </el-table-column>
            <el-table-column prop="cost_saved" label="节省费用" width="120">
              <template #default="scope">
                <span class="cost-saved">¥{{ scope.row.cost_saved }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="rank_change" label="排名变化" width="100">
              <template #default="scope">
                <span :class="{ 'rank-up': scope.row.rank_change < 0, 'rank-down': scope.row.rank_change > 0, 'rank-same': scope.row.rank_change === 0 }">
                  {{ scope.row.rank_change < 0 ? '↑' : scope.row.rank_change > 0 ? '↓' : '→' }} {{ Math.abs(scope.row.rank_change) }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showAddPlanDialog" title="添加节能方案" width="500px">
      <el-form :model="planForm" label-width="100px">
        <el-form-item label="方案名称">
          <el-input v-model="planForm.name" placeholder="请输入方案名称" />
        </el-form-item>
        <el-form-item label="方案类型">
          <el-select v-model="planForm.type" style="width: 100%;">
            <el-option label="照明节能" value="lighting" />
            <el-option label="空调节能" value="air conditioner" />
            <el-option label="热水节能" value="water heating" />
            <el-option label="综合节能" value="comprehensive" />
          </el-select>
        </el-form-item>
        <el-form-item label="节能效果">
          <el-input-number v-model="planForm.energy_saving" :min="0" :max="100" />
          <span style="margin-left: 10px;">%</span>
        </el-form-item>
        <el-form-item label="实施成本">
          <el-input-number v-model="planForm.cost" :min="0" />
          <span style="margin-left: 10px;">元</span>
        </el-form-item>
        <el-form-item label="适用面积">
          <el-input-number v-model="planForm.area_min" :min="0" style="width: 100px;" />
          <span style="margin: 0 10px;">至</span>
          <el-input-number v-model="planForm.area_max" :min="0" style="width: 100px;" />
          <span style="margin-left: 10px;">平方米</span>
        </el-form-item>
        <el-form-item label="方案描述">
          <el-input v-model="planForm.description" type="textarea" rows="4" placeholder="请输入方案详细描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddPlanDialog = false">取消</el-button>
        <el-button type="primary" @click="savePlan">保存</el-button>
      </template>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('devices')
const loading = ref(false)
const filterDeviceType = ref('')
const filterStatus = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddPlanDialog = ref(false)

const stats = ref({
  totalDevices: 1256,
  optimizedHomes: 890,
  energySaved: 5680,
  costSaved: 3450
})

const devices = ref([])
const plans = ref([])
const energyDistribution = ref([])
const energyTrend = ref([])
const userRanking = ref([])
const planForm = ref({ name: '', type: 'lighting', energy_saving: 0, cost: 0, area_min: 0, area_max: 0, description: '' })

const loadDevices = () => {
  devices.value = [
    { id: 1, name: '客厅空调', type: 'air conditioner', home_address: '幸福小区 1-101', status: 'online', energy_consumption: 12.5, last_active: '2024-01-15 10:30:00' },
    { id: 2, name: '卧室照明', type: 'light', home_address: '幸福小区 1-101', status: 'online', energy_consumption: 1.2, last_active: '2024-01-15 09:00:00' },
    { id: 3, name: '厨房热水器', type: 'water heater', home_address: '幸福小区 2-202', status: 'offline', energy_consumption: 8.7, last_active: '2024-01-14 20:00:00' }
  ]
  total.value = 3
}

const loadPlans = () => {
  plans.value = [
    { id: 1, name: 'LED照明改造', type: 'lighting', energy_saving: 75, cost: 500, popularity: 1256 },
    { id: 2, name: '智能空调控制', type: 'air conditioner', energy_saving: 30, cost: 800, popularity: 890 },
    { id: 3, name: '太阳能热水器', type: 'water heating', energy_saving: 80, cost: 3000, popularity: 456 },
    { id: 4, name: '全屋节能改造', type: 'comprehensive', energy_saving: 45, cost: 5000, popularity: 234 }
  ]
}

const loadStatistics = () => {
  energyDistribution.value = [
    { type: 'air conditioner', consumption: 4500, percentage: 45 },
    { type: 'water heater', consumption: 2500, percentage: 25 },
    { type: 'refrigerator', consumption: 1500, percentage: 15 },
    { type: 'light', consumption: 1000, percentage: 10 },
    { type: 'washing machine', consumption: 500, percentage: 5 }
  ]
  energyTrend.value = [
    { month: '1月', energy: 1200 },
    { month: '2月', energy: 1100 },
    { month: '3月', energy: 950 },
    { month: '4月', energy: 800 },
    { month: '5月', energy: 750 },
    { month: '6月', energy: 700 }
  ]
}

const loadUserRanking = () => {
  userRanking.value = [
    { rank: 1, user_name: '张三', home_address: '幸福小区 1-101', energy_saved: 1250, cost_saved: 750, rank_change: 0 },
    { rank: 2, user_name: '李四', home_address: '幸福小区 2-202', energy_saved: 980, cost_saved: 588, rank_change: 1 },
    { rank: 3, user_name: '王五', home_address: '幸福小区 3-303', energy_saved: 850, cost_saved: 510, rank_change: -1 },
    { rank: 4, user_name: '赵六', home_address: '幸福小区 4-404', energy_saved: 720, cost_saved: 432, rank_change: 2 },
    { rank: 5, user_name: '钱七', home_address: '幸福小区 5-505', energy_saved: 650, cost_saved: 390, rank_change: -1 }
  ]
}

const viewDevice = (device) => {
  ElMessage.info('查看设备详情')
}

const controlDevice = (device) => {
  ElMessage.info('控制设备')
}

const savePlan = () => {
  ElMessage.success('方案保存成功')
  showAddPlanDialog.value = false
  loadPlans()
}

const viewPlan = (plan) => {
  ElMessage.info('查看方案详情')
}

const editPlan = (plan) => {
  planForm.value = { ...plan }
  showAddPlanDialog.value = true
}

const deletePlan = async (plan) => {
  try {
    await ElMessageBox.confirm('确定要删除该方案吗？', '提示', { type: 'warning' })
    ElMessage.success('方案删除成功')
    loadPlans()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const getDeviceTypeName = (type) => {
  const map = { 'air conditioner': '空调', 'light': '照明', 'water heater': '热水器', 'refrigerator': '冰箱', 'washing machine': '洗衣机' }
  return map[type] || type
}

const getPlanType = (type) => {
  const map = { 'lighting': 'success', 'air conditioner': 'primary', 'water heating': 'warning', 'comprehensive': 'info' }
  return map[type] || 'info'
}

const getPlanTypeName = (type) => {
  const map = { 'lighting': '照明节能', 'air conditioner': '空调节能', 'water heating': '热水节能', 'comprehensive': '综合节能' }
  return map[type] || type
}

const getBarHeight = (energy) => {
  const max = Math.max(...energyTrend.value.map(t => t.energy), 1)
  return (energy / max) * 100
}

onMounted(() => {
  loadDevices()
  loadPlans()
  loadStatistics()
  loadUserRanking()
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
  flex-wrap: wrap;
  gap: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.plan-header h4 {
  margin: 0;
  font-size: 16px;
}

.energy-distribution {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
}

.energy-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.energy-info {
  display: flex;
  justify-content: space-between;
}

.energy-name {
  font-size: 14px;
  color: #606266;
}

.energy-value {
  font-size: 14px;
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
  background: linear-gradient(180deg, #67C23A 0%, #b3e699 100%);
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

.user-info {
  display: flex;
  align-items: center;
}

.rank-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: #606266;
}

.rank-number.top3 {
  background: #f7ba2a;
  color: white;
}

.energy-saved {
  color: #67C23A;
  font-weight: bold;
}

.cost-saved {
  color: #E6A23C;
  font-weight: bold;
}

.rank-up {
  color: #67C23A;
  font-weight: bold;
}

.rank-down {
  color: #F56C6C;
  font-weight: bold;
}

.rank-same {
  color: #909399;
}
</style>