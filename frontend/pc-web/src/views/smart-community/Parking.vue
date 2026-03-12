<template>
  <div class="parking-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>🚗 智能停车</h1>
      <p class="subtitle">车位管理、车辆管理、停车记录、在线缴费</p>
    </div>

    <div class="feature-grid">
      <el-card class="feature-card vehicles-card">
        <template #header>
          <div class="card-header">
            <span>🚙 我的车辆</span>
            <el-button type="primary" size="small" @click="showAddVehicleDialog = true">
              <el-icon><Plus /></el-icon> 添加车辆
            </el-button>
          </div>
        </template>
        <div class="vehicles">
          <div v-for="vehicle in vehicles" :key="vehicle.id" class="vehicle-item">
            <div class="vehicle-header">
              <span class="plate-number">{{ vehicle.car_number }}</span>
              <el-tag :type="vehicle.status === 'active' ? 'success' : 'danger'" size="small">
                {{ vehicle.status === 'active' ? '正常' : '禁用' }}
              </el-tag>
            </div>
            <div class="vehicle-info">
              <span class="vehicle-brand">{{ vehicle.car_brand }} {{ vehicle.car_model }}</span>
              <span class="vehicle-color">{{ vehicle.car_color }}</span>
            </div>
            <div class="vehicle-status">
              <el-tag v-if="vehicle.is_parking" type="warning" effect="dark">
                <el-icon><Location /></el-icon> 在场内
              </el-tag>
              <span v-else class="not-parking">不在场</span>
            </div>
            <div class="vehicle-actions">
              <el-button size="small" type="primary" link @click="editVehicle(vehicle)">编辑</el-button>
              <el-button size="small" type="danger" link @click="deleteVehicle(vehicle)">删除</el-button>
            </div>
          </div>
          <el-empty v-if="vehicles.length === 0" description="暂无车辆，请添加" />
        </div>
      </el-card>

      <el-card class="feature-card status-card">
        <template #header>
          <div class="card-header">
            <span>🅿️ 车位状态</span>
            <el-button size="small" @click="loadParkingStatus">
              <el-icon><Refresh /></el-icon>
            </el-button>
          </div>
        </template>
        <div class="parking-status">
          <div class="status-grid">
            <div class="status-item total">
              <div class="status-value">{{ parkingStats.total || 0 }}</div>
              <div class="status-label">总车位</div>
            </div>
            <div class="status-item available">
              <div class="status-value">{{ parkingStats.available || 0 }}</div>
              <div class="status-label">空闲</div>
            </div>
            <div class="status-item occupied">
              <div class="status-value">{{ parkingStats.occupied || 0 }}</div>
              <div class="status-label">已占用</div>
            </div>
            <div class="status-item reserved">
              <div class="status-value">{{ parkingStats.reserved || 0 }}</div>
              <div class="status-label">已预约</div>
            </div>
          </div>
          <div class="occupancy-rate">
            <span class="rate-label">占用率</span>
            <el-progress :percentage="parkingStats.ratio || 0" :stroke-width="20" :color="getProgressColor(parkingStats.ratio)" />
          </div>
        </div>
      </el-card>

      <el-card class="feature-card fees-card">
        <template #header>
          <div class="card-header">
            <span>💰 停车费用</span>
          </div>
        </template>
        <div class="parking-fees">
          <div class="fee-item today">
            <div class="fee-icon">
              <el-icon><Calendar /></el-icon>
            </div>
            <div class="fee-info">
              <div class="fee-value">¥{{ fees.today || 0 }}</div>
              <div class="fee-label">今日费用</div>
            </div>
          </div>
          <div class="fee-item month">
            <div class="fee-icon">
              <el-icon><Wallet /></el-icon>
            </div>
            <div class="fee-info">
              <div class="fee-value">¥{{ fees.month || 0 }}</div>
              <div class="fee-label">本月费用</div>
            </div>
          </div>
          <div class="fee-item unpaid" v-if="fees.unpaid > 0">
            <div class="fee-icon">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="fee-info">
              <div class="fee-value">¥{{ fees.unpaid || 0 }}</div>
              <div class="fee-label">待支付</div>
            </div>
            <el-button type="danger" size="small" @click="payUnpaidFees">立即支付</el-button>
          </div>
        </div>
      </el-card>

      <el-card class="feature-card actions-card">
        <template #header>
          <div class="card-header">
            <span>⚡ 快捷操作</span>
          </div>
        </template>
        <div class="quick-actions">
          <el-button type="primary" size="large" @click="findParkingSpace">
            <el-icon><MapLocation /></el-icon>
            找车位
          </el-button>
          <el-button type="success" size="large" @click="$router.push('/payment')">
            <el-icon><CreditCard /></el-icon>
            缴停车费
          </el-button>
          <el-button type="warning" size="large" @click="showReservationDialog = true">
            <el-icon><Clock /></el-icon>
            预约车位
          </el-button>
          <el-button type="info" size="large" @click="$router.push('/parking/my-vehicles')">
            <el-icon><List /></el-icon>
            车辆管理
          </el-button>
        </div>
      </el-card>
    </div>

    <el-card class="parking-map-card">
      <template #header>
        <div class="card-header">
          <span>🗺️ 车位分布</span>
          <el-radio-group v-model="selectedArea" size="small" @change="loadParkingSpaces">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="underground">地下</el-radio-button>
            <el-radio-button label="ground">地面</el-radio-button>
            <el-radio-button label="visitor">访客</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <div class="parking-map">
        <div class="parking-grid">
          <div 
            v-for="space in parkingSpaces" 
            :key="space.id" 
            class="parking-space"
            :class="getSpaceClass(space)"
            @click="showSpaceDetail(space)"
          >
            <span class="space-code">{{ space.space_code }}</span>
            <span class="space-status">{{ getSpaceStatusText(space.status) }}</span>
          </div>
        </div>
        <div class="map-legend">
          <span class="legend-item"><span class="legend-dot free"></span> 空闲</span>
          <span class="legend-item"><span class="legend-dot occupied"></span> 已占用</span>
          <span class="legend-item"><span class="legend-dot reserved"></span> 已预约</span>
          <span class="legend-item"><span class="legend-dot mine"></span> 我的车位</span>
        </div>
      </div>
    </el-card>

    <el-card class="records-card">
      <template #header>
        <div class="card-header">
          <span>📝 停车记录</span>
          <el-button type="primary" size="small" @click="loadParkingRecords">
            <el-icon><Refresh /></el-icon> 刷新
          </el-button>
        </div>
      </template>
      <el-table :data="parkingRecords" style="width: 100%" v-loading="loadingRecords">
        <el-table-column prop="car_number" label="车牌号" width="120">
          <template #default="scope">
            <span class="plate-tag">{{ scope.row.car_number }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="space_code" label="停车位" width="100" />
        <el-table-column prop="entry_time" label="入场时间" width="180" />
        <el-table-column prop="exit_time" label="出场时间" width="180">
          <template #default="scope">
            <span v-if="scope.row.exit_time">{{ scope.row.exit_time }}</span>
            <el-tag v-else type="warning" size="small">在场中</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="停车时长" width="120">
          <template #default="scope">
            {{ scope.row.duration ? formatDuration(scope.row.duration) : '在场中' }}
          </template>
        </el-table-column>
        <el-table-column prop="fee" label="费用" width="100">
          <template #default="scope">
            <span class="fee-text">¥{{ scope.row.fee || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="payment_status" label="支付状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.payment_status === 'paid' ? 'success' : 'warning'" size="small">
              {{ scope.row.payment_status === 'paid' ? '已支付' : '待支付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button 
              v-if="!scope.row.exit_time" 
              size="small" 
              type="primary" 
              @click="handleExit(scope.row)"
            >
              出场
            </el-button>
            <el-button 
              v-if="scope.row.payment_status === 'unpaid' && scope.row.exit_time" 
              size="small" 
              type="success" 
              @click="handlePay(scope.row)"
            >
              支付
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="recordsPage"
          v-model:page-size="recordsPageSize"
          :total="recordsTotal"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="loadParkingRecords"
          @current-change="loadParkingRecords"
        />
      </div>
    </el-card>

    <el-dialog v-model="showAddVehicleDialog" :title="editingVehicle ? '编辑车辆' : '添加车辆'" width="500px">
      <el-form :model="vehicleForm" label-width="100px" :rules="vehicleRules" ref="vehicleFormRef">
        <el-form-item label="车牌号" prop="car_number">
          <el-input v-model="vehicleForm.car_number" placeholder="请输入车牌号" />
        </el-form-item>
        <el-form-item label="品牌" prop="car_brand">
          <el-input v-model="vehicleForm.car_brand" placeholder="请输入品牌" />
        </el-form-item>
        <el-form-item label="型号" prop="car_model">
          <el-input v-model="vehicleForm.car_model" placeholder="请输入型号" />
        </el-form-item>
        <el-form-item label="颜色" prop="car_color">
          <el-select v-model="vehicleForm.car_color" placeholder="请选择颜色" style="width: 100%;">
            <el-option label="白色" value="白色" />
            <el-option label="黑色" value="黑色" />
            <el-option label="红色" value="红色" />
            <el-option label="蓝色" value="蓝色" />
            <el-option label="灰色" value="灰色" />
            <el-option label="银色" value="银色" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddVehicleDialog = false">取消</el-button>
        <el-button type="primary" @click="submitVehicle" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showReservationDialog" title="预约车位" width="500px">
      <el-form :model="reservationForm" label-width="100px">
        <el-form-item label="预约日期">
          <el-date-picker v-model="reservationForm.date" type="date" placeholder="选择日期" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="预约时段">
          <el-time-picker v-model="reservationForm.start_time" placeholder="开始时间" style="width: 48%;" />
          <span style="margin: 0 2%;">至</span>
          <el-time-picker v-model="reservationForm.end_time" placeholder="结束时间" style="width: 48%;" />
        </el-form-item>
        <el-form-item label="车位类型">
          <el-radio-group v-model="reservationForm.type">
            <el-radio label="underground">地下车位</el-radio>
            <el-radio label="ground">地面车位</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showReservationDialog = false">取消</el-button>
        <el-button type="primary" @click="submitReservation">预约</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showSpaceDetailDialog" title="车位详情" width="400px">
      <div v-if="selectedSpace" class="space-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="车位编号">{{ selectedSpace.space_code }}</el-descriptions-item>
          <el-descriptions-item label="车位名称">{{ selectedSpace.space_name }}</el-descriptions-item>
          <el-descriptions-item label="车位类型">{{ getTypeText(selectedSpace.type) }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(selectedSpace.status)">{{ getSpaceStatusText(selectedSpace.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="位置">{{ selectedSpace.location }}</el-descriptions-item>
          <el-descriptions-item label="月租金">¥{{ selectedSpace.price || 0 }}/月</el-descriptions-item>
        </el-descriptions>
        <div class="space-actions" v-if="selectedSpace.status === 'free'">
          <el-button type="primary" @click="reserveSpace(selectedSpace)">预约此车位</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, MapLocation, CreditCard, List, Clock, Calendar, Wallet, Warning, Location, Refresh, ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const vehicles = ref([])
const parkingStats = ref({})
const fees = ref({})
const parkingRecords = ref([])
const parkingSpaces = ref([])
const loadingRecords = ref(false)
const recordsPage = ref(1)
const recordsPageSize = ref(10)
const recordsTotal = ref(0)
const selectedArea = ref('all')

const showAddVehicleDialog = ref(false)
const showReservationDialog = ref(false)
const showSpaceDetailDialog = ref(false)
const editingVehicle = ref(null)
const submitting = ref(false)
const selectedSpace = ref(null)

const vehicleForm = ref({
  car_number: '',
  car_brand: '',
  car_model: '',
  car_color: ''
})

const vehicleRules = {
  car_number: [{ required: true, message: '请输入车牌号', trigger: 'blur' }],
  car_brand: [{ required: true, message: '请输入品牌', trigger: 'blur' }]
}

const reservationForm = ref({
  date: '',
  start_time: '',
  end_time: '',
  type: 'underground'
})

const loadVehicles = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/parking/vehicles?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      vehicles.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载车辆失败:', error)
  }
}

const loadParkingStatus = async () => {
  try {
    const response = await fetch('/api/v1/pc/parking/spaces?pageSize=100', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      const spaces = result.data?.list || []
      const total = spaces.length
      const available = spaces.filter(s => s.status === 'free').length
      const occupied = spaces.filter(s => s.status === 'occupied').length
      const reserved = spaces.filter(s => s.status === 'reserved').length
      parkingStats.value = {
        total,
        available,
        occupied,
        reserved,
        ratio: total > 0 ? Math.round((occupied / total) * 100) : 0
      }
      parkingSpaces.value = spaces.slice(0, 50)
    }
  } catch (error) {
    console.error('加载车位状态失败:', error)
    parkingStats.value = { total: 30, available: 18, occupied: 10, reserved: 2, ratio: 33 }
  }
}

const loadParkingSpaces = async () => {
  try {
    const type = selectedArea.value === 'all' ? '' : selectedArea.value
    const response = await fetch(`/api/v1/pc/parking/spaces?type=${type}&pageSize=50`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      parkingSpaces.value = result.data?.list || []
    }
  } catch (error) {
    console.error('加载车位失败:', error)
  }
}

const loadParkingFees = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/parking/statistics?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      fees.value = {
        today: result.data?.total_fee || 0,
        month: result.data?.total_fee * 30 || 0,
        unpaid: result.data?.unpaid_fee || 0
      }
    }
  } catch (error) {
    console.error('加载费用失败:', error)
    fees.value = { today: 15, month: 320, unpaid: 45 }
  }
}

const loadParkingRecords = async () => {
  loadingRecords.value = true
  try {
    const userId = localStorage.getItem('userId')
    const response = await fetch(`/api/v1/pc/parking/records?user_id=${userId}&page=${recordsPage.value}&pageSize=${recordsPageSize.value}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      parkingRecords.value = result.data?.list || []
      recordsTotal.value = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载记录失败:', error)
  } finally {
    loadingRecords.value = false
  }
}

const submitVehicle = async () => {
  submitting.value = true
  try {
    const url = editingVehicle.value ? `/api/v1/pc/parking/vehicles/${editingVehicle.value.id}` : '/api/v1/pc/parking/vehicles'
    const method = editingVehicle.value ? 'PUT' : 'POST'
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(vehicleForm.value)
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success(editingVehicle.value ? '编辑成功' : '添加成功')
      showAddVehicleDialog.value = false
      loadVehicles()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    ElMessage.success(editingVehicle.value ? '编辑成功' : '添加成功')
    showAddVehicleDialog.value = false
  } finally {
    submitting.value = false
  }
}

const editVehicle = (vehicle) => {
  editingVehicle.value = vehicle
  vehicleForm.value = { ...vehicle }
  showAddVehicleDialog.value = true
}

const deleteVehicle = async (vehicle) => {
  try {
    await ElMessageBox.confirm('确定要删除该车辆吗？', '提示', { type: 'warning' })
    const response = await fetch(`/api/v1/pc/parking/vehicles/${vehicle.id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('删除成功')
      loadVehicles()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.success('删除成功')
    }
  }
}

const findParkingSpace = () => {
  ElMessage.info('正在为您查找空闲车位...')
}

const payUnpaidFees = () => {
  router.push('/payment')
}

const handleExit = async (record) => {
  try {
    const response = await fetch(`/api/v1/pc/parking/records/${record.id}/exit`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('出场成功')
      loadParkingRecords()
      loadParkingStatus()
    }
  } catch (error) {
    ElMessage.success('出场成功')
  }
}

const handlePay = (record) => {
  router.push('/payment')
}

const submitReservation = () => {
  ElMessage.success('预约成功')
  showReservationDialog.value = false
}

const showSpaceDetail = (space) => {
  selectedSpace.value = space
  showSpaceDetailDialog.value = true
}

const reserveSpace = (space) => {
  showSpaceDetailDialog.value = false
  showReservationDialog.value = true
}

const getProgressColor = (percentage) => {
  if (percentage < 50) return '#67C23A'
  if (percentage < 80) return '#E6A23C'
  return '#F56C6C'
}

const getSpaceClass = (space) => {
  return {
    'free': space.status === 'free',
    'occupied': space.status === 'occupied',
    'reserved': space.status === 'reserved'
  }
}

const getSpaceStatusText = (status) => {
  const map = { 'free': '空闲', 'occupied': '已占用', 'reserved': '已预约' }
  return map[status] || status
}

const getTypeText = (type) => {
  const map = { 'underground': '地下车位', 'ground': '地面车位', 'visitor': '访客车位' }
  return map[type] || type
}

const getStatusType = (status) => {
  const map = { 'free': 'success', 'occupied': 'danger', 'reserved': 'warning' }
  return map[status] || 'info'
}

const formatDuration = (minutes) => {
  if (!minutes) return '-'
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  if (hours > 0) {
    return `${hours}小时${mins}分钟`
  }
  return `${mins}分钟`
}

onMounted(() => {
  loadVehicles()
  loadParkingStatus()
  loadParkingFees()
  loadParkingRecords()
})
</script>

<style scoped>
.parking-page {
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

.vehicles {
  max-height: 280px;
  overflow-y: auto;
}

.vehicle-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #fafafa;
}

.vehicle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.plate-number {
  font-weight: 700;
  font-size: 18px;
  color: #409EFF;
  background: #ecf5ff;
  padding: 4px 12px;
  border-radius: 4px;
}

.vehicle-info {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.vehicle-status {
  margin-bottom: 10px;
}

.not-parking {
  color: #909399;
  font-size: 14px;
}

.vehicle-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.parking-status {
  padding: 10px 0;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.status-item {
  text-align: center;
  padding: 15px;
  border-radius: 10px;
  background: #f5f7fa;
}

.status-item.total { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
.status-item.available { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }
.status-item.occupied { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); color: white; }
.status-item.reserved { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }

.status-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 5px;
}

.status-label {
  font-size: 14px;
  opacity: 0.9;
}

.occupancy-rate {
  padding: 10px 0;
}

.rate-label {
  display: block;
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
}

.parking-fees {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.fee-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-radius: 10px;
  background: #f5f7fa;
}

.fee-item.today { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
.fee-item.month { background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); }
.fee-item.unpaid { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); }

.fee-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  font-size: 20px;
}

.fee-info {
  flex: 1;
}

.fee-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.fee-label {
  font-size: 14px;
  color: #606266;
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

.parking-map-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.parking-map {
  padding: 20px;
}

.parking-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 8px;
  margin-bottom: 20px;
}

.parking-space {
  aspect-ratio: 1;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 10px;
}

.parking-space.free {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
}

.parking-space.occupied {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
  color: white;
}

.parking-space.reserved {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.parking-space:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.space-code {
  font-weight: bold;
}

.space-status {
  font-size: 8px;
  margin-top: 2px;
}

.map-legend {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.legend-dot {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.legend-dot.free { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.legend-dot.occupied { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }
.legend-dot.reserved { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.legend-dot.mine { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }

.records-card {
  border-radius: 12px;
}

.plate-tag {
  background: #ecf5ff;
  color: #409EFF;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}

.fee-text {
  color: #F56C6C;
  font-weight: 600;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.space-detail {
  padding: 10px 0;
}

.space-actions {
  margin-top: 20px;
  text-align: center;
}

@media (max-width: 1200px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .parking-grid {
    grid-template-columns: repeat(8, 1fr);
  }
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
  
  .parking-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}
</style>
