<template>
  <div class="my-bills-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📋 账单明细</h1>
      <p class="subtitle">查看所有历史账单和缴费记录</p>
    </div>

    <!-- 搜索筛选 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="账单类型">
          <el-select v-model="searchForm.billType" placeholder="选择类型">
            <el-option label="全部" value="" />
            <el-option label="水费" value="water" />
            <el-option label="电费" value="electric" />
            <el-option label="物业费" value="property" />
            <el-option label="停车费" value="parking" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="选择状态">
            <el-option label="全部" value="" />
            <el-option label="待支付" value="unpaid" />
            <el-option label="已支付" value="paid" />
            <el-option label="已逾期" value="overdue" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 280px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadBills">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 账单列表 -->
    <el-card class="bills-card">
      <template #header>
        <div class="card-header">
          <span>账单列表</span>
          <span class="total-count">共 {{ pagination.total }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="bills" style="width: 100%">
        <el-table-column prop="bill_no" label="账单编号" width="180" />
        <el-table-column prop="bill_type" label="账单类型" width="120" />
        <el-table-column prop="amount" label="金额" width="100">
          <template #default="scope">
            ¥{{ scope.row.amount }}
          </template>
        </el-table-column>
        <el-table-column prop="period" label="账单周期" width="150" />
        <el-table-column prop="due_date" label="截止日期" width="150" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag size="small" :type="getStatusColor(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="payment_time" label="支付时间" width="180">
          <template #default="scope">
            <span v-if="scope.row.payment_time">{{ scope.row.payment_time }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" type="primary" @click="viewBill(scope.row)">
              查看
            </el-button>
            <el-button 
              size="small" 
              type="success" 
              @click="payBill(scope.row)"
              v-if="scope.row.status === 'unpaid'"
            >
              支付
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

    <!-- 账单详情对话框 -->
    <el-dialog
      v-model="billDetailVisible"
      title="账单详情"
      width="600px"
    >
      <div v-if="currentBill" class="bill-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="账单编号">{{ currentBill.bill_no }}</el-descriptions-item>
          <el-descriptions-item label="账单类型">{{ currentBill.bill_type }}</el-descriptions-item>
          <el-descriptions-item label="账单金额">¥{{ currentBill.amount }}</el-descriptions-item>
          <el-descriptions-item label="账单周期">{{ currentBill.period }}</el-descriptions-item>
          <el-descriptions-item label="生成日期">{{ currentBill.created_at }}</el-descriptions-item>
          <el-descriptions-item label="截止日期">{{ currentBill.due_date }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusText(currentBill.status) }}</el-descriptions-item>
          <el-descriptions-item label="支付时间">{{ currentBill.payment_time || '-' }}</el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ currentBill.payment_method || '-' }}</el-descriptions-item>
          <el-descriptions-item label="支付流水">{{ currentBill.payment_transaction || '-' }}</el-descriptions-item>
        </el-descriptions>

        <!-- 费用明细 -->
        <div class="bill-items" style="margin-top: 20px">
          <h3>费用明细</h3>
          <el-table :data="currentBill.items || []" style="width: 100%">
            <el-table-column prop="item_name" label="项目" />
            <el-table-column prop="quantity" label="数量" width="100" />
            <el-table-column prop="unit_price" label="单价" width="100">
              <template #default="scope">
                ¥{{ scope.row.unit_price }}
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="金额" width="100">
              <template #default="scope">
                ¥{{ scope.row.amount }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>

    <!-- 支付对话框 -->
    <el-dialog
      v-model="payDialogVisible"
      title="支付账单"
      width="500px"
    >
      <div v-if="currentBill" class="pay-form">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="账单类型">{{ currentBill.bill_type }}</el-descriptions-item>
          <el-descriptions-item label="账单金额">¥{{ currentBill.amount }}</el-descriptions-item>
          <el-descriptions-item label="账单周期">{{ currentBill.period }}</el-descriptions-item>
          <el-descriptions-item label="截止日期">{{ currentBill.due_date }}</el-descriptions-item>
          <el-descriptions-item label="支付方式">
            <el-radio-group v-model="paymentMethod">
              <el-radio label="balance">账户余额</el-radio>
              <el-radio label="wechat">微信支付</el-radio>
              <el-radio label="alipay">支付宝</el-radio>
            </el-radio-group>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="payDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmPayment" :loading="paying">
            确认支付
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Search } from '@element-plus/icons-vue'

const bills = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})
const searchForm = ref({
  billType: '',
  status: '',
  dateRange: null
})
const billDetailVisible = ref(false)
const payDialogVisible = ref(false)
const currentBill = ref(null)
const paymentMethod = ref('balance')
const paying = ref(false)

// 加载账单
const loadBills = async () => {
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.currentPage)
    params.append('pageSize', pagination.value.pageSize)
    
    if (searchForm.value.billType) {
      params.append('bill_type', searchForm.value.billType)
    }
    if (searchForm.value.status) {
      params.append('status', searchForm.value.status)
    }
    if (searchForm.value.dateRange) {
      params.append('start_date', searchForm.value.dateRange[0])
      params.append('end_date', searchForm.value.dateRange[1])
    }

    const response = await fetch(`/api/v1/pc/payment/bills?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      bills.value = result.data?.list || []
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载账单失败:', error)
    ElMessage.error('加载账单失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadBills()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadBills()
}

const resetForm = () => {
  searchForm.value = {
    billType: '',
    status: '',
    dateRange: null
  }
  loadBills()
}

const viewBill = (bill) => {
  currentBill.value = bill
  billDetailVisible.value = true
}

const payBill = (bill) => {
  currentBill.value = bill
  paymentMethod.value = 'balance'
  payDialogVisible.value = true
}

const confirmPayment = async () => {
  if (!currentBill.value) return
  
  paying.value = true
  try {
    const response = await fetch(`/api/v1/pc/payment/bills/${currentBill.value.id}/pay`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        payment_method: paymentMethod.value
      })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('支付成功')
      payDialogVisible.value = false
      loadBills()
    } else {
      ElMessage.error(result.msg || '支付失败')
    }
  } catch (error) {
    console.error('支付失败:', error)
    ElMessage.error('支付失败')
  } finally {
    paying.value = false
  }
}

const getStatusText = (status) => {
  const map = {
    'unpaid': '待支付',
    'paid': '已支付',
    'overdue': '已逾期',
    'cancelled': '已取消'
  }
  return map[status] || status
}

const getStatusColor = (status) => {
  const map = {
    'unpaid': 'warning',
    'paid': 'success',
    'overdue': 'danger',
    'cancelled': 'info'
  }
  return map[status] || 'info'
}

onMounted(() => {
  loadBills()
})
</script>

<style scoped>
.my-bills-page {
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
.bills-card {
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

.bill-detail {
  padding: 20px 0;
}

.bill-items {
  margin-top: 20px;
}

.bill-items h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #303133;
}

.pay-form {
  padding: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
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
