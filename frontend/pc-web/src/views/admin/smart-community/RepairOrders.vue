<template>
  <AdminLayout>
    <div class="repair-orders">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>报修工单管理</h3>
            <el-button type="primary" @click="exportOrders">
              <el-icon><i-ep-download /></el-icon>
              导出工单
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="工单状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="待处理" value="pending" />
                <el-option label="处理中" value="processing" />
                <el-option label="已完成" value="completed" />
                <el-option label="已取消" value="cancelled" />
              </el-select>
            </el-form-item>
            <el-form-item label="报修类型">
              <el-select v-model="searchForm.type" placeholder="选择类型">
                <el-option label="水电维修" value="water_elec" />
                <el-option label="物业维修" value="property" />
                <el-option label="其他维修" value="other" />
              </el-select>
            </el-form-item>
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
              <el-button type="primary" @click="searchOrders">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="orders" style="width: 100%">
          <el-table-column prop="id" label="工单ID" width="80" />
          <el-table-column label="用户信息" width="200">
            <template #default="scope">
              <div>{{ scope.row.nickname || '未知' }}</div>
              <div class="text-xs text-gray-500">{{ scope.row.phone || '未知' }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="报修标题" />
          <el-table-column prop="type" label="报修类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ getTypeText(scope.row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="工单状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
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
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column prop="updated_at" label="更新时间" width="180" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewOrder(scope.row)">
                <el-icon><i-ep-view /></el-icon>
                查看
              </el-button>
              <el-button size="small" @click="assignTechnician(scope.row)" v-if="scope.row.status === 'pending'">
                <el-icon><i-ep-setting /></el-icon>
                派单
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
          <h4>工单统计</h4>
          <div class="statistics-grid">
            <div class="stat-item">
              <div class="stat-value">{{ totalOrders }}</div>
              <div class="stat-label">总工单数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ pendingOrders }}</div>
              <div class="stat-label">待处理</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ processingOrders }}</div>
              <div class="stat-label">处理中</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ completedOrders }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- 工单详情对话框 -->
      <el-dialog
        v-model="orderDialogVisible"
        title="工单详情"
        width="700px"
      >
        <div v-if="currentOrder" class="order-detail">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="工单ID">{{ currentOrder.id }}</el-descriptions-item>
            <el-descriptions-item label="工单状态">
              <el-tag :type="getStatusTag(currentOrder.status)">{{ getStatusText(currentOrder.status) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="报修用户">{{ currentOrder.nickname || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ currentOrder.phone || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="报修标题">{{ currentOrder.title }}</el-descriptions-item>
            <el-descriptions-item label="报修类型">{{ getTypeText(currentOrder.type) }}</el-descriptions-item>
            <el-descriptions-item label="优先级">{{ getPriorityText(currentOrder.priority) }}</el-descriptions-item>
            <el-descriptions-item label="报修时间">{{ currentOrder.created_at }}</el-descriptions-item>
            <el-descriptions-item label="地址" :span="2">{{ currentOrder.address }}</el-descriptions-item>
            <el-descriptions-item label="问题描述" :span="2">{{ currentOrder.description }}</el-descriptions-item>
            <el-descriptions-item label="处理结果" :span="2">{{ currentOrder.process_result || '暂无' }}</el-descriptions-item>
          </el-descriptions>
          
          <div class="order-actions mt-4" v-if="currentOrder.status === 'pending'">
            <el-button type="primary" @click="assignTechnician(currentOrder)">指派维修人员</el-button>
            <el-button @click="cancelOrder(currentOrder.id)">取消工单</el-button>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="orderDialogVisible = false">关闭</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 指派维修人员对话框 -->
      <el-dialog
        v-model="assignDialogVisible"
        title="指派维修人员"
        width="500px"
      >
        <el-form :model="assignForm" :rules="assignRules" ref="assignFormRef" label-width="100px">
          <el-form-item label="工单ID">{{ currentOrder?.id }}</el-form-item>
          <el-form-item label="维修人员" prop="technician_id">
            <el-select v-model="assignForm.technician_id" placeholder="选择维修人员">
              <el-option 
                v-for="tech in technicians" 
                :key="tech.id" 
                :label="`${tech.name} (${tech.specialty})`" 
                :value="tech.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="预计完成时间">
            <el-date-picker
              v-model="assignForm.estimated_time"
              type="datetime"
              placeholder="选择预计完成时间"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="备注">
            <el-input
              v-model="assignForm.remark"
              type="textarea"
              placeholder="请输入备注信息"
              rows="3"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="assignDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveAssignment">保存</el-button>
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

const orders = ref([])
const users = ref([])
const technicians = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  status: '',
  type: '',
  user_id: '',
  start_date: '',
  end_date: ''
})
const orderDialogVisible = ref(false)
const assignDialogVisible = ref(false)
const currentOrder = ref(null)
const assignForm = ref({
  technician_id: '',
  estimated_time: new Date(),
  remark: ''
})
const assignRules = ref({
  technician_id: [{ required: true, message: '请选择维修人员', trigger: 'change' }]
})
const assignFormRef = ref(null)

// 统计数据
const totalOrders = computed(() => total.value)
const pendingOrders = computed(() => orders.value.filter(o => o.status === 'pending').length)
const processingOrders = computed(() => orders.value.filter(o => o.status === 'processing').length)
const completedOrders = computed(() => orders.value.filter(o => o.status === 'completed').length)

// 获取类型文本
const getTypeText = (type) => {
  const types = {
    'water_elec': '水电维修',
    'property': '物业维修',
    'other': '其他维修'
  }
  return types[type] || type
}

// 获取类型标签样式
const getTypeTag = (type) => {
  const tags = {
    'water_elec': 'primary',
    'property': 'success',
    'other': 'warning'
  }
  return tags[type] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const statuses = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statuses[status] || status
}

// 获取状态标签样式
const getStatusTag = (status) => {
  const tags = {
    'pending': 'warning',
    'processing': 'info',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return tags[status] || 'default'
}

// 获取优先级文本
const getPriorityText = (priority) => {
  const priorities = {
    'low': '低',
    'medium': '中',
    'high': '高'
  }
  return priorities[priority] || priority
}

// 获取优先级标签样式
const getPriorityTag = (priority) => {
  const tags = {
    'low': 'success',
    'medium': 'warning',
    'high': 'danger'
  }
  return tags[priority] || 'default'
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

// 加载维修人员列表
const loadTechnicians = async () => {
  try {
    const response = await fetch('http://localhost:8081/api/v1/admin/repair/technicians', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      technicians.value = result.data
    }
  } catch (error) {
    console.error('加载维修人员列表失败:', error)
  }
}

// 加载工单列表
const loadOrders = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.status) params.append('status', searchForm.value.status)
    if (searchForm.value.type) params.append('type', searchForm.value.type)
    if (searchForm.value.user_id) params.append('user_id', searchForm.value.user_id)
    if (searchForm.value.start_date) params.append('start_date', searchForm.value.start_date)
    if (searchForm.value.end_date) params.append('end_date', searchForm.value.end_date)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`http://localhost:8081/api/v1/admin/repair/orders?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      orders.value = result.data.list
      total.value = result.data.total
    }
  } catch (error) {
    console.error('加载工单列表失败:', error)
    ElMessage.error('加载工单列表失败')
  }
}

// 搜索工单
const searchOrders = () => {
  page.value = 1
  loadOrders()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    status: '',
    type: '',
    user_id: '',
    start_date: '',
    end_date: ''
  }
  page.value = 1
  loadOrders()
}

// 查看工单
const viewOrder = (order) => {
  currentOrder.value = order
  orderDialogVisible.value = true
}

// 指派维修人员
const assignTechnician = (order) => {
  currentOrder.value = order
  assignForm.value = {
    technician_id: '',
    estimated_time: new Date(),
    remark: ''
  }
  assignDialogVisible.value = true
}

// 保存指派
const saveAssignment = async () => {
  if (!assignFormRef.value) return
  
  try {
    await assignFormRef.value.validate()
    
    const response = await fetch(`http://localhost:8081/api/v1/admin/repair/orders/${currentOrder.value.id}/assign`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(assignForm.value)
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('指派成功')
      assignDialogVisible.value = false
      orderDialogVisible.value = false
      loadOrders()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存指派失败:', error)
    ElMessage.error('保存指派失败')
  }
}

// 取消工单
const cancelOrder = async (orderId) => {
  try {
    if (confirm('确定要取消该工单吗？')) {
      const response = await fetch(`http://localhost:8081/api/v1/admin/repair/orders/${orderId}/cancel`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('工单已取消')
        orderDialogVisible.value = false
        loadOrders()
      } else {
        ElMessage.error(result.msg || '操作失败')
      }
    }
  } catch (error) {
    console.error('取消工单失败:', error)
    ElMessage.error('取消工单失败')
  }
}

// 导出工单
const exportOrders = () => {
  ElMessage.info('导出功能开发中')
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadOrders()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadOrders()
}

onMounted(() => {
  loadUsers()
  loadTechnicians()
  loadOrders()
})
</script>

<style scoped>
.repair-orders {
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

.order-detail {
  padding: 20px 0;
}

.order-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.text-xs {
  font-size: 12px;
}

.text-gray-500 {
  color: #909399;
}

.mt-4 {
  margin-top: 20px;
}
</style>