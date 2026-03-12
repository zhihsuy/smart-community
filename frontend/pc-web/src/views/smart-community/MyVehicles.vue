<template>
  <div class="my-vehicles-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>🚙 我的车辆</h1>
      <p class="subtitle">管理我的车辆信息</p>
    </div>

    <!-- 添加车辆按钮 -->
    <div class="add-vehicle-section">
      <el-button type="primary" @click="addVehicle">
        <el-icon><Plus /></el-icon>
        添加车辆
      </el-button>
    </div>

    <!-- 车辆列表 -->
    <el-card class="vehicles-card">
      <template #header>
        <div class="card-header">
          <span>车辆列表</span>
          <span class="total-count">共 {{ vehicles.length }} 辆</span>
        </div>
      </template>
      
      <div class="vehicles-list">
        <el-empty v-if="vehicles.length === 0" description="暂无车辆" />
        <div 
          v-for="vehicle in vehicles" 
          :key="vehicle.id"
          class="vehicle-card"
        >
          <div class="vehicle-header">
            <h3 class="plate-number">{{ vehicle.plate_number }}</h3>
            <el-dropdown>
              <el-button type="primary" size="small">
                操作
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="editVehicle(vehicle)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item @click="deleteVehicle(vehicle)" type="danger">
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-dropdown-item>
                  <el-dropdown-item @click="toggleVehicleStatus(vehicle)">
                    <el-icon>
                      <el-icon v-if="vehicle.status === 'active'"><Close /></el-icon>
                      <el-icon v-else><Check /></el-icon>
                    </el-icon>
                    {{ vehicle.status === 'active' ? '禁用' : '启用' }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          
          <div class="vehicle-info">
            <div class="info-item">
              <span class="label">车辆类型:</span>
              <span class="value">{{ vehicle.vehicle_type }}</span>
            </div>
            <div class="info-item">
              <span class="label">品牌:</span>
              <span class="value">{{ vehicle.brand }}</span>
            </div>
            <div class="info-item">
              <span class="label">型号:</span>
              <span class="value">{{ vehicle.model }}</span>
            </div>
            <div class="info-item">
              <span class="label">颜色:</span>
              <span class="value">{{ vehicle.color }}</span>
            </div>
            <div class="info-item">
              <span class="label">状态:</span>
              <el-tag :type="vehicle.status === 'active' ? 'success' : 'danger'">
                {{ vehicle.status === 'active' ? '正常' : '禁用' }}
              </el-tag>
            </div>
            <div class="info-item">
              <span class="label">是否在场:</span>
              <el-tag v-if="vehicle.is_parking" type="warning">
                在场内
              </el-tag>
              <span v-else>不在场</span>
            </div>
          </div>

          <!-- 车辆二维码 -->
          <div class="vehicle-qrcode">
            <h4>进场二维码</h4>
            <div class="qrcode-container">
              <img :src="`/api/v1/pc/parking/qrcode?vehicle_id=${vehicle.id}`" alt="进场二维码" />
            </div>
            <p class="qrcode-tip">进场时出示此二维码</p>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 添加/编辑车辆对话框 -->
    <el-dialog
      v-model="vehicleDialogVisible"
      :title="isEdit ? '编辑车辆' : '添加车辆'"
      width="500px"
    >
      <el-form :model="vehicleForm" label-width="100px" :rules="rules" ref="vehicleFormRef">
        <el-form-item label="车牌号" prop="plate_number">
          <el-input v-model="vehicleForm.plate_number" placeholder="请输入车牌号" />
        </el-form-item>
        <el-form-item label="车辆类型" prop="vehicle_type">
          <el-select v-model="vehicleForm.vehicle_type" placeholder="选择车辆类型">
            <el-option label="小型车" value="small" />
            <el-option label="中型车" value="medium" />
            <el-option label="大型车" value="large" />
            <el-option label="新能源" value="new_energy" />
          </el-select>
        </el-form-item>
        <el-form-item label="品牌" prop="brand">
          <el-input v-model="vehicleForm.brand" placeholder="请输入品牌" />
        </el-form-item>
        <el-form-item label="型号" prop="model">
          <el-input v-model="vehicleForm.model" placeholder="请输入型号" />
        </el-form-item>
        <el-form-item label="颜色" prop="color">
          <el-input v-model="vehicleForm.color" placeholder="请输入颜色" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="vehicleDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveVehicle" :loading="saving">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus, Edit, Delete, Check, Close, ArrowDown } from '@element-plus/icons-vue'

const vehicles = ref([])
const vehicleDialogVisible = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const vehicleFormRef = ref(null)
const currentVehicleId = ref(null)

const vehicleForm = ref({
  plate_number: '',
  vehicle_type: 'small',
  brand: '',
  model: '',
  color: ''
})

const rules = {
  plate_number: [{ required: true, message: '请输入车牌号', trigger: 'blur' }],
  brand: [{ required: true, message: '请输入品牌', trigger: 'blur' }],
  model: [{ required: true, message: '请输入型号', trigger: 'blur' }],
  color: [{ required: true, message: '请输入颜色', trigger: 'blur' }]
}

// 加载车辆列表
const loadVehicles = async () => {
  try {
    const response = await fetch('/api/v1/pc/parking/vehicles', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      vehicles.value = result.data || []
    }
  } catch (error) {
    console.error('加载车辆失败:', error)
    ElMessage.error('加载车辆失败')
  }
}

const addVehicle = () => {
  isEdit.value = false
  currentVehicleId.value = null
  vehicleForm.value = {
    plate_number: '',
    vehicle_type: 'small',
    brand: '',
    model: '',
    color: ''
  }
  vehicleDialogVisible.value = true
}

const editVehicle = (vehicle) => {
  isEdit.value = true
  currentVehicleId.value = vehicle.id
  vehicleForm.value = {
    plate_number: vehicle.plate_number,
    vehicle_type: vehicle.vehicle_type,
    brand: vehicle.brand,
    model: vehicle.model,
    color: vehicle.color
  }
  vehicleDialogVisible.value = true
}

const saveVehicle = async () => {
  const valid = await vehicleFormRef.value.validate().catch(() => false)
  if (!valid) return

  saving.value = true
  try {
    if (isEdit.value) {
      // 编辑车辆
      const response = await fetch(`/api/v1/pc/parking/vehicles/${currentVehicleId.value}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(vehicleForm.value)
      })
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('编辑成功')
        vehicleDialogVisible.value = false
        loadVehicles()
      } else {
        ElMessage.error(result.msg || '编辑失败')
      }
    } else {
      // 添加车辆
      const response = await fetch('/api/v1/pc/parking/vehicles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(vehicleForm.value)
      })
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('添加成功')
        vehicleDialogVisible.value = false
        loadVehicles()
      } else {
        ElMessage.error(result.msg || '添加失败')
      }
    }
  } catch (error) {
    console.error('保存车辆失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const deleteVehicle = async (vehicle) => {
  try {
    await ElMessageBox.confirm('确定要删除此车辆吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const response = await fetch(`/api/v1/pc/parking/vehicles/${vehicle.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('删除成功')
      loadVehicles()
    } else {
      ElMessage.error(result.msg || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除车辆失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const toggleVehicleStatus = async (vehicle) => {
  try {
    const response = await fetch(`/api/v1/pc/parking/vehicles/${vehicle.id}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        status: vehicle.status === 'active' ? 'inactive' : 'active'
      })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('状态更新成功')
      loadVehicles()
    } else {
      ElMessage.error(result.msg || '更新失败')
    }
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('更新失败')
  }
}

onMounted(() => {
  loadVehicles()
})
</script>

<style scoped>
.my-vehicles-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
  display: flex;
  gap: 20px;
  align-items: center;
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

.add-vehicle-section {
  margin-bottom: 20px;
  text-align: right;
}

.vehicles-card {
  border-radius: 8px;
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

.vehicles-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.vehicle-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s;
}

.vehicle-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.vehicle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.plate-number {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: #303133;
}

.vehicle-info {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 5px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.label {
  color: #909399;
  font-size: 14px;
}

.value {
  color: #303133;
  font-size: 14px;
  font-weight: 500;
}

.vehicle-qrcode {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
  text-align: center;
}

.vehicle-qrcode h4 {
  margin: 0 0 15px 0;
  font-size: 14px;
  color: #303133;
}

.qrcode-container {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.qrcode-container img {
  width: 120px;
  height: 120px;
}

.qrcode-tip {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .vehicles-list {
    grid-template-columns: 1fr;
  }
  
  .vehicle-card {
    padding: 15px;
  }
}
</style>
