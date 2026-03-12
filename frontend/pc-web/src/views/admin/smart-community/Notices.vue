<template>
  <AdminLayout>
    <div class="notices">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>公告通知管理</h3>
            <el-button type="primary" @click="openAddDialog">
              <el-icon><i-ep-plus /></el-icon>
              发布公告
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="标题">
              <el-input v-model="searchForm.title" placeholder="请输入公告标题" />
            </el-form-item>
            <el-form-item label="类型">
              <el-select v-model="searchForm.type" placeholder="选择公告类型">
                <el-option label="社区公告" value="community" />
                <el-option label="物业通知" value="property" />
                <el-option label="紧急通知" value="emergency" />
                <el-option label="活动通知" value="activity" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="已发布" value="published" />
                <el-option label="草稿" value="draft" />
                <el-option label="已过期" value="expired" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchNotices">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="notices" style="width: 100%">
          <el-table-column prop="id" label="公告ID" width="80" />
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="type" label="类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ getTypeText(scope.row.type) }}
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
          <el-table-column prop="author" label="发布人" width="120" />
          <el-table-column prop="publish_time" label="发布时间" width="180" />
          <el-table-column prop="expire_time" label="过期时间" width="180" />
          <el-table-column prop="view_count" label="浏览量" width="100" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewNotice(scope.row)">
                <el-icon><i-ep-view /></el-icon>
                查看
              </el-button>
              <el-button size="small" @click="openEditDialog(scope.row)">
                <el-icon><i-ep-edit /></el-icon>
                编辑
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
      
      <!-- 新增/编辑公告对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="700px"
      >
        <el-form :model="noticeForm" :rules="noticeRules" ref="noticeFormRef" label-width="100px">
          <el-form-item label="标题" prop="title">
            <el-input v-model="noticeForm.title" placeholder="请输入公告标题" />
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="noticeForm.type" placeholder="选择公告类型">
              <el-option label="社区公告" value="community" />
              <el-option label="物业通知" value="property" />
              <el-option label="紧急通知" value="emergency" />
              <el-option label="活动通知" value="activity" />
            </el-select>
          </el-form-item>
          <el-form-item label="内容" prop="content">
            <el-input
              v-model="noticeForm.content"
              type="textarea"
              placeholder="请输入公告内容"
              rows="8"
            />
          </el-form-item>
          <el-form-item label="发布时间" prop="publish_time">
            <el-date-picker
              v-model="noticeForm.publish_time"
              type="datetime"
              placeholder="选择发布时间"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="过期时间" prop="expire_time">
            <el-date-picker
              v-model="noticeForm.expire_time"
              type="datetime"
              placeholder="选择过期时间"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="noticeForm.status" placeholder="选择状态">
              <el-option label="已发布" value="published" />
              <el-option label="草稿" value="draft" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveNotice">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 查看公告对话框 -->
      <el-dialog
        v-model="viewDialogVisible"
        title="公告详情"
        width="700px"
      >
        <div v-if="currentNotice" class="notice-detail">
          <h3 class="notice-title">{{ currentNotice.title }}</h3>
          <div class="notice-meta">
            <span class="meta-item">
              <el-tag :type="getTypeTag(currentNotice.type)">{{ getTypeText(currentNotice.type) }}</el-tag>
            </span>
            <span class="meta-item">发布人：{{ currentNotice.author }}</span>
            <span class="meta-item">发布时间：{{ currentNotice.publish_time }}</span>
            <span class="meta-item">过期时间：{{ currentNotice.expire_time }}</span>
            <span class="meta-item">浏览量：{{ currentNotice.view_count }}</span>
          </div>
          <div class="notice-content">
            {{ currentNotice.content }}
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
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const notices = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  title: '',
  type: '',
  status: ''
})
const dialogVisible = ref(false)
const viewDialogVisible = ref(false)
const dialogType = ref('add')
const dialogTitle = computed(() => dialogType.value === 'add' ? '发布公告' : '编辑公告')
const noticeForm = ref({
  title: '',
  type: 'notice',
  content: '',
  publish_time: new Date(),
  expire_time: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 默认7天过期
  status: 'published'
})
const noticeRules = ref({
  title: [{ required: true, message: '请输入公告标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入公告内容', trigger: 'blur' }],
  publish_time: [{ required: true, message: '请选择发布时间', trigger: 'change' }],
  expire_time: [{ required: true, message: '请选择过期时间', trigger: 'change' }]
})
const noticeFormRef = ref(null)
const currentNotice = ref(null)

// 获取类型文本
const getTypeText = (type) => {
  const types = {
    'community': '社区公告',
    'property': '物业通知',
    'emergency': '紧急通知',
    'activity': '活动通知'
  }
  return types[type] || type
}

// 获取类型标签样式
const getTypeTag = (type) => {
  const tags = {
    'community': 'primary',
    'property': 'success',
    'emergency': 'danger',
    'activity': 'warning'
  }
  return tags[type] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const statuses = {
    'published': '已发布',
    'draft': '草稿',
    'expired': '已过期'
  }
  return statuses[status] || status
}

// 获取状态标签样式
const getStatusTag = (status) => {
  const tags = {
    'published': 'success',
    'draft': 'info',
    'expired': 'danger'
  }
  return tags[status] || 'default'
}

// 加载公告列表
const loadNotices = async () => {
  try {
    const response = await request.get('/v1/pc/notices', {
      params: {
        title: searchForm.value.title,
        type: searchForm.value.type,
        status: searchForm.value.status,
        page: page.value,
        pageSize: pageSize.value
      }
    })
    console.log('加载公告列表响应:', response)
    if (response.data.code === 0) {
      notices.value = response.data.data.list
      total.value = response.data.data.total
    } else {
      console.error('加载公告列表失败:', response.data.msg)
      ElMessage.error(response.data.msg || '加载公告列表失败')
    }
  } catch (error) {
    console.error('加载公告列表失败:', error)
    ElMessage.error('加载公告列表失败')
  }
}

// 搜索公告
const searchNotices = () => {
  page.value = 1
  loadNotices()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    title: '',
    type: '',
    status: ''
  }
  page.value = 1
  loadNotices()
}

// 打开新增对话框
const openAddDialog = () => {
  dialogType.value = 'add'
  noticeForm.value = {
    title: '',
    type: 'community',
    content: '',
    publish_time: new Date(),
    expire_time: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    status: 'published'
  }
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (notice) => {
  dialogType.value = 'edit'
  noticeForm.value = { ...notice }
  dialogVisible.value = true
}

// 查看公告
const viewNotice = (notice) => {
  currentNotice.value = notice
  viewDialogVisible.value = true
}

// 保存公告
const saveNotice = async () => {
  if (!noticeFormRef.value) return
  
  try {
    await noticeFormRef.value.validate()
    
    // 获取当前用户信息作为作者
    const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
    const noticeData = {
      ...noticeForm.value,
      author: userInfo.nickname || '管理员'
    }
    
    console.log('=== 前端调试信息 ===')
    console.log('操作类型:', dialogType.value === 'add' ? '新增' : '编辑')
    console.log('用户信息:', userInfo)
    console.log('表单数据:', noticeForm.value)
    console.log('发送的数据:', noticeData)
    console.log('Token:', localStorage.getItem('token'))
    
    let response
    if (dialogType.value === 'add') {
      console.log('请求URL:', '/v1/pc/notices')
      console.log('请求方法:', 'POST')
      response = await request.post('/v1/pc/notices', noticeData)
    } else {
      console.log('请求URL:', `/v1/pc/notices/${noticeForm.value.id}`)
      console.log('请求方法:', 'PUT')
      response = await request.put(`/v1/pc/notices/${noticeForm.value.id}`, noticeData)
    }
    
    console.log('后端响应:', response)
    console.log('后端响应数据:', response.data)
    
    if (response.data.code === 0) {
      ElMessage.success(dialogType.value === 'add' ? '发布公告成功' : '编辑公告成功')
      dialogVisible.value = false
      loadNotices()
    } else {
      console.error('后端返回错误:', response.data.msg)
      ElMessage.error(response.data.msg || '操作失败')
    }
  } catch (error) {
    console.error('=== 保存公告失败 ===')
    console.error('错误对象:', error)
    console.error('错误响应:', error.response)
    console.error('错误状态:', error.response?.status)
    console.error('错误数据:', error.response?.data)
    ElMessage.error('保存公告失败')
  }
}

// 删除公告
const deleteNotice = async (noticeId) => {
  try {
    if (confirm('确定要删除该公告吗？')) {
      const response = await request.delete(`/v1/pc/notices/${noticeId}`)
      console.log('删除公告响应:', response)
      if (response.data.code === 0) {
        ElMessage.success('删除公告成功')
        loadNotices()
      } else {
        console.error('删除公告失败:', response.data.msg)
        ElMessage.error(response.data.msg || '删除失败')
      }
    }
  } catch (error) {
    console.error('删除公告失败:', error)
    ElMessage.error('删除公告失败')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadNotices()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadNotices()
}

onMounted(() => {
  loadNotices()
})
</script>

<style scoped>
.notices {
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

.notice-detail {
  padding: 20px 0;
}

.notice-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
  text-align: center;
}

.notice-meta {
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

.notice-content {
  font-size: 16px;
  line-height: 1.6;
  color: #303133;
  white-space: pre-line;
}
</style>