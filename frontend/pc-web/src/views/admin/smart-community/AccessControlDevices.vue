<template>
  <AdminLayout>
    <div class="access-control-devices">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>门禁设备管理</h3>
            <div class="header-actions">
              <el-button type="success" @click="refreshDeviceStatus" size="small">
                <el-icon><i-ep-refresh /></el-icon>
                刷新状态
              </el-button>
              <el-button type="primary" @click="openAddDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增设备
              </el-button>
            </div>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="楼栋">
              <el-select v-model="searchForm.building_id" placeholder="选择楼栋">
                <el-option 
                  v-for="building in buildings" 
                  :key="building.id" 
                  :label="building.name" 
                  :value="building.id" 
                />
              </el-select>
            </el-form-item>
            <el-form-item label="设备类型">
              <el-select v-model="searchForm.device_type" placeholder="选择设备类型">
                <el-option label="人脸识别" value="face" />
                <el-option label="密码锁" value="password" />
                <el-option label="刷卡" value="card" />
                <el-option label="二维码" value="qrcode" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="正常" value="normal" />
                <el-option label="异常" value="abnormal" />
                <el-option label="离线" value="offline" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchDevices">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="devices" style="width: 100%">
          <el-table-column prop="id" label="设备ID" width="80" />
          <el-table-column prop="device_code" label="设备编码" width="150" />
          <el-table-column prop="device_name" label="设备名称" />
          <el-table-column prop="device_type" label="设备类型" width="120">
            <template #default="scope">
              <el-tag :type="getDeviceTypeTag(scope.row.device_type)">
                {{ getDeviceTypeText(scope.row.device_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="building_name" label="所属楼栋" />
          <el-table-column prop="location" label="安装位置" />
          <el-table-column prop="ip_address" label="IP地址" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button size="small" type="primary" @click="remoteOpen(scope.row.id, scope.row.device_name)" :disabled="scope.row.status !== 'normal'">
                <el-icon><i-ep-unlock /></el-icon>
                远程开门
              </el-button>
              <el-button size="small" @click="openEditDialog(scope.row)">
                <el-icon><i-ep-edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="deleteDevice(scope.row.id)">
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
      </el-card>
      
      <!-- 新增/编辑设备对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
      >
        <el-form :model="deviceForm" :rules="deviceRules" ref="deviceFormRef" label-width="100px" status-icon>
          <el-form-item label="设备编码" prop="device_code">
            <el-input v-model="deviceForm.device_code" placeholder="请输入设备编码" />
          </el-form-item>
          <el-form-item label="设备名称" prop="device_name">
            <el-input v-model="deviceForm.device_name" placeholder="请输入设备名称" />
          </el-form-item>
          <el-form-item label="设备类型" prop="device_type">
            <el-select v-model="deviceForm.device_type" placeholder="选择设备类型">
              <el-option label="人脸识别" value="face" />
              <el-option label="密码锁" value="password" />
              <el-option label="刷卡" value="card" />
              <el-option label="二维码" value="qrcode" />
            </el-select>
          </el-form-item>
          <el-form-item label="所属楼栋" prop="building_id">
            <el-select v-model="deviceForm.building_id" placeholder="选择楼栋">
              <el-option 
                v-for="building in buildings" 
                :key="building.id" 
                :label="building.name" 
                :value="building.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="安装位置" prop="location">
            <el-input v-model="deviceForm.location" placeholder="请输入安装位置" />
          </el-form-item>
          <el-form-item label="IP地址" prop="ip_address">
            <el-input v-model="deviceForm.ip_address" placeholder="请输入IP地址" />
          </el-form-item>
          <el-form-item label="状态" prop="status" v-if="dialogType === 'edit'">
            <el-select v-model="deviceForm.status" placeholder="选择状态">
              <el-option label="正常" value="normal" />
              <el-option label="异常" value="abnormal" />
              <el-option label="离线" value="offline" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveDevice">保存</el-button>
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

const devices = ref([])
const buildings = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  building_id: '',
  device_type: '',
  status: ''
})
const dialogVisible = ref(false)
const dialogType = ref('add')
const dialogTitle = computed(() => dialogType.value === 'add' ? '新增设备' : '编辑设备')
const deviceForm = ref({
  device_code: '',
  device_name: '',
  device_type: '',
  building_id: '',
  location: '',
  ip_address: '',
  status: 'normal'
})
const deviceRules = ref({
  device_code: [{ required: true, message: '请输入设备编码', trigger: 'blur' }],
  device_name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  device_type: [{ required: true, message: '请选择设备类型', trigger: 'change' }],
  building_id: [{ required: true, message: '请选择所属楼栋', trigger: 'change' }],
  location: [{ required: true, message: '请输入安装位置', trigger: 'blur' }],
  ip_address: [{ required: true, message: '请输入IP地址', trigger: 'blur' }]
})
const deviceFormRef = ref(null)

// 获取设备类型文本
const getDeviceTypeText = (type) => {
  const types = {
    'face': '人脸识别',
    'password': '密码锁',
    'card': '刷卡',
    'qrcode': '二维码'
  }
  return types[type] || type
}

// 获取设备类型标签样式
const getDeviceTypeTag = (type) => {
  const tags = {
    'face': 'primary',
    'password': 'success',
    'card': 'warning',
    'qrcode': 'info'
  }
  return tags[type] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const statuses = {
    'normal': '正常',
    'abnormal': '异常',
    'offline': '离线'
  }
  return statuses[status] || status
}

// 获取状态标签样式
const getStatusTag = (status) => {
  const tags = {
    'normal': 'success',
    'abnormal': 'danger',
    'offline': 'warning'
  }
  return tags[status] || 'default'
}

// 加载楼栋列表
const loadBuildings = async () => {
  try {
    const response = await fetch('/api/v1/pc/building/list', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    console.log('加载楼栋列表响应:', response)
    const result = await response.json()
    console.log('加载楼栋列表数据:', result)
    if (result.code === 0) {
      buildings.value = result.data
    }
  } catch (error) {
    console.error('加载楼栋列表失败:', error)
  }
}

// 加载设备列表
const loadDevices = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.building_id) params.append('building_id', searchForm.value.building_id)
    if (searchForm.value.device_type) params.append('type', searchForm.value.device_type)
    if (searchForm.value.status) params.append('status', searchForm.value.status)
    
    const response = await fetch(`http://localhost:8081/api/v1/pc/access/devices?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      devices.value = result.data
      total.value = result.data.length
    }
  } catch (error) {
    console.error('加载设备列表失败:', error)
    ElMessage.error('加载设备列表失败，请检查网络连接或服务是否运行')
  }
}

// 搜索设备
const searchDevices = () => {
  page.value = 1
  loadDevices()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    building_id: '',
    device_type: '',
    status: ''
  }
  page.value = 1
  loadDevices()
}

// 打开新增对话框
const openAddDialog = () => {
  dialogType.value = 'add'
  deviceForm.value = {
    device_code: '',
    device_name: '',
    device_type: '',
    building_id: '',
    location: '',
    ip_address: '',
    status: 'normal'
  }
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (device) => {
  dialogType.value = 'edit'
  deviceForm.value = { ...device }
  dialogVisible.value = true
}

// 保存设备
const saveDevice = async () => {
  if (!deviceFormRef.value) return
  
  try {
    await deviceFormRef.value.validate()
    
    const url = dialogType.value === 'add' 
      ? 'http://localhost:8081/api/v1/pc/access/devices' 
      : `http://localhost:8081/api/v1/pc/access/devices/${deviceForm.value.id}`
    
    const method = dialogType.value === 'add' ? 'POST' : 'PUT'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(deviceForm.value)
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success(dialogType.value === 'add' ? '新增设备成功' : '编辑设备成功')
      dialogVisible.value = false
      loadDevices()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存设备失败:', error)
    ElMessage.error('保存设备失败，请检查网络连接或服务是否运行')
  }
}

// 删除设备
const deleteDevice = async (deviceId) => {
  try {
    if (confirm('确定要删除该设备吗？')) {
      const response = await fetch(`http://localhost:8081/api/v1/pc/access/devices/${deviceId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('删除设备成功')
        loadDevices()
      } else {
        ElMessage.error(result.msg || '删除失败')
      }
    }
  } catch (error) {
    console.error('删除设备失败:', error)
    ElMessage.error('删除设备失败，请检查网络连接或服务是否运行')
  }
}

// 远程开门
const remoteOpen = async (deviceId, deviceName) => {
  try {
    if (confirm(`确定要远程开启 ${deviceName} 吗？`)) {
      const response = await fetch('http://localhost:8081/api/v1/pc/access/remote-open', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ device_id: deviceId })
      })
      
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('开门指令已发送')
      } else {
        ElMessage.error(result.msg || '操作失败')
      }
    }
  } catch (error) {
    console.error('远程开门失败:', error)
    ElMessage.error('远程开门失败，请检查网络连接或服务是否运行')
  }
}

// 刷新设备状态
const refreshDeviceStatus = async () => {
  try {
    ElMessage.loading('正在刷新设备状态...')
    await loadDevices()
    ElMessage.success('设备状态刷新成功')
  } catch (error) {
    console.error('刷新设备状态失败:', error)
    ElMessage.error('刷新设备状态失败，请检查网络连接或服务是否运行')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadDevices()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadDevices()
}

onMounted(() => {
  loadBuildings()
  loadDevices()
})
</script>

<style scoped>
.access-control-devices {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
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

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>