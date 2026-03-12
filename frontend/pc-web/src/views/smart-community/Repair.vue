<template>
  <div class="repair-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>🔧 物业报修</h1>
      <p class="subtitle">在线报修、进度查询、服务评价</p>
    </div>

    <div class="repair-container">
      <!-- 报修表单 -->
      <el-card class="repair-form-card">
        <template #header>
          <div class="card-header">
            <span>📝 提交报修</span>
          </div>
        </template>
        
        <el-form :model="repairForm" label-width="100px" :rules="rules" ref="repairFormRef">
          <el-form-item label="报修类型" prop="repair_type">
            <el-select v-model="repairForm.repair_type" placeholder="选择报修类型" style="width: 100%;">
              <el-option label="水暖" value="water" />
              <el-option label="电路" value="electric" />
              <el-option label="燃气" value="gas" />
              <el-option label="门窗" value="door" />
              <el-option label="电梯" value="elevator" />
              <el-option label="保洁" value="cleaning" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="紧急程度" prop="urgency">
            <el-radio-group v-model="repairForm.urgency">
              <el-radio label="low">一般</el-radio>
              <el-radio label="normal">普通</el-radio>
              <el-radio label="high">紧急</el-radio>
              <el-radio label="urgent">非常紧急</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item label="报修标题" prop="title">
            <el-input v-model="repairForm.title" placeholder="简要描述问题" />
          </el-form-item>
          
          <el-form-item label="问题描述" prop="description">
            <el-input 
              v-model="repairForm.description" 
              type="textarea" 
              :rows="4"
              placeholder="详细描述问题情况..." 
            />
          </el-form-item>
          
          <el-form-item label="联系电话" prop="contact_phone">
            <el-input v-model="repairForm.contact_phone" placeholder="请输入联系电话" />
          </el-form-item>
          
          <el-form-item label="上传图片">
            <el-upload
              action="/api/v1/pc/activities/upload-image"
              list-type="picture-card"
              :on-success="handleUploadSuccess"
              :on-remove="handleRemove"
              :headers="{ 'Authorization': `Bearer ${token}` }"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitRepair" :loading="submitting">
              提交报修
            </el-button>
            <el-button @click="$router.push('/repair/my-orders')">查看我的报修</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 报修统计 -->
      <el-card class="repair-stats-card">
        <template #header>
          <div class="card-header">
            <span>📊 服务统计</span>
          </div>
        </template>
        
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">⚡</div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pending_count || 0 }}</div>
              <div class="stat-label">待处理</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">🔧</div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.processing_count || 0 }}</div>
              <div class="stat-label">处理中</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">✅</div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.completed_count || 0 }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">⭐</div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.avg_rating || '5.0' }}</div>
              <div class="stat-label">平均评分</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 常见问题 -->
    <el-card class="faq-card">
      <template #header>
        <div class="card-header">
          <span>❓ 常见问题</span>
        </div>
      </template>
      <el-collapse>
        <el-collapse-item title="报修后多久会有人处理？" name="1">
          <div>一般情况下，普通报修24小时内响应，紧急报修2小时内响应，非常紧急报修30分钟内响应。</div>
        </el-collapse-item>
        <el-collapse-item title="如何查询报修进度？" name="2">
          <div>您可以在"我的报修"页面查看所有报修工单的处理进度和状态。</div>
        </el-collapse-item>
        <el-collapse-item title="维修完成后如何评价？" name="3">
          <div>维修完成后，您会收到评价提醒，也可以在"我的报修"中对已完成的工单进行评价。</div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const repairFormRef = ref(null)
const submitting = ref(false)
const token = localStorage.getItem('token')

const repairForm = ref({
  repair_type: '',
  urgency: 'normal',
  title: '',
  description: '',
  contact_phone: '',
  images: []
})

const rules = {
  repair_type: [{ required: true, message: '请选择报修类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入报修标题', trigger: 'blur' }],
  description: [{ required: true, message: '请描述问题', trigger: 'blur' }],
  contact_phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
}

const stats = ref({})

const handleUploadSuccess = (response, file) => {
  if (response.code === 0) {
    repairForm.value.images.push(response.data.imageUrl)
  }
}

const handleRemove = (file, fileList) => {
  const index = repairForm.value.images.indexOf(file.response?.data?.imageUrl)
  if (index > -1) {
    repairForm.value.images.splice(index, 1)
  }
}

const submitRepair = async () => {
  const valid = await repairFormRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
    const response = await fetch('/api/v1/pc/repair/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        title: repairForm.value.title,
        type: repairForm.value.repair_type,
        description: repairForm.value.description,
        address: `${userInfo.building_id || ''} ${userInfo.room_number || ''}`,
        images: repairForm.value.images,
        priority: repairForm.value.urgency
      })
    })
    const result = await response.json()
    console.log('提交报修响应:', result)
    if (result.code === 0) {
      ElMessage.success('报修提交成功')
      repairFormRef.value.resetFields()
      router.push('/repair/my-orders')
    } else {
      ElMessage.error(result.msg || '提交失败')
    }
  } catch (error) {
    console.error('提交报修失败:', error)
    ElMessage.error('提交失败')
  } finally {
    submitting.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await fetch('/api/v1/pc/repair/statistics', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const result = await response.json()
    console.log('加载统计响应:', result)
    if (result.code === 0) {
      stats.value = {
        pending_count: result.data?.orders?.pending || 0,
        processing_count: result.data?.orders?.processing || 0,
        completed_count: result.data?.orders?.completed || 0,
        avg_rating: '5.0' // 后端暂时没有提供评分数据
      }
    }
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.repair-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #303133;
}

.subtitle {
  color: #909399;
  margin: 0;
}

.repair-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.repair-form-card,
.repair-stats-card,
.faq-card {
  border-radius: 8px;
}

.card-header {
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-icon {
  font-size: 32px;
  margin-right: 15px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

@media (max-width: 768px) {
  .repair-container {
    grid-template-columns: 1fr;
  }
}
</style>
