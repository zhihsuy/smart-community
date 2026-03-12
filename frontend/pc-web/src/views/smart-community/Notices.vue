<template>
  <div class="notices-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <div>
        <h1>📢 公告通知</h1>
        <p class="subtitle">社区公告、活动通知、物业通知</p>
      </div>
    </div>



    <!-- 公告列表 -->
    <el-card class="notices-card">
      <template #header>
        <div class="card-header">
          <span>公告列表</span>
          <span class="unread-count" v-if="unreadCount > 0">
            未读: {{ unreadCount }}
          </span>
        </div>
      </template>
      
      <div class="notice-list">
        <el-empty v-if="notices.length === 0" description="暂无公告" />
        <div 
          v-for="notice in notices" 
          :key="notice.id"
          class="notice-item"
          :class="{ 'unread': notice.is_unread }"
          @click="viewNotice(notice.id)"
        >
          <div class="notice-header">
            <h3 class="notice-title">
              <span class="type-tag" :class="`type-${notice.type}`">
                {{ getNoticeTypeText(notice.type) }}
              </span>
              {{ notice.title }}
              <span v-if="notice.is_unread" class="unread-dot">●</span>
            </h3>
            <span class="notice-date">{{ notice.publish_time ? new Date(notice.publish_time).toLocaleString() : '' }}</span>
          </div>
          <div class="notice-content">{{ notice.content }}</div>
          <div class="notice-footer">
            <span class="publisher">{{ notice.author }}</span>
            <div class="notice-actions">
              <span class="read-count">阅读 {{ notice.view_count || 0 }}</span>
            </div>
          </div>
        </div>
      </div>

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

    <!-- 置顶公告 -->
    <el-card class="pinned-card" v-if="pinnedNotices.length > 0">
      <template #header>
        <div class="card-header">
          <span>📌 置顶公告</span>
        </div>
      </template>
      <div class="pinned-list">
        <div 
          v-for="notice in pinnedNotices" 
          :key="notice.id"
          class="pinned-item"
          :class="{ 'unread': notice.is_unread }"
          @click="viewNotice(notice.id)"
        >
          <h4 class="pinned-title">
            {{ notice.title }}
            <span v-if="notice.is_unread" class="unread-dot">●</span>
          </h4>
          <p class="pinned-content">{{ notice.content }}</p>
          <div class="pinned-footer">
            <span class="type-tag" :class="`type-${notice.type}`">
              {{ getNoticeTypeText(notice.type) }}
            </span>
            <div class="pinned-actions">
              <span class="pinned-date">{{ notice.publish_time ? new Date(notice.publish_time).toLocaleString() : '' }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>


  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const notices = ref([])
const pinnedNotices = ref([])
const unreadCount = ref(0)
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 加载公告
const loadNotices = async () => {
  try {
    const params = new URLSearchParams()
    params.append('page', pagination.value.currentPage)
    params.append('pageSize', pagination.value.pageSize)

    const response = await fetch(`/api/v1/pc/notices?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    console.log('加载公告响应:', result)
    if (result.code === 0) {
      notices.value = result.data?.list || []
      pinnedNotices.value = result.data?.pinned || []
      unreadCount.value = result.data?.unread_count || 0
      pagination.value.total = result.data?.total || 0
    }
  } catch (error) {
    console.error('加载公告失败:', error)
    ElMessage.error('加载公告失败')
  }
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  loadNotices()
}

const handleCurrentChange = (current) => {
  pagination.value.currentPage = current
  loadNotices()
}

const viewNotice = (noticeId) => {
  router.push(`/notices/${noticeId}`)
}

const getNoticeTypeText = (type) => {
  const map = {
    'community': '社区公告',
    'activity': '活动通知',
    'property': '物业通知',
    'urgent': '紧急通知'
  }
  return map[type] || type
}

onMounted(() => {
  loadNotices()
})
</script>

<style scoped>
.notices-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.page-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #303133;
}

.subtitle {
  color: #909399;
  margin: 0;
}

.notices-card,
.pinned-card {
  border-radius: 8px;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.unread-count {
  color: #F56C6C;
  font-weight: normal;
}

.notice-list {
  max-height: 600px;
  overflow-y: auto;
}

.notice-item {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  cursor: pointer;
  transition: all 0.3s;
}

.notice-item:hover {
  background-color: #f5f7fa;
}

.notice-item.unread {
  background-color: #ecf5ff;
}

.notice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.notice-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.type-tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: normal;
}

.type-community { background: #ecf5ff; color: #409EFF; }
.type-activity { background: #f0f9eb; color: #67C23A; }
.type-property { background: #fdf6ec; color: #E6A23C; }
.type-urgent { background: #fef0f0; color: #F56C6C; }

.unread-dot {
  color: #F56C6C;
  font-size: 12px;
  margin-left: 5px;
}

.notice-date {
  color: #909399;
  font-size: 14px;
}

.notice-content {
  color: #606266;
  line-height: 1.5;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.notice-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #909399;
}

.notice-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pinned-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pinned-card {
  border-left: 4px solid #409EFF;
}

.pinned-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.pinned-item {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.pinned-item:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pinned-item.unread {
  border-left: 3px solid #409EFF;
}

.pinned-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.pinned-content {
  font-size: 13px;
  color: #606266;
  margin: 0 0 10px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.pinned-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #909399;
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
  
  .pinned-list {
    grid-template-columns: 1fr;
  }
}
</style>
