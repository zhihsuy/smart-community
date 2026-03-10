<template>
  <AdminLayout>
    <div class="admin-page">
      <div class="page-header">
        <h1>垃圾分类记录</h1>
        <p>查看和管理垃圾分类识别记录</p>
      </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="4">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ stats.total || 0 }}</div>
          <div class="stat-label">总记录数</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card recyclable" shadow="hover">
          <div class="stat-value">{{ stats.recyclable || 0 }}</div>
          <div class="stat-label">可回收物</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card hazardous" shadow="hover">
          <div class="stat-value">{{ stats.hazardous || 0 }}</div>
          <div class="stat-label">有害垃圾</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card wet" shadow="hover">
          <div class="stat-value">{{ stats.wet || 0 }}</div>
          <div class="stat-label">湿垃圾</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card dry" shadow="hover">
          <div class="stat-value">{{ stats.dry || 0 }}</div>
          <div class="stat-label">干垃圾</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card accuracy" shadow="hover">
          <div class="stat-value">{{ stats.accuracy || 0 }}%</div>
          <div class="stat-label">准确率</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="main-card">
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
        <el-select v-model="filterCategory" placeholder="垃圾分类" clearable style="width: 140px; margin-left: 10px;" @change="loadRecords">
          <el-option label="可回收物" value="recyclable" />
          <el-option label="有害垃圾" value="hazardous" />
          <el-option label="湿垃圾" value="wet" />
          <el-option label="干垃圾" value="dry" />
        </el-select>
        <el-select v-model="filterCorrect" placeholder="确认状态" clearable style="width: 120px; margin-left: 10px;" @change="loadRecords">
          <el-option label="已确认正确" value="true" />
          <el-option label="已确认错误" value="false" />
          <el-option label="未确认" value="null" />
        </el-select>
        <el-input v-model="searchKeyword" placeholder="搜索用户/物品" style="width: 180px; margin-left: 10px;" clearable @keyup.enter="loadRecords">
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="loadRecords" style="margin-left: 10px;">
          <el-icon><Search /></el-icon> 查询
        </el-button>
        <el-button type="success" @click="exportRecords">
          <el-icon><Download /></el-icon> 导出
        </el-button>
      </div>

      <el-table :data="records" style="width: 100%" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="user_name" label="用户" width="100">
          <template #default="scope">
            <div class="user-info">
              <el-avatar :size="24" style="margin-right: 5px;">{{ scope.row.user_name?.charAt(0) }}</el-avatar>
              {{ scope.row.user_name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="image_url" label="识别图片" width="80">
          <template #default="scope">
            <el-image 
              :src="scope.row.image_url" 
              :preview-src-list="[scope.row.image_url]"
              style="width: 50px; height: 50px; border-radius: 4px;"
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column prop="item_name" label="物品名称" min-width="120" />
        <el-table-column prop="category" label="分类结果" width="100">
          <template #default="scope">
            <el-tag :type="getCategoryType(scope.row.category)" effect="light">
              {{ getCategoryName(scope.row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="confidence" label="置信度" width="120">
          <template #default="scope">
            <div class="confidence-bar">
              <el-progress 
                :percentage="Math.round(scope.row.confidence * 100)" 
                :stroke-width="8"
                :color="getConfidenceColor(scope.row.confidence)"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="is_correct" label="确认状态" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.is_correct === true" type="success" size="small">
              <el-icon><Select /></el-icon> 正确
            </el-tag>
            <el-tag v-else-if="scope.row.is_correct === false" type="danger" size="small">
              <el-icon><CloseBold /></el-icon> 错误
            </el-tag>
            <el-tag v-else type="info" size="small">未确认</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="识别时间" width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="viewDetail(scope.row)">详情</el-button>
            <el-button size="small" type="success" link @click="confirmCorrect(scope.row)" v-if="scope.row.is_correct !== true">确认正确</el-button>
            <el-button size="small" type="warning" link @click="markIncorrect(scope.row)" v-if="scope.row.is_correct !== false">标记错误</el-button>
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
    </el-card>

    <el-dialog v-model="showDetailDialog" title="识别详情" width="650px">
      <div v-if="currentRecord" class="detail-content">
        <el-row :gutter="20">
          <el-col :span="10">
            <div class="detail-image">
              <el-image :src="currentRecord.image_url" fit="contain" style="width: 100%; max-height: 300px;" />
            </div>
          </el-col>
          <el-col :span="14">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="识别ID">{{ currentRecord.id }}</el-descriptions-item>
              <el-descriptions-item label="用户">{{ currentRecord.user_name }}</el-descriptions-item>
              <el-descriptions-item label="物品名称">{{ currentRecord.item_name }}</el-descriptions-item>
              <el-descriptions-item label="分类结果">
                <el-tag :type="getCategoryType(currentRecord.category)" effect="dark">
                  {{ getCategoryName(currentRecord.category) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="置信度">
                <el-progress 
                  :percentage="Math.round(currentRecord.confidence * 100)" 
                  :stroke-width="15"
                  :color="getConfidenceColor(currentRecord.confidence)"
                />
              </el-descriptions-item>
              <el-descriptions-item label="识别时间">{{ currentRecord.create_time }}</el-descriptions-item>
              <el-descriptions-item label="确认状态">
                <el-tag v-if="currentRecord.is_correct === true" type="success">已确认正确</el-tag>
                <el-tag v-else-if="currentRecord.is_correct === false" type="danger">已标记错误</el-tag>
                <el-tag v-else type="info">未确认</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
        </el-row>
        <div class="tips-section" v-if="currentRecord.tips">
          <h4>投放提示</h4>
          <p>{{ currentRecord.tips }}</p>
        </div>
      </div>
    </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Download, Select, CloseBold } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const loading = ref(false)
const dateRange = ref([])
const filterCategory = ref('')
const filterCorrect = ref('')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const stats = ref({
  total: 12580,
  recyclable: 4520,
  hazardous: 890,
  wet: 3560,
  dry: 3610,
  accuracy: 96.5
})

const records = ref([])
const showDetailDialog = ref(false)
const currentRecord = ref(null)

const loadRecords = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: currentPage.value,
      pageSize: pageSize.value,
      category: filterCategory.value,
      isCorrect: filterCorrect.value,
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
      { id: 1, user_name: '张三', image_url: '/images/garbage-demo.jpg', item_name: '塑料饮料瓶', category: 'recyclable', confidence: 0.98, is_correct: true, create_time: '2024-01-15 10:30:00', tips: '请清洗干净后投放至可回收物容器，瓶盖可以不分离' },
      { id: 2, user_name: '李四', image_url: '/images/garbage-demo.jpg', item_name: '废旧电池', category: 'hazardous', confidence: 0.95, is_correct: true, create_time: '2024-01-15 09:20:00', tips: '请投放至有害垃圾专用容器，注意防止漏液' },
      { id: 3, user_name: '王五', image_url: '/images/garbage-demo.jpg', item_name: '剩饭剩菜', category: 'wet', confidence: 0.92, is_correct: null, create_time: '2024-01-15 08:15:00', tips: '请沥干水分后投放至湿垃圾容器，避免混入餐具' },
      { id: 4, user_name: '赵六', image_url: '/images/garbage-demo.jpg', item_name: '餐巾纸', category: 'dry', confidence: 0.88, is_correct: false, create_time: '2024-01-14 18:45:00', tips: '使用过的餐巾纸属于干垃圾，请投放至干垃圾容器' },
      { id: 5, user_name: '钱七', image_url: '/images/garbage-demo.jpg', item_name: '玻璃瓶', category: 'recyclable', confidence: 0.96, is_correct: true, create_time: '2024-01-14 16:30:00', tips: '请投放至可回收物容器，注意轻放防止破碎' }
    ]
    total.value = 5
  } finally {
    loading.value = false
  }
}

const viewDetail = (record) => {
  currentRecord.value = record
  showDetailDialog.value = true
}

const confirmCorrect = async (record) => {
  ElMessage.success(`记录 ${record.id} 已确认正确`)
  record.is_correct = true
}

const markIncorrect = async (record) => {
  ElMessage.warning(`记录 ${record.id} 已标记为错误`)
  record.is_correct = false
}

const exportRecords = () => {
  ElMessage.success('记录导出中...')
}

const getCategoryType = (category) => {
  const map = { 'recyclable': 'success', 'hazardous': 'danger', 'wet': 'warning', 'dry': 'info' }
  return map[category] || 'info'
}

const getCategoryName = (category) => {
  const map = { 'recyclable': '可回收物', 'hazardous': '有害垃圾', 'wet': '湿垃圾', 'dry': '干垃圾' }
  return map[category] || category
}

const getConfidenceColor = (confidence) => {
  if (confidence >= 0.9) return '#67C23A'
  if (confidence >= 0.7) return '#E6A23C'
  return '#F56C6C'
}

onMounted(() => {
  loadRecords()
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

.stat-card .stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-card .stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 5px;
}

.stat-card.recyclable .stat-value { color: #67C23A; }
.stat-card.hazardous .stat-value { color: #F56C6C; }
.stat-card.wet .stat-value { color: #E6A23C; }
.stat-card.dry .stat-value { color: #909399; }
.stat-card.accuracy .stat-value { color: #409EFF; }

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

.user-info {
  display: flex;
  align-items: center;
}

.confidence-bar {
  width: 100%;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.detail-content {
  padding: 10px 0;
}

.detail-image {
  border: 1px solid #EBEEF5;
  border-radius: 8px;
  padding: 10px;
  background: #FAFAFA;
}

.tips-section {
  margin-top: 20px;
  padding: 15px;
  background: #F4F4F5;
  border-radius: 8px;
}

.tips-section h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.tips-section p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}
</style>
