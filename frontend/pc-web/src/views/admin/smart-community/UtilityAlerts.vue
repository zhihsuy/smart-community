<template>
  <AdminLayout>
    <div class="utility-alerts">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>异常预警处理</h3>
            <el-button type="primary" @click="exportAlerts">
              <el-icon><i-ep-download /></el-icon>
              导出预警
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="预警类型">
              <el-select v-model="searchForm.alert_type" placeholder="选择预警类型">
                <el-option label="用量异常" value="usage_abnormal" />
                <el-option label="设备故障" value="device_fault" />
                <el-option label="表具离线" value="device_offline" />
                <el-option label="其他异常" value="other" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="未处理" value="pending" />
                <el-option label="处理中" value="processing" />
                <el-option label="已处理" value="processed" />
                <el-option label="已忽略" value="ignored" />
              </el-select>
            </el-form-item>
            <el-form-item label="表具类型">
              <el-select v-model="searchForm.meter_type" placeholder="选择表具类型">
                <el-option label="电表" value="electric" />
                <el-option label="水表" value="water" />
                <el-option label="燃气表" value="gas" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchAlerts">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="alerts" style="width: 100%">
          <el-table-column prop="id" label="预警ID" width="80" />
          <el-table-column prop="alert_type" label="预警类型" width="120">
            <template #default="scope">
              <el-tag :type="getAlertTypeTag(scope.row.alert_type)">
                {{ getAlertTypeText(scope.row.alert_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="meter_code" label="表具编号" width="150" />
          <el-table-column prop="meter_type" label="表具类型" width="100">
            <template #default="scope">
              <el-tag :type="getMeterTypeTag(scope.row.meter_type)">
                {{ getMeterTypeText(scope.row.meter_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="building_name" label="所属楼栋" />
          <el-table-column prop="unit" label="单元" width="80" />
          <el-table-column prop="room_number" label="房间号" width="100" />
          <el-table-column prop="alert_message" label="预警信息" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column prop="processed_at" label="处理时间" width="180" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewAlert(scope.row)">
                <el-icon><i-ep-view /></el-icon>
                查看
              </el-button>
              <el-button size="small" @click="processAlert(scope.row)" v-if="scope.row.status === 'pending'">
                <el-icon><i-ep-setting /></el-icon>
                处理
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
        
        <!-- 统计信息 -->
        <div class="statistics-card mt-4">
          <h4>预警统计</h4>
          <div class="statistics-grid">
            <div class="stat-item">
              <div class="stat-value">{{ totalAlerts }}</div>
              <div class="stat-label">总预警数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ pendingAlerts }}</div>
              <div class="stat-label">未处理</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ processingAlerts }}</div>
              <div class="stat-label">处理中</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ processedAlerts }}</div>
              <div class="stat-label">已处理</div>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- 预警详情对话框 -->
      <el-dialog
        v-model="alertDialogVisible"
        title="预警详情"
        width="600px"
      >
        <div v-if="currentAlert" class="alert-detail">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="预警ID">{{ currentAlert.id }}</el-descriptions-item>
            <el-descriptions-item label="预警类型">
              <el-tag :type="getAlertTypeTag(currentAlert.alert_type)">{{ getAlertTypeText(currentAlert.alert_type) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="表具编号">{{ currentAlert.meter_code }}</el-descriptions-item>
            <el-descriptions-item label="表具类型">{{ getMeterTypeText(currentAlert.meter_type) }}</el-descriptions-item>
            <el-descriptions-item label="所属楼栋">{{ currentAlert.building_name }}</el-descriptions-item>
            <el-descriptions-item label="房间号">{{ currentAlert.unit }}-{{ currentAlert.room_number }}</el-descriptions-item>
            <el-descriptions-item label="预警信息" :span="2">{{ currentAlert.alert_message }}</el-descriptions-item>
            <el-descriptions-item label="预警时间">{{ currentAlert.created_at }}</el-descriptions-item>
            <el-descriptions-item label="状态">{{ getStatusText(currentAlert.status) }}</el-descriptions-item>
            <el-descriptions-item label="处理时间">{{ currentAlert.processed_at || '未处理' }}</el-descriptions-item>
            <el-descriptions-item label="处理人">{{ currentAlert.processor || '未处理' }}</el-descriptions-item>
            <el-descriptions-item label="处理结果" :span="2">{{ currentAlert.process_result || '未处理' }}</el-descriptions-item>
          </el-descriptions>
          
          <div class="alert-actions mt-4" v-if="currentAlert.status === 'pending'">
            <el-form :model="processForm" :rules="processRules" ref="processFormRef" label-width="100px">
              <el-form-item label="处理结果" prop="process_result">
                <el-input
                  v-model="processForm.process_result"
                  type="textarea"
                  placeholder="请输入处理结果"
                  rows="3"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveProcess">保存处理结果</el-button>
                <el-button @click="ignoreAlert">忽略预警</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="alertDialogVisible = false">关闭</el-button>
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

const alerts = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  alert_type: '',
  status: '',
  meter_type: ''
})
const alertDialogVisible = ref(false)
const currentAlert = ref(null)
const processForm = ref({
  process_result: ''
})
const processRules = ref({
  process_result: [{ required: true, message: '请输入处理结果', trigger: 'blur' }]
})
const processFormRef = ref(null)

// 统计数据
const totalAlerts = computed(() => total.value)
const pendingAlerts = computed(() => alerts.value.filter(a => a.status === 'pending').length)
const processingAlerts = computed(() => alerts.value.filter(a => a.status === 'processing').length)
const processedAlerts = computed(() => alerts.value.filter(a => a.status === 'processed').length)

// 获取预警类型文本
const getAlertTypeText = (type) => {
  const types = {
    'usage_abnormal': '用量异常',
    'device_fault': '设备故障',
    'device_offline': '表具离线',
    'other': '其他异常'
  }
  return types[type] || type
}

// 获取预警类型标签样式
const getAlertTypeTag = (type) => {
  const tags = {
    'usage_abnormal': 'warning',
    'device_fault': 'danger',
    'device_offline': 'info',
    'other': 'default'
  }
  return tags[type] || 'default'
}

// 获取表具类型文本
const getMeterTypeText = (type) => {
  const types = {
    'electric': '电表',
    'water': '水表',
    'gas': '燃气表'
  }
  return types[type] || type
}

// 获取表具类型标签样式
const getMeterTypeTag = (type) => {
  const tags = {
    'electric': 'primary',
    'water': 'success',
    'gas': 'warning'
  }
  return tags[type] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const statuses = {
    'pending': '未处理',
    'processing': '处理中',
    'processed': '已处理',
    'ignored': '已忽略'
  }
  return statuses[status] || status
}

// 获取状态标签样式
const getStatusTag = (status) => {
  const tags = {
    'pending': 'danger',
    'processing': 'warning',
    'processed': 'success',
    'ignored': 'info'
  }
  return tags[status] || 'default'
}

// 加载预警列表
const loadAlerts = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.alert_type) params.append('alert_type', searchForm.value.alert_type)
    if (searchForm.value.status) params.append('status', searchForm.value.status)
    if (searchForm.value.meter_type) params.append('meter_type', searchForm.value.meter_type)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`/api/v1/admin/utility/alerts?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      alerts.value = result.data.list
      total.value = result.data.total
    }
  } catch (error) {
    console.error('加载预警列表失败:', error)
    ElMessage.error('加载预警列表失败')
  }
}

// 搜索预警
const searchAlerts = () => {
  page.value = 1
  loadAlerts()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    alert_type: '',
    status: '',
    meter_type: ''
  }
  page.value = 1
  loadAlerts()
}

// 查看预警
const viewAlert = (alert) => {
  currentAlert.value = alert
  processForm.value = {
    process_result: ''
  }
  alertDialogVisible.value = true
}

// 处理预警
const processAlert = (alert) => {
  currentAlert.value = alert
  processForm.value = {
    process_result: ''
  }
  alertDialogVisible.value = true
}

// 保存处理结果
const saveProcess = async () => {
  if (!processFormRef.value) return
  
  try {
    await processFormRef.value.validate()
    
    const response = await fetch(`/api/v1/admin/utility/alerts/${currentAlert.value.id}/process`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        process_result: processForm.value.process_result,
        status: 'processed'
      })
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('处理成功')
      alertDialogVisible.value = false
      loadAlerts()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存处理结果失败:', error)
    ElMessage.error('保存处理结果失败')
  }
}

// 忽略预警
const ignoreAlert = async () => {
  try {
    const response = await fetch(`/api/v1/admin/utility/alerts/${currentAlert.value.id}/ignore`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('已忽略预警')
      alertDialogVisible.value = false
      loadAlerts()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('忽略预警失败:', error)
    ElMessage.error('忽略预警失败')
  }
}

// 导出预警
const exportAlerts = () => {
  ElMessage.info('导出功能开发中')
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadAlerts()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadAlerts()
}

onMounted(() => {
  loadAlerts()
})
</script>

<style scoped>
.utility-alerts {
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

.alert-detail {
  padding: 20px 0;
}

.alert-actions {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.mt-4 {
  margin-top: 20px;
}
</style>