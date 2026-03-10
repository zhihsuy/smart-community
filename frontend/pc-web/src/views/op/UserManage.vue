<template>
  <div class="user-manage-container">
    <div class="page-header">
      <h1>用户管理</h1>
      <p>运营人员用户管理界面</p>
    </div>
    
    <div class="user-search">
      <input 
        v-model="searchParams.phone" 
        placeholder="手机号" 
        class="search-input"
      />
      <select v-model="searchParams.status" class="search-select">
        <option value="">状态</option>
        <option value="1">正常</option>
        <option value="0">禁用</option>
      </select>
      <button @click="searchUsers" class="search-btn">搜索</button>
    </div>
    
    <div class="user-table">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>手机号</th>
            <th>昵称</th>
            <th>头像</th>
            <th>角色</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.phone }}</td>
            <td>{{ user.nickname || user.phone }}</td>
            <td>
              <img v-if="user.avatar" :src="user.avatar" class="user-avatar" alt="头像" />
              <span v-else>无</span>
            </td>
            <td>{{ user.role }}</td>
            <td>{{ user.status === 1 ? '正常' : '禁用' }}</td>
            <td>{{ user.created_at }}</td>
            <td>
              <button @click="editUser(user)" class="edit-btn">编辑</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="pagination">
      <button @click="changePage(1)" :disabled="currentPage === 1">首页</button>
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">上一页</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">下一页</button>
      <button @click="changePage(totalPages)" :disabled="currentPage === totalPages">末页</button>
    </div>
    
    <!-- 编辑用户弹窗 -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>编辑用户</h3>
          <button @click="showEditModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveUser">
            <div class="form-item">
              <label>昵称</label>
              <input v-model="editUserForm.nickname" placeholder="请输入昵称" />
            </div>
            <div class="form-item">
              <label>邮箱</label>
              <input v-model="editUserForm.email" placeholder="请输入邮箱" />
            </div>
            <div class="form-item">
              <label>角色</label>
              <select v-model="editUserForm.role">
                <option value="居民">居民</option>
                <option value="运营">运营</option>
                <option value="管理员">管理员</option>
              </select>
            </div>
            <div class="form-item">
              <label>状态</label>
              <select v-model="editUserForm.status">
                <option value="1">正常</option>
                <option value="0">禁用</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" @click="showEditModal = false" class="cancel-btn">取消</button>
              <button type="submit" class="save-btn">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 状态
const users = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const searchParams = ref({ phone: '', status: '' })
const showEditModal = ref(false)
const editUserForm = ref({})

// 方法
const fetchUsers = async () => {
  try {
    const response = await axios.get('/api/v1/pc/user/op/list', {
      params: {
        page: currentPage.value,
        pageSize: 20,
        ...searchParams.value
      }
    })
    
    if (response.data.code === 0) {
      users.value = response.data.data.items
      totalPages.value = response.data.data.totalPages
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

const searchUsers = () => {
  currentPage.value = 1
  fetchUsers()
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchUsers()
  }
}

const editUser = (user) => {
  editUserForm.value = { ...user }
  showEditModal.value = true
}

const saveUser = async () => {
  try {
    const response = await axios.put(`/api/v1/pc/user/op/${editUserForm.value.id}`, editUserForm.value)
    
    if (response.data.code === 0) {
      showEditModal.value = false
      fetchUsers()
      alert('保存成功')
    }
  } catch (error) {
    console.error('保存用户失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-manage-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 24px;
  margin: 0 0 10px;
}

.page-header p {
  color: #666;
  margin: 0;
}

.user-search {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input,
.search-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-btn {
  padding: 8px 16px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.user-table {
  overflow-x: auto;
  margin-bottom: 20px;
}

.user-table table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th,
.user-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.user-table th {
  background: #f5f5f5;
  font-weight: 600;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.edit-btn {
  padding: 4px 8px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
}

.pagination button {
  padding: 4px 8px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}

.modal-header {
  padding: 16px;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 20px;
}

.form-item {
  margin-bottom: 16px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-item input,
.form-item select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.cancel-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn {
  padding: 8px 16px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>