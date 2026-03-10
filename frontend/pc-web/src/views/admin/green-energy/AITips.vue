<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>AI生活建议管理</h1>
        <p>管理AI生成的生活建议、用户反馈和系统配置</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.totalTips || 0 }}</div>
          <div class="stat-label">建议总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.activeUsers || 0 }}</div>
          <div class="stat-label">活跃用户</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.avgRating || 0 }}分</div>
          <div class="stat-label">平均评分</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.todayGenerated || 0 }}</div>
          <div class="stat-label">今日生成</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="建议管理" name="tips">
          <div class="filter-bar">
            <el-select v-model="filterCategory" placeholder="建议分类" clearable style="width: 150px;" @change="loadTips">
              <el-option label="健康养生" value="health" />
              <el-option label="绿色生活" value="green" />
              <el-option label="节能减碳" value="energy" />
              <el-option label="智能家居" value="smart" />
            </el-select>
            <el-select v-model="filterStatus" placeholder="状态" clearable style="width: 120px; margin-left: 10px;" @change="loadTips">
              <el-option label="启用" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
            <el-input v-model="searchKeyword" placeholder="搜索建议内容" style="width: 200px; margin-left: 10px;" clearable />
            <el-button type="primary" style="margin-left: 10px;" @click="loadTips">查询</el-button>
            <el-button type="success" @click="generateNewTip">
              <el-icon><MagicStick /></el-icon> 生成建议
            </el-button>
          </div>

          <el-table :data="tips" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="title" label="标题" min-width="200" />
            <el-table-column prop="category" label="分类" width="120">
              <template #default="scope">
                <el-tag size="small">{{ getCategoryName(scope.row.category) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="usage_count" label="使用次数" width="100" />
            <el-table-column prop="rating" label="评分" width="100">
              <template #default="scope">
                <el-rate v-model="scope.row.rating" disabled show-score text-color="#ff9900" />
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.status" @change="toggleTipStatus(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="创建时间" width="160" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewTip(scope.row)">查看</el-button>
                <el-button size="small" type="warning" link @click="editTip(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteTip(scope.row)">删除</el-button>
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

        <el-tab-pane label="用户反馈" name="feedback">
          <el-table :data="feedback" style="width: 100%" v-loading="loadingFeedback">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="user_name" label="用户" width="120" />
            <el-table-column prop="tip_title" label="建议标题" min-width="200" show-overflow-tooltip />
            <el-table-column prop="rating" label="评分" width="100">
              <template #default="scope">
                <el-rate v-model="scope.row.rating" disabled />
              </template>
            </el-table-column>
            <el-table-column prop="feedback" label="反馈内容" min-width="200" show-overflow-tooltip />
            <el-table-column prop="create_time" label="反馈时间" width="160" />
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewFeedback(scope.row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="系统配置" name="config">
          <el-form :model="config" label-width="150px" class="config-form">
            <el-form-item label="API密钥">
              <el-input v-model="config.apiKey" placeholder="输入AI API密钥" />
            </el-form-item>
            <el-form-item label="生成频率限制">
              <el-input-number v-model="config.frequencyLimit" :min="1" :max="100" />
              <span style="margin-left: 10px;">次/天/用户</span>
            </el-form-item>
            <el-form-item label="建议长度">
              <el-select v-model="config.tipLength" style="width: 200px;">
                <el-option label="简短 (100字)" value="short" />
                <el-option label="中等 (200字)" value="medium" />
                <el-option label="详细 (500字)" value="long" />
              </el-select>
            </el-form-item>
            <el-form-item label="建议分类">
              <el-checkbox-group v-model="config.categories">
                <el-checkbox label="health">健康养生</el-checkbox>
                <el-checkbox label="green">绿色生活</el-checkbox>
                <el-checkbox label="energy">节能减碳</el-checkbox>
                <el-checkbox label="smart">智能家居</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="启用AI学习">
              <el-switch v-model="config.aiLearning" />
            </el-form-item>
            <el-form-item label="学习频率">
              <el-select v-model="config.learningFrequency" style="width: 200px;">
                <el-option label="每日" value="daily" />
                <el-option label="每周" value="weekly" />
                <el-option label="每月" value="monthly" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveConfig">保存配置</el-button>
              <el-button type="warning" @click="testAI">测试AI</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="使用统计" name="statistics">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>分类使用统计</span>
                </template>
                <div class="category-stats">
                  <div v-for="stat in categoryStats" :key="stat.category" class="stat-item">
                    <div class="stat-info">
                      <span class="stat-name">{{ getCategoryName(stat.category) }}</span>
                      <span class="stat-value">{{ stat.count }}次</span>
                    </div>
                    <el-progress :percentage="stat.percentage" :stroke-width="10" />
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>生成趋势</span>
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
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showTipDialog" title="建议详情" width="600px">
      <div v-if="currentTip" class="tip-detail">
        <h3>{{ currentTip.title }}</h3>
        <div class="tip-meta">
          <span>分类: {{ getCategoryName(currentTip.category) }}</span>
          <span>使用: {{ currentTip.usage_count }}次</span>
          <span>评分: {{ currentTip.rating }}分</span>
        </div>
        <div class="tip-content">
          {{ currentTip.content }}
        </div>
      </div>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { MagicStick } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('tips')
const loading = ref(false)
const loadingFeedback = ref(false)
const filterCategory = ref('')
const filterStatus = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showTipDialog = ref(false)
const currentTip = ref(null)

const stats = ref({
  totalTips: 156,
  activeUsers: 890,
  avgRating: 4.5,
  todayGenerated: 12
})

const tips = ref([])
const feedback = ref([])
const config = ref({
  apiKey: 'sk-xxxxxxxxxxxxxxxx',
  frequencyLimit: 10,
  tipLength: 'medium',
  categories: ['health', 'green', 'energy', 'smart'],
  aiLearning: true,
  learningFrequency: 'weekly'
})

const categoryStats = ref([])
const trendData = ref([])

const loadTips = () => {
  tips.value = [
    { id: 1, title: '每日健康饮水建议', category: 'health', usage_count: 1256, rating: 4.8, status: true, create_time: '2024-01-15 10:30:00', content: '建议每天饮用8杯水，约2000ml，有助于维持身体水分平衡，促进新陈代谢。' },
    { id: 2, title: '家庭节能小技巧', category: 'energy', usage_count: 890, rating: 4.5, status: true, create_time: '2024-01-14 15:20:00', content: '关闭不必要的电器，使用节能灯泡，合理设置空调温度，可以有效减少家庭能耗。' },
    { id: 3, title: '绿色出行建议', category: 'green', usage_count: 654, rating: 4.2, status: false, create_time: '2024-01-13 09:10:00', content: '优先选择公共交通、骑行或步行，减少私家车使用，降低碳排放量。' }
  ]
  total.value = 3
}

const loadFeedback = () => {
  feedback.value = [
    { id: 1, user_name: '张三', tip_title: '每日健康饮水建议', rating: 5, feedback: '非常实用的建议，已经开始每天按时饮水了', create_time: '2024-01-15 11:00:00' },
    { id: 2, user_name: '李四', tip_title: '家庭节能小技巧', rating: 4, feedback: '建议很详细，学到了很多节能知识', create_time: '2024-01-14 16:00:00' }
  ]
}

const loadStatistics = () => {
  categoryStats.value = [
    { category: 'health', count: 65, percentage: 42 },
    { category: 'green', count: 45, percentage: 29 },
    { category: 'energy', count: 30, percentage: 19 },
    { category: 'smart', count: 16, percentage: 10 }
  ]
  trendData.value = [
    { date: '01-01', count: 8 },
    { date: '01-02', count: 10 },
    { date: '01-03', count: 12 },
    { date: '01-04', count: 9 },
    { date: '01-05', count: 11 },
    { date: '01-06', count: 12 }
  ]
}

const generateNewTip = () => {
  ElMessage.info('AI正在生成新建议...')
  setTimeout(() => {
    ElMessage.success('新建议生成成功')
    loadTips()
  }, 2000)
}

const viewTip = (tip) => {
  currentTip.value = tip
  showTipDialog.value = true
}

const editTip = (tip) => {
  ElMessage.info('编辑建议功能开发中')
}

const deleteTip = async (tip) => {
  try {
    await ElMessageBox.confirm('确定要删除该建议吗？', '提示', { type: 'warning' })
    ElMessage.success('建议已删除')
    loadTips()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const toggleTipStatus = (tip) => {
  ElMessage.success(`建议已${tip.status ? '启用' : '禁用'}`)
}

const viewFeedback = (item) => {
  ElMessage.info('查看反馈详情')
}

const saveConfig = () => {
  ElMessage.success('配置保存成功')
}

const testAI = () => {
  ElMessage.info('AI测试中...')
  setTimeout(() => {
    ElMessage.success('AI测试成功')
  }, 1000)
}

const getCategoryName = (category) => {
  const map = { 'health': '健康养生', 'green': '绿色生活', 'energy': '节能减碳', 'smart': '智能家居' }
  return map[category] || category
}

const getBarHeight = (count) => {
  const max = Math.max(...trendData.value.map(t => t.count), 1)
  return (count / max) * 100
}

onMounted(() => {
  loadTips()
  loadFeedback()
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

.config-form {
  max-width: 600px;
}

.category-stats {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-info {
  display: flex;
  justify-content: space-between;
}

.stat-name {
  font-size: 14px;
  color: #606266;
}

.stat-value {
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

.tip-detail h3 {
  margin: 0 0 15px 0;
}

.tip-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 13px;
  margin-bottom: 15px;
}

.tip-content {
  line-height: 1.8;
  color: #606266;
}
</style>
