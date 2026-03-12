<template>
  <div class="my-complaints-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📋 我的投诉</h1>
      <p class="subtitle">查看和管理我的所有投诉建议</p>
    </div>

    <!-- 搜索筛选 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="类型">
          <el-select v-model="searchForm.type" placeholder="选择类型">
            <el-option label="全部" value="" />
            <el-option label="投诉" value="complaint" />
            <el-option label="建议" value="suggestion" />
            <el-option label="咨询" value="consultation" />
            <el-option label="表扬" value="praise" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="选择状态">
            <el-option label="全部" value="" />
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="processing" />
            <el-option label="已完成" value="completed" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.keyword"
            placeholder="标题或内容"
            clearable
            style="width: 300px"
          >
            <template #append>
              <el-button @click="loadComplaints">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 投诉列表 -->
    <el-card class="complaints-card">
      <template #header>
        <div class="card-header">
          <span>投诉列表</span>
          <span class="total-count">共 {{ pagination.total }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="complaints" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="complaint_type" label="类型" width="120">
          <template #default="scope">
            <el-tag size="small" :type="getComplaintTypeColor(scope.row.complaint_type)">
              {{ getComplaintTypeText(scope.row.complaint_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag size="small" :type="getStatusColor(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="180" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewComplaint(scope.row)">
              查看
            </el-button>
            <el-button 
              v-if="scope.row.status === 'completed'" 
              size="small" 
              type="success" 
              @click="evaluateComplaint(scope.row)"
            >
              评价
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination" style="margin-top: 20px">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 投诉详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="投诉详情"
      width="600px"
    >
      <div v-if="currentComplaint" class="complaint-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="标题">{{ currentComplaint.title }}</el-descriptions-item>
          <el-descriptions-item label="类型">{{ getComplaintTypeText(currentComplaint.complaint_type) }}</el-descriptions-item>
          <el-descriptions-item label="内容">{{ currentComplaint.content }}</el-descriptions-item>
          <el-descriptions-item label="联系方式">{{ currentComplaint.contact_info }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusText(currentComplaint.status) }}</el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ currentComplaint.created_at }}</el-descriptions-item>
          <el-descriptions-item label="处理时间">{{ currentComplaint.updated_at }}</el-descriptions-item>
        </el-descriptions>

        <!-- 处理记录 -->
        <div class="process-records" style="margin-top: 20px">
          <h3>处理记录</h3>
          <el-timeline>
            <el-timeline-item
              v-for="(record, index) in currentComplaint.process_records || []"
              :key="index"
              :timestamp="record.created_at"
            >
              <el-card>
                <h4>{{ record.operator_name || '系统' }}</h4>
                <p>{{ record.content }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-dialog>

    <!-- 评价对话框 -->
    <el-dialog
      v-model="evaluationDialogVisible"
      title="满意度评价"
      width="500px"
    >
      <div v-if="currentComplaint" class="evaluation-form">
        <el-form :model="evaluationForm" label-width="80px">
          <el-form-item label="服务评分">
            <el-rate v-model="evaluationForm.rating" :max="5" show-score />
          </el-form-item>
          <el-form-item label="评价内容">
            <el-input 
              v-model="evaluationForm.content" 
              type="textarea" 
              :rows="4"
              placeholder="请输入您的评价..."
            />
          </el-form-item>
          <el-form-item label="是否满意">
            <el-switch v-model="evaluationForm.satisfied" />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="evaluationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEvaluation" :loading="submittingEvaluation">
            提交评价
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Search } from '@element-plus/icons-vue'

const complaints = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})
const searchForm = ref({
  type: '',
  status: '',
  keyword: ''
})
const detailDialogVisible = ref(false)
const evaluationDialogVisible = ref(false)
const currentComplaint = ref(null)
const submittingEvaluation = ref(false)
const evaluationForm = ref({
  rating: 5,
  content: '',
  satisfied: true
})

// 加载投诉列表
const loadComplaints = async () => {
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.currentPage)
    params.append('pageSize', pagination.value.pageSize)
    
    if (searchForm.value.type) {
      params.append('type', searchForm.value.type)
    }
    if (searchForm.value.status) {
      params.append('status', searchForm.value.status)
    }
    if (searchForm.value.keyword) {
      params.append('keyword', searchForm.value.keyword)
    }

    const response = await fetch(`/api/v1/pc/complaint/complaints?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      complaints.value = result.data?.list || []
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载投诉失败:', error)
    ElMessage.error('加载投诉失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadComplaints()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadComplaints()
}

const viewComplaint = (complaint) => {
  currentComplaint.value = complaint
  detailDialogVisible.value = true
}

const evaluateComplaint = (complaint) => {
  currentComplaint.value = complaint
  evaluationForm.value = {
    rating: 5,
    content: '',
    satisfied: true
  }
  evaluationDialogVisible.value = true
}

const submitEvaluation = async () => {
  if (!currentComplaint.value) return
  
  submittingEvaluation.value = true
  try {
    const response = await fetch(`/api/v1/pc/complaint/complaints/${currentComplaint.value.id}/evaluation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(evaluationForm.value)
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('评价提交成功')
      evaluationDialogVisible.value = false
      loadComplaints()
    } else {
      ElMessage.error(result.msg || '评价失败')
    }
  } catch (error) {
    console.error('提交评价失败:', error)
    ElMessage.error('评价失败')
  } finally {
    submittingEvaluation.value = false
  }
}

const getComplaintTypeText = (type) => {
  const map = {
    'complaint': '投诉',
    'suggestion': '建议',
    'consultation': '咨询',
    'praise': '表扬'
  }
  return map[type] || type
}

const getComplaintTypeColor = (type) => {
  const map = {
    'complaint': 'danger',
    'suggestion': 'info',
    'consultation': 'primary',
    'praise': 'success'
  }
  return map[type] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'closed': '已关闭'
  }
  return map[status] || status
}

const getStatusColor = (status) => {
  const map = {
    'pending': 'info',
    'processing': 'warning',
    'completed': 'success',
    'closed': 'danger'
  }
  return map[status] || 'info'
}

onMounted(() => {
  loadComplaints()
})
</script>

<style scoped>
.my-complaints-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.page-header h1 {
  margin: 10px 0 5px 0;
  font-size: 28px;
  color: #303133;
}

.subtitle {
  color: #909399;
  margin: 0;
}

.search-card,
.complaints-card {
  border-radius: 8px;
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.total-count {
  color: #409EFF;
  font-weight: normal;
}

.complaint-detail {
  padding: 20px 0;
}

.process-records {
  margin-top: 20px;
}

.process-records h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #303133;
}

.evaluation-form {
  padding: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
