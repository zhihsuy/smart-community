<template>
  <div class="notice-detail-page">
    <div class="page-header">
      <el-button type="primary" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h1>📢 公告详情</h1>
    </div>

    <el-card class="notice-card" v-if="notice">
      <div class="notice-header">
        <h2 class="notice-title">{{ notice.title }}</h2>
        <div class="notice-meta">
          <span class="type-tag" :class="`type-${notice.type}`">
            {{ getNoticeTypeText(notice.type) }}
          </span>
          <span class="publish-date">{{ notice.publish_date }}</span>
          <span class="read-count">阅读 {{ notice.read_count || 0 }}</span>
        </div>
      </div>

      <div class="notice-content">
        <div v-html="notice.content"></div>
      </div>

      <div class="notice-footer">
        <div class="publisher-info">
          <span class="publisher">发布人：{{ notice.publisher }}</span>
          <span class="department">发布部门：{{ notice.department || '物业部' }}</span>
        </div>
        <div class="actions">
          <el-button type="primary" @click="shareNotice">
            <el-icon><Share /></el-icon>
            分享
          </el-button>
          <el-button @click="$router.push('/notices')">
            <el-icon><List /></el-icon>
            查看更多
          </el-button>
        </div>
      </div>
    </el-card>

    <el-card class="related-notices" v-if="relatedNotices.length > 0">
      <template #header>
        <div class="card-header">
          <span>📋 相关公告</span>
        </div>
      </template>
      <div class="related-list">
        <div 
          v-for="item in relatedNotices" 
          :key="item.id"
          class="related-item"
          @click="viewNotice(item.id)"
        >
          <h4 class="related-title">{{ item.title }}</h4>
          <span class="related-date">{{ item.publish_date }}</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Share, List } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const notice = ref(null)
const relatedNotices = ref([])

// 加载公告详情
const loadNoticeDetail = async () => {
  const noticeId = route.params.id
  if (!noticeId) return

  try {
    const response = await fetch(`/api/v1/pc/notice/notices/${noticeId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      notice.value = result.data
    } else {
      ElMessage.error(result.msg || '加载公告失败')
    }
  } catch (error) {
    console.error('加载公告详情失败:', error)
    ElMessage.error('加载公告失败')
  }
}

// 加载相关公告
const loadRelatedNotices = async () => {
  const noticeId = route.params.id
  if (!noticeId) return

  try {
    const response = await fetch(`/api/v1/pc/notice/related-notices?notice_id=${noticeId}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    const result = await response.json()
    if (result.code === 0) {
      relatedNotices.value = result.data || []
    }
  } catch (error) {
    console.error('加载相关公告失败:', error)
  }
}

const viewNotice = (id) => {
  router.push(`/notices/${id}`)
}

const shareNotice = () => {
  if (!notice.value) return
  
  const shareText = `【${notice.value.title}】\n${notice.value.content.substring(0, 100)}...\n发布时间：${notice.value.publish_date}`
  
  if (navigator.share) {
    navigator.share({
      title: notice.value.title,
      text: shareText,
      url: window.location.href
    })
  } else {
    navigator.clipboard.writeText(window.location.href)
    ElMessage.success('链接已复制到剪贴板')
  }
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
  loadNoticeDetail()
  loadRelatedNotices()
})
</script>

<style scoped>
.notice-detail-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 10px 0 0 0;
  font-size: 28px;
  color: #303133;
}

.notice-card {
  border-radius: 8px;
  margin-bottom: 30px;
}

.notice-header {
  padding: 20px 0;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 20px;
}

.notice-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 15px 0;
  color: #303133;
}

.notice-meta {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 14px;
  color: #909399;
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

.notice-content {
  padding: 20px 0;
  line-height: 1.8;
  color: #303133;
  font-size: 16px;
}

.notice-content :deep(p) {
  margin-bottom: 15px;
}

.notice-content :deep(strong) {
  font-weight: 600;
}

.notice-content :deep(img) {
  max-width: 100%;
  height: auto;
  margin: 10px 0;
}

.notice-footer {
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.publisher-info {
  font-size: 14px;
  color: #909399;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.actions {
  display: flex;
  gap: 10px;
}

.related-notices {
  border-radius: 8px;
}

.card-header {
  font-weight: 600;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.related-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.related-item:hover {
  border-color: #409EFF;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.related-title {
  font-size: 14px;
  font-weight: 500;
  margin: 0;
  max-width: 70%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-date {
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .notice-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .notice-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .actions {
    justify-content: center;
  }
  
  .related-title {
    max-width: 60%;
  }
}
</style>
