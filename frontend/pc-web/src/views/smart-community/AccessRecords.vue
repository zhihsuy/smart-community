<template>
  <div class="access-records">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📝 出入记录</h1>
      <p class="subtitle">查看所有门禁出入记录</p>
    </div>

    <!-- 搜索筛选 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 280px"
          />
        </el-form-item>
        <el-form-item label="门禁设备">
          <el-select v-model="searchForm.deviceId" placeholder="选择设备">
            <el-option
              v-for="device in devices"
              :key="device.id"
              :label="device.device_name"
              :value="device.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="开门方式">
          <el-select v-model="searchForm.accessType" placeholder="选择方式">
            <el-option label="人脸识别" value="face" />
            <el-option label="指纹" value="fingerprint" />
            <el-option label="门禁卡" value="card" />
            <el-option label="二维码" value="qr_code" />
            <el-option label="密码" value="password" />
            <el-option label="远程" value="remote" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="选择状态">
            <el-option label="成功" value="success" />
            <el-option label="失败" value="failed" />
            <el-option label="超时" value="timeout" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadRecords">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 记录列表 -->
    <el-card class="records-card">
      <template #header>
        <div class="card-header">
          <span>记录列表</span>
          <span class="total-count">共 {{ pagination.total }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="records" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="record_time" label="时间" width="180" />
        <el-table-column prop="device_name" label="门禁设备" width="150" />
        <el-table-column prop="location" label="位置" width="150" />
        <el-table-column prop="nickname" label="用户" width="120">
          <template #default="scope">
            <span v-if="scope.row.nickname">{{ scope.row.nickname }}</span>
            <span v-else>访客</span>
          </template>
        </el-table-column>
        <el-table-column prop="access_type" label="开门方式" width="120">
          <template #default="scope">
            <el-tag size="small" :type="getAccessTypeType(scope.row.access_type)">
              {{ getAccessTypeText(scope.row.access_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="access_status" label="状态" width="100">
          <template #default="scope">
            <el-tag size="small" :type="scope.row.access_status === 'success' ? 'success' : 'danger'">
              {{ scope.row.access_status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="temperature" label="体温" width="100">
          <template #default="scope">
            <span v-if="scope.row.temperature">{{ scope.row.temperature }}°C</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewDetail(scope.row)">
              详情
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

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="记录详情"
      width="600px"
    >
      <div v-if="currentRecord" class="record-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="记录ID">{{ currentRecord.id }}</el-descriptions-item>
          <el-descriptions-item label="时间">{{ currentRecord.record_time }}</el-descriptions-item>
          <el-descriptions-item label="设备">{{ currentRecord.device_name }}</el-descriptions-item>
          <el-descriptions-item label="位置">{{ currentRecord.location }}</el-descriptions-item>
          <el-descriptions-item label="用户">{{ currentRecord.nickname || '访客' }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ currentRecord.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="开门方式">{{ getAccessTypeText(currentRecord.access_type) }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ currentRecord.access_status === 'success' ? '成功' : '失败' }}</el-descriptions-item>
          <el-descriptions-item label="体温">{{ currentRecord.temperature || '-' }}</el-descriptions-item>
          <el-descriptions-item label="照片">
            <el-image
              v-if="currentRecord.photo_url"
              :src="currentRecord.photo_url"
              fit="cover"
              style="width: 200px; height: 150px"
            />
            <span v-else>-</span>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, ArrowLeft } from '@element-plus/icons-vue'

const records = ref([])
const devices = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})
const searchForm = ref({
  dateRange: null,
  deviceId: '',
  accessType: '',
  status: ''
})
const detailVisible = ref(false)
const currentRecord = ref(null)

// 加载门禁设备
const loadDevices = async () => {
  try {
    const response = await fetch('/api/v1/pc/access/devices', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      devices.value = result.data || []
    }
  } catch (error) {
    console.error('加载设备失败:', error)
  }
}

// 加载记录
const loadRecords = async () => {
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.currentPage)
    params.append('pageSize', pagination.value.pageSize)
    
    if (searchForm.value.deviceId) {
      params.append('device_id', searchForm.value.deviceId)
    }
    if (searchForm.value.accessType) {
      params.append('access_type', searchForm.value.accessType)
    }
    if (searchForm.value.status) {
      params.append('status', searchForm.value.status)
    }
    if (searchForm.value.dateRange) {
      params.append('start_date', searchForm.value.dateRange[0])
      params.append('end_date', searchForm.value.dateRange[1])
    }

    const response = await fetch(`/api/v1/pc/access/records?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      records.value = result.data?.list || []
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载记录失败:', error)
    ElMessage.error('加载记录失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadRecords()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadRecords()
}

const resetForm = () => {
  searchForm.value = {
    dateRange: null,
    deviceId: '',
    accessType: '',
    status: ''
  }
  loadRecords()
}

const viewDetail = (record) => {
  currentRecord.value = record
  detailVisible.value = true
}

const getAccessTypeText = (type) => {
  const map = {
    'face': '人脸识别',
    'fingerprint': '指纹',
    'card': '门禁卡',
    'qr_code': '二维码',
    'password': '密码',
    'remote': '远程'
  }
  return map[type] || type
}

const getAccessTypeType = (type) => {
  const map = {
    'face': 'success',
    'fingerprint': 'primary',
    'card': 'warning',
    'qr_code': 'info',
    'password': 'danger',
    'remote': 'success'
  }
  return map[type] || 'info'
}

onMounted(() => {
  loadDevices()
  loadRecords()
})
</script>

<style scoped>
.access-records {
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

.search-card,
.records-card {
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

.record-detail {
  padding: 20px 0;
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
  
  .search-form .el-form-item {
    margin-bottom: 10px;
  }
}
</style>
