<template>
  <AdminLayout>
    <div class="activity-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>社区活动管理</h3>
          </div>
        </template>
        
        <div class="mb-4">
          <el-button type="primary" @click="openActivityDialog">
            <el-icon>
              <i class="el-icon-plus" />
            </el-icon>
            新增活动
          </el-button>
        </div>
        
        <el-table :data="activities" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="活动标题" min-width="150" show-overflow-tooltip />
          <el-table-column prop="start_time" label="开始时间" width="140" />
          <el-table-column prop="location" label="地点" width="100" show-overflow-tooltip />
          <el-table-column prop="max_participants" label="人数" width="70" />
          <el-table-column prop="status" label="状态" width="80">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="organizer" label="组织者" width="90" show-overflow-tooltip />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="editActivity(scope.row)">编辑</el-button>
              <el-button size="small" type="primary" @click="publishActivity(scope.row)" v-if="scope.row.status === 'draft'">发布</el-button>
              <el-button size="small" type="danger" @click="deleteActivity(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      
      <!-- 活动对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="800px"
        append-to-body
      >
        <el-form :model="activityForm" :rules="activityRules" ref="activityFormRef" label-width="100px">
          <el-form-item label="活动标题" prop="title">
            <el-input v-model="activityForm.title" placeholder="请输入活动标题" />
          </el-form-item>
          <el-form-item label="活动描述" prop="description">
            <el-input v-model="activityForm.description" type="textarea" :rows="4" placeholder="请输入活动描述" />
          </el-form-item>
          <el-form-item label="开始时间" prop="start_time">
            <el-date-picker v-model="activityForm.start_time" type="datetime" placeholder="选择开始时间" style="width: 100%" />
          </el-form-item>
          <el-form-item label="结束时间" prop="end_time">
            <el-date-picker v-model="activityForm.end_time" type="datetime" placeholder="选择结束时间" style="width: 100%" />
          </el-form-item>
          <el-form-item label="活动地点" prop="location">
            <el-input v-model="activityForm.location" placeholder="请输入活动地点" />
          </el-form-item>
          <el-form-item label="最大人数" prop="max_participants">
            <el-input-number v-model="activityForm.max_participants" :min="1" style="width: 100%" />
          </el-form-item>
          <el-form-item label="活动分类" prop="category">
            <el-select v-model="activityForm.category" placeholder="选择活动分类">
              <el-option label="文化活动" value="culture" />
              <el-option label="体育活动" value="sports" />
              <el-option label="教育活动" value="education" />
              <el-option label="公益活动" value="charity" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="组织者" prop="organizer">
            <el-input v-model="activityForm.organizer" placeholder="请输入组织者" />
          </el-form-item>
          <el-form-item label="联系电话" prop="contact_phone">
            <el-input v-model="activityForm.contact_phone" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="活动标签" prop="tags">
            <el-input v-model="activityForm.tags" placeholder="请输入活动标签，多个标签用逗号分隔" />
          </el-form-item>
          <el-form-item label="活动图片" prop="image_url">
            <el-upload
              class="upload-demo"
              action="/api/v1/pc/activities/upload-image"
              :headers="uploadHeaders"
              :on-success="handleImageUploadSuccess"
              :on-error="handleImageUploadError"
              :limit="1"
              :auto-upload="true"
            >
              <template #trigger>
                <el-button type="primary">
                  <el-icon>
                    <i class="el-icon-upload" />
                  </el-icon>
                  上传图片
                </el-button>
              </template>
              <template #file-list>
                <el-image
                  v-if="activityForm.image_url"
                  :src="activityForm.image_url"
                  style="width: 200px; height: 150px; margin-top: 10px"
                  fit="cover"
                />
              </template>
            </el-upload>
            <el-input
              v-model="activityForm.image_url"
              placeholder="请输入活动图片URL（或点击上传）"
              style="margin-top: 10px"
            />
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input v-model="activityForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveActivity">保存</el-button>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import AdminLayout from '@/components/AdminLayout.vue'

const activities = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新增活动')
const activityForm = ref({
  title: '',
  description: '',
  start_time: null,
  end_time: null,
  location: '',
  max_participants: 50,
  category: 'culture',
  organizer: '',
  contact_phone: '',
  tags: '',
  image_url: '',
  remark: ''
})

const activityFormRef = ref(null)

const uploadHeaders = computed(() => {
  return {
    Authorization: `Bearer ${localStorage.getItem('token') || ''}`
  }
})

const activityRules = {
  title: [{ required: true, message: '请输入活动标题', trigger: 'blur' }],
  description: [{ required: true, message: '请输入活动描述', trigger: 'blur' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
  location: [{ required: true, message: '请输入活动地点', trigger: 'blur' }],
  max_participants: [{ required: true, message: '请输入最大人数', trigger: 'blur' }],
  category: [{ required: true, message: '请选择活动分类', trigger: 'change' }],
  organizer: [{ required: true, message: '请输入组织者', trigger: 'blur' }],
  contact_phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
}

const openActivityDialog = () => {
  dialogTitle.value = '新增活动'
  activityForm.value = {
    title: '',
    description: '',
    start_time: null,
    end_time: null,
    location: '',
    max_participants: 50,
    category: 'culture',
    organizer: '',
    contact_phone: '',
    tags: '',
    image_url: '',
    remark: ''
  }
  dialogVisible.value = true
}

const editActivity = (activity) => {
  dialogTitle.value = '编辑活动'
  activityForm.value = { ...activity }
  dialogVisible.value = true
}

const saveActivity = async () => {
  try {
    // 表单验证
    if (activityFormRef.value) {
      await activityFormRef.value.validate()
    }
    
    console.log('保存活动:', activityForm.value)
    if (dialogTitle.value === '新增活动') {
      const response = await request.post('/v1/pc/activities', activityForm.value)
      console.log('新增活动响应:', response)
      ElMessage.success('新增活动成功')
    } else {
      const response = await request.put(`/v1/pc/activities/${activityForm.value.id}`, activityForm.value)
      console.log('更新活动响应:', response)
      ElMessage.success('更新活动成功')
    }
    dialogVisible.value = false
    loadActivities()
  } catch (error) {
    console.error('保存活动失败:', error)
    if (error.name !== 'ValidationError') {
      ElMessage.error('保存活动失败')
    }
  }
}

const publishActivity = async (activity) => {
  try {
    await request.post(`/v1/pc/activities/${activity.id}/publish`)
    ElMessage.success('活动发布成功')
    loadActivities()
  } catch (error) {
    ElMessage.error('活动发布失败')
  }
}

const deleteActivity = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该活动吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await request.delete(`/v1/pc/activities/${id}`)
    ElMessage.success('活动删除成功')
    loadActivities()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('活动删除失败')
    }
  }
}

const getStatusTag = (status) => {
  switch (status) {
    case 'draft': return 'info'
    case 'published': return 'success'
    case 'completed': return 'warning'
    case 'cancelled': return 'danger'
    default: return 'info'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'draft': return '草稿'
    case 'published': return '已发布'
    case 'completed': return '已完成'
    case 'cancelled': return '已取消'
    default: return status
  }
}

const loadActivities = async () => {
  try {
    const response = await request.get('/v1/pc/activities')
    activities.value = response.data.list
  } catch (error) {
    ElMessage.error('加载活动列表失败')
  }
}

const handleImageUploadSuccess = (response) => {
  if (response.code === 0) {
    activityForm.value.image_url = response.data.imageUrl
    ElMessage.success('图片上传成功')
  } else {
    ElMessage.error('图片上传失败: ' + response.msg)
  }
}

const handleImageUploadError = (error) => {
  ElMessage.error('图片上传失败')
  console.error('上传失败:', error)
}

onMounted(() => {
  loadActivities()
})
</script>

<style scoped>
.activity-management {
  min-height: 100%;
  padding: 0;
}

.activity-management :deep(.el-card) {
  margin-bottom: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}
</style>