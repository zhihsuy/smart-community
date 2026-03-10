<template>
  <div class="visitor-appointments-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📋 预约管理</h1>
      <p class="subtitle">查看和管理所有访客预约</p>
    </div>

    <!-- 搜索筛选 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="选择状态">
            <el-option label="全部" value="" />
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
            <el-option label="已取消" value="cancelled" />
            <el-option label="已过期" value="expired" />
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.keyword"
            placeholder="访客姓名或电话"
            clearable
            style="width: 300px"
          >
            <template #append>
              <el-button @click="loadAppointments">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 预约列表 -->
    <el-card class="appointments-card">
      <template #header>
        <div class="card-header">
          <span>预约列表</span>
          <span class="total-count">共 {{ pagination.total }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="appointments" style="width: 100%">
        <el-table-column prop="visitor_name" label="访客姓名" width="120" />
        <el-table-column prop="visitor_phone" label="联系电话" width="150" />
        <el-table-column prop="visit_time" label="来访时间" width="180" />
        <el-table-column prop="duration" label="预计时长" width="100">
          <template #default="scope">
            {{ scope.row.duration }}分钟
          </template>
        </el-table-column>
        <el-table-column prop="purpose" label="来访事由" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag size="small" :type="getStatusColor(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewAppointment(scope.row)">
              查看
            </el-button>
            <el-button 
              v-if="scope.row.status === 'approved'" 
              size="small" 
              type="success" 
              @click="viewQRCode(scope.row)"
            >
              二维码
            </el-button>
            <el-button 
              v-if="scope.row.status === 'pending'" 
              size="small" 
              type="danger" 
              @click="cancelAppointment(scope.row)"
            >
              取消
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

    <!-- 预约详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="预约详情"
      width="600px"
    >
      <div v-if="currentAppointment" class="appointment-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="访客姓名">{{ currentAppointment.visitor_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentAppointment.visitor_phone }}</el-descriptions-item>
          <el-descriptions-item label="来访时间">{{ currentAppointment.visit_time }}</el-descriptions-item>
          <el-descriptions-item label="预计时长">{{ currentAppointment.duration }}分钟</el-descriptions-item>
          <el-descriptions-item label="来访事由">{{ currentAppointment.purpose }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusText(currentAppointment.status) }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentAppointment.created_at }}</el-descriptions-item>
          <el-descriptions-item label="审核时间">{{ currentAppointment.approved_at || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

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
import { ArrowLeft, Search } from '@element-plus/icons-vue'

const appointments = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})
const searchForm = ref({
  status: '',
  keyword: ''
})
const detailDialogVisible = ref(false)
const qrCodeDialogVisible = ref(false)
const currentAppointment = ref(null)

// 加载预约列表
const loadAppointments = async () => {
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.currentPage)
    params.append('pageSize', pagination.value.pageSize)
    
    if (searchForm.value.status) {
      params.append('status', searchForm.value.status)
    }
    if (searchForm.value.keyword) {
      params.append('keyword', searchForm.value.keyword)
    }

    const response = await fetch(`/api/v1/pc/visitor/appointments?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      appointments.value = result.data?.list || []
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载预约失败:', error)
    ElMessage.error('加载预约失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadAppointments()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadAppointments()
}

const viewAppointment = (appointment) => {
  currentAppointment.value = appointment
  detailDialogVisible.value = true
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
      loadAppointments()
    } else {
      ElMessage.error(result.msg || '取消失败')
    }
  } catch (error) {
    console.error('取消预约失败:', error)
    ElMessage.error('取消失败')
  }
}

const getStatusText = (status) => {
  const map = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已拒绝',
    'cancelled': '已取消',
    'expired': '已过期'
  }
  return map[status] || status
}

const getStatusColor = (status) => {
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
  loadAppointments()
})
</script>

<style scoped>
.visitor-appointments-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
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
.appointments-card {
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

.appointment-detail {
  padding: 20px 0;
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
