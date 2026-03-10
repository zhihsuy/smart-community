<template>
  <AdminLayout>
    <div class="complaint-management">
      <el-card shadow="hover" class="mb-4">
        <template #header>
          <div class="card-header">
            <h3>投诉建议管理</h3>
          </div>
        </template>
        
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="投诉建议" name="complaints">
            <div class="mb-4">
              <el-button type="primary" @click="openComplaintDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增投诉建议
              </el-button>
            </div>
            
            <div class="search-filter mb-4">
              <el-form :inline="true" :model="searchForm" class="mb-4">
                <el-form-item label="状态">
                  <el-select v-model="searchForm.status" placeholder="选择状态">
                    <el-option label="全部" value="" />
                    <el-option label="待处理" value="pending" />
                    <el-option label="处理中" value="processing" />
                    <el-option label="已完成" value="completed" />
                  </el-select>
                </el-form-item>
                <el-form-item label="类型">
                  <el-select v-model="searchForm.type" placeholder="选择类型">
                    <el-option label="全部" value="" />
                    <el-option label="投诉" value="complaint" />
                    <el-option label="建议" value="suggestion" />
                  </el-select>
                </el-form-item>
                <el-form-item label="分类">
                  <el-select v-model="searchForm.category" placeholder="选择分类">
                    <el-option label="全部" value="" />
                    <el-option v-for="cat in categories" :key="cat.code" :label="cat.name" :value="cat.code" />
                  </el-select>
                </el-form-item>
                <el-form-item label="优先级">
                  <el-select v-model="searchForm.priority" placeholder="选择优先级">
                    <el-option label="全部" value="" />
                    <el-option label="高" value="high" />
                    <el-option label="中" value="medium" />
                    <el-option label="低" value="low" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="searchComplaints">查询</el-button>
                  <el-button @click="resetSearch">重置</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <el-table :data="complaints" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" />
              <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.type === 'complaint' ? 'danger' : 'success'">
                    {{ scope.row.type === 'complaint' ? '投诉' : '建议' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="category" label="分类" width="120">
                <template #default="scope">
                  {{ getCategoryName(scope.row.category) }}
                </template>
              </el-table-column>
              <el-table-column prop="user_name" label="提交人" width="120" />
              <el-table-column prop="priority" label="优先级" width="100">
                <template #default="scope">
                  <el-tag :type="getPriorityTag(scope.row.priority)">
                    {{ getPriorityText(scope.row.priority) }}
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
              <el-table-column prop="handler_name" label="处理人" width="120" />
              <el-table-column prop="created_at" label="提交时间" width="180" />
              <el-table-column label="操作" width="350" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="viewComplaint(scope.row)">
                    <el-icon><i-ep-view /></el-icon>
                    查看
                  </el-button>
                  <el-button size="small" type="primary" @click="assignHandler(scope.row)" v-if="scope.row.status === 'pending'">
                    <el-icon><i-ep-user /></el-icon>
                    指派
                  </el-button>
                  <el-button size="small" type="success" @click="handleComplaint(scope.row)" v-if="scope.row.status === 'processing'">
                    <el-icon><i-ep-check /></el-icon>
                    处理
                  </el-button>
                  <el-button size="small" type="warning" @click="submitSatisfaction(scope.row)" v-if="scope.row.status === 'completed' && !scope.row.satisfaction">
                    <el-icon><i-ep-star /></el-icon>
                    评价
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteComplaint(scope.row.id)">
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
          </el-tab-pane>
          
          <el-tab-pane label="分类管理" name="categories">
            <div class="mb-4">
              <el-button type="primary" @click="openCategoryDialog">
                <el-icon><i-ep-plus /></el-icon>
                新增分类
              </el-button>
            </div>
            
            <el-table :data="categories" style="width: 100%">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="分类名称" />
              <el-table-column prop="code" label="分类编码" />
              <el-table-column prop="description" label="描述" />
              <el-table-column prop="sort_order" label="排序" width="100" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                    {{ scope.row.status === 'active' ? '正常' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button size="small" @click="editCategory(scope.row)">
                    <el-icon><i-ep-edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteCategory(scope.row.id)">
                    <el-icon><i-ep-delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="投诉统计" name="statistics">
            <el-row :gutter="20" class="mb-4">
              <el-col :span="4">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #409EFF">
                      <el-icon><i-ep-document /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">总投诉数</div>
                      <div class="stat-value">{{ statistics.total }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #E6A23C">
                      <el-icon><i-ep-clock /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">待处理</div>
                      <div class="stat-value">{{ statistics.pending }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #67C23A">
                      <el-icon><i-ep-loading /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">处理中</div>
                      <div class="stat-value">{{ statistics.processing }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #67C23A">
                      <el-icon><i-ep-circle-check /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">已完成</div>
                      <div class="stat-value">{{ statistics.completed }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #909399">
                      <el-icon><i-ep-star /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">已评价</div>
                      <div class="stat-value">{{ statistics.evaluated }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card shadow="hover">
                  <div class="stat-card">
                    <div class="stat-icon" style="background: #F56C6C">
                      <el-icon><i-ep-trophy /></el-icon>
                    </div>
                    <div class="stat-content">
                      <div class="stat-label">平均满意度</div>
                      <div class="stat-value">{{ statistics.avg_satisfaction }}</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </el-tab-pane>
        </el-tabs>
      </el-card>
      
      <el-dialog
        v-model="complaintDialogVisible"
        :title="complaintDialogTitle"
        width="600px"
      >
        <el-form :model="complaintForm" :rules="complaintRules" ref="complaintFormRef" label-width="100px" status-icon>
          <el-form-item label="标题" prop="title">
            <el-input v-model="complaintForm.title" placeholder="请输入标题" />
          </el-form-item>
          <el-form-item label="类型" prop="type">
            <el-select v-model="complaintForm.type" placeholder="选择类型">
              <el-option label="投诉" value="complaint" />
              <el-option label="建议" value="suggestion" />
            </el-select>
          </el-form-item>
          <el-form-item label="分类" prop="category">
            <el-select v-model="complaintForm.category" placeholder="选择分类">
              <el-option v-for="cat in categories" :key="cat.code" :label="cat.name" :value="cat.code" />
            </el-select>
          </el-form-item>
          <el-form-item label="内容" prop="content">
            <el-input v-model="complaintForm.content" type="textarea" :rows="6" placeholder="请输入内容" />
          </el-form-item>
          <el-form-item label="地址" prop="address">
            <el-input v-model="complaintForm.address" placeholder="请输入地址（可选）" />
          </el-form-item>
          <el-form-item label="优先级" prop="priority">
            <el-select v-model="complaintForm.priority" placeholder="选择优先级">
              <el-option label="高" value="high" />
              <el-option label="中" value="medium" />
              <el-option label="低" value="low" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="complaintDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveComplaint">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="categoryDialogVisible"
        :title="categoryDialogTitle"
        width="500px"
      >
        <el-form :model="categoryForm" :rules="categoryRules" ref="categoryFormRef" label-width="100px" status-icon>
          <el-form-item label="分类名称" prop="name">
            <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
          </el-form-item>
          <el-form-item label="分类编码" prop="code">
            <el-input v-model="categoryForm.code" placeholder="请输入分类编码" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="categoryForm.description" type="textarea" :rows="3" placeholder="请输入描述" />
          </el-form-item>
          <el-form-item label="排序" prop="sort_order">
            <el-input-number v-model="categoryForm.sort_order" :min="0" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="categoryDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveCategory">保存</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="assignDialogVisible"
        title="指派处理人员"
        width="500px"
      >
        <el-form :model="assignForm" ref="assignFormRef" label-width="100px" status-icon>
          <el-form-item label="处理人员" prop="handler_id">
            <el-select v-model="assignForm.handler_id" placeholder="选择处理人员">
              <el-option 
                v-for="user in users" 
                :key="user.id" 
                :label="user.username" 
                :value="user.id" 
              />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="assignDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmAssign">确认指派</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="handleDialogVisible"
        title="处理投诉建议"
        width="500px"
      >
        <el-form :model="handleForm" ref="handleFormRef" label-width="100px" status-icon>
          <el-form-item label="处理结果" prop="handle_result">
            <el-input v-model="handleForm.handle_result" type="textarea" :rows="6" placeholder="请输入处理结果" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="handleDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmHandle">确认处理</el-button>
          </span>
        </template>
      </el-dialog>
      
      <el-dialog
        v-model="satisfactionDialogVisible"
        title="满意度评价"
        width="500px"
      >
        <el-form :model="satisfactionForm" ref="satisfactionFormRef" label-width="100px" status-icon>
          <el-form-item label="满意度" prop="satisfaction">
            <el-rate v-model="satisfactionForm.satisfaction" :max="5" show-score />
          </el-form-item>
          <el-form-item label="评价内容" prop="comment">
            <el-input v-model="satisfactionForm.comment" type="textarea" :rows="4" placeholder="请输入评价内容（可选）" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="satisfactionDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmSatisfaction">提交评价</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const activeTab = ref('complaints')
const complaints = ref([])
const categories = ref([])
const users = ref([])
const statistics = ref({
  total: 0,
  pending: 0,
  processing: 0,
  completed: 0,
  evaluated: 0,
  avg_satisfaction: 0
})

const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const searchForm = ref({
  status: '',
  type: '',
  category: '',
  priority: ''
})

const complaintDialogVisible = ref(false)
const complaintDialogTitle = ref('新增投诉建议')
const complaintForm = ref({
  title: '',
  type: 'complaint',
  category: '',
  content: '',
  address: '',
  priority: 'medium'
})

const categoryDialogVisible = ref(false)
const categoryDialogTitle = ref('新增分类')
const categoryForm = ref({
  name: '',
  code: '',
  description: '',
  sort_order: 0
})

const assignDialogVisible = ref(false)
const assignForm = ref({
  complaint_id: null,
  handler_id: null
})

const handleDialogVisible = ref(false)
const handleForm = ref({
  complaint_id: null,
  handle_result: ''
})

const satisfactionDialogVisible = ref(false)
const satisfactionForm = ref({
  complaint_id: null,
  satisfaction: 5,
  comment: ''
})

const complaintRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const categoryRules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入分类编码', trigger: 'blur' }]
}

const handleTabChange = (tab) => {
  if (tab === 'complaints') {
    loadComplaints()
  } else if (tab === 'categories') {
    loadCategories()
  } else if (tab === 'statistics') {
    loadStatistics()
  }
}

const loadComplaints = async () => {
  try {
    const response = await axios.get('/api/v1/pc/complaints', {
      params: {
        page: page.value,
        pageSize: pageSize.value,
        ...searchForm.value
      }
    })
    complaints.value = response.data.data.list
    total.value = response.data.data.total
  } catch (error) {
    ElMessage.error('加载投诉建议列表失败')
  }
}

const loadCategories = async () => {
  try {
    const response = await axios.get('/api/v1/pc/complaints/categories')
    categories.value = response.data.data
  } catch (error) {
    ElMessage.error('加载分类列表失败')
  }
}

const loadStatistics = async () => {
  try {
    const response = await axios.get('/api/v1/pc/complaints/statistics')
    statistics.value = response.data.data
  } catch (error) {
    ElMessage.error('加载统计失败')
  }
}

const openComplaintDialog = () => {
  complaintDialogTitle.value = '新增投诉建议'
  complaintForm.value = {
    title: '',
    type: 'complaint',
    category: '',
    content: '',
    address: '',
    priority: 'medium'
  }
  complaintDialogVisible.value = true
}

const saveComplaint = async () => {
  try {
    await axios.post('/api/v1/pc/complaints', complaintForm.value)
    ElMessage.success('提交投诉建议成功')
    complaintDialogVisible.value = false
    loadComplaints()
  } catch (error) {
    ElMessage.error('提交投诉建议失败')
  }
}

const viewComplaint = (complaint) => {
  ElMessageBox.alert(
    `<div>
      <p><strong>标题：</strong>${complaint.title}</p>
      <p><strong>类型：</strong>${complaint.type === 'complaint' ? '投诉' : '建议'}</p>
      <p><strong>分类：</strong>${getCategoryName(complaint.category)}</p>
      <p><strong>内容：</strong>${complaint.content}</p>
      <p><strong>地址：</strong>${complaint.address || '无'}</p>
      <p><strong>优先级：</strong>${getPriorityText(complaint.priority)}</p>
      <p><strong>状态：</strong>${getStatusText(complaint.status)}</p>
      <p><strong>提交人：</strong>${complaint.user_name}</p>
      <p><strong>处理人：</strong>${complaint.handler_name || '未指派'}</p>
      <p><strong>处理结果：</strong>${complaint.handle_result || '暂无'}</p>
      <p><strong>满意度：</strong>${complaint.satisfaction ? complaint.satisfaction + '星' : '未评价'}</p>
      <p><strong>提交时间：</strong>${complaint.created_at}</p>
    </div>`,
    '投诉建议详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭'
    }
  )
}

const assignHandler = (complaint) => {
  assignForm.value = {
    complaint_id: complaint.id,
    handler_id: null
  }
  assignDialogVisible.value = true
}

const confirmAssign = async () => {
  try {
    const selectedUser = users.value.find(u => u.id === assignForm.value.handler_id)
    await axios.post(`/api/v1/pc/complaints/${assignForm.value.complaint_id}/assign`, {
      handler_id: assignForm.value.handler_id,
      handler_name: selectedUser?.username
    })
    ElMessage.success('指派成功')
    assignDialogVisible.value = false
    loadComplaints()
  } catch (error) {
    ElMessage.error('指派失败')
  }
}

const handleComplaint = (complaint) => {
  handleForm.value = {
    complaint_id: complaint.id,
    handle_result: ''
  }
  handleDialogVisible.value = true
}

const confirmHandle = async () => {
  try {
    await axios.post(`/api/v1/pc/complaints/${handleForm.value.complaint_id}/handle`, handleForm.value)
    ElMessage.success('处理成功')
    handleDialogVisible.value = false
    loadComplaints()
  } catch (error) {
    ElMessage.error('处理失败')
  }
}

const submitSatisfaction = (complaint) => {
  satisfactionForm.value = {
    complaint_id: complaint.id,
    satisfaction: 5,
    comment: ''
  }
  satisfactionDialogVisible.value = true
}

const confirmSatisfaction = async () => {
  try {
    await axios.post(`/api/v1/pc/complaints/${satisfactionForm.value.complaint_id}/satisfaction`, satisfactionForm.value)
    ElMessage.success('评价提交成功')
    satisfactionDialogVisible.value = false
    loadComplaints()
  } catch (error) {
    ElMessage.error('评价提交失败')
  }
}

const deleteComplaint = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该投诉建议吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/v1/pc/complaints/${id}`)
    ElMessage.success('删除成功')
    loadComplaints()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const openCategoryDialog = () => {
  categoryDialogTitle.value = '新增分类'
  categoryForm.value = {
    name: '',
    code: '',
    description: '',
    sort_order: 0
  }
  categoryDialogVisible.value = true
}

const editCategory = (category) => {
  categoryDialogTitle.value = '编辑分类'
  categoryForm.value = { ...category }
  categoryDialogVisible.value = true
}

const saveCategory = async () => {
  try {
    if (categoryDialogTitle.value === '新增分类') {
      await axios.post('/api/v1/pc/complaints/categories', categoryForm.value)
      ElMessage.success('新增分类成功')
    } else {
      await axios.put(`/api/v1/pc/complaints/categories/${categoryForm.value.id}`, categoryForm.value)
      ElMessage.success('更新分类成功')
    }
    categoryDialogVisible.value = false
    loadCategories()
  } catch (error) {
    ElMessage.error('保存分类失败')
  }
}

const deleteCategory = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该分类吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await axios.delete(`/api/v1/pc/complaints/categories/${id}`)
    ElMessage.success('删除分类成功')
    loadCategories()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除分类失败')
    }
  }
}

const searchComplaints = () => {
  page.value = 1
  loadComplaints()
}

const resetSearch = () => {
  searchForm.value = {
    status: '',
    type: '',
    category: '',
    priority: ''
  }
  page.value = 1
  loadComplaints()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  loadComplaints()
}

const handleCurrentChange = (currentPage) => {
  page.value = currentPage
  loadComplaints()
}

const getCategoryName = (code) => {
  const category = categories.value.find(c => c.code === code)
  return category ? category.name : code
}

const getPriorityTag = (priority) => {
  const priorityMap = {
    'low': 'info',
    'medium': 'warning',
    'high': 'danger'
  }
  return priorityMap[priority] || ''
}

const getPriorityText = (priority) => {
  const priorityMap = {
    'low': '低',
    'medium': '中',
    'high': '高'
  }
  return priorityMap[priority] || priority
}

const getStatusTag = (status) => {
  const statusMap = {
    'pending': 'warning',
    'processing': 'primary',
    'completed': 'success'
  }
  return statusMap[status] || ''
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成'
  }
  return statusMap[status] || status
}

onMounted(() => {
  loadComplaints()
  loadCategories()
})
</script>

<style scoped>
.complaint-management {
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
