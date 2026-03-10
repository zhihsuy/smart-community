<template>
  <AdminLayout>
    <div class="locker">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>快递柜管理</h3>
            <el-button type="primary" @click="openAddDialog">
              <el-icon><i-ep-plus /></el-icon>
              新增柜子
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="柜子编号">
              <el-input v-model="searchForm.locker_code" placeholder="请输入柜子编号" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="空闲" value="free" />
                <el-option label="占用" value="occupied" />
                <el-option label="故障" value="fault" />
                <el-option label="维护中" value="maintenance" />
              </el-select>
            </el-form-item>
            <el-form-item label="位置">
              <el-input v-model="searchForm.location" placeholder="请输入位置" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchLockers">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="lockers" style="width: 100%">
          <el-table-column prop="id" label="柜子ID" width="80" />
          <el-table-column prop="locker_code" label="柜子编号" width="150" />
          <el-table-column prop="location" label="位置" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="capacity" label="容量" width="100" />
          <el-table-column prop="used_slots" label="已用格口" width="100" />
          <el-table-column prop="free_slots" label="空闲格口" width="100" />
          <el-table-column prop="last_maintenance" label="最后维护" width="180" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="viewLocker(scope.row)">
                <el-icon><i-ep-view /></el-icon>
                查看
              </el-button>
              <el-button size="small" @click="openEditDialog(scope.row)">
                <el-icon><i-ep-edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="deleteLocker(scope.row.id)">
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
        
        <!-- 统计信息 -->
        <div class="statistics-card mt-4">
          <h4>快递柜统计</h4>
          <div class="statistics-grid">
            <div class="stat-item">
              <div class="stat-value">{{ totalLockers }}</div>
              <div class="stat-label">总柜子数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ freeLockers }}</div>
              <div class="stat-label">空闲柜子</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ occupiedLockers }}</div>
              <div class="stat-label">占用柜子</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ faultLockers }}</div>
              <div class="stat-label">故障柜子</div>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- 新增/编辑柜子对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
      >
        <el-form :model="lockerForm" :rules="lockerRules" ref="lockerFormRef" label-width="100px">
          <el-form-item label="柜子编号" prop="locker_code">
            <el-input v-model="lockerForm.locker_code" placeholder="请输入柜子编号" />
          </el-form-item>
          <el-form-item label="位置" prop="location">
            <el-input v-model="lockerForm.location" placeholder="请输入柜子位置" />
          </el-form-item>
          <el-form-item label="容量" prop="capacity">
            <el-input-number v-model="lockerForm.capacity" :min="1" :max="100" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="lockerForm.status" placeholder="选择状态">
              <el-option label="空闲" value="free" />
              <el-option label="占用" value="occupied" />
              <el-option label="故障" value="fault" />
              <el-option label="维护中" value="maintenance" />
            </el-select>
          </el-form-item>
          <el-form-item label="备注">
            <el-input
              v-model="lockerForm.remark"
              type="textarea"
              placeholder="请输入备注信息"
              rows="3"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveLocker">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 柜子详情对话框 -->
      <el-dialog
        v-model="detailDialogVisible"
        title="柜子详情"
        width="600px"
      >
        <div v-if="currentLocker" class="locker-detail">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="柜子ID">{{ currentLocker.id }}</el-descriptions-item>
            <el-descriptions-item label="柜子编号">{{ currentLocker.locker_code }}</el-descriptions-item>
            <el-descriptions-item label="位置">{{ currentLocker.location }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusTag(currentLocker.status)">{{ getStatusText(currentLocker.status) }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="容量">{{ currentLocker.capacity }} 格口</el-descriptions-item>
            <el-descriptions-item label="已用格口">{{ currentLocker.used_slots }} 个</el-descriptions-item>
            <el-descriptions-item label="空闲格口">{{ currentLocker.free_slots }} 个</el-descriptions-item>
            <el-descriptions-item label="使用率">{{ Math.round((currentLocker.used_slots / currentLocker.capacity) * 100) }}%</el-descriptions-item>
            <el-descriptions-item label="最后维护">{{ currentLocker.last_maintenance || '未维护' }}</el-descriptions-item>
            <el-descriptions-item label="安装时间">{{ currentLocker.install_date || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">{{ currentLocker.remark || '无' }}</el-descriptions-item>
          </el-descriptions>
          
          <!-- 格口状态 -->
          <div class="slots-status mt-4">
            <h4>格口状态</h4>
            <div class="slots-grid">
              <div 
                v-for="slot in generateSlots(currentLocker.capacity)" 
                :key="slot"
                class="slot-item"
                :class="{ 'free': slot <= currentLocker.free_slots, 'occupied': slot > currentLocker.free_slots }"
              >
                {{ slot }}
              </div>
            </div>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="detailDialogVisible = false">关闭</el-button>
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

const lockers = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  locker_code: '',
  status: '',
  location: ''
})
const dialogVisible = ref(false)
const detailDialogVisible = ref(false)
const dialogType = ref('add')
const dialogTitle = computed(() => dialogType.value === 'add' ? '新增柜子' : '编辑柜子')
const lockerForm = ref({
  locker_code: '',
  location: '',
  capacity: 20,
  status: 'free',
  remark: ''
})
const lockerRules = ref({
  locker_code: [{ required: true, message: '请输入柜子编号', trigger: 'blur' }],
  location: [{ required: true, message: '请输入柜子位置', trigger: 'blur' }],
  capacity: [{ required: true, message: '请输入容量', trigger: 'blur' }]
})
const lockerFormRef = ref(null)
const currentLocker = ref(null)

// 统计数据
const totalLockers = computed(() => total.value)
const freeLockers = computed(() => lockers.value.filter(l => l.status === 'free').length)
const occupiedLockers = computed(() => lockers.value.filter(l => l.status === 'occupied').length)
const faultLockers = computed(() => lockers.value.filter(l => l.status === 'fault').length)

// 获取状态文本
const getStatusText = (status) => {
  const statuses = {
    'free': '空闲',
    'occupied': '占用',
    'fault': '故障',
    'maintenance': '维护中'
  }
  return statuses[status] || status
}

// 获取状态标签样式
const getStatusTag = (status) => {
  const tags = {
    'free': 'success',
    'occupied': 'danger',
    'fault': 'warning',
    'maintenance': 'info'
  }
  return tags[status] || 'default'
}

// 生成格口数组
const generateSlots = (capacity) => {
  return Array.from({ length: capacity }, (_, i) => i + 1)
}

// 加载柜子列表
const loadLockers = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.locker_code) params.append('locker_code', searchForm.value.locker_code)
    if (searchForm.value.status) params.append('status', searchForm.value.status)
    if (searchForm.value.location) params.append('location', searchForm.value.location)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`/api/v1/admin/locker/cabinets?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      lockers.value = result.data.list
      total.value = result.data.total
    }
  } catch (error) {
    console.error('加载柜子列表失败:', error)
    ElMessage.error('加载柜子列表失败')
  }
}

// 搜索柜子
const searchLockers = () => {
  page.value = 1
  loadLockers()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    locker_code: '',
    status: '',
    location: ''
  }
  page.value = 1
  loadLockers()
}

// 打开新增对话框
const openAddDialog = () => {
  dialogType.value = 'add'
  lockerForm.value = {
    locker_code: '',
    location: '',
    capacity: 20,
    status: 'free',
    remark: ''
  }
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (locker) => {
  dialogType.value = 'edit'
  lockerForm.value = { ...locker }
  dialogVisible.value = true
}

// 查看柜子
const viewLocker = (locker) => {
  currentLocker.value = locker
  detailDialogVisible.value = true
}

// 保存柜子
const saveLocker = async () => {
  if (!lockerFormRef.value) return
  
  try {
    await lockerFormRef.value.validate()
    
    const url = dialogType.value === 'add' 
      ? '/api/v1/admin/locker/cabinets' 
      : `/api/v1/admin/locker/cabinets/${lockerForm.value.id}`
    
    const method = dialogType.value === 'add' ? 'POST' : 'PUT'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(lockerForm.value)
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success(dialogType.value === 'add' ? '新增柜子成功' : '编辑柜子成功')
      dialogVisible.value = false
      loadLockers()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存柜子失败:', error)
    ElMessage.error('保存柜子失败')
  }
}

// 删除柜子
const deleteLocker = async (lockerId) => {
  try {
    if (confirm('确定要删除该柜子吗？')) {
      const response = await fetch(`/api/v1/admin/locker/cabinets/${lockerId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('删除柜子成功')
        loadLockers()
      } else {
        ElMessage.error(result.msg || '删除失败')
      }
    }
  } catch (error) {
    console.error('删除柜子失败:', error)
    ElMessage.error('删除柜子失败')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadLockers()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadLockers()
}

onMounted(() => {
  loadLockers()
})
</script>

<style scoped>
.locker {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
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

.statistics-card {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
}

.statistics-card h4 {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.locker-detail {
  padding: 20px 0;
}

.slots-status {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.slots-status h4 {
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.slots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 10px;
}

.slot-item {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.slot-item.free {
  background: #f0f9eb;
  color: #67c23a;
  border: 1px solid #c2e7b0;
}

.slot-item.occupied {
  background: #fef0f0;
  color: #f56c6c;
  border: 1px solid #fbc4c4;
}

.mt-4 {
  margin-top: 20px;
}
</style>