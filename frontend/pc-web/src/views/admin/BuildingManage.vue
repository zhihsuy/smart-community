<template>
  <AdminLayout>
    <div class="building-manage">
      <div class="page-header">
        <h2 class="page-title">🏢 楼栋管理</h2>
        <div class="header-actions">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索楼栋名称"
            style="width: 300px; margin-right: 10px"
            @keyup.enter="loadBuildings"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="loadBuildings">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button type="success" @click="addBuilding">
            <el-icon><Plus /></el-icon>
            新增楼栋
          </el-button>
        </div>
      </div>

      <div class="building-table">
        <el-table :data="buildings" style="width: 100%">
          <el-table-column prop="id" label="楼栋ID" width="80" />
          <el-table-column prop="name" label="楼栋名称" width="150" />
          <el-table-column prop="unit_count" label="单元数" width="100" />
          <el-table-column prop="household_count" label="户数" width="100" />
          <el-table-column prop="user_count" label="实际住户数" width="100" />
          <el-table-column prop="address" label="详细地址" min-width="200" />
          <el-table-column prop="status" label="状态" width="150">
            <template #default="scope">
              <el-switch
                v-model="scope.row.status"
                active-value="active"
                inactive-value="inactive"
                @change="toggleBuildingStatus(scope.row)"
                active-text="启用"
                inactive-text="禁用"
              />
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button
                size="small"
                type="primary"
                @click="editBuilding(scope.row)"
                style="margin-right: 5px"
              >
                编辑
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="deleteBuilding(scope.row.id)"
              >
                删除
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

      <!-- 楼栋编辑对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="isEdit ? '编辑楼栋' : '新增楼栋'"
        width="500px"
      >
        <el-form :model="buildingForm" label-width="120px">
          <el-form-item label="社区ID">
            <el-input v-model="buildingForm.community_id" placeholder="请输入社区ID" />
          </el-form-item>
          <el-form-item label="楼栋名称">
            <el-input v-model="buildingForm.name" placeholder="请输入楼栋名称" />
          </el-form-item>
          <el-form-item label="单元数">
            <el-input-number
              v-model="buildingForm.unit_count"
              :min="1"
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="楼层数">
            <el-input-number
              v-model="buildingForm.floor_count"
              :min="1"
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="户数">
            <el-input-number
              v-model="buildingForm.household_count"
              :min="1"
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="详细地址">
            <el-input v-model="buildingForm.address" placeholder="请输入详细地址" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="saveBuilding">保存</el-button>
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

const buildings = ref([])
const searchKeyword = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const buildingForm = ref({})

const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

import axios from '@/utils/request'

const loadBuildings = async () => {
  try {
    console.log('加载楼栋列表，Token:', localStorage.getItem('token'))
    const response = await axios.get(`/v1/admin/buildings`, {
      params: {
        page: pagination.value.currentPage,
        pageSize: pagination.value.pageSize,
        keyword: searchKeyword.value
      }
    })
    console.log('加载楼栋列表响应状态:', response.status)
    console.log('加载楼栋列表响应数据:', response.data)
    if (response.data.code === 0) {
      buildings.value = response.data.data?.list || []
      pagination.value.total = response.data.data?.total || 0
    } else {
      ElMessage.error(response.data.msg || '加载失败')
    }
  } catch (error) {
    console.error('加载楼栋列表失败:', error)
    ElMessage.error('加载楼栋列表失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadBuildings()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadBuildings()
}

const addBuilding = () => {
  isEdit.value = false
  buildingForm.value = {
    community_id: 1,
    name: '',
    unit_count: 1,
    floor_count: 1,
    household_count: 1,
    address: ''
  }
  dialogVisible.value = true
}

const editBuilding = (building) => {
  isEdit.value = true
  buildingForm.value = { ...building }
  dialogVisible.value = true
}

const saveBuilding = async () => {
  try {
    const method = isEdit.value ? 'put' : 'post'
    const url = isEdit.value ? `/v1/admin/buildings/${buildingForm.value.id}` : '/v1/admin/buildings'
    
    // 准备发送的数据
    const sendData = {
      community_id: buildingForm.value.community_id,
      name: buildingForm.value.name,
      unit_count: buildingForm.value.unit_count,
      floor_count: buildingForm.value.floor_count,
      household_count: buildingForm.value.household_count
    }
    
    // 只在有地址时添加address字段
    if (buildingForm.value.address) {
      sendData.address = buildingForm.value.address
    }
    
    // 只在编辑时添加status字段
    if (isEdit.value && buildingForm.value.status) {
      sendData.status = buildingForm.value.status
    }
    
    console.log('发送数据:', sendData)
    console.log('Token:', localStorage.getItem('token'))
    
    const response = await axios({ 
      method, 
      url, 
      data: sendData 
    })
    
    console.log('响应状态:', response.status)
    console.log('响应数据:', response.data)
    
    if (response.data.code === 0) {
      ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
      dialogVisible.value = false
      loadBuildings()
    } else {
      ElMessage.error(response.data.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存楼栋失败:', error)
    ElMessage.error('操作失败')
  }
}

const toggleBuildingStatus = async (building) => {
  try {
    const response = await axios.put(`/v1/admin/buildings/${building.id}/status`, {
      status: building.status
    })
    console.log('切换楼栋状态响应状态:', response.status)
    console.log('切换楼栋状态响应数据:', response.data)
    if (response.data.code === 0) {
      ElMessage.success('状态更新成功')
    } else {
      ElMessage.error(response.data.msg || '状态更新失败')
      // 恢复原来的状态
      building.status = building.status === 'active' ? 'inactive' : 'active'
    }
  } catch (error) {
    console.error('切换楼栋状态失败:', error)
    ElMessage.error('状态更新失败')
    // 恢复原来的状态
    building.status = building.status === 'active' ? 'inactive' : 'active'
  }
}

const deleteBuilding = async (buildingId) => {
  if (!confirm('确定要删除此楼栋吗？')) {
    return
  }
  
  try {
    const response = await axios.delete(`/v1/admin/buildings/${buildingId}`)
    console.log('删除楼栋响应状态:', response.status)
    console.log('删除楼栋响应数据:', response.data)
    if (response.data.code === 0) {
      ElMessage.success('删除成功')
      loadBuildings()
    } else {
      ElMessage.error(response.data.msg || '删除失败')
    }
  } catch (error) {
    console.error('删除楼栋失败:', error)
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadBuildings()
})
</script>

<style scoped>
.building-manage {
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

.building-table {
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
  
  .building-table {
    padding: 10px;
  }
  
  .pagination {
    justify-content: center;
  }
}
</style>