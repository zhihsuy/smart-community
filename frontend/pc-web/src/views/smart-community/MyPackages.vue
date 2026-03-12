<template>
  <div class="my-packages-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📦 我的包裹</h1>
      <p class="subtitle">查看和管理我的所有包裹</p>
    </div>

    <!-- 搜索筛选 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="包裹状态">
          <el-select v-model="searchForm.status" placeholder="选择状态">
            <el-option label="全部" value="" />
            <el-option label="已存入" value="stored" />
            <el-option label="已取件" value="picked" />
            <el-option label="已过期" value="expired" />
            <el-option label="已退回" value="returned" />
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.keyword"
            placeholder="包裹号或快递公司"
            clearable
            style="width: 300px"
          >
            <template #append>
              <el-button @click="loadPackages">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 包裹列表 -->
    <el-card class="packages-card">
      <template #header>
        <div class="card-header">
          <span>包裹列表</span>
          <span class="total-count">共 {{ pagination.total }} 个包裹</span>
        </div>
      </template>
      
      <el-table :data="packages" style="width: 100%">
        <el-table-column prop="package_code" label="包裹号" width="180" />
        <el-table-column prop="express_company" label="快递公司" width="120" />
        <el-table-column prop="locker_code" label="快递柜" width="120" />
        <el-table-column prop="cabin_number" label="格口" width="80" />
        <el-table-column prop="pickup_code" label="取件码" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag size="small" :type="getStatusColor(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="存入时间" width="180" />
        <el-table-column prop="expire_time" label="过期时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button 
              size="small" 
              type="primary" 
              @click="pickupPackage(scope.row)"
              v-if="scope.row.status === 'stored'"
            >
              取件
            </el-button>
            <el-button 
              size="small" 
              type="info" 
              @click="viewDetail(scope.row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
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
    </el-card>

    <!-- 包裹详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="包裹详情"
      width="500px"
    >
      <div v-if="currentPackage" class="package-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="包裹号">{{ currentPackage.package_code }}</el-descriptions-item>
          <el-descriptions-item label="快递公司">{{ currentPackage.express_company }}</el-descriptions-item>
          <el-descriptions-item label="快递单号">{{ currentPackage.tracking_number || '-' }}</el-descriptions-item>
          <el-descriptions-item label="快递柜">{{ currentPackage.locker_code }}</el-descriptions-item>
          <el-descriptions-item label="格口">{{ currentPackage.cabin_number }}</el-descriptions-item>
          <el-descriptions-item label="取件码">{{ currentPackage.pickup_code }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusText(currentPackage.status) }}</el-descriptions-item>
          <el-descriptions-item label="存入时间">{{ currentPackage.created_at }}</el-descriptions-item>
          <el-descriptions-item label="过期时间">{{ currentPackage.expire_time }}</el-descriptions-item>
          <el-descriptions-item label="取件时间">{{ currentPackage.picked_at || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 取件对话框 -->
    <el-dialog
      v-model="pickupDialogVisible"
      title="取件确认"
      width="400px"
    >
      <div v-if="currentPackage" class="pickup-form">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="包裹号">{{ currentPackage.package_code }}</el-descriptions-item>
          <el-descriptions-item label="快递公司">{{ currentPackage.express_company }}</el-descriptions-item>
          <el-descriptions-item label="快递柜">{{ currentPackage.locker_code }}-{{ currentPackage.cabin_number }}</el-descriptions-item>
          <el-descriptions-item label="取件码">{{ currentPackage.pickup_code }}</el-descriptions-item>
        </el-descriptions>
        <div class="pickup-tip">
          <el-icon><Warning /></el-icon>
          请在5分钟内完成取件
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="pickupDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmPickup" :loading="pickingUp">
            确认取件
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Search, Warning } from '@element-plus/icons-vue'

const packages = ref([])
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})
const searchForm = ref({
  status: '',
  keyword: ''
})
const detailDialogVisible = ref(false)
const pickupDialogVisible = ref(false)
const currentPackage = ref(null)
const pickingUp = ref(false)

// 加载包裹列表
const loadPackages = async () => {
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.currentPage)
    params.append('pageSize', pagination.value.pageSize)
    
    if (searchForm.value.status) {
      params.append('status', searchForm.value.status)
    }
    if (searchForm.value.keyword) {
      params.append('keyword', searchForm.value.keyword)
    }

    const response = await fetch(`/api/v1/pc/locker/packages?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      packages.value = result.data?.list || []
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载包裹失败:', error)
    ElMessage.error('加载包裹失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadPackages()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadPackages()
}

const viewDetail = (pkg) => {
  currentPackage.value = pkg
  detailDialogVisible.value = true
}

const pickupPackage = (pkg) => {
  currentPackage.value = pkg
  pickupDialogVisible.value = true
}

const confirmPickup = async () => {
  if (!currentPackage.value) return
  
  pickingUp.value = true
  try {
    const response = await fetch(`/api/v1/pc/locker/packages/${currentPackage.value.id}/pickup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const result = await response.json()
    if (result.code === 0) {
      ElMessage.success('取件成功')
      pickupDialogVisible.value = false
      loadPackages()
    } else {
      ElMessage.error(result.msg || '取件失败')
    }
  } catch (error) {
    console.error('取件失败:', error)
    ElMessage.error('取件失败')
  } finally {
    pickingUp.value = false
  }
}

const getStatusText = (status) => {
  const map = {
    'stored': '已存入',
    'picked': '已取件',
    'expired': '已过期',
    'returned': '已退回'
  }
  return map[status] || status
}

const getStatusColor = (status) => {
  const map = {
    'stored': 'warning',
    'picked': 'success',
    'expired': 'danger',
    'returned': 'info'
  }
  return map[status] || 'info'
}

onMounted(() => {
  loadPackages()
})
</script>

<style scoped>
.my-packages-page {
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

.search-card,
.packages-card {
  border-radius: 8px;
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
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

.package-detail {
  padding: 20px 0;
}

.pickup-form {
  padding: 20px 0;
}

.pickup-tip {
  margin-top: 20px;
  padding: 10px;
  background: #fdf6ec;
  border: 1px solid #fde2cf;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #E6A23C;
  font-size: 14px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
