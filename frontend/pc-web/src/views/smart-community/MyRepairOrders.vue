<template>
  <div class="my-repair-orders">
    <div class="page-header">
      <h1>🔧 我的报修</h1>
      <p class="subtitle">查看和管理我的报修工单</p>
    </div>

    <!-- 状态筛选 -->
    <div class="status-tabs">
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="全部" name="all">
          <span class="badge" v-if="tabCounts.all">{{ tabCounts.all }}</span>
        </el-tab-pane>
        <el-tab-pane label="待处理" name="pending">
          <span class="badge" v-if="tabCounts.pending">{{ tabCounts.pending }}</span>
        </el-tab-pane>
        <el-tab-pane label="处理中" name="processing">
          <span class="badge" v-if="tabCounts.processing">{{ tabCounts.processing }}</span>
        </el-tab-pane>
        <el-tab-pane label="已完成" name="completed">
          <span class="badge" v-if="tabCounts.completed">{{ tabCounts.completed }}</span>
        </el-tab-pane>
        <el-tab-pane label="已关闭" name="closed">
          <span class="badge" v-if="tabCounts.closed">{{ tabCounts.closed }}</span>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 工单列表 -->
    <el-card class="orders-card">
      <template #header>
        <div class="card-header">
          <span>我的工单</span>
          <el-button type="primary" @click="$router.push('/repair')">
            <el-icon><Plus /></el-icon>
            新提交
          </el-button>
        </div>
      </template>
      
      <el-table :data="orders" style="width: 100%">
        <el-table-column prop="order_no" label="工单编号" width="180" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="repair_type" label="类型" width="120">
          <template #default="scope">
            <el-tag size="small" :type="getRepairTypeColor(scope.row.repair_type)">
              {{ getRepairTypeText(scope.row.repair_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="urgency" label="紧急程度" width="120">
          <template #default="scope">
            <el-tag size="small" :type="getUrgencyColor(scope.row.urgency)">
              {{ getUrgencyText(scope.row.urgency) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag size="small" :type="getStatusColor(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewOrder(scope.row)">
              查看
            </el-button>
            <el-button 
              size="small" 
              type="success" 
              @click="handleEvaluation(scope.row)"
              v-if="scope.row.status === 'completed' && !scope.row.evaluation"
            >
              评价
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

    <!-- 工单详情对话框 -->
    <el-dialog
      v-model="orderDetailVisible"
      title="工单详情"
      width="600px"
    >
      <div v-if="currentOrder" class="order-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="工单编号">{{ currentOrder.order_no }}</el-descriptions-item>
          <el-descriptions-item label="标题">{{ currentOrder.title }}</el-descriptions-item>
          <el-descriptions-item label="类型">{{ getRepairTypeText(currentOrder.repair_type) }}</el-descriptions-item>
          <el-descriptions-item label="紧急程度">{{ getUrgencyText(currentOrder.urgency) }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusText(currentOrder.status) }}</el-descriptions-item>
          <el-descriptions-item label="描述">{{ currentOrder.description }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.contact_phone }}</el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ currentOrder.created_at }}</el-descriptions-item>
          <el-descriptions-item label="处理人员">{{ currentOrder.handler_name || '待分配' }}</el-descriptions-item>
          <el-descriptions-item label="预计完成时间">{{ currentOrder.estimated_time || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="实际完成时间">{{ currentOrder.completed_at || '未完成' }}</el-descriptions-item>
        </el-descriptions>

        <!-- 处理记录 -->
        <div class="process-records" style="margin-top: 20px">
          <h3>处理记录</h3>
          <el-timeline>
            <el-timeline-item
              v-for="(record, index) in currentOrder.process_records || []"
              :key="index"
              :timestamp="record.created_at"
            >
              <el-card>
                <h4>{{ record.operator_name || '系统' }}</h4>
                <p>{{ record.content }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-dialog>

    <!-- 评价对话框 -->
    <el-dialog
      v-model="evaluationVisible"
      title="服务评价"
      width="500px"
    >
      <div v-if="currentOrder" class="evaluation-form">
        <el-form :model="evaluationForm" label-width="80px">
          <el-form-item label="服务评分">
            <el-rate v-model="evaluationForm.rating" :max="5" show-score />
          </el-form-item>
          <el-form-item label="评价内容">
            <el-input 
              v-model="evaluationForm.content" 
              type="textarea" 
              :rows="4"
              placeholder="请输入您的评价..."
            />
          </el-form-item>
          <el-form-item label="是否推荐">
            <el-switch v-model="evaluationForm.recommend" />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="evaluationVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEvaluation">提交评价</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const activeTab = ref('all')
const orders = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})
const tabCounts = ref({
  all: 0,
  pending: 0,
  processing: 0,
  completed: 0,
  closed: 0
})
const orderDetailVisible = ref(false)
const evaluationVisible = ref(false)
const currentOrder = ref(null)
const evaluationForm = ref({
  rating: 5,
  content: '',
  recommend: true
})

// 加载工单
const loadOrders = async () => {
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.currentPage)
    params.append('pageSize', pagination.value.pageSize)
    if (activeTab.value !== 'all') {
      params.append('status', activeTab.value)
    }

    const response = await fetch(`/api/v1/pc/repair/my-orders?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      orders.value = result.data?.list || []
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载工单失败:', error)
    ElMessage.error('加载工单失败')
  }
}

// 加载统计
const loadStatistics = async () => {
  try {
    const response = await fetch('/api/v1/pc/repair/statistics', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      tabCounts.value = result.data || {}
    }
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

const handleTabClick = () => {
  loadOrders()
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadOrders()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadOrders()
}

const viewOrder = (order) => {
  currentOrder.value = order
  orderDetailVisible.value = true
}

const handleEvaluation = (order) => {
  currentOrder.value = order
  evaluationForm.value = {
    rating: 5,
    content: '',
    recommend: true
  }
  evaluationVisible.value = true
}

const submitEvaluation = async () => {
  if (!currentOrder.value) return
  
  try {
    const response = await fetch(`/api/v1/pc/repair/orders/${currentOrder.value.id}/evaluation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        rating: evaluationForm.value.rating,
        content: evaluationForm.value.content,
        recommend: evaluationForm.value.recommend
      })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('评价提交成功')
      evaluationVisible.value = false
      loadOrders()
    } else {
      ElMessage.error(result.msg || '评价失败')
    }
  } catch (error) {
    console.error('提交评价失败:', error)
    ElMessage.error('评价失败')
  }
}

const getRepairTypeText = (type) => {
  const map = {
    'water': '水暖',
    'electric': '电路',
    'gas': '燃气',
    'door': '门窗',
    'elevator': '电梯',
    'cleaning': '保洁',
    'other': '其他'
  }
  return map[type] || type
}

const getRepairTypeColor = (type) => {
  const map = {
    'water': 'primary',
    'electric': 'danger',
    'gas': 'warning',
    'door': 'info',
    'elevator': 'success',
    'cleaning': 'purple',
    'other': 'info'
  }
  return map[type] || 'info'
}

const getUrgencyText = (level) => {
  const map = {
    'low': '一般',
    'normal': '普通',
    'high': '紧急',
    'urgent': '非常紧急'
  }
  return map[level] || level
}

const getUrgencyColor = (level) => {
  const map = {
    'low': 'info',
    'normal': 'primary',
    'high': 'warning',
    'urgent': 'danger'
  }
  return map[level] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'closed': '已关闭',
    'cancelled': '已取消'
  }
  return map[status] || status
}

const getStatusColor = (status) => {
  const map = {
    'pending': 'info',
    'processing': 'warning',
    'completed': 'success',
    'closed': 'danger',
    'cancelled': 'danger'
  }
  return map[status] || 'info'
}

onMounted(() => {
  loadOrders()
  loadStatistics()
})
</script>

<style scoped>
.my-repair-orders {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
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

.status-tabs {
  margin-bottom: 20px;
}

.badge {
  margin-left: 8px;
  background: #409EFF;
  color: white;
  border-radius: 10px;
  padding: 0 8px;
  font-size: 12px;
}

.orders-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

.order-detail {
  padding: 20px 0;
}

.process-records {
  margin-top: 20px;
}

.process-records h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #303133;
}

.evaluation-form {
  padding: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
