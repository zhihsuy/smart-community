<template>
  <AdminLayout>
    <div class="repair-technicians">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>维修人员管理</h3>
            <el-button type="primary" @click="openAddDialog">
              <el-icon><i-ep-plus /></el-icon>
              新增维修人员
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="姓名">
              <el-input v-model="searchForm.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="专业技能">
              <el-select v-model="searchForm.specialty" placeholder="选择专业技能">
                <el-option label="水电维修" value="water_elec" />
                <el-option label="木工" value="carpentry" />
                <el-option label="电工" value="electrician" />
                <el-option label="管道工" value="plumber" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="在线" value="online" />
                <el-option label="离线" value="offline" />
                <el-option label="忙碌" value="busy" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchTechnicians">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="technicians" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="phone" label="联系电话" width="150" />
          <el-table-column prop="specialty" label="专业技能" width="120">
            <template #default="scope">
              <el-tag :type="getSpecialtyTag(scope.row.specialty)">
                {{ getSpecialtyText(scope.row.specialty) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="experience" label="工作经验" width="100" />
          <el-table-column prop="rating" label="评分" width="100">
            <template #default="scope">
              <el-rate v-model="scope.row.rating" disabled />
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="openEditDialog(scope.row)">
                <el-icon><i-ep-edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="deleteTechnician(scope.row.id)">
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
      
      <!-- 新增/编辑维修人员对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
      >
        <el-form :model="technicianForm" :rules="technicianRules" ref="technicianFormRef" label-width="100px">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="technicianForm.name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="technicianForm.phone" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="专业技能" prop="specialty">
            <el-select v-model="technicianForm.specialty" placeholder="选择专业技能">
              <el-option label="水电维修" value="water_elec" />
              <el-option label="木工" value="carpentry" />
              <el-option label="电工" value="electrician" />
              <el-option label="管道工" value="plumber" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="工作经验" prop="experience">
            <el-input v-model="technicianForm.experience" type="number" placeholder="请输入工作经验（年）" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="technicianForm.status" placeholder="选择状态">
              <el-option label="在线" value="online" />
              <el-option label="离线" value="offline" />
              <el-option label="忙碌" value="busy" />
            </el-select>
          </el-form-item>
          <el-form-item label="备注">
            <el-input
              v-model="technicianForm.remark"
              type="textarea"
              placeholder="请输入备注信息"
              rows="3"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveTechnician">保存</el-button>
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

const technicians = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  name: '',
  specialty: '',
  status: ''
})
const dialogVisible = ref(false)
const dialogType = ref('add')
const dialogTitle = computed(() => dialogType.value === 'add' ? '新增维修人员' : '编辑维修人员')
const technicianForm = ref({
  name: '',
  phone: '',
  specialty: '',
  experience: 1,
  status: 'online',
  remark: ''
})
const technicianRules = ref({
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  specialty: [{ required: true, message: '请选择专业技能', trigger: 'change' }],
  experience: [{ required: true, message: '请输入工作经验', trigger: 'blur' }]
})
const technicianFormRef = ref(null)

// 获取专业技能文本
const getSpecialtyText = (specialty) => {
  const specialties = {
    'water_elec': '水电维修',
    'carpentry': '木工',
    'electrician': '电工',
    'plumber': '管道工',
    'other': '其他'
  }
  return specialties[specialty] || specialty
}

// 获取专业技能标签样式
const getSpecialtyTag = (specialty) => {
  const tags = {
    'water_elec': 'primary',
    'carpentry': 'success',
    'electrician': 'warning',
    'plumber': 'info',
    'other': 'default'
  }
  return tags[specialty] || 'default'
}

// 获取状态文本
const getStatusText = (status) => {
  const statuses = {
    'online': '在线',
    'offline': '离线',
    'busy': '忙碌'
  }
  return statuses[status] || status
}

// 获取状态标签样式
const getStatusTag = (status) => {
  const tags = {
    'online': 'success',
    'offline': 'danger',
    'busy': 'warning'
  }
  return tags[status] || 'default'
}

// 加载维修人员列表
const loadTechnicians = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.status) params.append('status', searchForm.value.status)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`/api/v1/pc/repair/technicians?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    console.log('加载维修人员列表响应:', result)
    if (result.code === 0) {
      technicians.value = result.data.list
      total.value = result.data.total
    }
  } catch (error) {
    console.error('加载维修人员列表失败:', error)
    ElMessage.error('加载维修人员列表失败')
  }
}

// 搜索维修人员
const searchTechnicians = () => {
  page.value = 1
  loadTechnicians()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    name: '',
    specialty: '',
    status: ''
  }
  page.value = 1
  loadTechnicians()
}

// 打开新增对话框
const openAddDialog = () => {
  dialogType.value = 'add'
  technicianForm.value = {
    name: '',
    phone: '',
    specialty: '',
    experience: 1,
    status: 'online',
    remark: ''
  }
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (technician) => {
  dialogType.value = 'edit'
  technicianForm.value = { ...technician }
  dialogVisible.value = true
}

// 保存维修人员
const saveTechnician = async () => {
  if (!technicianFormRef.value) return
  
  try {
    await technicianFormRef.value.validate()
    
    const url = dialogType.value === 'add' 
      ? '/api/v1/pc/repair/technicians' 
      : `/api/v1/pc/repair/technicians/${technicianForm.value.id}`
    
    const method = dialogType.value === 'add' ? 'POST' : 'PUT'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(technicianForm.value)
    })
    
    const result = await response.json()
    console.log('保存维修人员响应:', result)
    if (result.code === 0) {
      ElMessage.success(dialogType.value === 'add' ? '新增维修人员成功' : '编辑维修人员成功')
      dialogVisible.value = false
      loadTechnicians()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存维修人员失败:', error)
    ElMessage.error('保存维修人员失败')
  }
}

// 删除维修人员
const deleteTechnician = async (technicianId) => {
  try {
    if (confirm('确定要删除该维修人员吗？')) {
      const response = await fetch(`/api/v1/pc/repair/technicians/${technicianId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      const result = await response.json()
      console.log('删除维修人员响应:', result)
      if (result.code === 0) {
        ElMessage.success('删除维修人员成功')
        loadTechnicians()
      } else {
        ElMessage.error(result.msg || '删除失败')
      }
    }
  } catch (error) {
    console.error('删除维修人员失败:', error)
    ElMessage.error('删除维修人员失败')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadTechnicians()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadTechnicians()
}

onMounted(() => {
  loadTechnicians()
})
</script>

<style scoped>
.repair-technicians {
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

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>