<template>
  <AdminLayout>
    <div class="user-manage">
      <div class="page-header">
        <h2 class="page-title">👥 用户管理</h2>
        <div class="header-actions">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索用户账号/姓名/手机号"
            style="width: 300px; margin-right: 10px"
            @keyup.enter="loadUsers"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="loadUsers">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button type="success" @click="openAddDialog" style="margin-left: 10px">
            <el-icon><Plus /></el-icon>
            添加用户
          </el-button>
        </div>
      </div>

      <div class="user-table">
        <el-table :data="users" style="width: 100%">
          <el-table-column prop="id" label="用户ID" width="80" />
          <el-table-column prop="nickname" label="姓名" width="120" />
          <el-table-column prop="phone" label="手机号" width="150" />
          <el-table-column prop="role" label="角色" width="100">
            <template #default="scope">
              <el-tag :type="getRoleType(scope.row.role)">
                {{ scope.row.role }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="building_name" label="所属楼栋" width="150" />
          <el-table-column prop="created_at" label="注册时间" width="180" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                {{ scope.row.status === 'active' ? '活跃' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button
                size="small"
                type="primary"
                @click="editUser(scope.row)"
                style="margin-right: 5px"
              >
                编辑
              </el-button>
              <el-button
                size="small"
                :type="scope.row.status === 'active' ? 'danger' : 'success'"
                @click="toggleStatus(scope.row)"
              >
                {{ scope.row.status === 'active' ? '禁用' : '启用' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination" style="margin-top: 20px">
          <el-pagination
            v-model:current-page="pagination.currentPage"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 添加用户对话框 -->
      <el-dialog
        v-model="addDialogVisible"
        title="添加用户"
        width="500px"
      >
        <el-form :model="addForm" label-width="100px">
          <el-form-item label="姓名">
            <el-input v-model="addForm.nickname" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="addForm.phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="addForm.password" type="password" placeholder="请输入密码" />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="addForm.role" placeholder="请选择角色">
              <el-option label="居民" value="居民" />
              <el-option label="物业管理员" value="物业管理员" />
              <el-option label="管理员" value="管理员" />
            </el-select>
          </el-form-item>
          <el-form-item label="所属楼栋">
            <el-select v-model="addForm.building_id" placeholder="请选择楼栋">
              <el-option
                v-for="building in buildings"
                :key="building.id"
                :label="building.name"
                :value="building.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-switch
              v-model="addForm.status"
              active-value="active"
              inactive-value="inactive"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="addDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveAddUser">保存</el-button>
          </span>
        </template>
      </el-dialog>

      <!-- 编辑用户对话框 -->
      <el-dialog
        v-model="dialogVisible"
        title="编辑用户"
        width="500px"
      >
        <el-form :model="editForm" label-width="100px">
          <el-form-item label="姓名">
            <el-input v-model="editForm.nickname" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="editForm.phone" placeholder="请输入手机号" disabled />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="editForm.role" placeholder="请选择角色">
              <el-option label="居民" value="居民" />
              <el-option label="物业管理员" value="物业管理员" />
              <el-option label="管理员" value="管理员" />
            </el-select>
          </el-form-item>
          <el-form-item label="所属楼栋">
            <el-select v-model="editForm.building_id" placeholder="请选择楼栋">
              <el-option
                v-for="building in buildings"
                :key="building.id"
                :label="building.name"
                :value="building.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-switch
              v-model="editForm.status"
              active-value="active"
              inactive-value="inactive"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveUser">保存</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import AdminLayout from '@/components/AdminLayout.vue'

const users = ref([])
const buildings = ref([])
const searchKeyword = ref('')
const dialogVisible = ref(false)
const addDialogVisible = ref(false)
const editForm = ref({})
const addForm = ref({
  nickname: '',
  phone: '',
  password: '',
  role: '居民',
  building_id: '',
  status: 'active'
})

const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

const getRoleType = (role) => {
  const roleTypes = {
    '管理员': 'danger',
    '物业管理员': 'warning',
    '居民': 'success'
  }
  return roleTypes[role] || 'info'
}

const loadUsers = async () => {
  try {
    const response = await fetch(`/api/v1/admin/users?page=${pagination.value.currentPage}&pageSize=${pagination.value.pageSize}&keyword=${searchKeyword.value}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      users.value = result.data?.list || []
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载用户列表失败')
  }
}

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
      buildings.value = result.data || []
    }
  } catch (error) {
    console.error('加载楼栋列表失败:', error)
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadUsers()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadUsers()
}

const editUser = (user) => {
  editForm.value = { ...user }
  dialogVisible.value = true
}

const openAddDialog = () => {
  addForm.value = {
    nickname: '',
    phone: '',
    password: '',
    role: '居民',
    building_id: '',
    status: 'active'
  }
  addDialogVisible.value = true
}

const saveAddUser = async () => {
  try {
    const response = await fetch('/api/v1/admin/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(addForm.value)
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('添加用户成功')
      addDialogVisible.value = false
      loadUsers()
    } else {
      ElMessage.error(result.msg || '添加失败')
    }
  } catch (error) {
    console.error('添加用户失败:', error)
    ElMessage.error('添加失败')
  }
}

const saveUser = async () => {
  try {
    const response = await fetch('/api/v1/admin/users', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(editForm.value)
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('保存成功')
      dialogVisible.value = false
      loadUsers()
    } else {
      ElMessage.error(result.msg || '保存失败')
    }
  } catch (error) {
    console.error('保存用户失败:', error)
    ElMessage.error('保存失败')
  }
}

const toggleStatus = async (user) => {
  try {
    const response = await fetch(`/api/v1/admin/users/${user.id}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ status: user.status === 'active' ? 'inactive' : 'active' })
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('操作成功')
      loadUsers()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('切换状态失败:', error)
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadUsers()
  loadBuildings()
})
</script>

<style scoped>
.user-manage {
  min-height: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e4e7ed;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.header-actions {
  display: flex;
  align-items: center;
}

.user-table {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .header-actions .el-input {
    flex: 1;
    margin-right: 10px;
  }
  
  .user-table {
    padding: 10px;
  }
  
  .pagination {
    justify-content: center;
  }
}
</style>
