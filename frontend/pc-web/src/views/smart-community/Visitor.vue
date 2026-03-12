<template>
  <div class="visitor-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>👥 访客管理</h1>
      <p class="subtitle">访客预约、二维码生成、进出记录</p>
    </div>

    <div class="feature-grid">
      <!-- 访客预约 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📝 访客预约</span>
          </div>
        </template>
        <div class="visitor-form">
          <el-form :model="visitorForm" label-width="100px" :rules="rules" ref="visitorFormRef">
            <el-form-item label="访客姓名" prop="visitor_name">
              <el-input v-model="visitorForm.visitor_name" placeholder="请输入访客姓名" />
            </el-form-item>
            <el-form-item label="联系电话" prop="visitor_phone">
              <el-input v-model="visitorForm.visitor_phone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item label="来访时间" prop="visit_time">
              <el-date-picker
                v-model="visitorForm.visit_time"
                type="datetime"
                placeholder="选择来访时间"
                style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="预计时长" prop="duration">
              <el-select v-model="visitorForm.duration" placeholder="选择预计时长">
                <el-option label="30分钟" value="30" />
                <el-option label="1小时" value="60" />
                <el-option label="2小时" value="120" />
                <el-option label="4小时" value="240" />
                <el-option label="8小时" value="480" />
              </el-select>
            </el-form-item>
            <el-form-item label="来访事由" prop="purpose">
              <el-input 
                v-model="visitorForm.purpose" 
                type="textarea" 
                :rows="3"
                placeholder="请输入来访事由"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitVisitor" :loading="submitting">
                提交预约
              </el-button>
              <el-button @click="$router.push('/visitor/appointments')">查看预约</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <!-- 我的预约 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📋 我的预约</span>
            <el-button type="primary" size="small" @click="$router.push('/visitor/appointments')">
              查看全部
            </el-button>
          </div>
        </template>
        <div class="appointments">
          <div v-for="appointment in recentAppointments" :key="appointment.id" class="appointment-item">
            <div class="appointment-header">
              <span class="visitor-name">{{ appointment.visitor_name }}</span>
              <el-tag :type="getAppointmentStatusType(appointment.status)">
                {{ getAppointmentStatusText(appointment.status) }}
              </el-tag>
            </div>
            <div class="appointment-info">
              <span class="visit-time">{{ appointment.visit_time }}</span>
              <span class="duration">{{ appointment.duration }}分钟</span>
            </div>
            <div class="appointment-actions">
              <el-button 
                v-if="appointment.status === 'approved'" 
                type="primary" 
                size="small" 
                @click="viewQRCode(appointment)"
              >
                查看二维码
              </el-button>
              <el-button 
                v-if="appointment.status === 'pending'" 
                type="danger" 
                size="small" 
                @click="cancelAppointment(appointment)"
              >
                取消预约
              </el-button>
            </div>
          </div>
          <el-empty v-if="recentAppointments.length === 0" description="暂无预约" />
        </div>
      </el-card>

      <!-- 访客统计 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📊 访客统计</span>
          </div>
        </template>
        <div class="visitor-stats">
          <div class="stat-item">
            <div class="stat-value">{{ stats.today_count || 0 }}</div>
            <div class="stat-label">今日访客</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.week_count || 0 }}</div>
            <div class="stat-label">本周访客</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.month_count || 0 }}</div>
            <div class="stat-label">本月访客</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_count || 0 }}</div>
            <div class="stat-label">总访客数</div>
          </div>
        </div>
      </el-card>

      <!-- 快捷操作 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>⚡ 快捷操作</span>
          </div>
        </template>
        <div class="quick-actions">
          <el-button type="primary" plain @click="$router.push('/visitor/appointments')">
            <el-icon><List /></el-icon>
            预约管理
          </el-button>
          <el-button type="success" plain @click="scanQRCode">
            <el-icon><Position /></el-icon>
            扫码验证
          </el-button>
          <el-button type="info" plain @click="viewVisitorRecords">
            <el-icon><DataAnalysis /></el-icon>
            访客记录
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 最近访客记录 -->
    <el-card class="records-card">
      <template #header>
        <div class="card-header">
          <span>📝 最近访客记录</span>
          <el-button text @click="viewAllRecords">查看全部</el-button>
        </div>
      </template>
      <el-table :data="visitorRecords" style="width: 100%">
        <el-table-column prop="visitor_name" label="访客姓名" width="120" />
        <el-table-column prop="visitor_phone" label="联系电话" width="150" />
        <el-table-column prop="visit_time" label="来访时间" width="180" />
        <el-table-column prop="exit_time" label="离开时间" width="180">
          <template #default="scope">
            <span v-if="scope.row.exit_time">{{ scope.row.exit_time }}</span>
            <span v-else>未离开</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag size="small" :type="scope.row.status === 'completed' ? 'success' : 'warning'">
              {{ scope.row.status === 'completed' ? '已完成' : '进行中' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 二维码对话框 -->
    <el-dialog
      v-model="qrCodeDialogVisible"
      title="访客二维码"
      width="400px"
    >
      <div v-if="currentAppointment" class="qr-code-container">
        <div class="qr-code-info">
          <p><strong>访客姓名:</strong> {{ currentAppointment.visitor_name }}</p>
          <p><strong>预约时间:</strong> {{ currentAppointment.visit_time }}</p>
          <p><strong>有效期:</strong> 24小时</p>
        </div>
        <div class="qr-code-image">
          <img :src="`/api/v1/pc/visitor/qrcode?appointment_id=${currentAppointment.id}`" alt="访客二维码" />
        </div>
        <div class="qr-code-tip">
          请将此二维码展示给门卫或门禁系统
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { List, Position, DataAnalysis, ArrowLeft } from '@element-plus/icons-vue'

const visitorForm = ref({
  visitor_name: '',
  visitor_phone: '',
  visit_time: null,
  duration: '60',
  purpose: ''
})

const rules = {
  visitor_name: [{ required: true, message: '请输入访客姓名', trigger: 'blur' }],
  visitor_phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  visit_time: [{ required: true, message: '请选择来访时间', trigger: 'change' }],
  purpose: [{ required: true, message: '请输入来访事由', trigger: 'blur' }]
}

const visitorFormRef = ref(null)
const submitting = ref(false)
const recentAppointments = ref([])
const visitorRecords = ref([])
const stats = ref({})
const qrCodeDialogVisible = ref(false)
const currentAppointment = ref(null)

// 提交访客预约
const submitVisitor = async () => {
  const valid = await visitorFormRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
    const response = await fetch('/api/v1/pc/visitor/appointments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        ...visitorForm.value,
        building_id: userInfo.building_id,
        room_number: userInfo.room_number
      })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('预约提交成功')
      visitorFormRef.value.resetFields()
      loadRecentAppointments()
    } else {
      ElMessage.error(result.msg || '提交失败')
    }
  } catch (error) {
    console.error('提交预约失败:', error)
    ElMessage.error('提交失败')
  } finally {
    submitting.value = false
  }
}

// 加载最近预约
const loadRecentAppointments = async () => {
  try {
    const response = await fetch('/api/v1/pc/visitor/appointments?pageSize=5', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      recentAppointments.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载预约失败:', error)
  }
}

// 加载访客记录
const loadVisitorRecords = async () => {
  try {
    const response = await fetch('/api/v1/pc/visitor/records?pageSize=5', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      visitorRecords.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载记录失败:', error)
  }
}

// 加载统计
const loadStats = async () => {
  try {
    const response = await fetch('/api/v1/pc/visitor/statistics', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      stats.value = result.data || {}
    }
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

const viewQRCode = (appointment) => {
  currentAppointment.value = appointment
  qrCodeDialogVisible.value = true
}

const cancelAppointment = async (appointment) => {
  try {
    const response = await fetch(`/api/v1/pc/visitor/appointments/${appointment.id}/cancel`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('预约已取消')
      loadRecentAppointments()
    } else {
      ElMessage.error(result.msg || '取消失败')
    }
  } catch (error) {
    console.error('取消预约失败:', error)
    ElMessage.error('取消失败')
  }
}

const scanQRCode = () => {
  ElMessage.info('扫码验证功能开发中')
}

const viewVisitorRecords = () => {
  ElMessage.info('访客记录功能开发中')
}

const viewAllRecords = () => {
  ElMessage.info('查看全部记录功能开发中')
}

const getAppointmentStatusText = (status) => {
  const map = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已拒绝',
    'cancelled': '已取消',
    'expired': '已过期'
  }
  return map[status] || status
}

const getAppointmentStatusType = (status) => {
  const map = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger',
    'cancelled': 'info',
    'expired': 'danger'
  }
  return map[status] || 'info'
}

onMounted(() => {
  loadRecentAppointments()
  loadVisitorRecords()
  loadStats()
})
</script>

<style scoped>
.visitor-page {
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

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.appointments {
  max-height: 300px;
  overflow-y: auto;
}

.appointment-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 15px;
}

.appointment-item:last-child {
  margin-bottom: 0;
}

.appointment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.visitor-name {
  font-weight: 600;
}

.appointment-info {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.appointment-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.visitor-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  padding: 20px 0;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.records-card {
  border-radius: 8px;
}

.qr-code-container {
  padding: 20px 0;
  text-align: center;
}

.qr-code-info {
  margin-bottom: 20px;
  text-align: left;
}

.qr-code-image {
  margin-bottom: 20px;
}

.qr-code-image img {
  width: 200px;
  height: 200px;
}

.qr-code-tip {
  font-size: 14px;
  color: #909399;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .visitor-stats {
    grid-template-columns: 1fr;
  }
}
</style>
