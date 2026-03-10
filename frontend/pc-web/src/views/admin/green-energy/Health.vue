<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>健康管理</h1>
        <p>管理居民健康数据、健康建议和健康活动</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalUsers || 0 }}</div>
          <div class="stat-label">健康档案</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.healthActivities || 0 }}</div>
          <div class="stat-label">健康活动</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.healthTips || 0 }}</div>
          <div class="stat-label">健康建议</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.avgHealthScore || 0 }}</div>
          <div class="stat-label">平均健康分</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="健康档案" name="profiles">
          <div class="filter-bar">
            <el-input v-model="searchKeyword" placeholder="搜索用户" style="width: 200px;" clearable />
            <el-select v-model="filterHealthLevel" placeholder="健康等级" clearable style="width: 120px; margin-left: 10px;" @change="loadProfiles">
              <el-option label="优秀" value="excellent" />
              <el-option label="良好" value="good" />
              <el-option label="一般" value="normal" />
              <el-option label="需要关注" value="attention" />
            </el-select>
            <el-button type="primary" style="margin-left: 10px;" @click="loadProfiles">查询</el-button>
            <el-button type="success" @click="exportProfiles">
              <el-icon><Download /></el-icon> 导出档案
            </el-button>
          </div>

          <el-table :data="profiles" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="user_name" label="用户" width="120">
              <template #default="scope">
                <div class="user-info">
                  <el-avatar :size="24">{{ scope.row.user_name?.charAt(0) }}</el-avatar>
                  <span style="margin-left: 8px;">{{ scope.row.user_name }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="age" label="年龄" width="80" />
            <el-table-column prop="gender" label="性别" width="80">
              <template #default="scope">
                <el-tag :type="scope.row.gender === 'male' ? 'primary' : 'success'" size="small">
                  {{ scope.row.gender === 'male' ? '男' : '女' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="health_score" label="健康评分" width="100">
              <template #default="scope">
                <div class="health-score" :class="getHealthLevelClass(scope.row.health_score)">
                  {{ scope.row.health_score }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="health_level" label="健康等级" width="120">
              <template #default="scope">
                <el-tag :type="getHealthLevelType(scope.row.health_level)" size="small">
                  {{ getHealthLevelName(scope.row.health_level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="last_update" label="更新时间" width="160" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewProfile(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="generateHealthReport(scope.row)">报告</el-button>
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

        <el-tab-pane label="健康活动" name="activities">
          <div class="activity-header">
            <h4>健康活动管理</h4>
            <el-button type="primary" @click="showAddActivityDialog = true">
              <el-icon><Plus /></el-icon> 添加活动
            </el-button>
          </div>

          <el-table :data="activities" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="title" label="活动标题" min-width="200" />
            <el-table-column prop="type" label="活动类型" width="120">
              <template #default="scope">
                <el-tag :type="getActivityType(scope.row.type)" size="small">
                  {{ getActivityTypeName(scope.row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="start_time" label="开始时间" width="160" />
            <el-table-column prop="end_time" label="结束时间" width="160" />
            <el-table-column prop="participants" label="参与人数" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getActivityStatusType(scope.row.status)" size="small">
                  {{ getActivityStatusName(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewActivity(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="editActivity(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteActivity(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="健康建议" name="tips">
          <div class="tip-header">
            <h4>健康建议管理</h4>
            <el-button type="primary" @click="showAddTipDialog = true">
              <el-icon><Plus /></el-icon> 添加建议
            </el-button>
          </div>

          <el-table :data="healthTips" style="width: 100%">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="title" label="建议标题" min-width="200" />
            <el-table-column prop="category" label="建议分类" width="120">
              <template #default="scope">
                <el-tag size="small">{{ getCategoryName(scope.row.category) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="适用人群" label="适用人群" width="150">
              <template #default="scope">
                {{ scope.row.target_audience }}
              </template>
            </el-table-column>
            <el-table-column prop="view_count" label="查看次数" width="100" />
            <el-table-column prop="create_time" label="创建时间" width="160" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewTip(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="editTip(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteTip(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="健康统计" name="statistics">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>健康等级分布</span>
                </template>
                <div class="health-distribution">
                  <div class="pie-chart">
                    <div class="pie-segment excellent" :style="{ transform: `rotate(${getPieRotation('excellent')}deg)` }"></div>
                    <div class="pie-segment good" :style="{ transform: `rotate(${getPieRotation('good')}deg)` }"></div>
                    <div class="pie-segment normal" :style="{ transform: `rotate(${getPieRotation('normal')}deg)` }"></div>
                    <div class="pie-segment attention" :style="{ transform: `rotate(${getPieRotation('attention')}deg)` }"></div>
                  </div>
                  <div class="pie-legend">
                    <div class="legend-item">
                      <span class="legend-dot excellent"></span>
                      <span>优秀</span>
                      <span class="legend-value">{{ healthStats.excellent || 0 }}%</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-dot good"></span>
                      <span>良好</span>
                      <span class="legend-value">{{ healthStats.good || 0 }}%</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-dot normal"></span>
                      <span>一般</span>
                      <span class="legend-value">{{ healthStats.normal || 0 }}%</span>
                    </div>
                    <div class="legend-item">
                      <span class="legend-dot attention"></span>
                      <span>需要关注</span>
                      <span class="legend-value">{{ healthStats.attention || 0 }}%</span>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>健康评分趋势</span>
                </template>
                <div class="trend-chart">
                  <div class="chart-bars">
                    <div v-for="(item, index) in healthTrend" :key="index" class="bar-item">
                      <div class="bar" :style="{ height: getBarHeight(item.score) + '%' }">
                        <span class="bar-value">{{ item.score }}</span>
                      </div>
                      <span class="bar-label">{{ item.month }}</span>
                    </div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showAddActivityDialog" title="添加健康活动" width="500px">
      <el-form :model="activityForm" label-width="100px">
        <el-form-item label="活动标题">
          <el-input v-model="activityForm.title" placeholder="请输入活动标题" />
        </el-form-item>
        <el-form-item label="活动类型">
          <el-select v-model="activityForm.type" style="width: 100%;">
            <el-option label="运动健身" value="exercise" />
            <el-option label="健康讲座" value="lecture" />
            <el-option label="体检活动" value="physical" />
            <el-option label="心理健康" value="mental" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间">
          <el-date-picker v-model="activityForm.start_time" type="datetime" placeholder="选择开始时间" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker v-model="activityForm.end_time" type="datetime" placeholder="选择结束时间" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="活动地点">
          <el-input v-model="activityForm.location" placeholder="请输入活动地点" />
        </el-form-item>
        <el-form-item label="活动描述">
          <el-input v-model="activityForm.description" type="textarea" rows="4" placeholder="请输入活动详细描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddActivityDialog = false">取消</el-button>
        <el-button type="primary" @click="saveActivity">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showAddTipDialog" title="添加健康建议" width="500px">
      <el-form :model="tipForm" label-width="100px">
        <el-form-item label="建议标题">
          <el-input v-model="tipForm.title" placeholder="请输入建议标题" />
        </el-form-item>
        <el-form-item label="建议分类">
          <el-select v-model="tipForm.category" style="width: 100%;">
            <el-option label="饮食健康" value="diet" />
            <el-option label="运动健康" value="exercise" />
            <el-option label="心理健康" value="mental" />
            <el-option label="生活习惯" value="habit" />
          </el-select>
        </el-form-item>
        <el-form-item label="适用人群">
          <el-input v-model="tipForm.target_audience" placeholder="请输入适用人群" />
        </el-form-item>
        <el-form-item label="建议内容">
          <el-input v-model="tipForm.content" type="textarea" rows="4" placeholder="请输入建议详细内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddTipDialog = false">取消</el-button>
        <el-button type="primary" @click="saveTip">保存</el-button>
      </template>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('profiles')
const loading = ref(false)
const searchKeyword = ref('')
const filterHealthLevel = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showAddActivityDialog = ref(false)
const showAddTipDialog = ref(false)

const stats = ref({
  totalUsers: 2890,
  healthActivities: 56,
  healthTips: 128,
  avgHealthScore: 85
})

const profiles = ref([])
const activities = ref([])
const healthTips = ref([])
const healthStats = ref({})
const healthTrend = ref([])
const activityForm = ref({ title: '', type: 'exercise', start_time: '', end_time: '', location: '', description: '' })
const tipForm = ref({ title: '', category: 'diet', target_audience: '', content: '' })

const loadProfiles = () => {
  profiles.value = [
    { id: 1, user_name: '张三', age: 35, gender: 'male', health_score: 95, health_level: 'excellent', last_update: '2024-01-15 10:30:00' },
    { id: 2, user_name: '李四', age: 42, gender: 'female', health_score: 85, health_level: 'good', last_update: '2024-01-14 16:00:00' },
    { id: 3, user_name: '王五', age: 50, gender: 'male', health_score: 75, health_level: 'normal', last_update: '2024-01-13 09:00:00' },
    { id: 4, user_name: '赵六', age: 65, gender: 'female', health_score: 65, health_level: 'attention', last_update: '2024-01-12 14:00:00' }
  ]
  total.value = 4
}

const loadActivities = () => {
  activities.value = [
    { id: 1, title: '社区健步走活动', type: 'exercise', start_time: '2024-01-20 09:00:00', end_time: '2024-01-20 11:00:00', location: '社区公园', participants: 56, status: 'upcoming' },
    { id: 2, title: '健康饮食讲座', type: 'lecture', start_time: '2024-01-15 14:00:00', end_time: '2024-01-15 16:00:00', location: '社区活动中心', participants: 32, status: 'completed' },
    { id: 3, title: '免费体检活动', type: 'physical', start_time: '2024-01-25 08:00:00', end_time: '2024-01-25 12:00:00', location: '社区医院', participants: 89, status: 'upcoming' }
  ]
}

const loadHealthTips = () => {
  healthTips.value = [
    { id: 1, title: '每日饮水量建议', category: 'diet', target_audience: '所有人群', view_count: 1256, create_time: '2024-01-15 10:00:00', content: '建议每天饮用8杯水，约2000ml，有助于维持身体水分平衡。' },
    { id: 2, title: '适合中老年人的运动', category: 'exercise', target_audience: '中老年人', view_count: 890, create_time: '2024-01-14 15:00:00', content: '建议中老年人每天进行30分钟的有氧运动，如散步、太极等。' },
    { id: 3, title: '缓解压力的方法', category: 'mental', target_audience: '上班族', view_count: 654, create_time: '2024-01-13 09:00:00', content: '建议通过冥想、深呼吸等方式缓解工作压力。' }
  ]
}

const loadStatistics = () => {
  healthStats.value = {
    excellent: 25,
    good: 40,
    normal: 25,
    attention: 10
  }
  healthTrend.value = [
    { month: '1月', score: 82 },
    { month: '2月', score: 83 },
    { month: '3月', score: 84 },
    { month: '4月', score: 85 },
    { month: '5月', score: 86 },
    { month: '6月', score: 87 }
  ]
}

const viewProfile = (profile) => {
  ElMessage.info('查看健康档案详情')
}

const generateHealthReport = (profile) => {
  ElMessage.info('生成健康报告')
}

const exportProfiles = () => {
  ElMessage.success('健康档案导出成功')
}

const saveActivity = () => {
  ElMessage.success('活动保存成功')
  showAddActivityDialog.value = false
  loadActivities()
}

const viewActivity = (activity) => {
  ElMessage.info('查看活动详情')
}

const editActivity = (activity) => {
  activityForm.value = { ...activity }
  showAddActivityDialog.value = true
}

const deleteActivity = async (activity) => {
  try {
    await ElMessageBox.confirm('确定要删除该活动吗？', '提示', { type: 'warning' })
    ElMessage.success('活动删除成功')
    loadActivities()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const saveTip = () => {
  ElMessage.success('建议保存成功')
  showAddTipDialog.value = false
  loadHealthTips()
}

const viewTip = (tip) => {
  ElMessage.info('查看建议详情')
}

const editTip = (tip) => {
  tipForm.value = { ...tip }
  showAddTipDialog.value = true
}

const deleteTip = async (tip) => {
  try {
    await ElMessageBox.confirm('确定要删除该建议吗？', '提示', { type: 'warning' })
    ElMessage.success('建议删除成功')
    loadHealthTips()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const getHealthLevelClass = (score) => {
  if (score >= 90) return 'excellent'
  if (score >= 80) return 'good'
  if (score >= 70) return 'normal'
  return 'attention'
}

const getHealthLevelType = (level) => {
  const map = { 'excellent': 'success', 'good': 'primary', 'normal': 'warning', 'attention': 'danger' }
  return map[level] || 'info'
}

const getHealthLevelName = (level) => {
  const map = { 'excellent': '优秀', 'good': '良好', 'normal': '一般', 'attention': '需要关注' }
  return map[level] || level
}

const getActivityType = (type) => {
  const map = { 'exercise': 'success', 'lecture': 'primary', 'physical': 'warning', 'mental': 'info' }
  return map[type] || 'info'
}

const getActivityTypeName = (type) => {
  const map = { 'exercise': '运动健身', 'lecture': '健康讲座', 'physical': '体检活动', 'mental': '心理健康' }
  return map[type] || type
}

const getActivityStatusType = (status) => {
  const map = { 'upcoming': 'warning', 'ongoing': 'primary', 'completed': 'success' }
  return map[status] || 'info'
}

const getActivityStatusName = (status) => {
  const map = { 'upcoming': '即将开始', 'ongoing': '进行中', 'completed': '已完成' }
  return map[status] || status
}

const getCategoryName = (category) => {
  const map = { 'diet': '饮食健康', 'exercise': '运动健康', 'mental': '心理健康', 'habit': '生活习惯' }
  return map[category] || category
}

const getPieRotation = (level) => {
  const order = ['excellent', 'good', 'normal', 'attention']
  let rotation = 0
  for (const l of order) {
    if (l === level) break
    rotation += (healthStats.value[l] || 0) * 3.6
  }
  return rotation
}

const getBarHeight = (score) => {
  const max = Math.max(...healthTrend.value.map(t => t.score), 1)
  return (score / max) * 100
}

onMounted(() => {
  loadProfiles()
  loadActivities()
  loadHealthTips()
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
  flex-wrap: wrap;
  gap: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.activity-header, .tip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activity-header h4, .tip-header h4 {
  margin: 0;
  font-size: 16px;
}

.user-info {
  display: flex;
  align-items: center;
}

.health-score {
  font-weight: bold;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 14px;
}

.health-score.excellent {
  background: #f0f9eb;
  color: #67C23A;
}

.health-score.good {
  background: #ecf5ff;
  color: #409EFF;
}

.health-score.normal {
  background: #fdf6ec;
  color: #E6A23C;
}

.health-score.attention {
  background: #fef0f0;
  color: #F56C6C;
}

.health-distribution {
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
    #409EFF 90deg 234deg,
    #E6A23C 234deg 324deg,
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

.legend-dot.excellent { background: #67C23A; }
.legend-dot.good { background: #409EFF; }
.legend-dot.normal { background: #E6A23C; }
.legend-dot.attention { background: #F56C6C; }

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
  background: linear-gradient(180deg, #409EFF 0%, #79bbff 100%);
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