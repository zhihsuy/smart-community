<template>
  <AdminLayout>
    <div class="notice-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>公告管理</h3>
          </div>
        </template>
        
        <div class="mb-4">
          <el-button type="primary" @click="openNoticeDialog">
            <el-icon><i-ep-plus /></el-icon>
            新增公告
          </el-button>
        </div>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="公告标题">
              <el-input v-model="searchForm.title" placeholder="输入公告标题" />
            </el-form-item>
            <el-form-item label="公告类型">
              <el-select v-model="searchForm.type" placeholder="选择类型">
                <el-option label="全部" value="" />
                <el-option label="社区通知" value="community" />
                <el-option label="活动通知" value="activity" />
                <el-option label="安全通知" value="security" />
                <el-option label="维修通知" value="maintenance" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="全部" value="" />
                <el-option label="已发布" value="published" />
                <el-option label="草稿" value="draft" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchNotices">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="notices" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="title" label="公告标题" />
          <el-table-column prop="type" label="类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ getTypeText(scope.row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="author" label="发布人" width="120" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'published' ? 'success' : 'info'">
                {{ scope.row.status === 'published' ? '已发布' : '草稿' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="view_count" label="浏览量" width="100" />
          <el-table-column prop="publish_time" label="发布时间" width="180" />
          <el-table-column label="操作" width="300" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewNotice(scope.row)">
                <el-icon><i-ep-view /></el-icon>
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editNotice(scope.row)">
                <el-icon><i-ep-edit /></el-icon>
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="success" 
                @click="publishNotice(scope.row)" 
                v-if="scope.row.status === 'draft'"
              >
                <el-icon><i-ep-upload /></el-icon>
                发布
              </el-button>
              <el-button 
                size="small" 
                type="warning" 
                @click="unpublishNotice(scope.row)" 
                v-if="scope.row.status === 'published'"
              >
                <el-icon><i-ep-download /></el-icon>
                取消发布
              </el-button>
              <el-button size="small" type="danger" @click="deleteNotice(scope.row.id)">
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
      
      <el-dialog
        v-model="noticeDialogVisible"
        :title="noticeDialogTitle"
        width="800px"
      >
        <el-form :model="noticeForm" :rules="noticeRules" ref="noticeFormRef" label-width="100px" status-icon>
          <el-form-item label="公告标题" prop="title">
            <el-input v-model="noticeForm.title" placeholder="请输入公告标题" />
          </el-form-item>
          <el-form-item label="公告类型" prop="type">
            <el-select v-model="noticeForm.type" placeholder="选择公告类型">
              <el-option label="社区通知" value="community" />
              <el-option label="活动通知" value="activity" />
              <el-option label="安全通知" value="security" />
              <el-option label="维修通知" value="maintenance" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="公告内容" prop="content">
            <el-input v-model="noticeForm.content" type="textarea" :rows="10" placeholder="请输入公告内容" />
          </el-form-item>
          <el-form-item label="发布人" prop="author">
            <el-input v-model="noticeForm.author" placeholder="请输入发布人姓名" />
          </el-form-item>
          <el-form-item label="过期时间" prop="expire_time">
            <el-date-picker
              v-model="noticeForm.expire_time"
              type="datetime"
              placeholder="选择过期时间（可选）"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="noticeForm.status" placeholder="选择状态">
              <el-option label="草稿" value="draft" />
              <el-option label="已发布" value="published" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="noticeDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveNotice">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="viewDialogVisible"
        title="公告详情"
        width="800px"
      >
        <div v-if="currentNotice" class="notice-detail">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="公告标题">{{ currentNotice.title }}</el-descriptions-item>
            <el-descriptions-item label="公告类型">
              <el-tag :type="getTypeTag(currentNotice.type)">
                {{ getTypeText(currentNotice.type) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="发布人">{{ currentNotice.author }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="currentNotice.status === 'published' ? 'success' : 'info'">
                {{ currentNotice.status === 'published' ? '已发布' : '草稿' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="发布时间">{{ currentNotice.publish_time }}</el-descriptions-item>
            <el-descriptions-item label="过期时间">{{ currentNotice.expire_time || '无' }}</el-descriptions-item>
            <el-descriptions-item label="浏览量">{{ currentNotice.view_count }}</el-descriptions-item>
          </el-descriptions>
          <div class="notice-content mt-4">
            <h4>公告内容</h4>
            <div class="content-text">{{ currentNotice.content }}</div>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="viewDialogVisible = false">关闭</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const notices = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const searchForm = ref({
  title: '',
  type: '',
  status: ''
})

const noticeDialogVisible = ref(false)
const noticeDialogTitle = ref('新增公告')
const noticeForm = ref({
  title: '',
  type: 'community',
  content: '',
  author: '',
  expire_time: null,
  status: 'draft'
})

const viewDialogVisible = ref(false)
const currentNotice = ref(null)

const noticeRules = {
  title: [{ required: true, message: '请输入公告标题', trigger: 'blur' }],
  type: [{ required: true, message: '请选择公告类型', trigger: 'change' }],
  content: [{ required: true, message: '请输入公告内容', trigger: 'blur' }],
  author: [{ required: true, message: '请输入发布人姓名', trigger: 'blur' }]
}

const loadNotices = async () => {
  try {
    const response = await axios.get('/api/v1/pc/notices', {
      params: {
        page: page.value,
        pageSize: pageSize.value,
        ...searchForm.value
      }
    })
    notices.value = response.data.data.list
    total.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载公告列表失败')
  }
}

const openNoticeDialog = () => {
  noticeDialogTitle.value = '新增公告'
  noticeForm.value = {
    title: '',
    type: 'community',
    content: '',
    author: '',
    expire_time: null,
    status: 'draft'
  }
  noticeDialogVisible.value = true
}

const saveNotice = async () => {
  try {
    if (noticeDialogTitle.value === '新增公告') {
      await axios.post('/api/v1/pc/notices', noticeForm.value)
      ElMessage.success('新增公告成功')
    } else {
      await axios.put(`/api/v1/pc/notices/${noticeForm.value.id}`, noticeForm.value)
      ElMessage.success('更新公告成功')
    }
    noticeDialogVisible.value = false
    loadNotices()
  } catch (error) {
    ElMessage.error('保存公告失败')
  }
}

const viewNotice = async (notice) => {
  try {
    const response = await axios.get(`/api/v1/pc/notices/${notice.id}`)
    currentNotice.value = response.data.data
    viewDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取公告详情失败')
  }
}

const editNotice = (notice) => {
  noticeDialogTitle.value = '编辑公告'
  noticeForm.value = { ...notice }
  noticeDialogVisible.value = true
}

const publishNotice = async (notice) => {
  try {
    await axios.post(`/api/v1/pc/notices/${notice.id}/publish`)
    ElMessage.success('发布公告成功')
    loadNotices()
  } catch (error) {
    ElMessage.error('发布公告失败')
  }
}

const unpublishNotice = async (notice) => {
  try {
    await axios.post(`/api/v1/pc/notices/${notice.id}/unpublish`)
    ElMessage.success('取消发布成功')
    loadNotices()
  } catch (error) {
    ElMessage.error('取消发布失败')
  }
}

const deleteNotice = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该公告吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/v1/pc/notices/${id}`)
    ElMessage.success('删除公告成功')
    loadNotices()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除公告失败')
    }
  }
}

const searchNotices = () => {
  page.value = 1
  loadNotices()
}

const resetSearch = () => {
  searchForm.value = {
    title: '',
    type: '',
    status: ''
  }
  page.value = 1
  loadNotices()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  loadNotices()
}

const handleCurrentChange = (currentPage) => {
  page.value = currentPage
  loadNotices()
}

const getTypeTag = (type) => {
  const typeMap = {
    'community': 'primary',
    'activity': 'success',
    'security': 'danger',
    'maintenance': 'warning',
    'other': 'info'
  }
  return typeMap[type] || ''
}

const getTypeText = (type) => {
  const typeMap = {
    'community': '社区通知',
    'activity': '活动通知',
    'security': '安全通知',
    'maintenance': '维修通知',
    'other': '其他'
  }
  return typeMap[type] || type
}

onMounted(() => {
  loadNotices()
})
</script>

<style scoped>
.notice-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
}

.search-filter {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.notice-detail {
  padding: 10px;
}

.notice-content {
  margin-top: 20px;
}

.notice-content h4 {
  margin-bottom: 10px;
  color: #303133;
}

.content-text {
  padding: 15px;
  background: #f5f5f5;
  border-radius: 4px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.mt-4 {
  margin-top: 16px;
}
</style>
