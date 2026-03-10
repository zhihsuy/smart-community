<template>
  <AdminLayout>
    <div class="visitor-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>访客管理</h3>
            <el-button type="primary" @click="openAddDialog">
              <el-icon><i-ep-plus /></el-icon>
              新增访客
            </el-button>
          </div>
        </template>
        
        <div class="search-filter mb-4">
          <el-form :inline="true" :model="searchForm" class="mb-4">
            <el-form-item label="访客姓名">
              <el-input v-model="searchForm.visitor_name" placeholder="请输入访客姓名" />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="searchForm.visitor_phone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="searchForm.status" placeholder="选择状态">
                <el-option label="待审批" value="pending" />
                <el-option label="已通过" value="approved" />
                <el-option label="已拒绝" value="rejected" />
                <el-option label="已完成" value="completed" />
              </el-select>
            </el-form-item>
            <el-form-item label="访问日期">
              <el-date-picker
                v-model="searchForm.visit_date"
                type="date"
                placeholder="选择访问日期"
                style="width: 180px"
              />
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
            <el-form-item>
              <el-button type="primary" @click="searchVisitors">查询</el-button>
              <el-button @click="resetSearch">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="visitors" style="width: 100%">
          <el-table-column prop="id" label="访客ID" width="80" />
          <el-table-column prop="visitor_name" label="访客姓名" />
          <el-table-column prop="visitor_phone" label="联系电话" />
          <el-table-column prop="visitor_idcard" label="身份证号" width="180" />
          <el-table-column label="被访人" width="150">
            <template #default="scope">
              {{ scope.row.host_name }} ({{ scope.row.host_phone }})
            </template>
          </el-table-column>
          <el-table-column label="访问信息" width="250">
            <template #default="scope">
              <div>{{ scope.row.visit_date }}</div>
              <div>{{ scope.row.visit_time_start }} - {{ scope.row.visit_time_end }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="building_id" label="楼栋" />
          <el-table-column prop="room_number" label="房间号" />
          <el-table-column prop="visit_purpose" label="访问目的" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button size="small" type="primary" @click="viewVisitor(scope.row)">
                        <el-icon><i-ep-view /></el-icon>
                        查看
                      </el-button>
                      <el-button size="small" @click="openEditDialog(scope.row)">
                        <el-icon><i-ep-edit /></el-icon>
                        编辑
                      </el-button>
                      <el-button size="small" type="success" @click="createAccessPermission(scope.row)" v-if="scope.row.status === 'approved'">
                        <el-icon><i-ep-key /></el-icon>
                        权限
                      </el-button>
                      <el-button size="small" type="danger" @click="deleteVisitor(scope.row.id)">
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
      
      <!-- 新增/编辑访客对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogTitle"
        width="500px"
      >
        <el-form :model="visitorForm" :rules="visitorRules" ref="visitorFormRef" label-width="100px" status-icon>
          <el-form-item label="访客姓名" prop="visitor_name">
            <el-input v-model="visitorForm.visitor_name" placeholder="请输入访客姓名" />
          </el-form-item>
          <el-form-item label="联系电话" prop="visitor_phone">
            <el-input v-model="visitorForm.visitor_phone" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="身份证号" prop="visitor_idcard">
            <el-input v-model="visitorForm.visitor_idcard" placeholder="请输入身份证号" />
          </el-form-item>
          <el-form-item label="被访人ID" prop="host_id">
            <el-input v-model="visitorForm.host_id" placeholder="请输入被访人ID" />
          </el-form-item>
          <el-form-item label="被访人姓名" prop="host_name">
            <el-input v-model="visitorForm.host_name" placeholder="请输入被访人姓名" />
          </el-form-item>
          <el-form-item label="被访人电话" prop="host_phone">
            <el-input v-model="visitorForm.host_phone" placeholder="请输入被访人电话" />
          </el-form-item>
          <el-form-item label="楼栋" prop="building_id">
            <el-select v-model="visitorForm.building_id" placeholder="选择楼栋">
              <el-option 
                v-for="building in buildings" 
                :key="building.id" 
                :label="building.name" 
                :value="building.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="房间号" prop="room_number">
            <el-input v-model="visitorForm.room_number" placeholder="请输入房间号" />
          </el-form-item>
          <el-form-item label="访问目的" prop="visit_purpose">
            <el-input v-model="visitorForm.visit_purpose" placeholder="请输入访问目的" />
          </el-form-item>
          <el-form-item label="访问日期" prop="visit_date">
            <el-date-picker
              v-model="visitorForm.visit_date"
              type="date"
              placeholder="选择访问日期"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="开始时间" prop="visit_time_start">
            <el-time-picker
              v-model="visitorForm.visit_time_start"
              placeholder="选择开始时间"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="结束时间" prop="visit_time_end">
            <el-time-picker
              v-model="visitorForm.visit_time_end"
              placeholder="选择结束时间"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="状态" prop="status" v-if="dialogType === 'edit'">
            <el-select v-model="visitorForm.status" placeholder="选择状态">
              <el-option label="待审批" value="pending" />
              <el-option label="已通过" value="approved" />
              <el-option label="已拒绝" value="rejected" />
              <el-option label="已完成" value="completed" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveVisitor">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 访客详情对话框 -->
      <el-dialog
        v-model="detailVisible"
        title="访客详情"
        width="600px"
      >
        <el-descriptions :column="2" border>
          <el-descriptions-item label="访客ID">{{ currentVisitor.id }}</el-descriptions-item>
          <el-descriptions-item label="访客姓名">{{ currentVisitor.visitor_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentVisitor.visitor_phone }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ currentVisitor.visitor_idcard }}</el-descriptions-item>
          <el-descriptions-item label="被访人ID">{{ currentVisitor.host_id }}</el-descriptions-item>
          <el-descriptions-item label="被访人姓名">{{ currentVisitor.host_name }}</el-descriptions-item>
          <el-descriptions-item label="被访人电话">{{ currentVisitor.host_phone }}</el-descriptions-item>
          <el-descriptions-item label="楼栋">{{ currentVisitor.building_id }}</el-descriptions-item>
          <el-descriptions-item label="房间号">{{ currentVisitor.room_number }}</el-descriptions-item>
          <el-descriptions-item label="访问目的">{{ currentVisitor.visit_purpose }}</el-descriptions-item>
          <el-descriptions-item label="访问日期">{{ currentVisitor.visit_date }}</el-descriptions-item>
          <el-descriptions-item label="访问时间">{{ currentVisitor.visit_time_start }} - {{ currentVisitor.visit_time_end }}</el-descriptions-item>
          <el-descriptions-item label="二维码">{{ currentVisitor.qr_code }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusText(currentVisitor.status) }}</el-descriptions-item>
          <el-descriptions-item label="进入时间">{{ currentVisitor.entry_time }}</el-descriptions-item>
          <el-descriptions-item label="离开时间">{{ currentVisitor.exit_time }}</el-descriptions-item>
          <el-descriptions-item label="审批时间">{{ currentVisitor.approve_time }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentVisitor.created_at }}</el-descriptions-item>
        </el-descriptions>
        <div class="mt-4" v-if="currentVisitor.status === 'pending'">
          <el-button type="primary" @click="approveVisitor(currentVisitor.id)">审核通过</el-button>
          <el-button type="danger" @click="rejectVisitor(currentVisitor.id)">拒绝</el-button>
        </div>
        <div class="mt-4" v-else-if="currentVisitor.status === 'approved'">
          <el-button type="success" @click="completeVisitor(currentVisitor.id)">标记完成</el-button>
          <el-button type="primary" @click="viewAccessPermission(currentVisitor.id)">查看权限</el-button>
        </div>
      </el-dialog>
      
      <!-- 访问权限对话框 -->
      <el-dialog
        v-model="permissionVisible"
        title="访问权限"
        width="600px"
      >
        <div v-if="accessPermissions.length > 0">
          <el-table :data="accessPermissions" style="width: 100%">
            <el-table-column prop="id" label="权限ID" width="80" />
            <el-table-column prop="device_id" label="设备ID" width="100" />
            <el-table-column prop="start_time" label="开始时间" width="180" />
            <el-table-column prop="end_time" label="结束时间" width="180" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                  {{ scope.row.status === 'active' ? '有效' : '无效' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <el-empty v-else description="暂无访问权限" />
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="permissionVisible = false">关闭</el-button>
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

const visitors = ref([])
const buildings = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  visitor_name: '',
  visitor_phone: '',
  status: '',
  visit_date: '',
  building_id: ''
})
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogType = ref('add')
const dialogTitle = computed(() => dialogType.value === 'add' ? '新增访客' : '编辑访客')
const visitorForm = ref({
  visitor_name: '',
  visitor_phone: '',
  visitor_idcard: '',
  host_id: '',
  host_name: '',
  host_phone: '',
  building_id: '',
  room_number: '',
  visit_purpose: '',
  visit_date: '',
  visit_time_start: '',
  visit_time_end: '',
  status: 'pending'
})
const visitorRules = ref({
  visitor_name: [{ required: true, message: '请输入访客姓名', trigger: 'blur' }],
  visitor_phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  visitor_idcard: [{ required: true, message: '请输入身份证号', trigger: 'blur' }],
  host_id: [{ required: true, message: '请输入被访人ID', trigger: 'blur' }],
  host_name: [{ required: true, message: '请输入被访人姓名', trigger: 'blur' }],
  host_phone: [{ required: true, message: '请输入被访人电话', trigger: 'blur' }],
  building_id: [{ required: true, message: '请选择楼栋', trigger: 'change' }],
  room_number: [{ required: true, message: '请输入房间号', trigger: 'blur' }],
  visit_purpose: [{ required: true, message: '请输入访问目的', trigger: 'blur' }],
  visit_date: [{ required: true, message: '请选择访问日期', trigger: 'change' }],
  visit_time_start: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  visit_time_end: [{ required: true, message: '请选择结束时间', trigger: 'change' }]
})
const visitorFormRef = ref(null)
const currentVisitor = ref({})
const permissionVisible = ref(false)
const accessPermissions = ref([])

// 获取状态文本
const getStatusText = (status) => {
  const statuses = {
    'pending': '待审批',
    'approved': '已通过',
    'rejected': '已拒绝',
    'completed': '已完成'
  }
  return statuses[status] || status
}

// 获取状态标签样式
const getStatusTag = (status) => {
  const tags = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger',
    'completed': 'info'
  }
  return tags[status] || 'default'
}

// 加载楼栋列表
const loadBuildings = async () => {
  try {
    const response = await fetch('http://localhost:8081/api/v1/pc/building/list')
    const result = await response.json()
    if (result.code === 0) {
      buildings.value = result.data
    }
  } catch (error) {
    console.error('加载楼栋列表失败:', error)
  }
}

// 加载访客列表
const loadVisitors = async () => {
  try {
    const params = new URLSearchParams()
    if (searchForm.value.visitor_name) params.append('visitor_name', searchForm.value.visitor_name)
    if (searchForm.value.visitor_phone) params.append('visitor_phone', searchForm.value.visitor_phone)
    if (searchForm.value.status) params.append('status', searchForm.value.status)
    if (searchForm.value.visit_date) params.append('visit_date', searchForm.value.visit_date)
    if (searchForm.value.building_id) params.append('building_id', searchForm.value.building_id)
    params.append('page', page.value)
    params.append('pageSize', pageSize.value)
    
    const response = await fetch(`http://localhost:8081/api/v1/pc/visitor?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      visitors.value = result.data.list
      total.value = result.data.total
    }
  } catch (error) {
    console.error('加载访客列表失败:', error)
    ElMessage.error('加载访客列表失败，请检查网络连接或服务是否运行')
  }
}

// 搜索访客
const searchVisitors = () => {
  page.value = 1
  loadVisitors()
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    visitor_name: '',
    visitor_phone: '',
    status: '',
    visit_date: '',
    building_id: ''
  }
  page.value = 1
  loadVisitors()
}

// 打开新增对话框
const openAddDialog = () => {
  dialogType.value = 'add'
  visitorForm.value = {
    visitor_name: '',
    visitor_phone: '',
    visitor_idcard: '',
    host_id: '',
    host_name: '',
    host_phone: '',
    building_id: '',
    room_number: '',
    visit_purpose: '',
    visit_date: '',
    visit_time_start: '',
    visit_time_end: '',
    status: 'pending'
  }
  dialogVisible.value = true
}

// 打开编辑对话框
const openEditDialog = (visitor) => {
  dialogType.value = 'edit'
  visitorForm.value = { ...visitor }
  dialogVisible.value = true
}

// 查看访客详情
const viewVisitor = (visitor) => {
  currentVisitor.value = { ...visitor }
  detailVisible.value = true
}

// 保存访客
const saveVisitor = async () => {
  if (!visitorFormRef.value) return
  
  try {
    await visitorFormRef.value.validate()
    
    const url = dialogType.value === 'add' 
      ? 'http://localhost:8081/api/v1/pc/visitor' 
      : `http://localhost:8081/api/v1/pc/visitor/${visitorForm.value.id}`
    
    const method = dialogType.value === 'add' ? 'POST' : 'PUT'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(visitorForm.value)
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success(dialogType.value === 'add' ? '新增访客成功' : '编辑访客成功')
      dialogVisible.value = false
      loadVisitors()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存访客失败:', error)
    ElMessage.error('保存访客失败，请检查网络连接或服务是否运行')
  }
}

// 删除访客
const deleteVisitor = async (visitorId) => {
  try {
    if (confirm('确定要删除该访客吗？')) {
      const response = await fetch(`http://localhost:8081/api/v1/pc/visitor/${visitorId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      const result = await response.json()
      if (result.code === 0) {
        ElMessage.success('删除访客成功')
        loadVisitors()
      } else {
        ElMessage.error(result.msg || '删除失败')
      }
    }
  } catch (error) {
    console.error('删除访客失败:', error)
    ElMessage.error('删除访客失败，请检查网络连接或服务是否运行')
  }
}

// 审核通过
const approveVisitor = async (visitorId) => {
  try {
    const response = await fetch(`http://localhost:8081/api/v1/pc/visitor/${visitorId}/approve`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('审核通过')
      detailVisible.value = false
      loadVisitors()
    } else {
      ElMessage.error(result.msg || '审核失败')
    }
  } catch (error) {
    console.error('审核访客失败:', error)
    ElMessage.error('审核访客失败，请检查网络连接或服务是否运行')
  }
}

// 拒绝访客
const rejectVisitor = async (visitorId) => {
  try {
    const response = await fetch(`http://localhost:8081/api/v1/pc/visitor/${visitorId}/reject`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('拒绝成功')
      detailVisible.value = false
      loadVisitors()
    } else {
      ElMessage.error(result.msg || '拒绝失败')
    }
  } catch (error) {
    console.error('拒绝访客失败:', error)
    ElMessage.error('拒绝访客失败，请检查网络连接或服务是否运行')
  }
}

// 标记完成
const completeVisitor = async (visitorId) => {
  try {
    const response = await fetch(`http://localhost:8081/api/v1/pc/visitor/${visitorId}/complete`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('标记完成成功')
      detailVisible.value = false
      loadVisitors()
    } else {
      ElMessage.error(result.msg || '标记完成失败')
    }
  } catch (error) {
    console.error('标记访客完成失败:', error)
    ElMessage.error('标记访客完成失败，请检查网络连接或服务是否运行')
  }
}

// 创建访问权限
const createAccessPermission = async (visitor) => {
  try {
    const response = await fetch(`http://localhost:8081/api/v1/pc/visitor/${visitor.id}/access-permission`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('临时访问权限创建成功')
    } else {
      ElMessage.error(result.msg || '创建访问权限失败')
    }
  } catch (error) {
    console.error('创建访问权限失败:', error)
    ElMessage.error('创建访问权限失败，请检查网络连接或服务是否运行')
  }
}

// 查看访问权限
const viewAccessPermission = async (visitorId) => {
  try {
    const response = await fetch(`http://localhost:8081/api/v1/pc/visitor/${visitorId}/access-permission`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    const result = await response.json()
    if (result.code === 0) {
      accessPermissions.value = result.data
      permissionVisible.value = true
    } else {
      ElMessage.error(result.msg || '获取访问权限失败')
    }
  } catch (error) {
    console.error('获取访问权限失败:', error)
    ElMessage.error('获取访问权限失败，请检查网络连接或服务是否运行')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  loadVisitors()
}

const handleCurrentChange = (current) => {
  page.value = current
  loadVisitors()
}

onMounted(() => {
  loadBuildings()
  loadVisitors()
})
</script>

<style scoped>
.visitor-management {
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
