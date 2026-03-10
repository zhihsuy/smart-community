<template>
  <AdminLayout>
    <div class="complaints">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>投诉管理</h3>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="标题">
              <el-input v-model="searchForm.title" placeholder="请输入投诉标题" />
            </el-form-item>
            <el-form-item label="类型">
              <el-select v-model="searchForm.type" placeholder="选择投诉类型">
                <el-option label="服务" value="service" />
                <el-option label="设施" value="facility" />
                <el-option label="环境" value="environment" />
                <el-option label="安全" value="security" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="待处理" value="pending" />
                <el-option label="处理中" value="processing" />
                <el-option label="已解决" value="resolved" />
                <el-option label="已拒绝" value="rejected" />
              </el-select>
            </el-form-item>
            <el-form-item label="优先级">
              <el-select v-model="searchForm.priority" placeholder="选择优先级">
                <el-option label="低" value="low" />
                <el-option label="中" value="medium" />
                <el-option label="高" value="high" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchComplaints">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="complaints" style="width: 100%">
          <el-table-column prop="id" label="投诉ID" width="80" />
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="type" label="类型" width="100">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ getTypeText(scope.row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="priority" label="优先级" width="100">
            <template #default="scope">
              <el-tag :type="getPriorityTag(scope.row.priority)">
                {{ getPriorityText(scope.row.priority) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="handler_name" label="处理人" width="120" />
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewComplaint(scope.row)">
                <el-icon><i-ep-view /></el-icon>
                查看
              </el-button>
              <el-button size="small" type="primary" @click="openHandleDialog(scope.row)" v-if="scope.row.status === 'pending'">
                <el-icon><i-ep-edit /></el-icon>
                处理
              </el-button>
              <el-button size="small" type="danger" @click="deleteComplaint(scope.row.id)">
                <el-icon><i-ep-delete /></el-icon>
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination" v-if="total > 0">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-card>
      
      <!-- 查看投诉对话框 -->
      <el-dialog
        v-model="viewDialogVisible"
        title="投诉详情"
        width="700px"
      >
        <div v-if="currentComplaint" class="complaint-detail">
          <h3 class="complaint-title">{{ currentComplaint.title }}</h3>
          <div class="complaint-meta">
            <span class="meta-item">
              <el-tag :type="getTypeTag(currentComplaint.type)">{{ getTypeText(currentComplaint.type) }}</el-tag>
            </span>
            <span class="meta-item">
              <el-tag :type="getPriorityTag(currentComplaint.priority)">{{ getPriorityText(currentComplaint.priority) }}</el-tag>
            </span>
            <span class="meta-item">
              <el-tag :type="getStatusTag(currentComplaint.status)">{{ getStatusText(currentComplaint.status) }}</el-tag>
            </span>
            <span class="meta-item">创建时间：{{ currentComplaint.created_at }}</span>
          </div>
          <div class="complaint-content">
            <p>{{ currentComplaint.content }}</p>
          </div>
          <div v-if="currentComplaint.handle_result" class="complaint-result">
            <h4>处理结果</h4>
            <p>{{ currentComplaint.handle_result }}</p>
            <p>处理人：{{ currentComplaint.handler_name }}</p>
            <p v-if="currentComplaint.handle_time">处理时间：{{ currentComplaint.handle_time }}</p>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="viewDialogVisible = false">关闭</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 处理投诉对话框 -->
      <el-dialog
        v-model="handleDialogVisible"
        title="处理投诉"
        width="600px"
      >
        <el-form :model="handleForm" :rules="handleRules" ref="handleFormRef" label-width="100px">
          <el-form-item label="处理状态" prop="status">
            <el-radio-group v-model="handleForm.status">
              <el-radio label="processing">处理中</el-radio>
              <el-radio label="resolved">已解决</el-radio>
              <el-radio label="rejected">已拒绝</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="处理结果" prop="handle_result">
            <el-input
              v-model="handleForm.handle_result"
              type="textarea"
              placeholder="请输入处理结果"
              rows="6"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="handleDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveHandle">保存</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import { ElMessage } from 'element-plus'

const complaints = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  title: '',
  type: '',
  status: '',
  priority: ''
})
const viewDialogVisible = ref(false)
const handleDialogVisible = ref(false)
const currentComplaint = ref(null)
const handleForm = ref({
  status: 'processing',
  handle_result: ''
})
const handleRules = ref({
  status: [{ required: true, message: '请选择处理状态', trigger: 'change' }],
  handle_result: [{ required: true, message: '请输入处理结果', trigger: 'blur' }]
})
const handleFormRef = ref(null)

const getTypeText = (type) => {
  const types = {
    'service': '服务',
    'facility': '设施',
    'environment': '环境',
    'security': '安全',
    'other': '其他'
  }
  return types[type] || type
}

const getTypeTag = (type) => {
  const tags = {
    'service': 'primary',
    'facility': 'success',
    'environment': 'warning',
    'security': 'danger',
    'other': 'info'
  }
  return tags[type] || 'default'
}

const getPriorityText = (priority) => {
  const priorities = {
    'low': '低',
    'medium': '中',
    'high': '高'
  }
  return priorities[priority] || priority
}

const getPriorityTag = (priority) => {
  const tags = {
    'low': 'info',
    'medium': 'warning',
    'high': 'danger'
  }
  return tags[priority] || 'default'
}

const getStatusText = (status) => {
  const statuses = {
    'pending': '待处理',
    'processing': '处理中',
    'resolved': '已解决',
    'rejected': '已拒绝'
  }
  return statuses[status] || status
}

const getStatusTag = (status) => {
  const tags = {
    'pending': 'warning',
    'processing': 'primary',
    'resolved': 'success',
    'rejected': 'danger'
  }
  return tags[status] || 'default'
}

const loadComplaints = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.title) params.append('title', searchForm.value.title)
    if (searchForm.value.type) params.append('type', searchForm.value.type)
    if (searchForm.value.status) params.append('status', searchForm.value.status)
    if (searchForm.value.priority) params.append('priority', searchForm.value.priority)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`http://localhost:8081/api/v1/admin/complaints?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      complaints.value = result.data.list
      total.value = result.data.total
    }
  } catch (error) {
    console.error('加载投诉列表失败:', error)
    ElMessage.error('加载投诉列表失败')
  }
}

const searchComplaints = () => {
  page.value = 1
  loadComplaints()
}

const resetSearch = () => {
  searchForm.value = {
    title: '',
    type: '',
    status: '',
    priority: ''
  }
  page.value = 1
  loadComplaints()
}

const viewComplaint = (complaint) => {
  currentComplaint.value = complaint
  viewDialogVisible.value = true
}

const openHandleDialog = (complaint) => {
  currentComplaint.value = complaint
  handleForm.value = {
    status: 'processing',
    handle_result: ''
  }
  handleDialogVisible.value = true
}

const saveHandle = async () => {
  if (!handleFormRef.value) return
  
  try {
    await handleFormRef.value.validate()
    
    let url = ''
    if (handleForm.value.status === 'resolved') {
      url = `http://localhost:8081/api/v1/admin/complaints/${currentComplaint.value.id}/resolve`
    } else if (handleForm.value.status === 'rejected') {
      url = `http://localhost:8081/api/v1/admin/complaints/${currentComplaint.value.id}/reject`
    } else {
      url = `http://localhost:8081/api/v1/admin/complaints/${currentComplaint.value.id}/handle`
    }
    
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(handleForm.value)
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('处理投诉成功')
      handleDialogVisible.value = false
      loadComplaints()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('处理投诉失败:', error)
    ElMessage.error('处理投诉失败')
  }
}

const deleteComplaint = async (complaintId) => {
  try {
    if (confirm('确定要删除该投诉吗？')) {
      const response = await fetch(`http://localhost:8081/api/v1/admin/complaints/${complaintId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('删除投诉成功')
        loadComplaints()
      } else {
        ElMessage.error(result.msg || '删除失败')
      }
    }
  } catch (error) {
    console.error('删除投诉失败:', error)
    ElMessage.error('删除投诉失败')
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  loadComplaints()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadComplaints()
}

onMounted(() => {
  loadComplaints()
})
</script>

<style scoped>
.complaints {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-filter {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.complaint-detail {
  padding: 20px 0;
}

.complaint-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
  text-align: center;
}

.complaint-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e4e7ed;
}

.meta-item {
  font-size: 14px;
  color: #606266;
}

.complaint-content {
  font-size: 16px;
  line-height: 1.6;
  color: #303133;
  margin-bottom: 20px;
  white-space: pre-line;
}

.complaint-result {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
}

.complaint-result h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 15px;
}

.complaint-result p {
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  margin-bottom: 10px;
}
</style>
