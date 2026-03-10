<template>
  <AdminLayout>
    <div class="repair-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>报修管理</h3>
          </div>
        </template>
        
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="工单管理" name="orders">
            <div class="mb-4">
              <el-button type="primary" @click="openOrderDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增工单
              </el-button>
            </div>
            
            <div class="search-filter mb-4">
              <el-form :inline="true" :model="orderSearchForm" class="mb-4">
                <el-form-item label="状态">
                  <el-select v-model="orderSearchForm.status" placeholder="选择状态">
                    <el-option label="全部" value="" />
                    <el-option label="待处理" value="pending" />
                    <el-option label="处理中" value="processing" />
                    <el-option label="已完成" value="completed" />
                    <el-option label="已取消" value="cancelled" />
                  </el-select>
                </el-form-item>
                <el-form-item label="类型">
                  <el-select v-model="orderSearchForm.type" placeholder="选择类型">
                    <el-option label="全部" value="" />
                    <el-option label="水电维修" value="water_elec" />
                    <el-option label="物业维修" value="property" />
                    <el-option label="其他" value="other" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="searchOrders">查询</el-button>
                  <el-button @click="resetOrderSearch">重置</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <el-table :data="orders" style="width: 100%">
              <el-table-column prop="id" label="工单ID" width="80" />
              <el-table-column prop="title" label="报修标题" />
              <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                  <el-tag :type="getTypeTag(scope.row.type)">
                    {{ getTypeText(scope.row.type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="address" label="报修地址" />
              <el-table-column prop="priority" label="优先级" width="100">
                <template #default="scope">
                  <el-tag :type="getPriorityTag(scope.row.priority)">
                    {{ getPriorityText(scope.row.priority) }}
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
              <el-table-column prop="created_at" label="创建时间" width="180" />
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="viewOrder(scope.row)">
                    <el-icon><i-ep-view /></el-icon>
                    查看
                  </el-button>
                  <el-button size="small" type="primary" @click="assignTechnician(scope.row)" v-if="scope.row.status === 'pending'">
                    <el-icon><i-ep-user /></el-icon>
                    指派
                  </el-button>
                  <el-button size="small" type="success" @click="completeOrder(scope.row)" v-if="scope.row.status === 'processing'">
                    <el-icon><i-ep-check /></el-icon>
                    完成
                  </el-button>
                  <el-button size="small" type="danger" @click="cancelOrder(scope.row)" v-if="scope.row.status === 'pending'">
                    <el-icon><i-ep-close /></el-icon>
                    取消
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination" v-if="orderTotal > 0">
              <el-pagination
                v-model:current-page="orderPage"
                v-model:page-size="orderPageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="orderTotal"
                @size-change="handleOrderSizeChange"
                @current-change="handleOrderCurrentChange"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="维修人员" name="technicians">
            <div class="mb-4">
              <el-button type="primary" @click="openTechnicianDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增维修人员
              </el-button>
            </div>
            
            <el-table :data="technicians" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="姓名" />
              <el-table-column prop="phone" label="联系电话" />
              <el-table-column prop="specialty" label="专业领域" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                    {{ scope.row.status === 'active' ? '正常' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="editTechnician(scope.row)">
                    <el-icon><i-ep-edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteTechnician(scope.row.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination" v-if="technicianTotal > 0">
              <el-pagination
                v-model:current-page="technicianPage"
                v-model:page-size="technicianPageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="technicianTotal"
                @size-change="handleTechnicianSizeChange"
                @current-change="handleTechnicianCurrentChange"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="维修统计" name="statistics">
            <el-row :gutter="20" class="mb-4">
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #409EFF">
                      <el-icon><i-ep-document /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总工单数</div>
                      <div class="stat-value">{{ statistics.orders.total }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #E6A23C">
                      <el-icon><i-ep-clock /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">待处理</div>
                      <div class="stat-value">{{ statistics.orders.pending }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #67C23A">
                      <el-icon><i-ep-circle-check /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">已完成</div>
                      <div class="stat-value">{{ statistics.orders.completed }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #909399">
                      <el-icon><i-ep-user /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">维修人员</div>
                      <div class="stat-value">{{ statistics.technicians.total }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </el-tab-pane>
        </el-tabs>
      </el-card>
      
      <el-dialog
        v-model="orderDialogVisible"
        :title="orderDialogTitle"
        width="600px"
      >
        <el-form :model="orderForm" :rules="orderRules" ref="orderFormRef" label-width="100px" status-icon>
          <el-form-item label="报修标题" prop="title">
            <el-input v-model="orderForm.title" placeholder="请输入报修标题" />
          </el-form-item>
          <el-form-item label="报修类型" prop="type">
            <el-select v-model="orderForm.type" placeholder="选择报修类型">
              <el-option label="水电维修" value="water_elec" />
              <el-option label="物业维修" value="property" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="问题描述" prop="description">
            <el-input v-model="orderForm.description" type="textarea" :rows="4" placeholder="请输入问题描述" />
          </el-form-item>
          <el-form-item label="报修地址" prop="address">
            <el-input v-model="orderForm.address" placeholder="请输入报修地址" />
          </el-form-item>
          <el-form-item label="优先级" prop="priority">
            <el-select v-model="orderForm.priority" placeholder="选择优先级">
              <el-option label="低" value="low" />
              <el-option label="中" value="medium" />
              <el-option label="高" value="high" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="orderDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveOrder">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="technicianDialogVisible"
        :title="technicianDialogTitle"
        width="500px"
      >
        <el-form :model="technicianForm" :rules="technicianRules" ref="technicianFormRef" label-width="100px" status-icon>
          <el-form-item label="姓名" prop="name">
            <el-input v-model="technicianForm.name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="technicianForm.phone" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="专业领域" prop="specialty">
            <el-input v-model="technicianForm.specialty" placeholder="请输入专业领域" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="technicianForm.status" placeholder="选择状态">
              <el-option label="正常" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="technicianDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveTechnician">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="assignDialogVisible"
        title="指派维修人员"
        width="500px"
      >
        <el-form :model="assignForm" ref="assignFormRef" label-width="100px" status-icon>
          <el-form-item label="维修人员" prop="technician_id">
            <el-select v-model="assignForm.technician_id" placeholder="选择维修人员">
              <el-option 
                v-for="tech in technicians" 
                :key="tech.id" 
                :label="tech.name" 
                :value="tech.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="预计完成时间" prop="estimated_time">
            <el-date-picker
              v-model="assignForm.estimated_time"
              type="datetime"
              placeholder="选择预计完成时间"
              style="width: 100%"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="assignDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmAssign">确认指派</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="completeDialogVisible"
        title="完成维修"
        width="500px"
      >
        <el-form :model="completeForm" ref="completeFormRef" label-width="100px" status-icon>
          <el-form-item label="处理结果" prop="process_result">
            <el-input v-model="completeForm.process_result" type="textarea" :rows="4" placeholder="请输入处理结果" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="completeDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmComplete">确认完成</el-button>
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

const activeTab = ref('orders')
const orders = ref([])
const technicians = ref([])
const statistics = ref({
  orders: {
    total: 0,
    pending: 0,
    processing: 0,
    completed: 0,
    cancelled: 0
  },
  technicians: {
    total: 0
  }
})

const orderPage = ref(1)
const orderPageSize = ref(20)
const orderTotal = ref(0)

const technicianPage = ref(1)
const technicianPageSize = ref(20)
const technicianTotal = ref(0)

const orderSearchForm = ref({
  status: '',
  type: ''
})

const orderDialogVisible = ref(false)
const orderDialogTitle = ref('新增工单')
const orderForm = ref({
  title: '',
  type: 'water_elec',
  description: '',
  address: '',
  priority: 'medium'
})

const technicianDialogVisible = ref(false)
const technicianDialogTitle = ref('新增维修人员')
const technicianForm = ref({
  name: '',
  phone: '',
  specialty: '',
  status: 'active'
})

const assignDialogVisible = ref(false)
const assignForm = ref({
  order_id: null,
  technician_id: null,
  estimated_time: null
})

const completeDialogVisible = ref(false)
const completeForm = ref({
  order_id: null,
  process_result: ''
})

const orderRules = {
  title: [{ required: true, message: '请输入报修标题', trigger: 'blur' }],
  type: [{ required: true, message: '请选择报修类型', trigger: 'change' }],
  description: [{ required: true, message: '请输入问题描述', trigger: 'blur' }],
  address: [{ required: true, message: '请输入报修地址', trigger: 'blur' }]
}

const technicianRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
}

const handleTabChange = (tab) => {
  if (tab === 'orders') {
    loadOrders()
  } else if (tab === 'technicians') {
    loadTechnicians()
  } else if (tab === 'statistics') {
    loadStatistics()
  }
}

const loadOrders = async () => {
  try {
    const response = await axios.get('/api/v1/pc/repair/orders', {
      params: {
        page: orderPage.value,
        pageSize: orderPageSize.value,
        ...orderSearchForm.value
      }
    })
    orders.value = response.data.data.list
    orderTotal.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载工单列表失败')
  }
}

const loadTechnicians = async () => {
  try {
    const response = await axios.get('/api/v1/pc/repair/technicians', {
      params: {
        page: technicianPage.value,
        pageSize: technicianPageSize.value
      }
    })
    technicians.value = response.data.data.list
    technicianTotal.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载维修人员列表失败')
  }
}

const loadStatistics = async () => {
  try {
    const response = await axios.get('/api/v1/pc/repair/statistics')
    statistics.value = response.data.data
  } catch (error) {
    ElMessage.error('加载维修统计失败')
  }
}

const openOrderDialog = () => {
  orderDialogTitle.value = '新增工单'
  orderForm.value = {
    title: '',
    type: 'water_elec',
    description: '',
    address: '',
    priority: 'medium'
  }
  orderDialogVisible.value = true
}

const saveOrder = async () => {
  try {
    await axios.post('/api/v1/pc/repair/orders', orderForm.value)
    ElMessage.success('新增工单成功')
    orderDialogVisible.value = false
    loadOrders()
  } catch (error) {
    ElMessage.error('保存工单失败')
  }
}

const viewOrder = (order) => {
  ElMessageBox.alert(
    `<div>
      <p><strong>报修标题：</strong>${order.title}</p>
      <p><strong>报修类型：</strong>${getTypeText(order.type)}</p>
      <p><strong>问题描述：</strong>${order.description}</p>
      <p><strong>报修地址：</strong>${order.address}</p>
      <p><strong>优先级：</strong>${getPriorityText(order.priority)}</p>
      <p><strong>状态：</strong>${getStatusText(order.status)}</p>
      <p><strong>创建时间：</strong>${order.created_at}</p>
    </div>`,
    '工单详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭'
    }
  )
}

const assignTechnician = (order) => {
  assignForm.value = {
    order_id: order.id,
    technician_id: null,
    estimated_time: null
  }
  assignDialogVisible.value = true
}

const confirmAssign = async () => {
  try {
    await axios.post(`/api/v1/pc/repair/orders/${assignForm.value.order_id}/assign`, assignForm.value)
    ElMessage.success('指派成功')
    assignDialogVisible.value = false
    loadOrders()
  } catch (error) {
    ElMessage.error('指派失败')
  }
}

const completeOrder = (order) => {
  completeForm.value = {
    order_id: order.id,
    process_result: ''
  }
  completeDialogVisible.value = true
}

const confirmComplete = async () => {
  try {
    await axios.post(`/api/v1/pc/repair/orders/${completeForm.value.order_id}/complete`, completeForm.value)
    ElMessage.success('工单已完成')
    completeDialogVisible.value = false
    loadOrders()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const cancelOrder = async (order) => {
  try {
    await axios.post(`/api/v1/pc/repair/orders/${order.id}/cancel`)
    ElMessage.success('工单已取消')
    loadOrders()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const openTechnicianDialog = () => {
  technicianDialogTitle.value = '新增维修人员'
  technicianForm.value = {
    name: '',
    phone: '',
    specialty: '',
    status: 'active'
  }
  technicianDialogVisible.value = true
}

const editTechnician = (technician) => {
  technicianDialogTitle.value = '编辑维修人员'
  technicianForm.value = { ...technician }
  technicianDialogVisible.value = true
}

const saveTechnician = async () => {
  try {
    if (technicianDialogTitle.value === '新增维修人员') {
      await axios.post('/api/v1/pc/repair/technicians', technicianForm.value)
      ElMessage.success('新增维修人员成功')
    } else {
      await axios.put(`/api/v1/pc/repair/technicians/${technicianForm.value.id}`, technicianForm.value)
      ElMessage.success('更新维修人员成功')
    }
    technicianDialogVisible.value = false
    loadTechnicians()
  } catch (error) {
    ElMessage.error('保存维修人员失败')
  }
}

const deleteTechnician = async (id) => {
  try {
    await axios.delete(`/api/v1/pc/repair/technicians/${id}`)
    ElMessage.success('删除维修人员成功')
    loadTechnicians()
  } catch (error) {
    ElMessage.error('删除维修人员失败')
  }
}

const searchOrders = () => {
  orderPage.value = 1
  loadOrders()
}

const resetOrderSearch = () => {
  orderSearchForm.value = {
    status: '',
    type: ''
  }
  orderPage.value = 1
  loadOrders()
}

const handleOrderSizeChange = (size) => {
  orderPageSize.value = size
  loadOrders()
}

const handleOrderCurrentChange = (page) => {
  orderPage.value = page
  loadOrders()
}

const handleTechnicianSizeChange = (size) => {
  technicianPageSize.value = size
  loadTechnicians()
}

const handleTechnicianCurrentChange = (page) => {
  technicianPage.value = page
  loadTechnicians()
}

const getTypeTag = (type) => {
  const typeMap = {
    'water_elec': 'primary',
    'property': 'success',
    'other': 'info'
  }
  return typeMap[type] || ''
}

const getTypeText = (type) => {
  const typeMap = {
    'water_elec': '水电维修',
    'property': '物业维修',
    'other': '其他'
  }
  return typeMap[type] || type
}

const getPriorityTag = (priority) => {
  const priorityMap = {
    'low': 'info',
    'medium': 'warning',
    'high': 'danger'
  }
  return priorityMap[priority] || ''
}

const getPriorityText = (priority) => {
  const priorityMap = {
    'low': '低',
    'medium': '中',
    'high': '高'
  }
  return priorityMap[priority] || priority
}

const getStatusTag = (status) => {
  const statusMap = {
    'pending': 'warning',
    'processing': 'primary',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return statusMap[status] || ''
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.repair-management {
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

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 30px;
  margin-right: 20px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}
</style>
