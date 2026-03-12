<template>
  <AdminLayout>
    <div class="utility-meters">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>水电表具管理</h3>
            <el-button type="primary" @click="openAddDialog">
              <el-icon><i-ep-plus /></el-icon>
              新增表具
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="表具编号">
              <el-input v-model="searchForm.meter_no" placeholder="请输入表具编号" />
            </el-form-item>
            <el-form-item label="表具类型">
              <el-select v-model="searchForm.meter_type" placeholder="选择表具类型">
                <el-option label="电表" value="electric" />
                <el-option label="水表" value="water" />
                <el-option label="燃气表" value="gas" />
              </el-select>
            </el-form-item>
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
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="正常" value="normal" />
                <el-option label="异常" value="abnormal" />
                <el-option label="离线" value="offline" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchMeters">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <div class="table-container">
          <el-table :data="meters" style="width: 100%">
            <el-table-column prop="id" label="表具ID" width="60" />
            <el-table-column prop="meter_no" label="表具编号" width="120" />
            <el-table-column prop="meter_type" label="表具类型" width="100">
              <template #default="scope">
                <el-tag :type="getMeterTypeTag(scope.row.meter_type)">
                  {{ getMeterTypeText(scope.row.meter_type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="building_name" label="所属楼栋" width="140" />
            <el-table-column prop="unit" label="单元" width="80" />
            <el-table-column prop="room_number" label="房间号" width="80" />
            <el-table-column prop="last_reading" label="上次读数" width="100" />
            <el-table-column prop="current_reading" label="当前读数" width="100" />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="scope">
                <el-tag :type="getStatusTag(scope.row.status)">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="last_update" label="最后更新" width="140" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button size="small" @click="openEditDialog(scope.row)">
                  <el-icon><i-ep-edit /></el-icon>
                  编辑
                </el-button>
                <el-button size="small" type="danger" @click="deleteMeter(scope.row.id)">
                  <el-icon><i-ep-delete /></el-icon>
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        
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
      
      <!-- 新增/编辑表具对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
      >
        <el-form :model="meterForm" :rules="meterRules" ref="meterFormRef" label-width="100px">
          <el-form-item label="表具编号" prop="meter_no">
            <el-input v-model="meterForm.meter_no" placeholder="请输入表具编号" />
          </el-form-item>
          <el-form-item label="表具类型" prop="meter_type">
            <el-select v-model="meterForm.meter_type" placeholder="选择表具类型">
              <el-option label="电表" value="electric" />
              <el-option label="水表" value="water" />
              <el-option label="燃气表" value="gas" />
            </el-select>
          </el-form-item>
          <el-form-item label="所属楼栋" prop="building_id">
            <el-select v-model="meterForm.building_id" placeholder="选择楼栋">
              <el-option 
                v-for="building in buildings" 
                :key="building.id" 
                :label="building.name" 
                :value="building.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="单元" prop="unit">
            <el-input v-model="meterForm.unit" placeholder="请输入单元" />
          </el-form-item>
          <el-form-item label="房间号" prop="room_number">
            <el-input v-model="meterForm.room_number" placeholder="请输入房间号" />
          </el-form-item>
          <el-form-item label="初始度数" prop="initial_reading">
            <el-input-number v-model="meterForm.initial_reading" :min="0" :precision="2" placeholder="请输入初始度数" />
          </el-form-item>
          <el-form-item label="安装位置" prop="location">
            <el-input v-model="meterForm.location" placeholder="请输入安装位置" />
          </el-form-item>
          <el-form-item label="安装时间" prop="install_time">
            <el-date-picker
              v-model="meterForm.install_time"
              type="date"
              placeholder="选择安装时间"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="meterForm.status" placeholder="选择状态">
              <el-option label="正常" value="normal" />
              <el-option label="异常" value="abnormal" />
              <el-option label="离线" value="offline" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveMeter">保存</el-button>
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

const meters = ref([])
const buildings = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  meter_no: '',
  meter_type: '',
  building_id: '',
  status: ''
})
const dialogVisible = ref(false)
const dialogType = ref('add')
const dialogTitle = computed(() => dialogType.value === 'add' ? '新增表具' : '编辑表具')
const meterForm = ref({
  meter_no: '',
  meter_type: 'electric',
  building_id: '',
  unit: '',
  room_number: '',
  initial_reading: 0,
  location: '',
  install_time: new Date().toISOString().split('T')[0],
  status: 'normal'
})
const meterRules = ref({
  meter_no: [{ required: true, message: '请输入表具编号', trigger: 'blur' }],
  meter_type: [{ required: true, message: '请选择表具类型', trigger: 'change' }],
  building_id: [{ required: true, message: '请选择所属楼栋', trigger: 'change' }],
  unit: [{ required: true, message: '请输入单元', trigger: 'blur' }],
  room_number: [{ required: true, message: '请输入房间号', trigger: 'blur' }]
})
const meterFormRef = ref(null)

// 获取表具类型文本
const getMeterTypeText = (type) => {
  const types = {
    'electric': '电表',
    'water': '水表',
    'gas': '燃气表'
  }
  return types[type] || type
}

// 获取表具类型标签样式
const getMeterTypeTag = (type) => {
  const tags = {
    'electric': 'primary',
    'water': 'success',
    'gas': 'warning'
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

// 加载表具列表
const loadMeters = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.meter_no) params.append('meter_no', searchForm.value.meter_no)
    if (searchForm.value.meter_type) params.append('type', searchForm.value.meter_type)
    if (searchForm.value.building_id) params.append('building_id', searchForm.value.building_id)
    if (searchForm.value.status) params.append('status', searchForm.value.status)
    
    const response = await fetch(`/api/v1/pc/utility/meters?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    console.log('加载表具列表响应:', response)
    const result = await response.json()
    console.log('加载表具列表数据:', result)
    if (result.code === 0) {
      meters.value = result.data
      total.value = result.data.length
    }
  } catch (error) {
    console.error('加载表具列表失败:', error)
    ElMessage.error('加载表具列表失败')
  }
}

// 搜索表具
const searchMeters = () => {
  page.value = 1
  loadMeters()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    meter_code: '',
    meter_type: '',
    building_id: '',
    status: ''
  }
  page.value = 1
  loadMeters()
}

// 打开新增对话框
const openAddDialog = () => {
  dialogType.value = 'add'
  meterForm.value = {
    meter_no: '',
    meter_type: 'electric',
    building_id: '',
    unit: '',
    room_number: '',
    initial_reading: 0,
    location: '',
    install_time: new Date().toISOString().split('T')[0],
    status: 'normal'
  }
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (meter) => {
  dialogType.value = 'edit'
  meterForm.value = { ...meter }
  dialogVisible.value = true
}

// 保存表具
const saveMeter = async () => {
  if (!meterFormRef.value) return
  
  try {
    await meterFormRef.value.validate()
    
    const url = dialogType.value === 'add' 
      ? '/api/v1/pc/utility/meters' 
      : `/api/v1/pc/utility/meters/${meterForm.value.id}`
    
    const method = dialogType.value === 'add' ? 'POST' : 'PUT'
    
    // 准备提交数据
    const submitData = {
      ...meterForm.value,
      user_id: 1 // 默认用户ID，实际应用中应该根据选择的房间号关联用户
    }
    
    // 转换日期格式为 MySQL DATETIME 格式
    if (submitData.install_time) {
      const installDate = new Date(submitData.install_time)
      submitData.install_time = installDate.toISOString().split('T')[0] + ' 00:00:00'
    }
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(submitData)
    })
    
    console.log('保存表具响应:', response)
    const result = await response.json()
    console.log('保存表具数据:', result)
    if (result.code === 0) {
      ElMessage.success(dialogType.value === 'add' ? '新增表具成功' : '编辑表具成功')
      dialogVisible.value = false
      loadMeters()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存表具失败:', error)
    ElMessage.error('保存表具失败')
  }
}

// 删除表具
const deleteMeter = async (meterId) => {
  try {
    if (confirm('确定要删除该表具吗？')) {
      const response = await fetch(`/api/v1/pc/utility/meters/${meterId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      console.log('删除表具响应:', response)
      const result = await response.json()
      console.log('删除表具数据:', result)
      if (result.code === 0) {
        ElMessage.success('删除表具成功')
        loadMeters()
      } else {
        ElMessage.error(result.msg || '删除失败')
      }
    }
  } catch (error) {
    console.error('删除表具失败:', error)
    ElMessage.error('删除表具失败')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadMeters()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadMeters()
}

onMounted(() => {
  loadBuildings()
  loadMeters()
})
</script>

<style scoped>
.utility-meters {
  padding: 0;
  width: 100%;
  box-sizing: border-box;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.search-filter {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow-x: auto;
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

.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
  width: 100%;
}

/* 响应式样式 */
@media (max-width: 1200px) {
  .el-table {
    font-size: 13px;
  }
  
  .el-table-column {
    white-space: nowrap;
  }
  
  .el-button {
    padding: 0 8px;
    font-size: 12px;
  }
  
  .el-button .el-icon {
    font-size: 12px;
  }
}

@media (max-width: 992px) {
  .search-filter {
    padding: 15px;
  }
  
  .el-form-item {
    margin-right: 10px;
  }
  
  .el-input {
    width: 120px;
  }
  
  .el-select {
    width: 120px;
  }
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .el-form {
    flex-wrap: wrap;
  }
  
  .el-form-item {
    margin-right: 15px;
    margin-bottom: 10px;
  }
  
  .el-table {
    font-size: 12px;
  }
  
  .el-table-column {
    min-width: 60px;
  }
}
</style>