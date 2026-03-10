<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>碳足迹管理</h1>
        <p>管理用户碳足迹数据、减排目标和减排活动</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon carbon">
              <el-icon :size="32"><Cloudy /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalCarbon || 0 }}</div>
              <div class="stat-label">总碳排放量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon reduction">
              <el-icon :size="32"><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.reduction || 0 }}%</div>
              <div class="stat-label">减排比例</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon users">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.activeUsers || 0 }}</div>
              <div class="stat-label">参与用户</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon target">
              <el-icon :size="32"><Aim /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.targetProgress || 0 }}%</div>
              <div class="stat-label">目标进度</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="碳排放概览" name="overview">
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="chart-section">
                <h4>碳排放趋势</h4>
                <div class="trend-chart">
                  <div class="chart-line">
                    <svg viewBox="0 0 400 150" class="line-svg">
                      <polyline
                        :points="carbonLinePoints"
                        fill="none"
                        stroke="#409EFF"
                        stroke-width="2"
                      />
                    </svg>
                  </div>
                  <div class="chart-labels">
                    <span v-for="(item, index) in carbonTrend" :key="index">{{ item.month }}</span>
                  </div>
                </div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-section">
                <h4>碳排放来源分布</h4>
                <div class="source-list">
                  <div v-for="source in carbonSources" :key="source.name" class="source-item">
                    <div class="source-info">
                      <span class="source-name">{{ source.name }}</span>
                      <span class="source-value">{{ source.value }} kg CO₂</span>
                    </div>
                    <el-progress :percentage="source.percentage" :stroke-width="10" :color="source.color" />
                  </div>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>

        <el-tab-pane label="用户碳足迹" name="users">
          <div class="filter-bar">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
            />
            <el-input v-model="searchKeyword" placeholder="搜索用户" style="width: 200px; margin-left: 10px;" clearable>
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button type="primary" style="margin-left: 10px;" @click="loadUserCarbon">查询</el-button>
          </div>

          <el-table :data="userCarbonList" style="width: 100%" v-loading="loading">
            <el-table-column prop="user_name" label="用户" width="120">
              <template #default="scope">
                <div class="user-info">
                  <el-avatar :size="24">{{ scope.row.user_name?.charAt(0) }}</el-avatar>
                  <span style="margin-left: 8px;">{{ scope.row.user_name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="total_carbon" label="总碳排放" width="120">
              <template #default="scope">
                {{ scope.row.total_carbon }} kg CO₂
              </template>
            </el-table-column>
            <el-table-column prop="transport_carbon" label="交通排放" width="120">
              <template #default="scope">
                {{ scope.row.transport_carbon }} kg CO₂
              </template>
            </el-table-column>
            <el-table-column prop="energy_carbon" label="能源排放" width="120">
              <template #default="scope">
                {{ scope.row.energy_carbon }} kg CO₂
              </template>
            </el-table-column>
            <el-table-column prop="food_carbon" label="饮食排放" width="120">
              <template #default="scope">
                {{ scope.row.food_carbon }} kg CO₂
              </template>
            </el-table-column>
            <el-table-column prop="reduction" label="减排量" width="100">
              <template #default="scope">
                <span class="reduction-value">-{{ scope.row.reduction }} kg</span>
              </template>
            </el-table-column>
            <el-table-column prop="update_time" label="更新时间" width="160" />
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewUserDetail(scope.row)">详情</el-button>
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

        <el-tab-pane label="减排目标" name="targets">
          <div class="target-header">
            <h4>年度减排目标设置</h4>
            <el-button type="primary" @click="showAddTargetDialog = true">
              <el-icon><Plus /></el-icon> 添加目标
            </el-button>
          </div>

          <el-table :data="targets" style="width: 100%">
            <el-table-column prop="year" label="年份" width="100" />
            <el-table-column prop="target_value" label="目标减排量" width="150">
              <template #default="scope">
                {{ scope.row.target_value }} kg CO₂
              </template>
            </el-table-column>
            <el-table-column prop="current_value" label="当前减排量" width="150">
              <template #default="scope">
                {{ scope.row.current_value }} kg CO₂
              </template>
            </el-table-column>
            <el-table-column prop="progress" label="完成进度" width="200">
              <template #default="scope">
                <el-progress :percentage="scope.row.progress" :stroke-width="15" />
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
                  {{ scope.row.status === 'active' ? '进行中' : '已完成' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editTarget(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteTarget(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="减排活动" name="activities">
          <div class="activity-header">
            <h4>减排活动管理</h4>
            <el-button type="primary" @click="showAddActivityDialog = true">
              <el-icon><Plus /></el-icon> 创建活动
            </el-button>
          </div>

          <el-row :gutter="20">
            <el-col :span="8" v-for="activity in activities" :key="activity.id">
              <el-card class="activity-card" shadow="hover">
                <div class="activity-image">
                  <el-icon :size="48"><Calendar /></el-icon>
                </div>
                <div class="activity-content">
                  <h4>{{ activity.name }}</h4>
                  <p class="activity-desc">{{ activity.description }}</p>
                  <div class="activity-stats">
                    <span>参与: {{ activity.participants }}人</span>
                    <span>减排: {{ activity.reduction }}kg CO₂</span>
                  </div>
                  <div class="activity-actions">
                    <el-button size="small" type="primary" @click="editActivity(activity)">编辑</el-button>
                    <el-button size="small" type="danger" @click="deleteActivity(activity)">删除</el-button>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showAddTargetDialog" title="添加减排目标" width="500px">
      <el-form :model="targetForm" label-width="120px">
        <el-form-item label="年份">
          <el-date-picker v-model="targetForm.year" type="year" placeholder="选择年份" />
        </el-form-item>
        <el-form-item label="目标减排量">
          <el-input-number v-model="targetForm.target_value" :min="0" />
          <span style="margin-left: 10px;">kg CO₂</span>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="targetForm.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddTargetDialog = false">取消</el-button>
        <el-button type="primary" @click="saveTarget">保存</el-button>
      </template>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Cloudy, TrendCharts, User, Aim, Search, Plus, Calendar } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('overview')
const loading = ref(false)
const dateRange = ref([])
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddTargetDialog = ref(false)

const stats = ref({
  totalCarbon: 125680,
  reduction: 15.8,
  activeUsers: 4520,
  targetProgress: 68
})

const carbonTrend = ref([
  { month: '1月', value: 12000 },
  { month: '2月', value: 11500 },
  { month: '3月', value: 10800 },
  { month: '4月', value: 10200 },
  { month: '5月', value: 9800 },
  { month: '6月', value: 9200 }
])

const carbonSources = ref([
  { name: '交通出行', value: 45000, percentage: 36, color: '#409EFF' },
  { name: '家庭能源', value: 38000, percentage: 30, color: '#67C23A' },
  { name: '饮食消费', value: 28000, percentage: 22, color: '#E6A23C' },
  { name: '购物消费', value: 14680, percentage: 12, color: '#F56C6C' }
])

const userCarbonList = ref([])
const targets = ref([])
const activities = ref([])
const targetForm = ref({ year: '', target_value: 0, description: '' })

const carbonLinePoints = computed(() => {
  const max = Math.max(...carbonTrend.value.map(t => t.value))
  return carbonTrend.value.map((t, i) => {
    const x = (i / (carbonTrend.value.length - 1)) * 380 + 10
    const y = 140 - (t.value / max) * 120
    return `${x},${y}`
  }).join(' ')
})

const loadUserCarbon = () => {
  userCarbonList.value = [
    { user_name: '张三', total_carbon: 1250, transport_carbon: 450, energy_carbon: 380, food_carbon: 420, reduction: 180, update_time: '2024-01-15' },
    { user_name: '李四', total_carbon: 980, transport_carbon: 320, energy_carbon: 290, food_carbon: 370, reduction: 150, update_time: '2024-01-15' },
    { user_name: '王五', total_carbon: 1560, transport_carbon: 580, energy_carbon: 420, food_carbon: 560, reduction: 200, update_time: '2024-01-14' }
  ]
  total.value = 3
}

const loadTargets = () => {
  targets.value = [
    { year: 2024, target_value: 50000, current_value: 34000, progress: 68, status: 'active' },
    { year: 2023, target_value: 40000, current_value: 42000, progress: 105, status: 'completed' }
  ]
}

const loadActivities = () => {
  activities.value = [
    { id: 1, name: '绿色出行周', description: '鼓励居民使用公共交通', participants: 256, reduction: 1250 },
    { id: 2, name: '节能减碳日', description: '减少家庭能源消耗', participants: 189, reduction: 890 },
    { id: 3, name: '植树活动', description: '社区植树造林活动', participants: 120, reduction: 560 }
  ]
}

const viewUserDetail = (row) => {
  ElMessage.info(`查看用户 ${row.user_name} 的碳足迹详情`)
}

const saveTarget = () => {
  ElMessage.success('目标保存成功')
  showAddTargetDialog.value = false
  loadTargets()
}

const editTarget = (row) => {
  targetForm.value = { ...row }
  showAddTargetDialog.value = true
}

const deleteTarget = (row) => {
  ElMessage.success('目标删除成功')
  loadTargets()
}

const editActivity = (row) => {
  ElMessage.info(`编辑活动: ${row.name}`)
}

const deleteActivity = (row) => {
  ElMessage.success('活动删除成功')
  loadActivities()
}

onMounted(() => {
  loadUserCarbon()
  loadTargets()
  loadActivities()
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

.stat-content {
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

.stat-icon.carbon { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-icon.reduction { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.stat-icon.users { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-icon.target { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.main-card {
  border-radius: 12px;
}

.chart-section {
  padding: 20px;
}

.chart-section h4 {
  margin: 0 0 20px 0;
  font-size: 16px;
  color: #303133;
}

.trend-chart {
  height: 200px;
  position: relative;
}

.line-svg {
  width: 100%;
  height: 150px;
}

.chart-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
  font-size: 12px;
  color: #909399;
}

.source-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.source-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.source-info {
  display: flex;
  justify-content: space-between;
}

.source-name {
  font-size: 14px;
  color: #606266;
}

.source-value {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
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

.reduction-value {
  color: #67C23A;
  font-weight: bold;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.target-header, .activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.target-header h4, .activity-header h4 {
  margin: 0;
  font-size: 16px;
}

.activity-card {
  margin-bottom: 20px;
}

.activity-image {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px 8px 0 0;
}

.activity-content {
  padding: 15px;
}

.activity-content h4 {
  margin: 0 0 10px 0;
}

.activity-desc {
  font-size: 13px;
  color: #909399;
  margin-bottom: 10px;
}

.activity-stats {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #606266;
  margin-bottom: 10px;
}

.activity-actions {
  display: flex;
  gap: 10px;
}
</style>
