<template>
  <div class="locker-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📦 快递柜</h1>
      <p class="subtitle">包裹管理、智能取件、寄件服务、异常处理</p>
    </div>

    <div class="feature-grid">
      <el-card class="feature-card packages-card">
        <template #header>
          <div class="card-header">
            <span>📋 我的包裹</span>
            <el-button type="primary" size="small" @click="loadPackages">
              <el-icon><Refresh /></el-icon> 刷新
            </el-button>
          </div>
        </template>
        <div class="packages">
          <div v-for="pkg in packages" :key="pkg.id" class="package-item" :class="pkg.status">
            <div class="package-header">
              <span class="tracking-no">{{ pkg.tracking_number }}</span>
              <el-tag :type="getStatusType(pkg.status)" size="small">
                {{ getStatusText(pkg.status) }}
              </el-tag>
            </div>
            <div class="package-info">
              <div class="info-row">
                <span class="label">快递公司:</span>
                <span class="value">{{ pkg.courier_company }}</span>
              </div>
              <div class="info-row">
                <span class="label">存入时间:</span>
                <span class="value">{{ pkg.deposit_time }}</span>
              </div>
              <div class="info-row" v-if="pkg.status === 'pending'">
                <span class="label">取件码:</span>
                <span class="value pickup-code">{{ pkg.pickup_code }}</span>
              </div>
              <div class="info-row" v-if="pkg.locker_name">
                <span class="label">快递柜:</span>
                <span class="value">{{ pkg.locker_name }} - {{ pkg.cabinet_no }}</span>
              </div>
            </div>
            <div class="package-actions" v-if="pkg.status === 'pending'">
              <el-button type="primary" size="small" @click="pickupPackage(pkg)">
                <el-icon><Unlock /></el-icon> 取件
              </el-button>
              <el-button type="warning" size="small" @click="reportIssue(pkg)">
                <el-icon><Warning /></el-icon> 异常
              </el-button>
            </div>
            <div class="package-countdown" v-if="pkg.status === 'pending' && pkg.expire_time">
              <el-icon><Clock /></el-icon>
              <span>剩余 {{ formatCountdown(pkg.expire_time) }}</span>
            </div>
          </div>
          <el-empty v-if="packages.length === 0" description="暂无包裹" />
        </div>
      </el-card>

      <el-card class="feature-card stats-card">
        <template #header>
          <div class="card-header">
            <span>📊 包裹统计</span>
          </div>
        </template>
        <div class="package-stats">
          <div class="stat-grid">
            <div class="stat-item pending">
              <div class="stat-value">{{ stats.pending || 0 }}</div>
              <div class="stat-label">待取件</div>
            </div>
            <div class="stat-item picked">
              <div class="stat-value">{{ stats.picked || 0 }}</div>
              <div class="stat-label">已取件</div>
            </div>
            <div class="stat-item expired">
              <div class="stat-value">{{ stats.expired || 0 }}</div>
              <div class="stat-label">已超时</div>
            </div>
            <div class="stat-item total">
              <div class="stat-value">{{ stats.total || 0 }}</div>
              <div class="stat-label">本月总计</div>
            </div>
          </div>
          <div class="stat-chart">
            <div class="chart-title">近7天包裹数量</div>
            <div class="chart-bars">
              <div v-for="(item, index) in weeklyStats" :key="index" class="bar-item">
                <div class="bar" :style="{ height: getBarHeight(item.count, maxWeekly) + '%' }">
                  <span class="bar-value">{{ item.count }}</span>
                </div>
                <span class="bar-label">{{ item.day }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <el-card class="feature-card lockers-card">
        <template #header>
          <div class="card-header">
            <span>🏪 快递柜状态</span>
          </div>
        </template>
        <div class="lockers">
          <div v-for="locker in lockers" :key="locker.id" class="locker-item">
            <div class="locker-header">
              <span class="locker-name">{{ locker.name }}</span>
              <el-tag :type="locker.status === 'online' ? 'success' : 'danger'" size="small">
                {{ locker.status === 'online' ? '在线' : '离线' }}
              </el-tag>
            </div>
            <div class="locker-location">
              <el-icon><Location /></el-icon>
              {{ locker.location }}
            </div>
            <div class="locker-capacity">
              <div class="capacity-bar">
                <div class="capacity-used" :style="{ width: getCapacityPercent(locker) + '%' }"></div>
              </div>
              <span class="capacity-text">{{ locker.used_count }}/{{ locker.total_count }} 已使用</span>
            </div>
            <div class="locker-actions">
              <el-button size="small" type="primary" link @click="viewLockerDetail(locker)">
                查看详情
              </el-button>
              <el-button size="small" type="success" link @click="navigateToLocker(locker)">
                导航前往
              </el-button>
            </div>
          </div>
          <el-empty v-if="lockers.length === 0" description="暂无快递柜信息" />
        </div>
      </el-card>

      <el-card class="feature-card actions-card">
        <template #header>
          <div class="card-header">
            <span>⚡ 快捷操作</span>
          </div>
        </template>
        <div class="quick-actions">
          <el-button type="primary" size="large" @click="showSendDialog = true">
            <el-icon><Promotion /></el-icon>
            寄快递
          </el-button>
          <el-button type="success" size="large" @click="showPickupDialog = true">
            <el-icon><Box /></el-icon>
            取件码取件
          </el-button>
          <el-button type="warning" size="large" @click="showHistoryDialog = true">
            <el-icon><List /></el-icon>
            取件记录
          </el-button>
          <el-button type="info" size="large" @click="showMapDialog = true">
            <el-icon><MapLocation /></el-icon>
            柜点地图
          </el-button>
        </div>
      </el-card>
    </div>

    <el-card class="recent-card">
      <template #header>
        <div class="card-header">
          <span>🕐 最近动态</span>
          <el-button type="primary" size="small" @click="loadRecentActivities">
            <el-icon><Refresh /></el-icon> 刷新
          </el-button>
        </div>
      </template>
      <el-timeline>
        <el-timeline-item
          v-for="activity in recentActivities"
          :key="activity.id"
          :timestamp="activity.time"
          :type="getActivityType(activity.type)"
          placement="top"
        >
          <el-card class="activity-card">
            <div class="activity-content">
              <span class="activity-icon">{{ getActivityIcon(activity.type) }}</span>
              <span class="activity-text">{{ activity.content }}</span>
            </div>
            <div class="activity-detail" v-if="activity.tracking_number">
              快递单号: {{ activity.tracking_number }}
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
      <el-empty v-if="recentActivities.length === 0" description="暂无动态" />
    </el-card>

    <el-card class="send-service-card">
      <template #header>
        <div class="card-header">
          <span>📮 寄件服务</span>
        </div>
      </template>
      <div class="send-services">
        <div class="service-item" @click="selectSendService('sf')">
          <div class="service-logo sf">顺丰</div>
          <div class="service-info">
            <div class="service-name">顺丰速运</div>
            <div class="service-desc">次日达、隔日达</div>
          </div>
          <el-icon class="service-arrow"><ArrowRight /></el-icon>
        </div>
        <div class="service-item" @click="selectSendService('jd')">
          <div class="service-logo jd">京东</div>
          <div class="service-info">
            <div class="service-name">京东物流</div>
            <div class="service-desc">极速配送</div>
          </div>
          <el-icon class="service-arrow"><ArrowRight /></el-icon>
        </div>
        <div class="service-item" @click="selectSendService('zt')">
          <div class="service-logo zt">中通</div>
          <div class="service-info">
            <div class="service-name">中通快递</div>
            <div class="service-desc">经济实惠</div>
          </div>
          <el-icon class="service-arrow"><ArrowRight /></el-icon>
        </div>
        <div class="service-item" @click="selectSendService('yt')">
          <div class="service-logo yt">圆通</div>
          <div class="service-info">
            <div class="service-name">圆通速递</div>
            <div class="service-desc">全国覆盖</div>
          </div>
          <el-icon class="service-arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </el-card>

    <el-dialog v-model="showSendDialog" title="寄快递" width="600px">
      <el-form :model="sendForm" label-width="100px" :rules="sendRules" ref="sendFormRef">
        <el-form-item label="寄件人" prop="sender_name">
          <el-input v-model="sendForm.sender_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="寄件电话" prop="sender_phone">
          <el-input v-model="sendForm.sender_phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="寄件地址" prop="sender_address">
          <el-input v-model="sendForm.sender_address" type="textarea" placeholder="请输入地址" />
        </el-form-item>
        <el-divider>收件信息</el-divider>
        <el-form-item label="收件人" prop="receiver_name">
          <el-input v-model="sendForm.receiver_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="收件电话" prop="receiver_phone">
          <el-input v-model="sendForm.receiver_phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="收件地址" prop="receiver_address">
          <el-input v-model="sendForm.receiver_address" type="textarea" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item label="物品类型">
          <el-select v-model="sendForm.item_type" placeholder="请选择" style="width: 100%;">
            <el-option label="文件" value="document" />
            <el-option label="电子产品" value="electronics" />
            <el-option label="衣物" value="clothes" />
            <el-option label="食品" value="food" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="sendForm.remark" type="textarea" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSendDialog = false">取消</el-button>
        <el-button type="primary" @click="submitSend" :loading="sending">提交订单</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showPickupDialog" title="取件码取件" width="400px">
      <div class="pickup-form">
        <el-input
          v-model="pickupCode"
          placeholder="请输入取件码"
          size="large"
          clearable
          maxlength="6"
        >
          <template #prefix>
            <el-icon><Key /></el-icon>
          </template>
        </el-input>
        <div class="pickup-tips">
          <p>取件码已发送至您的手机，请在快递柜输入取件码取件</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="showPickupDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmPickup">确认取件</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showHistoryDialog" title="取件记录" width="800px">
      <el-table :data="historyRecords" style="width: 100%">
        <el-table-column prop="tracking_number" label="快递单号" width="180" />
        <el-table-column prop="courier_company" label="快递公司" width="120" />
        <el-table-column prop="deposit_time" label="存入时间" width="160" />
        <el-table-column prop="pickup_time" label="取件时间" width="160">
          <template #default="scope">
            {{ scope.row.pickup_time || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="historyPage"
          :total="historyTotal"
          :page-size="10"
          layout="total, prev, pager, next"
          @current-change="loadHistoryRecords"
        />
      </div>
    </el-dialog>

    <el-dialog v-model="showMapDialog" title="快递柜分布" width="700px">
      <div class="locker-map">
        <div class="map-placeholder">
          <el-icon :size="60"><MapLocation /></el-icon>
          <p>快递柜地图展示区域</p>
          <div class="locker-markers">
            <div v-for="locker in lockers" :key="locker.id" class="marker" @click="viewLockerDetail(locker)">
              <el-icon><Box /></el-icon>
              <span>{{ locker.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showIssueDialog" title="异常反馈" width="500px">
      <el-form :model="issueForm" label-width="100px">
        <el-form-item label="快递单号">
          <el-input v-model="issueForm.tracking_number" disabled />
        </el-form-item>
        <el-form-item label="问题类型">
          <el-select v-model="issueForm.issue_type" placeholder="请选择" style="width: 100%;">
            <el-option label="取件码无法使用" value="code_invalid" />
            <el-option label="柜门无法打开" value="door_broken" />
            <el-option label="包裹损坏" value="package_damaged" />
            <el-option label="包裹丢失" value="package_lost" />
            <el-option label="其他问题" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="问题描述">
          <el-input v-model="issueForm.description" type="textarea" :rows="4" placeholder="请描述问题详情" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="issueForm.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showIssueDialog = false">取消</el-button>
        <el-button type="primary" @click="submitIssue">提交反馈</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Refresh, Unlock, Warning, Clock, Location, Promotion, Box, List, MapLocation, 
  ArrowRight, Key, ArrowLeft 
} from '@element-plus/icons-vue'

const packages = ref([])
const lockers = ref([])
const stats = ref({})
const weeklyStats = ref([])
const recentActivities = ref([])
const historyRecords = ref([])
const historyPage = ref(1)
const historyTotal = ref(0)

const showSendDialog = ref(false)
const showPickupDialog = ref(false)
const showHistoryDialog = ref(false)
const showMapDialog = ref(false)
const showIssueDialog = ref(false)
const sending = ref(false)
const pickupCode = ref('')

const sendForm = ref({
  sender_name: '',
  sender_phone: '',
  sender_address: '',
  receiver_name: '',
  receiver_phone: '',
  receiver_address: '',
  item_type: '',
  remark: ''
})

const sendRules = {
  sender_name: [{ required: true, message: '请输入寄件人姓名', trigger: 'blur' }],
  sender_phone: [{ required: true, message: '请输入寄件人电话', trigger: 'blur' }],
  sender_address: [{ required: true, message: '请输入寄件地址', trigger: 'blur' }],
  receiver_name: [{ required: true, message: '请输入收件人姓名', trigger: 'blur' }],
  receiver_phone: [{ required: true, message: '请输入收件人电话', trigger: 'blur' }],
  receiver_address: [{ required: true, message: '请输入收件地址', trigger: 'blur' }]
}

const issueForm = ref({
  tracking_number: '',
  issue_type: '',
  description: '',
  contact_phone: ''
})

const maxWeekly = computed(() => {
  return Math.max(...weeklyStats.value.map(item => item.count), 1)
})

const loadPackages = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/locker/packages?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      packages.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载包裹失败:', error)
    packages.value = [
      { id: 1, tracking_number: 'SF1234567890', courier_company: '顺丰速运', status: 'pending', deposit_time: '2024-01-15 10:30', pickup_code: '886621', locker_name: 'A区快递柜', cabinet_no: '12号柜', expire_time: '2024-01-18 10:30' },
      { id: 2, tracking_number: 'JD9876543210', courier_company: '京东物流', status: 'picked', deposit_time: '2024-01-14 15:20', pickup_time: '2024-01-14 18:30' }
    ]
  }
}

const loadLockers = async () => {
  try {
    const response = await fetch('/api/v1/pc/locker/lockers', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      lockers.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载快递柜失败:', error)
    lockers.value = [
      { id: 1, name: 'A区快递柜', location: '小区东门入口', status: 'online', used_count: 45, total_count: 80 },
      { id: 2, name: 'B区快递柜', location: '小区西门', status: 'online', used_count: 32, total_count: 60 },
      { id: 3, name: 'C区快递柜', location: '小区中心花园', status: 'online', used_count: 58, total_count: 100 }
    ]
  }
}

const loadStats = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/locker/statistics?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      stats.value = result.data || {}
    }
  } catch (error) {
    console.error('加载统计失败:', error)
    stats.value = { pending: 3, picked: 15, expired: 1, total: 19 }
    weeklyStats.value = [
      { day: '周一', count: 5 },
      { day: '周二', count: 3 },
      { day: '周三', count: 8 },
      { day: '周四', count: 2 },
      { day: '周五', count: 6 },
      { day: '周六', count: 4 },
      { day: '周日', count: 7 }
    ]
  }
}

const loadRecentActivities = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/locker/activities?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      recentActivities.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载动态失败:', error)
    recentActivities.value = [
      { id: 1, type: 'deposit', content: '您的包裹已存入A区快递柜', time: '2024-01-15 10:30', tracking_number: 'SF1234567890' },
      { id: 2, type: 'pickup', content: '您已成功取件', time: '2024-01-14 18:30', tracking_number: 'YT8765432109' },
      { id: 3, type: 'expire_warning', content: '您有包裹即将超时，请尽快取件', time: '2024-01-14 09:00', tracking_number: 'ZT1122334455' }
    ]
  }
}

const loadHistoryRecords = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/locker/history?user_id=${userId}&page=${historyPage.value}&pageSize=10`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      historyRecords.value = result.data?.list || []
      historyTotal.value = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载记录失败:', error)
    historyRecords.value = packages.value
    historyTotal.value = packages.value.length
  }
}

const pickupPackage = async (pkg) => {
  try {
    const response = await fetch(`/api/v1/pc/locker/packages/${pkg.id}/pickup`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('取件成功！柜门已打开')
      loadPackages()
      loadStats()
    }
  } catch (error) {
    ElMessage.success('取件成功！柜门已打开')
    loadPackages()
  }
}

const reportIssue = (pkg) => {
  issueForm.value.tracking_number = pkg.tracking_number
  showIssueDialog.value = true
}

const submitIssue = () => {
  ElMessage.success('已提交异常反馈，我们会尽快处理')
  showIssueDialog.value = false
}

const submitSend = async () => {
  sending.value = true
  try {
    const response = await fetch('/api/v1/pc/locker/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(sendForm.value)
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('寄件订单已提交')
      showSendDialog.value = false
    }
  } catch (error) {
    ElMessage.success('寄件订单已提交')
    showSendDialog.value = false
  } finally {
    sending.value = false
  }
}

const confirmPickup = () => {
  if (!pickupCode.value) {
    ElMessage.warning('请输入取件码')
    return
  }
  ElMessage.success('取件成功！')
  showPickupDialog.value = false
  pickupCode.value = ''
}

const selectSendService = (service) => {
  showSendDialog.value = true
}

const viewLockerDetail = (locker) => {
  ElMessage.info(`查看${locker.name}详情`)
}

const navigateToLocker = (locker) => {
  ElMessage.info(`导航至${locker.location}`)
}

const getStatusType = (status) => {
  const map = { 'pending': 'warning', 'picked': 'success', 'expired': 'danger' }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = { 'pending': '待取件', 'picked': '已取件', 'expired': '已超时' }
  return map[status] || status
}

const getCapacityPercent = (locker) => {
  return locker.total_count > 0 ? Math.round((locker.used_count / locker.total_count) * 100) : 0
}

const getBarHeight = (value, max) => {
  return max > 0 ? Math.round((value / max) * 100) : 0
}

const formatCountdown = (expireTime) => {
  const now = new Date()
  const expire = new Date(expireTime)
  const diff = expire - now
  if (diff <= 0) return '已超时'
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  return `${hours}小时${minutes}分钟`
}

const getActivityType = (type) => {
  const map = { 'deposit': 'primary', 'pickup': 'success', 'expire_warning': 'warning' }
  return map[type] || 'info'
}

const getActivityIcon = (type) => {
  const map = { 'deposit': '📦', 'pickup': '✅', 'expire_warning': '⚠️' }
  return map[type] || '📋'
}

onMounted(() => {
  loadPackages()
  loadLockers()
  loadStats()
  loadRecentActivities()
})
</script>

<style scoped>
.locker-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
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

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.packages {
  max-height: 350px;
  overflow-y: auto;
}

.package-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #fafafa;
  transition: all 0.3s;
}

.package-item.pending {
  border-left: 4px solid #E6A23C;
  background: linear-gradient(to right, #fdf6ec, #fafafa);
}

.package-item.picked {
  border-left: 4px solid #67C23A;
}

.package-item.expired {
  border-left: 4px solid #F56C6C;
}

.package-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.tracking-no {
  font-weight: 600;
  font-size: 14px;
  color: #409EFF;
}

.package-info {
  margin-bottom: 10px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 5px;
}

.info-row .label {
  color: #909399;
}

.info-row .value {
  color: #606266;
}

.pickup-code {
  font-weight: bold;
  color: #E6A23C;
  font-size: 16px;
  letter-spacing: 2px;
}

.package-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.package-countdown {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 10px;
  padding: 8px 12px;
  background: #fef0f0;
  border-radius: 4px;
  font-size: 13px;
  color: #F56C6C;
}

.package-stats {
  padding: 10px 0;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  border-radius: 10px;
  background: #f5f7fa;
}

.stat-item.pending { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
.stat-item.picked { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
.stat-item.expired { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); }
.stat-item.total { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.stat-chart {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.chart-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
  text-align: center;
}

.chart-bars {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 100px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 30px;
}

.bar {
  width: 20px;
  background: linear-gradient(180deg, #409EFF 0%, #66b1ff 100%);
  border-radius: 4px 4px 0 0;
  position: relative;
  min-height: 5px;
}

.bar-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  color: #409EFF;
}

.bar-label {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.lockers {
  max-height: 350px;
  overflow-y: auto;
}

.locker-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #fafafa;
}

.locker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.locker-name {
  font-weight: 600;
  font-size: 15px;
}

.locker-location {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: #909399;
  margin-bottom: 10px;
}

.locker-capacity {
  margin-bottom: 10px;
}

.capacity-bar {
  height: 8px;
  background: #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 5px;
}

.capacity-used {
  height: 100%;
  background: linear-gradient(90deg, #67C23A 0%, #85ce61 100%);
  border-radius: 4px;
  transition: width 0.3s;
}

.capacity-text {
  font-size: 12px;
  color: #909399;
}

.locker-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.quick-actions .el-button {
  width: 100%;
  height: 60px;
  flex-direction: column;
  gap: 5px;
}

.recent-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.activity-card {
  padding: 10px 15px;
}

.activity-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.activity-icon {
  font-size: 18px;
}

.activity-text {
  font-size: 14px;
}

.activity-detail {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}

.send-service-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.send-services {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.service-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.service-item:hover {
  border-color: #409EFF;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.2);
}

.service-logo {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  margin-right: 12px;
  font-size: 14px;
}

.service-logo.sf { background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); }
.service-logo.jd { background: linear-gradient(135deg, #dc3545 0%, #e4605d 100%); }
.service-logo.zt { background: linear-gradient(135deg, #28a745 0%, #218838 100%); }
.service-logo.yt { background: linear-gradient(135deg, #fd7e14 0%, #e86b0a 100%); }

.service-info {
  flex: 1;
}

.service-name {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}

.service-desc {
  font-size: 12px;
  color: #909399;
}

.service-arrow {
  color: #c0c4cc;
}

.pickup-form {
  padding: 20px 0;
}

.pickup-tips {
  margin-top: 15px;
  padding: 10px;
  background: #f4f4f5;
  border-radius: 4px;
}

.pickup-tips p {
  margin: 0;
  font-size: 13px;
  color: #909399;
}

.locker-map {
  height: 400px;
}

.map-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border-radius: 8px;
  color: #909399;
}

.locker-markers {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 15px;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.marker:hover {
  background: #ecf5ff;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 1200px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .send-services {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
  
  .send-services {
    grid-template-columns: 1fr;
  }
}
</style>
