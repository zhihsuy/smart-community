<template>
  <AdminLayout>
    <div class="access-control-permissions">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>门禁权限管理</h3>
            <el-button type="primary" @click="openAddDialog">
              <el-icon><i-ep-plus /></el-icon>
              新增权限
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="用户">
              <el-select v-model="searchForm.user_id" placeholder="选择用户">
                <el-option 
                  v-for="user in users" 
                  :key="user.id" 
                  :label="`${user.nickname} (${user.phone})`" 
                  :value="user.id" 
                />
              </el-select>
            </el-form-item>
            <el-form-item label="设备">
              <el-select v-model="searchForm.device_id" placeholder="选择设备">
                <el-option 
                  v-for="device in devices" 
                  :key="device.id" 
                  :label="`${device.device_name} (${device.device_code})`" 
                  :value="device.id" 
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchPermissions">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="permissions" style="width: 100%">
          <el-table-column prop="id" label="权限ID" width="80" />
          <el-table-column label="用户信息" width="200">
            <template #default="scope">
              <div>{{ scope.row.nickname || '未知' }}</div>
              <div class="text-xs text-gray-500">{{ scope.row.phone || '未知' }}</div>
            </template>
          </el-table-column>
          <el-table-column label="设备信息" width="200">
            <template #default="scope">
              <div>{{ scope.row.device_name || '未知' }}</div>
              <div class="text-xs text-gray-500">{{ scope.row.device_type || '未知' }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="access_type" label="权限类型" width="120">
            <template #default="scope">
              <el-tag :type="getAccessTypeTag(scope.row.access_type)">
                {{ getAccessTypeText(scope.row.access_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="access_code" label="访问码" width="150" />
          <el-table-column prop="start_time" label="开始时间" width="180" />
          <el-table-column prop="end_time" label="结束时间" width="180" />
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="scope">
              <el-button size="small" type="danger" @click="deletePermission(scope.row.id)">
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
      
      <!-- 新增权限对话框 -->
      <el-dialog
        v-model="dialogVisible"
        title="新增权限"
        width="500px"
      >
        <el-form :model="permissionForm" :rules="permissionRules" ref="permissionFormRef" label-width="100px" status-icon>
          <el-form-item label="用户" prop="user_id">
            <el-select v-model="permissionForm.user_id" placeholder="选择用户">
              <el-option 
                v-for="user in users" 
                :key="user.id" 
                :label="`${user.nickname} (${user.phone})`" 
                :value="user.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="设备" prop="device_id">
            <el-select v-model="permissionForm.device_id" placeholder="选择设备">
              <el-option 
                v-for="device in devices" 
                :key="device.id" 
                :label="`${device.device_name} (${device.device_code})`" 
                :value="device.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="权限类型" prop="access_type">
            <el-select v-model="permissionForm.access_type" placeholder="选择权限类型">
              <el-option label="永久权限" value="permanent" />
              <el-option label="临时权限" value="temporary" />
              <el-option label="访客权限" value="visitor" />
            </el-select>
          </el-form-item>
          <el-form-item label="访问码" prop="access_code">
            <el-input v-model="permissionForm.access_code" placeholder="请输入访问码" />
          </el-form-item>
          <el-form-item label="开始时间" prop="start_time">
            <el-date-picker
              v-model="permissionForm.start_time"
              type="datetime"
              placeholder="选择开始时间"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="结束时间" prop="end_time">
            <el-date-picker
              v-model="permissionForm.end_time"
              type="datetime"
              placeholder="选择结束时间"
              style="width: 100%"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="savePermission">保存</el-button>
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

const permissions = ref([])
const users = ref([])
const devices = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  user_id: '',
  device_id: ''
})
const dialogVisible = ref(false)
const permissionForm = ref({
  user_id: '',
  device_id: '',
  access_type: 'permanent',
  access_code: '',
  start_time: new Date(),
  end_time: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000) // 默认1年
})
const permissionRules = ref({
  user_id: [{ required: true, message: '请选择用户', trigger: 'change' }],
  device_id: [{ required: true, message: '请选择设备', trigger: 'change' }],
  access_type: [{ required: true, message: '请选择权限类型', trigger: 'change' }]
})
const permissionFormRef = ref(null)

// 获取权限类型文本
const getAccessTypeText = (type) => {
  const types = {
    'permanent': '永久权限',
    'temporary': '临时权限',
    'visitor': '访客权限'
  }
  return types[type] || type
}

// 获取权限类型标签样式
const getAccessTypeTag = (type) => {
  const tags = {
    'permanent': 'success',
    'temporary': 'warning',
    'visitor': 'info'
  }
  return tags[type] || 'default'
}

// 加载用户列表
const loadUsers = async () => {
  try {
    const response = await fetch('http://localhost:8081/api/v1/admin/users?page=1&pageSize=100', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      users.value = result.data.list
    }
  } catch (error) {
    console.error('加载用户列表失败:', error)
  }
}

// 加载设备列表
const loadDevices = async () => {
  try {
    const response = await fetch('http://localhost:8081/api/v1/pc/access/devices', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      devices.value = result.data
    }
  } catch (error) {
    console.error('加载设备列表失败:', error)
  }
}

// 加载权限列表
const loadPermissions = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.user_id) params.append('user_id', searchForm.value.user_id)
    if (searchForm.value.device_id) params.append('device_id', searchForm.value.device_id)
    
    const response = await fetch(`http://localhost:8081/api/v1/pc/access/permissions?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      permissions.value = result.data
      total.value = result.data.length
    }
  } catch (error) {
    console.error('加载权限列表失败:', error)
    ElMessage.error('加载权限列表失败，请检查网络连接或服务是否运行')
  }
}

// 搜索权限
const searchPermissions = () => {
  page.value = 1
  loadPermissions()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    user_id: '',
    device_id: ''
  }
  page.value = 1
  loadPermissions()
}

// 打开新增对话框
const openAddDialog = () => {
  permissionForm.value = {
    user_id: '',
    device_id: '',
    access_type: 'permanent',
    access_code: '',
    start_time: new Date(),
    end_time: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
  }
  dialogVisible.value = true
}

// 保存权限
const savePermission = async () => {
  if (!permissionFormRef.value) return
  
  try {
    await permissionFormRef.value.validate()
    
    const response = await fetch('http://localhost:8081/api/v1/pc/access/permissions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(permissionForm.value)
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('新增权限成功')
      dialogVisible.value = false
      loadPermissions()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存权限失败:', error)
    ElMessage.error('保存权限失败，请检查网络连接或服务是否运行')
  }
}

// 删除权限
const deletePermission = async (permissionId) => {
  try {
    if (confirm('确定要删除该权限吗？')) {
      const response = await fetch(`http://localhost:8081/api/v1/pc/access/permissions/${permissionId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('删除权限成功')
        loadPermissions()
      } else {
        ElMessage.error(result.msg || '删除失败')
      }
    }
  } catch (error) {
    console.error('删除权限失败:', error)
    ElMessage.error('删除权限失败，请检查网络连接或服务是否运行')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadPermissions()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadPermissions()
}

onMounted(() => {
  loadUsers()
  loadDevices()
  loadPermissions()
})
</script>

<style scoped>
.access-control-permissions {
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

.text-xs {
  font-size: 12px;
}

.text-gray-500 {
  color: #909399;
}
</style>