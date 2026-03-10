<template>
  <div class="payment-page">
    <div class="page-header">
      <h1>💰 费用缴纳</h1>
      <p class="subtitle">水费、电费、物业费、停车费</p>
    </div>

    <div class="feature-grid">
      <!-- 待缴费 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📋 待缴费</span>
          </div>
        </template>
        <div class="unpaid-bills">
          <div v-for="bill in unpaidBills" :key="bill.id" class="bill-item">
            <div class="bill-header">
              <span class="bill-type">{{ bill.bill_type }}</span>
              <el-tag type="danger">待支付</el-tag>
            </div>
            <div class="bill-amount">¥{{ bill.amount }}</div>
            <div class="bill-details">
              <span>账单周期: {{ bill.period }}</span>
              <span>截止日期: {{ bill.due_date }}</span>
            </div>
            <el-button type="primary" @click="payBill(bill)" style="width: 100%; margin-top: 10px;">
              立即支付
            </el-button>
          </div>
          <el-empty v-if="unpaidBills.length === 0" description="暂无待缴费账单" />
        </div>
      </el-card>

      <!-- 账户余额 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>💳 账户余额</span>
          </div>
        </template>
        <div class="balance-info">
          <div class="balance-amount">¥{{ balance.amount || 0 }}</div>
          <div class="balance-label">可用余额</div>
          <el-button type="success" @click="recharge" style="width: 100%; margin-top: 20px;">
            <el-icon><Top /></el-icon>
            充值
          </el-button>
        </div>
      </el-card>

      <!-- 缴费统计 -->
      <el-card class="feature-card">
        <template #header>
          <div class="card-header">
            <span>📊 缴费统计</span>
          </div>
        </template>
        <div class="payment-stats">
          <div class="stat-item">
            <div class="stat-value">¥{{ stats.total_paid || 0 }}</div>
            <div class="stat-label">本月已缴</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">¥{{ stats.total_unpaid || 0 }}</div>
            <div class="stat-label">本月待缴</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.payment_count || 0 }}</div>
            <div class="stat-label">缴费次数</div>
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
          <el-button type="primary" plain @click="$router.push('/payment/bills')">
            <el-icon><List /></el-icon>
            账单明细
          </el-button>
          <el-button type="success" plain @click="batchPayment">
            <el-icon><Collection /></el-icon>
            批量缴费
          </el-button>
          <el-button type="info" plain @click="autoPayment">
            <el-icon><Timer /></el-icon>
            自动缴费
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 缴费记录 -->
    <el-card class="records-card">
      <template #header>
        <div class="card-header">
          <span>📝 缴费记录</span>
          <el-button text @click="$router.push('/payment/bills')">查看全部</el-button>
        </div>
      </template>
      <el-table :data="paymentRecords" style="width: 100%">
        <el-table-column prop="bill_type" label="账单类型" width="120" />
        <el-table-column prop="amount" label="金额" width="100">
          <template #default="scope">
            ¥{{ scope.row.amount }}
          </template>
        </el-table-column>
        <el-table-column prop="payment_method" label="支付方式" width="120" />
        <el-table-column prop="payment_time" label="支付时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag size="small" :type="scope.row.status === 'success' ? 'success' : 'danger'">
              {{ scope.row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

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

    <!-- 充值对话框 -->
    <el-dialog
      v-model="rechargeDialogVisible"
      title="账户充值"
      width="400px"
    >
      <el-form :model="rechargeForm" label-width="80px">
        <el-form-item label="充值金额">
          <el-input-number v-model="rechargeForm.amount" :min="10" :max="10000" :step="10" />
        </el-form-item>
        <el-form-item label="充值方式">
          <el-radio-group v-model="rechargeForm.method">
            <el-radio label="wechat">微信支付</el-radio>
            <el-radio label="alipay">支付宝</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="rechargeDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmRecharge" :loading="recharging">
            确认充值
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Top, List, Collection, Timer } from '@element-plus/icons-vue'

const unpaidBills = ref([])
const paymentRecords = ref([])
const balance = ref({})
const stats = ref({})
const payDialogVisible = ref(false)
const rechargeDialogVisible = ref(false)
const currentBill = ref(null)
const paymentMethod = ref('balance')
const paying = ref(false)
const recharging = ref(false)
const rechargeForm = ref({
  amount: 100,
  method: 'wechat'
})

// 加载待缴费账单
const loadUnpaidBills = async () => {
  try {
    const response = await fetch('/api/v1/pc/payment/unpaid-bills', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      unpaidBills.value = result.data || []
    }
  } catch (error) {
    console.error('加载待缴费账单失败:', error)
  }
}

// 加载缴费记录
const loadPaymentRecords = async () => {
  try {
    const response = await fetch('/api/v1/pc/payment/records?pageSize=5', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      paymentRecords.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载缴费记录失败:', error)
  }
}

// 加载账户余额
const loadBalance = async () => {
  try {
    const response = await fetch('/api/v1/pc/payment/balance', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      balance.value = result.data || {}
    }
  } catch (error) {
    console.error('加载余额失败:', error)
  }
}

// 加载统计
const loadStats = async () => {
  try {
    const response = await fetch('/api/v1/pc/payment/statistics', {
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
      loadUnpaidBills()
      loadBalance()
      loadStats()
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

const recharge = () => {
  rechargeForm.value = {
    amount: 100,
    method: 'wechat'
  }
  rechargeDialogVisible.value = true
}

const confirmRecharge = async () => {
  recharging.value = true
  try {
    const response = await fetch('/api/v1/pc/payment/recharge', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(rechargeForm.value)
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('充值成功')
      rechargeDialogVisible.value = false
      loadBalance()
    } else {
      ElMessage.error(result.msg || '充值失败')
    }
  } catch (error) {
    console.error('充值失败:', error)
    ElMessage.error('充值失败')
  } finally {
    recharging.value = false
  }
}

const batchPayment = () => {
  ElMessage.info('批量缴费功能开发中')
}

const autoPayment = () => {
  ElMessage.info('自动缴费功能开发中')
}

onMounted(() => {
  loadUnpaidBills()
  loadPaymentRecords()
  loadBalance()
  loadStats()
})
</script>

<style scoped>
.payment-page {
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

.unpaid-bills {
  max-height: 300px;
  overflow-y: auto;
}

.bill-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 15px;
}

.bill-item:last-child {
  margin-bottom: 0;
}

.bill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.bill-type {
  font-weight: 600;
}

.bill-amount {
  font-size: 24px;
  font-weight: bold;
  color: #F56C6C;
  margin-bottom: 10px;
}

.bill-details {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.balance-info {
  text-align: center;
  padding: 20px 0;
}

.balance-amount {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.balance-label {
  color: #909399;
  font-size: 14px;
}

.payment-stats {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px 0;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.records-card {
  border-radius: 8px;
}

.pay-form {
  padding: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
