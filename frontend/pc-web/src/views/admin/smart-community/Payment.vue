<template>
  <AdminLayout>
    <div class="payment-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>缴费管理</h3>
          </div>
        </template>
        
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="缴费记录" name="payments">
            <div class="mb-4">
              <el-button type="primary" @click="openPaymentDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增缴费记录
              </el-button>
            </div>
            
            <div class="search-filter mb-4">
              <el-form :inline="true" :model="searchForm" class="mb-4">
                <el-form-item label="状态">
                  <el-select v-model="searchForm.status" placeholder="选择状态">
                    <el-option label="全部" value="" />
                    <el-option label="未缴费" value="unpaid" />
                    <el-option label="已缴费" value="paid" />
                    <el-option label="已逾期" value="overdue" />
                  </el-select>
                </el-form-item>
                <el-form-item label="类型">
                  <el-select v-model="searchForm.type" placeholder="选择类型">
                    <el-option label="全部" value="" />
                    <el-option label="物业费" value="property" />
                    <el-option label="水电费" value="utility" />
                    <el-option label="停车费" value="parking" />
                    <el-option label="其他" value="other" />
                  </el-select>
                </el-form-item>
                <el-form-item label="费用类型">
                  <el-select v-model="searchForm.fee_type" placeholder="选择费用类型">
                    <el-option label="全部" value="" />
                    <el-option v-for="fee in feeTypes" :key="fee.code" :label="fee.name" :value="fee.code" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="searchPayments">查询</el-button>
                  <el-button @click="resetSearch">重置</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <el-table :data="payments" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="user_name" label="住户" />
              <el-table-column prop="building_name" label="楼栋" />
              <el-table-column prop="room_number" label="房号" />
              <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                  <el-tag :type="getTypeTag(scope.row.type)">
                    {{ getTypeText(scope.row.type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="fee_type" label="费用类型" width="120">
                <template #default="scope">
                  {{ getFeeTypeName(scope.row.fee_type) }}
                </template>
              </el-table-column>
              <el-table-column prop="amount" label="金额" width="100">
                <template #default="scope">
                  ¥{{ scope.row.amount.toFixed(2) }}
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getStatusTag(scope.row.status)">
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="due_date" label="截止日期" width="120" />
              <el-table-column prop="paid_time" label="缴费时间" width="180" />
              <el-table-column label="操作" width="250" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="viewPayment(scope.row)">
                    <el-icon><i-ep-view /></el-icon>
                    查看
                  </el-button>
                  <el-button size="small" type="success" @click="payPayment(scope.row)" v-if="scope.row.status === 'unpaid'">
                    <el-icon><i-ep-money /></el-icon>
                    缴费
                  </el-button>
                  <el-button size="small" type="danger" @click="deletePayment(scope.row.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
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
          </el-tab-pane>
          
          <el-tab-pane label="费用类型" name="fee-types">
            <div class="mb-4">
              <el-button type="primary" @click="openFeeTypeDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增费用类型
              </el-button>
            </div>
            
            <el-table :data="feeTypes" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="费用名称" />
              <el-table-column prop="code" label="编码" />
              <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                  <el-tag :type="getTypeTag(scope.row.type)">
                    {{ getTypeText(scope.row.type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="unit_price" label="单价" width="100">
                <template #default="scope">
                  ¥{{ scope.row.unit_price.toFixed(2) }}/{{ scope.row.unit }}
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                    {{ scope.row.status === 'active' ? '正常' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="editFeeType(scope.row)">
                    <el-icon><i-ep-edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteFeeType(scope.row.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="缴费统计" name="statistics">
            <el-row :gutter="20" class="mb-4">
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #409EFF">
                      <el-icon><i-ep-document /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总记录数</div>
                      <div class="stat-value">{{ statistics.total }}</div>
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
                      <div class="stat-label">未缴费</div>
                      <div class="stat-value">{{ statistics.unpaid }}</div>
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
                      <div class="stat-label">已缴费</div>
                      <div class="stat-value">{{ statistics.paid }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #F56C6C">
                      <el-icon><i-ep-warning /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">已逾期</div>
                      <div class="stat-value">{{ statistics.overdue }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            
            <el-row :gutter="20" class="mb-4">
              <el-col :span="8">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #409EFF">
                      <el-icon><i-ep-money /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总金额</div>
                      <div class="stat-value">¥{{ statistics.total_amount.toFixed(2) }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #67C23A">
                      <el-icon><i-ep-wallet /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">已收金额</div>
                      <div class="stat-value">¥{{ statistics.paid_amount.toFixed(2) }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #E6A23C">
                      <el-icon><i-ep-coin /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">待收金额</div>
                      <div class="stat-value">¥{{ statistics.unpaid_amount.toFixed(2) }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            
            <el-card shadow="hover" class="mt-4">
              <template #header>
                <span>按类型统计</span>
              </template>
              <el-table :data="statisticsByType" style="width: 100%">
                <el-table-column prop="type" label="类型">
                  <template #default="scope">
                    <el-tag :type="getTypeTag(scope.row.type)">
                      {{ getTypeText(scope.row.type) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="count" label="记录数" />
                <el-table-column prop="total_amount" label="总金额">
                  <template #default="scope">
                    ¥{{ scope.row.total_amount.toFixed(2) }}
                  </template>
                </el-table-column>
                <el-table-column prop="paid_amount" label="已收金额">
                  <template #default="scope">
                    ¥{{ scope.row.paid_amount.toFixed(2) }}
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-card>
      
      <el-dialog
        v-model="paymentDialogVisible"
        :title="paymentDialogTitle"
        width="600px"
      >
        <el-form :model="paymentForm" :rules="paymentRules" ref="paymentFormRef" label-width="100px" status-icon>
          <el-form-item label="住户" prop="user_id">
            <el-select v-model="paymentForm.user_id" placeholder="选择住户">
              <el-option 
                v-for="user in users" 
                :key="user.id" 
                :label="user.username" 
                :value="user.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="楼栋" prop="building_id">
            <el-select v-model="paymentForm.building_id" placeholder="选择楼栋">
              <el-option 
                v-for="building in buildings" 
                :key="building.id" 
                :label="building.building_name" 
                :value="building.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="缴费类型" prop="type">
            <el-select v-model="paymentForm.type" placeholder="选择缴费类型">
              <el-option label="物业费" value="property" />
              <el-option label="水电费" value="utility" />
              <el-option label="停车费" value="parking" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="费用类型" prop="fee_type">
            <el-select v-model="paymentForm.fee_type" placeholder="选择费用类型">
              <el-option v-for="fee in feeTypes" :key="fee.code" :label="fee.name" :value="fee.code" />
            </el-select>
          </el-form-item>
          <el-form-item label="金额" prop="amount">
            <el-input-number v-model="paymentForm.amount" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
          <el-form-item label="周期开始" prop="period_start">
            <el-date-picker v-model="paymentForm.period_start" type="date" placeholder="选择周期开始日期" style="width: 100%" />
          </el-form-item>
          <el-form-item label="周期结束" prop="period_end">
            <el-date-picker v-model="paymentForm.period_end" type="date" placeholder="选择周期结束日期" style="width: 100%" />
          </el-form-item>
          <el-form-item label="截止日期" prop="due_date">
            <el-date-picker v-model="paymentForm.due_date" type="date" placeholder="选择截止日期" style="width: 100%" />
          </el-form-item>
          <el-form-item label="备注" prop="remark">
            <el-input v-model="paymentForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="paymentDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="savePayment">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="feeTypeDialogVisible"
        :title="feeTypeDialogTitle"
        width="500px"
      >
        <el-form :model="feeTypeForm" :rules="feeTypeRules" ref="feeTypeFormRef" label-width="100px" status-icon>
          <el-form-item label="费用名称" prop="name">
            <el-input v-model="feeTypeForm.name" placeholder="请输入费用名称" />
          </el-form-item>
          <el-form-item label="编码" prop="code">
            <el-input v-model="feeTypeForm.code" placeholder="请输入编码" />
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="feeTypeForm.type" placeholder="选择类型">
              <el-option label="物业费" value="property" />
              <el-option label="水电费" value="utility" />
              <el-option label="停车费" value="parking" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="单价" prop="unit_price">
            <el-input-number v-model="feeTypeForm.unit_price" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
          <el-form-item label="单位" prop="unit">
            <el-input v-model="feeTypeForm.unit" placeholder="如：月、平方米、度" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="feeTypeForm.description" type="textarea" :rows="3" placeholder="请输入描述" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="feeTypeDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveFeeType">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="payDialogVisible"
        title="缴费"
        width="500px"
      >
        <el-form :model="payForm" ref="payFormRef" label-width="100px" status-icon>
          <el-form-item label="缴费金额" prop="paid_amount">
            <el-input-number v-model="payForm.paid_amount" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
          <el-form-item label="支付方式" prop="payment_method">
            <el-select v-model="payForm.payment_method" placeholder="选择支付方式">
              <el-option label="现金" value="cash" />
              <el-option label="微信" value="wechat" />
              <el-option label="支付宝" value="alipay" />
              <el-option label="银行卡" value="card" />
            </el-select>
          </el-form-item>
          <el-form-item label="交易号" prop="transaction_id">
            <el-input v-model="payForm.transaction_id" placeholder="请输入交易号（可选）" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="payDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmPay">确认缴费</el-button>
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

const activeTab = ref('payments')
const payments = ref([])
const feeTypes = ref([])
const users = ref([])
const buildings = ref([])
const statistics = ref({
  total: 0,
  unpaid: 0,
  paid: 0,
  overdue: 0,
  total_amount: 0,
  paid_amount: 0,
  unpaid_amount: 0
})
const statisticsByType = ref([])

const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const searchForm = ref({
  status: '',
  type: '',
  fee_type: ''
})

const paymentDialogVisible = ref(false)
const paymentDialogTitle = ref('新增缴费记录')
const paymentForm = ref({
  user_id: null,
  building_id: null,
  type: 'property',
  fee_type: '',
  amount: 0,
  period_start: null,
  period_end: null,
  due_date: null,
  remark: ''
})

const feeTypeDialogVisible = ref(false)
const feeTypeDialogTitle = ref('新增费用类型')
const feeTypeForm = ref({
  name: '',
  code: '',
  type: 'property',
  unit_price: 0,
  unit: '',
  description: ''
})

const payDialogVisible = ref(false)
const payForm = ref({
  payment_id: null,
  paid_amount: 0,
  payment_method: 'cash',
  transaction_id: ''
})

const paymentRules = {
  user_id: [{ required: true, message: '请选择住户', trigger: 'change' }],
  building_id: [{ required: true, message: '请选择楼栋', trigger: 'change' }],
  type: [{ required: true, message: '请选择缴费类型', trigger: 'change' }],
  fee_type: [{ required: true, message: '请选择费用类型', trigger: 'change' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  due_date: [{ required: true, message: '请选择截止日期', trigger: 'change' }]
}

const feeTypeRules = {
  name: [{ required: true, message: '请输入费用名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入编码', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  unit_price: [{ required: true, message: '请输入单价', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }]
}

const handleTabChange = (tab) => {
  if (tab === 'payments') {
    loadPayments()
  } else if (tab === 'fee-types') {
    loadFeeTypes()
  } else if (tab === 'statistics') {
    loadStatistics()
  }
}

const loadPayments = async () => {
  try {
    const response = await axios.get('/api/v1/pc/payments', {
      params: {
        page: page.value,
        pageSize: pageSize.value,
        ...searchForm.value
      }
    })
    payments.value = response.data.data.list
    total.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载缴费记录列表失败')
  }
}

const loadFeeTypes = async () => {
  try {
    const response = await axios.get('/api/v1/pc/payments/fee-types')
    feeTypes.value = response.data.data
  } catch (error) {
    ElMessage.error('加载费用类型列表失败')
  }
}

const loadStatistics = async () => {
  try {
    const [statsResponse, typeStatsResponse] = await Promise.all([
      axios.get('/api/v1/pc/payments/statistics'),
      axios.get('/api/v1/pc/payments/statistics/by-type')
    ])
    statistics.value = statsResponse.data.data
    statisticsByType.value = typeStatsResponse.data.data
  } catch (error) {
    ElMessage.error('加载统计失败')
  }
}

const openPaymentDialog = () => {
  paymentDialogTitle.value = '新增缴费记录'
  paymentForm.value = {
    user_id: null,
    building_id: null,
    type: 'property',
    fee_type: '',
    amount: 0,
    period_start: null,
    period_end: null,
    due_date: null,
    remark: ''
  }
  paymentDialogVisible.value = true
}

const savePayment = async () => {
  try {
    await axios.post('/api/v1/pc/payments', paymentForm.value)
    ElMessage.success('新增缴费记录成功')
    paymentDialogVisible.value = false
    loadPayments()
  } catch (error) {
    ElMessage.error('保存缴费记录失败')
  }
}

const viewPayment = (payment) => {
  ElMessageBox.alert(
    `<div>
      <p><strong>住户：</strong>${payment.user_name}</p>
      <p><strong>楼栋：</strong>${payment.building_name}</p>
      <p><strong>房号：</strong>${payment.room_number}</p>
      <p><strong>类型：</strong>${getTypeText(payment.type)}</p>
      <p><strong>费用类型：</strong>${getFeeTypeName(payment.fee_type)}</p>
      <p><strong>金额：</strong>¥${payment.amount.toFixed(2)}</p>
      <p><strong>状态：</strong>${getStatusText(payment.status)}</p>
      <p><strong>周期：</strong>${payment.period_start} 至 ${payment.period_end}</p>
      <p><strong>截止日期：</strong>${payment.due_date}</p>
      <p><strong>缴费时间：</strong>${payment.paid_time || '未缴费'}</p>
      <p><strong>支付方式：</strong>${payment.payment_method || '无'}</p>
      <p><strong>备注：</strong>${payment.remark || '无'}</p>
    </div>`,
    '缴费详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭'
    }
  )
}

const payPayment = (payment) => {
  payForm.value = {
    payment_id: payment.id,
    paid_amount: payment.amount,
    payment_method: 'cash',
    transaction_id: ''
  }
  payDialogVisible.value = true
}

const confirmPay = async () => {
  try {
    await axios.post(`/api/v1/pc/payments/${payForm.value.payment_id}/pay`, payForm.value)
    ElMessage.success('缴费成功')
    payDialogVisible.value = false
    loadPayments()
  } catch (error) {
    ElMessage.error('缴费失败')
  }
}

const deletePayment = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该缴费记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/v1/pc/payments/${id}`)
    ElMessage.success('删除成功')
    loadPayments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const openFeeTypeDialog = () => {
  feeTypeDialogTitle.value = '新增费用类型'
  feeTypeForm.value = {
    name: '',
    code: '',
    type: 'property',
    unit_price: 0,
    unit: '',
    description: ''
  }
  feeTypeDialogVisible.value = true
}

const editFeeType = (feeType) => {
  feeTypeDialogTitle.value = '编辑费用类型'
  feeTypeForm.value = { ...feeType }
  feeTypeDialogVisible.value = true
}

const saveFeeType = async () => {
  try {
    if (feeTypeDialogTitle.value === '新增费用类型') {
      await axios.post('/api/v1/pc/payments/fee-types', feeTypeForm.value)
      ElMessage.success('新增费用类型成功')
    } else {
      await axios.put(`/api/v1/pc/payments/fee-types/${feeTypeForm.value.id}`, feeTypeForm.value)
      ElMessage.success('更新费用类型成功')
    }
    feeTypeDialogVisible.value = false
    loadFeeTypes()
  } catch (error) {
    ElMessage.error('保存费用类型失败')
  }
}

const deleteFeeType = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该费用类型吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/v1/pc/payments/fee-types/${id}`)
    ElMessage.success('删除费用类型成功')
    loadFeeTypes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除费用类型失败')
    }
  }
}

const searchPayments = () => {
  page.value = 1
  loadPayments()
}

const resetSearch = () => {
  searchForm.value = {
    status: '',
    type: '',
    fee_type: ''
  }
  page.value = 1
  loadPayments()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  loadPayments()
}

const handleCurrentChange = (currentPage) => {
  page.value = currentPage
  loadPayments()
}

const getTypeTag = (type) => {
  const typeMap = {
    'property': 'primary',
    'utility': 'success',
    'parking': 'warning',
    'other': 'info'
  }
  return typeMap[type] || ''
}

const getTypeText = (type) => {
  const typeMap = {
    'property': '物业费',
    'utility': '水电费',
    'parking': '停车费',
    'other': '其他'
  }
  return typeMap[type] || type
}

const getStatusTag = (status) => {
  const statusMap = {
    'unpaid': 'warning',
    'paid': 'success',
    'overdue': 'danger'
  }
  return statusMap[status] || ''
}

const getStatusText = (status) => {
  const statusMap = {
    'unpaid': '未缴费',
    'paid': '已缴费',
    'overdue': '已逾期'
  }
  return statusMap[status] || status
}

const getFeeTypeName = (code) => {
  const feeType = feeTypes.value.find(f => f.code === code)
  return feeType ? feeType.name : code
}

onMounted(() => {
  loadPayments()
  loadFeeTypes()
})
</script>

<style scoped>
.payment-management {
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
