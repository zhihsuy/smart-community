<template>
  <AdminLayout>
    <div class="parking-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>停车管理</h3>
          </div>
        </template>
        
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="车位管理" name="spaces">
            <div class="mb-4">
              <el-button type="primary" @click="openSpaceDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增车位
              </el-button>
            </div>
            
            <el-table :data="spaces" style="width: 100%">
              <el-table-column prop="id" label="车位ID" width="80" />
              <el-table-column prop="space_code" label="车位编码" />
              <el-table-column prop="space_name" label="车位名称" />
              <el-table-column prop="type" label="车位类型" width="100">
                <template #default="scope">
                  <el-tag :type="getTypeTag(scope.row.type)">
                    {{ getTypeText(scope.row.type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="location" label="位置" />
              <el-table-column prop="price" label="月租金" width="100">
                <template #default="scope">
                  {{ scope.row.price ? `¥${scope.row.price}` : '-' }}
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getStatusTag(scope.row.status)">
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="editSpace(scope.row)">
                    <el-icon><i-ep-edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteSpace(scope.row.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination" v-if="spaceTotal > 0">
              <el-pagination
                v-model:current-page="spacePage"
                v-model:page-size="spacePageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="spaceTotal"
                @size-change="handleSpaceSizeChange"
                @current-change="handleSpaceCurrentChange"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="车辆管理" name="vehicles">
            <div class="mb-4">
              <el-button type="primary" @click="openVehicleDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增车辆
              </el-button>
            </div>
            
            <el-table :data="vehicles" style="width: 100%">
              <el-table-column prop="id" label="车辆ID" width="80" />
              <el-table-column prop="car_number" label="车牌号" />
              <el-table-column prop="car_brand" label="品牌" />
              <el-table-column prop="car_model" label="型号" />
              <el-table-column prop="car_color" label="颜色" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                    {{ scope.row.status === 'active' ? '正常' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="editVehicle(scope.row)">
                    <el-icon><i-ep-edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteVehicle(scope.row.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination" v-if="vehicleTotal > 0">
              <el-pagination
                v-model:current-page="vehiclePage"
                v-model:page-size="vehiclePageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="vehicleTotal"
                @size-change="handleVehicleSizeChange"
                @current-change="handleVehicleCurrentChange"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="停车记录" name="records">
            <div class="search-filter mb-4">
              <el-form :inline="true" :model="recordSearchForm" class="mb-4">
                <el-form-item label="车牌号">
                  <el-input v-model="recordSearchForm.car_number" placeholder="请输入车牌号" />
                </el-form-item>
                <el-form-item label="支付状态">
                  <el-select v-model="recordSearchForm.payment_status" placeholder="选择支付状态">
                    <el-option label="全部" value="" />
                    <el-option label="未支付" value="unpaid" />
                    <el-option label="已支付" value="paid" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="searchRecords">查询</el-button>
                  <el-button @click="resetRecordSearch">重置</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <el-table :data="records" style="width: 100%">
              <el-table-column prop="id" label="记录ID" width="80" />
              <el-table-column prop="car_number" label="车牌号" />
              <el-table-column prop="entry_time" label="进入时间" width="180" />
              <el-table-column prop="exit_time" label="离开时间" width="180" />
              <el-table-column prop="duration" label="停车时长(分钟)" width="120" />
              <el-table-column prop="fee" label="停车费用" width="100">
                <template #default="scope">
                  {{ scope.row.fee ? `¥${scope.row.fee}` : '-' }}
                </template>
              </el-table-column>
              <el-table-column prop="payment_status" label="支付状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.payment_status === 'paid' ? 'success' : 'warning'">
                    {{ scope.row.payment_status === 'paid' ? '已支付' : '未支付' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="scope">
                  <el-button size="small" type="success" @click="payRecord(scope.row)" v-if="scope.row.payment_status === 'unpaid'">
                    <el-icon><i-ep-money /></el-icon>
                    支付
                  </el-button>
                  <el-button size="small" type="primary" @click="exitRecord(scope.row)" v-if="!scope.row.exit_time">
                    <el-icon><i-ep-top-right /></el-icon>
                    出场
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination" v-if="recordTotal > 0">
              <el-pagination
                v-model:current-page="recordPage"
                v-model:page-size="recordPageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="recordTotal"
                @size-change="handleRecordSizeChange"
                @current-change="handleRecordCurrentChange"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="停车统计" name="statistics">
            <el-row :gutter="20" class="mb-4">
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #409EFF">
                      <el-icon><i-ep-data-line /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总停车次数</div>
                      <div class="stat-value">{{ statistics.total_count }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #67C23A">
                      <el-icon><i-ep-timer /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总停车时长</div>
                      <div class="stat-value">{{ statistics.total_hours }} 小时</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #E6A23C">
                      <el-icon><i-ep-money /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总停车费用</div>
                      <div class="stat-value">¥{{ statistics.total_fee }}</div>
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
                      <div class="stat-label">待支付费用</div>
                      <div class="stat-value">¥{{ statistics.unpaid_fee }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </el-tab-pane>
        </el-tabs>
      </el-card>
      
      <el-dialog
        v-model="spaceDialogVisible"
        :title="spaceDialogTitle"
        width="500px"
      >
        <el-form :model="spaceForm" :rules="spaceRules" ref="spaceFormRef" label-width="100px" status-icon>
          <el-form-item label="车位编码" prop="space_code">
            <el-input v-model="spaceForm.space_code" placeholder="请输入车位编码" />
          </el-form-item>
          <el-form-item label="车位名称" prop="space_name">
            <el-input v-model="spaceForm.space_name" placeholder="请输入车位名称" />
          </el-form-item>
          <el-form-item label="车位类型" prop="type">
            <el-select v-model="spaceForm.type" placeholder="选择车位类型">
              <el-option label="地下车位" value="underground" />
              <el-option label="地面车位" value="ground" />
              <el-option label="访客车位" value="visitor" />
            </el-select>
          </el-form-item>
          <el-form-item label="位置描述" prop="location">
            <el-input v-model="spaceForm.location" placeholder="请输入位置描述" />
          </el-form-item>
          <el-form-item label="月租金" prop="price">
            <el-input-number v-model="spaceForm.price" :min="0" :precision="2" placeholder="请输入月租金" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="spaceForm.status" placeholder="选择状态">
              <el-option label="空闲" value="free" />
              <el-option label="占用" value="occupied" />
              <el-option label="预订" value="reserved" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="spaceDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveSpace">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="vehicleDialogVisible"
        :title="vehicleDialogTitle"
        width="500px"
      >
        <el-form :model="vehicleForm" :rules="vehicleRules" ref="vehicleFormRef" label-width="100px" status-icon>
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
            <el-input v-model="vehicleForm.car_color" placeholder="请输入颜色" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="vehicleForm.status" placeholder="选择状态">
              <el-option label="正常" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="vehicleDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveVehicle">保存</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const activeTab = ref('spaces')
const spaces = ref([])
const vehicles = ref([])
const records = ref([])
const statistics = ref({
  total_count: 0,
  total_hours: 0,
  total_fee: 0,
  unpaid_fee: 0
})

const spacePage = ref(1)
const spacePageSize = ref(20)
const spaceTotal = ref(0)

const vehiclePage = ref(1)
const vehiclePageSize = ref(20)
const vehicleTotal = ref(0)

const recordPage = ref(1)
const recordPageSize = ref(20)
const recordTotal = ref(0)

const recordSearchForm = ref({
  car_number: '',
  payment_status: ''
})

const spaceDialogVisible = ref(false)
const spaceDialogTitle = ref('新增车位')
const spaceForm = ref({
  space_code: '',
  space_name: '',
  type: 'underground',
  location: '',
  price: 0,
  status: 'free'
})

const vehicleDialogVisible = ref(false)
const vehicleDialogTitle = ref('新增车辆')
const vehicleForm = ref({
  car_number: '',
  car_brand: '',
  car_model: '',
  car_color: '',
  status: 'active'
})

const spaceRules = {
  space_code: [{ required: true, message: '请输入车位编码', trigger: 'blur' }],
  space_name: [{ required: true, message: '请输入车位名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择车位类型', trigger: 'change' }],
  location: [{ required: true, message: '请输入位置描述', trigger: 'blur' }]
}

const vehicleRules = {
  car_number: [{ required: true, message: '请输入车牌号', trigger: 'blur' }]
}

const handleTabChange = (tab) => {
  if (tab === 'spaces') {
    loadSpaces()
  } else if (tab === 'vehicles') {
    loadVehicles()
  } else if (tab === 'records') {
    loadRecords()
  } else if (tab === 'statistics') {
    loadStatistics()
  }
}

const loadSpaces = async () => {
  try {
    const response = await axios.get('/api/v1/pc/parking/spaces', {
      params: {
        page: spacePage.value,
        pageSize: spacePageSize.value
      }
    })
    spaces.value = response.data.data.list
    spaceTotal.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载车位列表失败')
  }
}

const loadVehicles = async () => {
  try {
    const response = await axios.get('/api/v1/pc/parking/vehicles', {
      params: {
        page: vehiclePage.value,
        pageSize: vehiclePageSize.value
      }
    })
    vehicles.value = response.data.data.list
    vehicleTotal.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载车辆列表失败')
  }
}

const loadRecords = async () => {
  try {
    const response = await axios.get('/api/v1/pc/parking/records', {
      params: {
        page: recordPage.value,
        pageSize: recordPageSize.value,
        ...recordSearchForm.value
      }
    })
    records.value = response.data.data.list
    recordTotal.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载停车记录失败')
  }
}

const loadStatistics = async () => {
  try {
    const response = await axios.get('/api/v1/pc/parking/statistics')
    statistics.value = response.data.data
  } catch (error) {
    ElMessage.error('加载停车统计失败')
  }
}

const openSpaceDialog = () => {
  spaceDialogTitle.value = '新增车位'
  spaceForm.value = {
    space_code: '',
    space_name: '',
    type: 'underground',
    location: '',
    price: 0,
    status: 'free'
  }
  spaceDialogVisible.value = true
}

const editSpace = (space) => {
  spaceDialogTitle.value = '编辑车位'
  spaceForm.value = { ...space }
  spaceDialogVisible.value = true
}

const saveSpace = async () => {
  try {
    if (spaceDialogTitle.value === '新增车位') {
      await axios.post('/api/v1/pc/parking/spaces', spaceForm.value)
      ElMessage.success('新增车位成功')
    } else {
      await axios.put(`/api/v1/pc/parking/spaces/${spaceForm.value.id}`, spaceForm.value)
      ElMessage.success('更新车位成功')
    }
    spaceDialogVisible.value = false
    loadSpaces()
  } catch (error) {
    ElMessage.error('保存车位失败')
  }
}

const deleteSpace = async (id) => {
  try {
    await axios.delete(`/api/v1/pc/parking/spaces/${id}`)
    ElMessage.success('删除车位成功')
    loadSpaces()
  } catch (error) {
    ElMessage.error('删除车位失败')
  }
}

const openVehicleDialog = () => {
  vehicleDialogTitle.value = '新增车辆'
  vehicleForm.value = {
    car_number: '',
    car_brand: '',
    car_model: '',
    car_color: '',
    status: 'active'
  }
  vehicleDialogVisible.value = true
}

const editVehicle = (vehicle) => {
  vehicleDialogTitle.value = '编辑车辆'
  vehicleForm.value = { ...vehicle }
  vehicleDialogVisible.value = true
}

const saveVehicle = async () => {
  try {
    if (vehicleDialogTitle.value === '新增车辆') {
      await axios.post('/api/v1/pc/parking/vehicles', vehicleForm.value)
      ElMessage.success('新增车辆成功')
    } else {
      await axios.put(`/api/v1/pc/parking/vehicles/${vehicleForm.value.id}`, vehicleForm.value)
      ElMessage.success('更新车辆成功')
    }
    vehicleDialogVisible.value = false
    loadVehicles()
  } catch (error) {
    ElMessage.error('保存车辆失败')
  }
}

const deleteVehicle = async (id) => {
  try {
    await axios.delete(`/api/v1/pc/parking/vehicles/${id}`)
    ElMessage.success('删除车辆成功')
    loadVehicles()
  } catch (error) {
    ElMessage.error('删除车辆失败')
  }
}

const searchRecords = () => {
  recordPage.value = 1
  loadRecords()
}

const resetRecordSearch = () => {
  recordSearchForm.value = {
    car_number: '',
    payment_status: ''
  }
  recordPage.value = 1
  loadRecords()
}

const payRecord = async (record) => {
  try {
    await axios.post(`/api/v1/pc/parking/records/${record.id}/pay`)
    ElMessage.success('支付成功')
    loadRecords()
  } catch (error) {
    ElMessage.error('支付失败')
  }
}

const exitRecord = async (record) => {
  try {
    await axios.post(`/api/v1/pc/parking/records/${record.id}/exit`)
    ElMessage.success('车辆出场成功')
    loadRecords()
  } catch (error) {
    ElMessage.error('车辆出场失败')
  }
}

const handleSpaceSizeChange = (size) => {
  spacePageSize.value = size
  loadSpaces()
}

const handleSpaceCurrentChange = (page) => {
  spacePage.value = page
  loadSpaces()
}

const handleVehicleSizeChange = (size) => {
  vehiclePageSize.value = size
  loadVehicles()
}

const handleVehicleCurrentChange = (page) => {
  vehiclePage.value = page
  loadVehicles()
}

const handleRecordSizeChange = (size) => {
  recordPageSize.value = size
  loadRecords()
}

const handleRecordCurrentChange = (page) => {
  recordPage.value = page
  loadRecords()
}

const getTypeTag = (type) => {
  const typeMap = {
    'underground': 'success',
    'ground': 'warning',
    'visitor': 'info'
  }
  return typeMap[type] || ''
}

const getTypeText = (type) => {
  const typeMap = {
    'underground': '地下车位',
    'ground': '地面车位',
    'visitor': '访客车位'
  }
  return typeMap[type] || type
}

const getStatusTag = (status) => {
  const statusMap = {
    'free': 'success',
    'occupied': 'danger',
    'reserved': 'warning'
  }
  return statusMap[status] || ''
}

const getStatusText = (status) => {
  const statusMap = {
    'free': '空闲',
    'occupied': '占用',
    'reserved': '预订'
  }
  return statusMap[status] || status
}

onMounted(() => {
  loadSpaces()
})
</script>

<style scoped>
.parking-management {
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
