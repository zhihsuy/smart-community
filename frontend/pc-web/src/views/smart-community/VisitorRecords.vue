<template>
  <div class="visitor-records-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📝 访客记录</h1>
      <p class="subtitle">查看和管理所有访客记录</p>
    </div>

    <!-- 搜索筛选 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="访客ID">
          <el-input v-model="searchForm.visitor_id" placeholder="请输入访客ID" />
        </el-form-item>
        <el-form-item label="设备ID">
          <el-input v-model="searchForm.device_id" placeholder="请输入设备ID" />
        </el-form-item>
        <el-form-item label="记录类型">
          <el-select v-model="searchForm.record_type" placeholder="选择记录类型">
            <el-option label="全部" value="" />
            <el-option label="进入" value="entry" />
            <el-option label="离开" value="exit" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker
            v-model="searchForm.start_date"
            type="date"
            placeholder="选择开始日期"
            style="width: 180px"
          />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker
            v-model="searchForm.end_date"
            type="date"
            placeholder="选择结束日期"
            style="width: 180px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadRecords">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 记录列表 -->
    <el-card class="records-card">
      <template #header>
        <div class="card-header">
          <span>记录列表</span>
          <span class="total-count">共 {{ pagination.total }} 条记录</span>
        </div>
      </template>
      
      <el-table :data="records" style="width: 100%">
        <el-table-column prop="id" label="记录ID" width="80" />
        <el-table-column prop="visitor_id" label="访客ID" width="100" />
        <el-table-column prop="device_id" label="设备ID" width="100" />
        <el-table-column prop="record_type" label="记录类型" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.record_type === 'entry' ? 'success' : 'info'">
              {{ scope.row.record_type === 'entry' ? '进入' : '离开' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="photo_url" label="照片" width="120">
          <template #default="scope">
            <el-image
              v-if="scope.row.photo_url"
              :src="scope.row.photo_url"
              fit="cover"
              style="width: 60px; height: 60px"
              preview-src-list="[scope.row.photo_url]"
            />
            <span v-else>无</span>
          </template>
        </el-table-column>
        <el-table-column prop="temperature" label="体温" width="80" />
        <el-table-column prop="record_time" label="记录时间" width="180" />
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ArrowLeft } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import request from '@/utils/request';

// 搜索表单
const searchForm = ref({
  visitor_id: '',
  device_id: '',
  record_type: '',
  start_date: '',
  end_date: ''
});

// 记录列表
const records = ref([]);

// 分页信息
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
});

// 加载记录
const loadRecords = async () => {
  try {
    const response = await request.get('/api/v1/pc/visitor/records', {
      params: {
        visitor_id: searchForm.value.visitor_id,
        device_id: searchForm.value.device_id,
        record_type: searchForm.value.record_type,
        start_date: searchForm.value.start_date ? searchForm.value.start_date + ' 00:00:00' : '',
        end_date: searchForm.value.end_date ? searchForm.value.end_date + ' 23:59:59' : '',
        page: pagination.value.currentPage,
        pageSize: pagination.value.pageSize
      }
    });
    
    if (response.code === 0) {
      records.value = response.data.list;
      pagination.value.total = response.data.total;
    } else {
      ElMessage.error(response.msg);
    }
  } catch (error) {
    ElMessage.error('获取记录失败');
    console.error('获取记录失败:', error);
  }
};

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    visitor_id: '',
    device_id: '',
    record_type: '',
    start_date: '',
    end_date: ''
  };
  pagination.value.currentPage = 1;
  loadRecords();
};

// 分页处理
const handleSizeChange = (size) => {
  pagination.value.pageSize = size;
  loadRecords();
};

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current;
  loadRecords();
};

// 组件挂载时加载数据
onMounted(() => {
  loadRecords();
});
</script>

<style scoped>
.visitor-records-page {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.search-card {
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.search-form {
  width: 100%;
}

.records-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-count {
  font-size: 14px;
  color: #909399;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}
</style>