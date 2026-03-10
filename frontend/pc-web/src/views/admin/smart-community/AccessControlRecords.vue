<template>
  <AdminLayout>
    <div class="access-control-records">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>进出记录查询</h3>
            <el-button type="primary" @click="exportRecords">
              <el-icon><i-ep-download /></el-icon>
              导出记录
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="用户">
              <el-select v-model="searchForm.user_id" placeholder="选择用户">
                <el-option 
                  v-for="user in users" 
                  :key="user.id" 
                  :label="`${user.nickname} (${user.phone})`" 
                  :value="user.id" 
                />
              </el-select>
            </el-form-item>
            <el-form-item label="设备">
              <el-select v-model="searchForm.device_id" placeholder="选择设备">
                <el-option 
                  v-for="device in devices" 
                  :key="device.id" 
                  :label="`${device.device_name} (${device.device_code})`" 
                  :value="device.id" 
                />
              </el-select>
            </el-form-item>
            <el-form-item label="开始日期">
              <el-date-picker
                v-model="searchForm.start_date"
                type="date"
                placeholder="选择开始日期"
                style="width: 150px"
              />
            </el-form-item>
            <el-form-item label="结束日期">
              <el-date-picker
                v-model="searchForm.end_date"
                type="date"
                placeholder="选择结束日期"
                style="width: 150px"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchRecords">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="records" style="width: 100%">
          <el-table-column prop="id" label="记录ID" width="80" />
          <el-table-column label="用户信息" width="200">
            <template #default="scope">
              <div>{{ scope.row.nickname || '未知' }}</div>
              <div class="text-xs text-gray-500">{{ scope.row.phone || '未知' }}</div>
            </template>
          </el-table-column>
          <el-table-column label="设备信息" width="200">
            <template #default="scope">
              <div>{{ scope.row.device_name || '未知' }}</div>
              <div class="text-xs text-gray-500">{{ scope.row.location || '未知' }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="access_type" label="访问类型" width="120">
            <template #default="scope">
              <el-tag :type="getAccessTypeTag(scope.row.access_type)">
                {{ getAccessTypeText(scope.row.access_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="access_status" label="访问状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.access_status)">
                {{ getStatusText(scope.row.access_status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="record_time" label="记录时间" width="180" />
          <el-table-column prop="remark" label="备注" />
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
        
        <!-- 统计信息 -->
        <div class="statistics-card mt-4">
          <h4>统计信息</h4>
          <div class="statistics-grid">
            <div class="stat-item">
              <div class="stat-value">{{ totalRecords }}</div>
              <div class="stat-label">总记录数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ successRecords }}</div>
              <div class="stat-label">成功次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ failedRecords }}</div>
              <div class="stat-label">失败次数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ successRate }}%</div>
              <div class="stat-label">成功率</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import AdminLayout from '@/components/AdminLayout.vue'
import { ElMessage } from 'element-plus'

const records = ref([])
const users = ref([])
const devices = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  user_id: '',
  device_id: '',
  start_date: '',
  end_date: ''
})

// 统计数据
const totalRecords = computed(() => total.value)
const successRecords = computed(() => records.value.filter(r => r.access_status === 'success').length)
const failedRecords = computed(() => records.value.filter(r => r.access_status === 'failed').length)
const successRate = computed(() => {
  if (totalRecords.value === 0) return 0
  return Math.round((successRecords.value / totalRecords.value) * 100)
})

// 获取访问类型文本
const getAccessTypeText = (type) => {
  const types = {
    'face': '人脸识别',
    'password': '密码',
    'card': '刷卡',
    'qrcode': '二维码',
    'remote': '远程开门'
  }
  return types[type] || type
}

// 获取访问类型标签样式
const getAccessTypeTag = (type) => {
  const tags = {
    'face': 'primary',
    'password': 'success',
    'card': 'warning',
    'qrcode': 'info',
    'remote': 'danger'
  }
  return tags[type] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const statuses = {
    'success': '成功',
    'failed': '失败'
  }
  return statuses[status] || status
}

// 获取状态标签样式
const getStatusTag = (status) => {
  const tags = {
    'success': 'success',
    'failed': 'danger'
  }
  return tags[status] || 'default'
}

// 加载用户列表
const loadUsers = async () => {
  try {
    const response = await fetch('http://localhost:8081/api/v1/admin/users?page=1&pageSize=100', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      users.value = result.data.list
    }
  } catch (error) {
    console.error('加载用户列表失败:', error)
  }
}

// 加载设备列表
const loadDevices = async () => {
  try {
    const response = await fetch('http://localhost:8081/api/v1/pc/access/devices', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      devices.value = result.data
    }
  } catch (error) {
    console.error('加载设备列表失败:', error)
  }
}

// 加载记录列表
const loadRecords = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.user_id) params.append('user_id', searchForm.value.user_id)
    if (searchForm.value.device_id) params.append('device_id', searchForm.value.device_id)
    if (searchForm.value.start_date) params.append('start_date', searchForm.value.start_date)
    if (searchForm.value.end_date) params.append('end_date', searchForm.value.end_date)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`http://localhost:8081/api/v1/pc/access/records?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      records.value = result.data.list
      total.value = result.data.total
    }
  } catch (error) {
    console.error('加载记录列表失败:', error)
    ElMessage.error('加载记录列表失败，请检查网络连接或服务是否运行')
  }
}

// 搜索记录
const searchRecords = () => {
  page.value = 1
  loadRecords()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    user_id: '',
    device_id: '',
    start_date: '',
    end_date: ''
  }
  page.value = 1
  loadRecords()
}

// 导出记录
const exportRecords = () => {
  ElMessage.info('导出功能开发中')
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadRecords()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadRecords()
}

onMounted(() => {
  loadUsers()
  loadDevices()
  loadRecords()
})
</script>

<style scoped>
.access-control-records {
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

.statistics-card {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
}

.statistics-card h4 {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.text-xs {
  font-size: 12px;
}

.text-gray-500 {
  color: #909399;
}
</style>