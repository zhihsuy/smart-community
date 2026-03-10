<template>
  <div class="activities-container">
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1>社区活动</h1>
          <p>精彩活动，丰富社区生活</p>
        </div>
        <button v-if="canPublish" class="publish-btn" @click="goToPublish">
          <span class="icon">+</span>
          发布活动
        </button>
      </div>
    </div>
    
    <div class="filter-bar">
      <div class="filter-item">
        <label>活动类型：</label>
        <select v-model="selectedType" @change="filterActivities">
          <option value="">全部</option>
          <option value="sports">运动健身</option>
          <option value="culture">文化艺术</option>
          <option value="education">教育培训</option>
          <option value="social">社交聚会</option>
        </select>
      </div>
      <div class="filter-item">
        <label>活动状态：</label>
        <select v-model="selectedStatus" @change="filterActivities">
          <option value="">全部</option>
          <option value="upcoming">即将开始</option>
          <option value="ongoing">进行中</option>
          <option value="ended">已结束</option>
        </select>
      </div>
    </div>
    
    <div class="activities-list">
      <div 
        v-for="activity in filteredActivities" 
        :key="activity.id" 
        class="activity-card"
        @click="goToDetail(activity.id)"
      >
        <div class="activity-image">
          <img :src="activity.image" :alt="activity.title" />
          <span :class="['status-badge', activity.status]">{{ statusText(activity.status) }}</span>
        </div>
        <div class="activity-content">
          <h3 class="activity-title">{{ activity.title }}</h3>
          <p class="activity-desc">{{ activity.description }}</p>
          <div class="activity-info">
            <div class="info-item">
              <span class="icon">📅</span>
              <span>{{ activity.date }}</span>
            </div>
            <div class="info-item">
              <span class="icon">📍</span>
              <span>{{ activity.location }}</span>
            </div>
            <div class="info-item">
              <span class="icon">👥</span>
              <span>{{ activity.participants }}/{{ activity.maxParticipants }}人</span>
            </div>
          </div>
          <div class="activity-footer">
            <span class="organizer">主办方：{{ activity.organizer }}</span>
            <button class="join-btn" @click.stop="joinActivity(activity)">
              {{ activity.status === 'ended' ? '已结束' : '立即报名' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 从localStorage获取用户信息
const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')

// 判断是否有发布权限（管理员、运营、物业等）
const canPublish = computed(() => {
  const role = userInfo.role || '居民'
  return ['管理员', '运营', '物业', '居委会'].includes(role)
})

// 跳转到发布活动页面
const goToPublish = () => {
  router.push('/admin/smart-community/activity')
}

const selectedType = ref('')
const selectedStatus = ref('')
const activities = ref([])
const loading = ref(false)

// 加载活动列表
const loadActivities = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/v1/pc/activities', {
      params: {
        status: selectedStatus.value === 'upcoming' ? 'published' : 
                selectedStatus.value === 'ongoing' ? 'published' : 
                selectedStatus.value === 'ended' ? 'completed' : '',
        category: selectedType.value
      }
    })
    
    if (response.data.code === 0) {
      activities.value = response.data.data.list.map(activity => ({
        ...activity,
        date: activity.start_time,
        participants: activity.current_participants,
        maxParticipants: activity.max_participants,
        type: activity.category,
        status: activity.status === 'published' ? 'upcoming' : 
               activity.status === 'completed' ? 'ended' : activity.status
      }))
    } else {
      ElMessage.error('加载活动列表失败')
    }
  } catch (error) {
    console.error('加载活动列表失败:', error)
    ElMessage.error('加载活动列表失败')
  } finally {
    loading.value = false
  }
}

const filteredActivities = computed(() => {
  let result = [...activities.value]
  
  if (selectedType.value) {
    result = result.filter(a => a.type === selectedType.value)
  }
  
  if (selectedStatus.value) {
    result = result.filter(a => a.status === selectedStatus.value)
  }
  
  return result
})

const statusText = (status) => {
  const statusMap = {
    upcoming: '即将开始',
    ongoing: '进行中',
    ended: '已结束'
  }
  return statusMap[status] || status
}

const filterActivities = () => {
  loadActivities()
}

const goToDetail = (id) => {
  router.push(`/activities/detail/${id}`)
}

const joinActivity = (activity) => {
  if (activity.status === 'ended') {
    return
  }
  
  if (activity.participants >= activity.maxParticipants) {
    ElMessage.warning('活动名额已满')
    return
  }
  
  // 这里可以添加报名逻辑
  ElMessage.success(`报名成功：${activity.title}`)
}

onMounted(() => {
  loadActivities()
})
</script>

<style scoped>
.activities-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header-text {
  text-align: left;
}

.header-text h1 {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0 0 10px;
}

.header-text p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.publish-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.publish-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.publish-btn .icon {
  font-size: 18px;
  font-weight: 300;
}

.filter-bar {
  background: white;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 24px;
  display: flex;
  gap: 30px;
  align-items: center;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-item label {
  font-size: 14px;
  color: #666;
}

.filter-item select {
  padding: 6px 12px;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  font-size: 14px;
}

.activities-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.activity-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.activity-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.activity-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.activity-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.status-badge.upcoming {
  background: #2196F3;
}

.status-badge.ongoing {
  background: #4CAF50;
}

.status-badge.ended {
  background: #999;
}

.activity-content {
  padding: 20px;
}

.activity-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px;
}

.activity-desc {
  font-size: 14px;
  color: #666;
  margin: 0 0 16px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.activity-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.icon {
  font-size: 16px;
}

.activity-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #f5f5f5;
}

.organizer {
  font-size: 12px;
  color: #999;
}

.join-btn {
  padding: 8px 20px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
}

.join-btn:hover:not(:disabled) {
  background: #1976D2;
}

.join-btn:disabled {
  background: #999;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .activities-list {
    grid-template-columns: 1fr;
  }
}
</style>