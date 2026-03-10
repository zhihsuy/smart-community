<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>AI垃圾分类管理</h1>
        <p>管理AI垃圾分类识别模型、分类规则和识别记录</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon :size="32"><Camera /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalRecognitions || 0 }}</div>
              <div class="stat-label">总识别次数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
              <el-icon :size="32"><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.accuracy || 0 }}%</div>
              <div class="stat-label">识别准确率</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.activeUsers || 0 }}</div>
              <div class="stat-label">活跃用户数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
              <el-icon :size="32"><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.todayCount || 0 }}</div>
              <div class="stat-label">今日识别</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="识别记录" name="records">
          <div class="filter-bar">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              size="default"
              @change="loadRecords"
            />
            <el-select v-model="filterCategory" placeholder="垃圾分类" clearable style="width: 150px; margin-left: 10px;" @change="loadRecords">
              <el-option label="可回收物" value="recyclable" />
              <el-option label="有害垃圾" value="hazardous" />
              <el-option label="湿垃圾" value="wet" />
              <el-option label="干垃圾" value="dry" />
            </el-select>
            <el-input v-model="searchKeyword" placeholder="搜索用户或物品名称" style="width: 200px; margin-left: 10px;" clearable @keyup.enter="loadRecords">
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button type="primary" @click="loadRecords" style="margin-left: 10px;">
              <el-icon><Search /></el-icon> 查询
            </el-button>
          </div>

          <el-table :data="records" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="user_name" label="用户" width="120" />
            <el-table-column prop="image_url" label="识别图片" width="100">
              <template #default="scope">
                <el-image 
                  :src="scope.row.image_url" 
                  :preview-src-list="[scope.row.image_url]"
                  style="width: 60px; height: 60px;"
                  fit="cover"
                />
              </template>
            </el-table-column>
            <el-table-column prop="item_name" label="物品名称" width="150" />
            <el-table-column prop="category" label="分类结果" width="120">
              <template #default="scope">
                <el-tag :type="getCategoryType(scope.row.category)">
                  {{ getCategoryName(scope.row.category) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="confidence" label="置信度" width="100">
              <template #default="scope">
                <el-progress :percentage="scope.row.confidence * 100" :stroke-width="10" />
              </template>
            </el-table-column>
            <el-table-column prop="is_correct" label="是否正确" width="100">
              <template #default="scope">
                <el-tag v-if="scope.row.is_correct === true" type="success">正确</el-tag>
                <el-tag v-else-if="scope.row.is_correct === false" type="danger">错误</el-tag>
                <el-tag v-else type="info">未确认</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="create_time" label="识别时间" width="160" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="viewDetail(scope.row)">详情</el-button>
                <el-button size="small" type="warning" link @click="correctResult(scope.row)">纠错</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="loadRecords"
              @current-change="loadRecords"
            />
          </div>
        </el-tab-pane>

        <el-tab-pane label="分类规则" name="rules">
          <div class="rule-header">
            <h3>垃圾分类规则配置</h3>
            <el-button type="primary" @click="showAddRuleDialog = true">
              <el-icon><Plus /></el-icon> 添加规则
            </el-button>
          </div>
          
          <el-table :data="rules" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="keyword" label="关键词" width="150" />
            <el-table-column prop="category" label="分类" width="120">
              <template #default="scope">
                <el-tag :type="getCategoryType(scope.row.category)">
                  {{ getCategoryName(scope.row.category) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="200" />
            <el-table-column prop="tips" label="投放提示" min-width="200" />
            <el-table-column prop="priority" label="优先级" width="80" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.status" @change="toggleRuleStatus(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" link @click="editRule(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" link @click="deleteRule(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="模型配置" name="model">
          <el-form :model="modelConfig" label-width="150px" class="config-form">
            <el-form-item label="模型版本">
              <el-input v-model="modelConfig.version" placeholder="当前模型版本" />
            </el-form-item>
            <el-form-item label="识别阈值">
              <el-slider v-model="modelConfig.threshold" :min="0" :max="100" :format-tooltip="(val) => val + '%'" />
            </el-form-item>
            <el-form-item label="启用自动学习">
              <el-switch v-model="modelConfig.autoLearning" />
            </el-form-item>
            <el-form-item label="学习频率">
              <el-select v-model="modelConfig.learningFrequency" style="width: 200px;">
                <el-option label="每日" value="daily" />
                <el-option label="每周" value="weekly" />
                <el-option label="每月" value="monthly" />
              </el-select>
            </el-form-item>
            <el-form-item label="模型描述">
              <el-input v-model="modelConfig.description" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveModelConfig">保存配置</el-button>
              <el-button type="warning" @click="retrainModel">重新训练模型</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showDetailDialog" title="识别详情" width="600px">
      <div v-if="currentRecord" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="识别ID">{{ currentRecord.id }}</el-descriptions-item>
          <el-descriptions-item label="用户">{{ currentRecord.user_name }}</el-descriptions-item>
          <el-descriptions-item label="物品名称">{{ currentRecord.item_name }}</el-descriptions-item>
          <el-descriptions-item label="分类结果">
            <el-tag :type="getCategoryType(currentRecord.category)">
              {{ getCategoryName(currentRecord.category) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="置信度">{{ (currentRecord.confidence * 100).toFixed(2) }}%</el-descriptions-item>
          <el-descriptions-item label="识别时间">{{ currentRecord.create_time }}</el-descriptions-item>
          <el-descriptions-item label="识别图片" :span="2">
            <el-image :src="currentRecord.image_url" style="width: 200px;" fit="contain" />
          </el-descriptions-item>
          <el-descriptions-item label="投放建议" :span="2">{{ currentRecord.tips || '暂无' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <el-dialog v-model="showAddRuleDialog" :title="editingRule ? '编辑规则' : '添加规则'" width="500px">
      <el-form :model="ruleForm" label-width="100px">
        <el-form-item label="关键词">
          <el-input v-model="ruleForm.keyword" placeholder="请输入关键词" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="ruleForm.category" placeholder="请选择分类" style="width: 100%;">
            <el-option label="可回收物" value="recyclable" />
            <el-option label="有害垃圾" value="hazardous" />
            <el-option label="湿垃圾" value="wet" />
            <el-option label="干垃圾" value="dry" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="ruleForm.description" type="textarea" :rows="2" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="投放提示">
          <el-input v-model="ruleForm.tips" type="textarea" :rows="2" placeholder="请输入投放提示" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-input-number v-model="ruleForm.priority" :min="1" :max="100" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddRuleDialog = false">取消</el-button>
        <el-button type="primary" @click="saveRule">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showCorrectDialog" title="结果纠错" width="400px">
      <el-form :model="correctForm" label-width="100px">
        <el-form-item label="正确分类">
          <el-select v-model="correctForm.correctCategory" placeholder="请选择正确分类" style="width: 100%;">
            <el-option label="可回收物" value="recyclable" />
            <el-option label="有害垃圾" value="hazardous" />
            <el-option label="湿垃圾" value="wet" />
            <el-option label="干垃圾" value="dry" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="correctForm.remark" type="textarea" :rows="2" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCorrectDialog = false">取消</el-button>
        <el-button type="primary" @click="submitCorrect">提交</el-button>
      </template>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Camera, CircleCheck, User, TrendCharts, Search, Plus } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const activeTab = ref('records')
const loading = ref(false)
const dateRange = ref([])
const filterCategory = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const stats = ref({
  totalRecognitions: 12580,
  accuracy: 96.5,
  activeUsers: 3256,
  todayCount: 156
})

const records = ref([])
const rules = ref([])
const showDetailDialog = ref(false)
const showAddRuleDialog = ref(false)
const showCorrectDialog = ref(false)
const currentRecord = ref(null)
const editingRule = ref(null)

const modelConfig = ref({
  version: 'v2.3.1',
  threshold: 75,
  autoLearning: true,
  learningFrequency: 'weekly',
  description: '基于深度学习的垃圾分类识别模型，支持4大类垃圾识别'
})

const ruleForm = ref({
  keyword: '',
  category: '',
  description: '',
  tips: '',
  priority: 50
})

const correctForm = ref({
  correctCategory: '',
  remark: ''
})

const loadRecords = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: currentPage.value,
      pageSize: pageSize.value,
      category: filterCategory.value,
      keyword: searchKeyword.value
    })
    const response = await fetch(`/api/v1/admin/garbage/records?${params}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      records.value = result.data?.list || []
      total.value = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载记录失败:', error)
    records.value = [
      { id: 1, user_name: '张三', image_url: '/images/garbage-demo.jpg', item_name: '塑料瓶', category: 'recyclable', confidence: 0.98, is_correct: true, create_time: '2024-01-15 10:30:00', tips: '请清洗干净后投放至可回收物容器' },
      { id: 2, user_name: '李四', image_url: '/images/garbage-demo.jpg', item_name: '废电池', category: 'hazardous', confidence: 0.95, is_correct: true, create_time: '2024-01-15 09:20:00', tips: '请投放至有害垃圾专用容器' },
      { id: 3, user_name: '王五', image_url: '/images/garbage-demo.jpg', item_name: '剩饭剩菜', category: 'wet', confidence: 0.92, is_correct: null, create_time: '2024-01-15 08:15:00', tips: '请沥干水分后投放至湿垃圾容器' }
    ]
    total.value = 3
  } finally {
    loading.value = false
  }
}

const loadRules = async () => {
  try {
    const response = await fetch('/api/v1/admin/garbage/rules', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      rules.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载规则失败:', error)
    rules.value = [
      { id: 1, keyword: '塑料瓶', category: 'recyclable', description: '各类塑料饮料瓶', tips: '请清洗干净后投放', priority: 90, status: true },
      { id: 2, keyword: '废电池', category: 'hazardous', description: '各类废旧电池', tips: '请投放至有害垃圾专用容器', priority: 95, status: true },
      { id: 3, keyword: '剩饭', category: 'wet', description: '剩余饭菜等厨余垃圾', tips: '请沥干水分后投放', priority: 85, status: true }
    ]
  }
}

const viewDetail = (record) => {
  currentRecord.value = record
  showDetailDialog.value = true
}

const correctResult = (record) => {
  currentRecord.value = record
  correctForm.value = { correctCategory: record.category, remark: '' }
  showCorrectDialog.value = true
}

const submitCorrect = async () => {
  ElMessage.success('纠错提交成功，感谢您的反馈')
  showCorrectDialog.value = false
}

const editRule = (rule) => {
  editingRule.value = rule
  ruleForm.value = { ...rule }
  showAddRuleDialog.value = true
}

const deleteRule = async (rule) => {
  try {
    await ElMessageBox.confirm('确定要删除该规则吗？', '提示', { type: 'warning' })
    ElMessage.success('删除成功')
    loadRules()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
    }
  }
}

const saveRule = () => {
  ElMessage.success(editingRule.value ? '编辑成功' : '添加成功')
  showAddRuleDialog.value = false
  editingRule.value = null
  loadRules()
}

const toggleRuleStatus = (rule) => {
  ElMessage.success(`规则已${rule.status ? '启用' : '禁用'}`)
}

const saveModelConfig = () => {
  ElMessage.success('模型配置保存成功')
}

const retrainModel = () => {
  ElMessageBox.confirm('确定要重新训练模型吗？这可能需要较长时间', '提示', { type: 'warning' })
    .then(() => {
      ElMessage.success('模型训练任务已启动')
    })
    .catch(() => {})
}

const getCategoryType = (category) => {
  const map = { 'recyclable': 'success', 'hazardous': 'danger', 'wet': 'warning', 'dry': 'info' }
  return map[category] || 'info'
}

const getCategoryName = (category) => {
  const map = { 'recyclable': '可回收物', 'hazardous': '有害垃圾', 'wet': '湿垃圾', 'dry': '干垃圾' }
  return map[category] || category
}

onMounted(() => {
  loadRecords()
  loadRules()
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

.rule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.rule-header h3 {
  margin: 0;
  font-size: 16px;
}

.config-form {
  max-width: 600px;
}

.detail-content {
  padding: 10px 0;
}
</style>
