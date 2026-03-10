<template>
  <div class="detail-container">
    <div class="activity-header">
      <div class="activity-image">
        <img :src="activity.image" :alt="activity.title" />
        <span :class="['status-badge', activity.status]">{{ statusText(activity.status) }}</span>
      </div>
      <div class="activity-info">
        <h1 class="activity-title">{{ activity.title }}</h1>
        <p class="activity-description">{{ activity.description }}</p>
        
        <div class="activity-meta">
          <div class="meta-item">
            <span class="meta-label">时间：</span>
            <span class="meta-value">{{ activity.date }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">地点：</span>
            <span class="meta-value">{{ activity.location }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">主办方：</span>
            <span class="meta-value">{{ activity.organizer }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">参与人数：</span>
            <span class="meta-value">{{ activity.participants }}/{{ activity.maxParticipants }}人</span>
          </div>
        </div>
        
        <div class="action-buttons">
          <button 
            class="join-btn" 
            :disabled="activity.status === 'ended' || activity.participants >= activity.maxParticipants"
            @click="joinActivity"
          >
            {{ joinButtonText }}
          </button>
          <button class="share-btn" @click="shareActivity">分享活动</button>
        </div>
      </div>
    </div>
    
    <div class="activity-tabs">
      <div class="tab-header">
        <button 
          v-for="tab in tabs" 
          :key="tab.key"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>
      
      <div class="tab-content">
        <div v-if="activeTab === 'detail'" class="detail-content">
          <h3>活动详情</h3>
          <p>{{ activity.detailDescription }}</p>
          
          <div class="activity-requirements">
            <h4>报名要求</h4>
            <ul>
              <li v-for="req in activity.requirements" :key="req">{{ req }}</li>
            </ul>
          </div>
          
          <div class="activity-contact">
            <h4>联系方式</h4>
            <p>联系人：{{ activity.contactName }}</p>
            <p>联系电话：{{ activity.contactPhone }}</p>
          </div>
        </div>
        
        <div v-if="activeTab === 'participants'" class="participants-content">
          <h3>参与人员</h3>
          <div class="participants-list">
            <div v-for="participant in participants" :key="participant.id" class="participant-item">
              <div class="participant-avatar">
                <img :src="participant.avatar" :alt="participant.name" />
              </div>
              <div class="participant-info">
                <span class="participant-name">{{ participant.name }}</span>
                <span class="participant-time">{{ participant.joinTime }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const route = useRoute()

const activeTab = ref('detail')
const activity = ref({})
const participants = ref([])
const loading = ref(false)

const tabs = [
  { key: 'detail', label: '活动详情' },
  { key: 'participants', label: '参与人员' }
]

// 加载活动详情
const loadActivityDetail = async () => {
  const activityId = route.params.id
  if (!activityId) return
  
  loading.value = true
  try {
    // 加载活动基本信息
    const activityResponse = await axios.get(`/api/v1/pc/activities/${activityId}`)
    if (activityResponse.data.code === 0) {
      const data = activityResponse.data.data
      activity.value = {
        ...data,
        detailDescription: data.description,
        date: `${data.start_time} - ${data.end_time}`,
        participants: data.current_participants,
        maxParticipants: data.max_participants,
        contactName: data.organizer,
        contactPhone: data.contact_phone,
        status: data.status === 'published' ? 'upcoming' : 
               data.status === 'completed' ? 'ended' : data.status,
        requirements: [
          '年龄在18-65岁之间',
          '身体健康，无心脏病等不适合运动的疾病',
          '自备运动服装和运动鞋',
          '遵守比赛规则，服从裁判判决'
        ]
      }
    } else {
      ElMessage.error('加载活动详情失败')
    }
    
    // 加载参与者列表
    const participantsResponse = await axios.get(`/api/v1/pc/activities/${activityId}/participants`)
    if (participantsResponse.data.code === 0) {
      participants.value = participantsResponse.data.data.map(p => ({
        id: p.id,
        name: p.user_name,
        avatar: `https://via.placeholder.com/40x40?text=${p.user_name.charAt(0)}`,
        joinTime: p.created_at
      }))
    } else {
      ElMessage.error('加载参与者列表失败')
    }
  } catch (error) {
    console.error('加载活动详情失败:', error)
    ElMessage.error('加载活动详情失败')
  } finally {
    loading.value = false
  }
}

const joinButtonText = computed(() => {
  if (activity.value.status === 'ended') {
    return '活动已结束'
  } else if (activity.value.participants >= activity.value.maxParticipants) {
    return '名额已满'
  } else {
    return '立即报名'
  }
})

const statusText = (status) => {
  const statusMap = {
    upcoming: '即将开始',
    ongoing: '进行中',
    ended: '已结束'
  }
  return statusMap[status] || status
}

const joinActivity = async () => {
  const activityId = route.params.id
  if (!activityId) return
  
  try {
    // 获取用户信息
    const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
    
    const response = await axios.post(`/api/v1/pc/activities/${activityId}/participants`, {
      user_id: userInfo.id,
      user_name: userInfo.nickname || userInfo.phone,
      user_phone: userInfo.phone
    })
    
    if (response.data.code === 0) {
      ElMessage.success('报名成功！')
      // 重新加载活动详情
      loadActivityDetail()
    } else {
      ElMessage.error('报名失败: ' + response.data.msg)
    }
  } catch (error) {
    console.error('报名失败:', error)
    ElMessage.error('报名失败')
  }
}

const shareActivity = () => {
  ElMessage.info('分享功能开发中...')
}

onMounted(() => {
  loadActivityDetail()
})
</script>

<style scoped>
.detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.activity-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.activity-image {
  position: relative;
  height: 400px;
  border-radius: 8px;
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
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 14px;
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

.activity-info {
  background: white;
  border-radius: 8px;
  padding: 30px;
}

.activity-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px;
}

.activity-description {
  font-size: 16px;
  color: #666;
  margin: 0 0 24px;
  line-height: 1.6;
}

.activity-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
  padding: 16px 0;
  border-top: 1px solid #f5f5f5;
  border-bottom: 1px solid #f5f5f5;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-label {
  font-size: 14px;
  color: #999;
  min-width: 80px;
}

.meta-value {
  font-size: 14px;
  color: #333;
}

.action-buttons {
  display: flex;
  gap: 16px;
}

.join-btn,
.share-btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.join-btn {
  background: #2196F3;
  color: white;
}

.join-btn:hover:not(:disabled) {
  background: #1976D2;
}

.join-btn:disabled {
  background: #999;
  cursor: not-allowed;
}

.share-btn {
  background: #f5f5f5;
  color: #333;
}

.share-btn:hover {
  background: #e8e8e8;
}

.activity-tabs {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.tab-header {
  display: flex;
  gap: 30px;
  border-bottom: 1px solid #e8e8e8;
  margin-bottom: 20px;
}

.tab-header button {
  padding: 12px 0;
  background: none;
  border: none;
  font-size: 16px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab-header button.active {
  color: #2196F3;
  border-bottom-color: #2196F3;
}

.tab-content h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 16px;
}

.tab-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.8;
  margin-bottom: 16px;
}

.activity-requirements,
.activity-contact {
  margin: 24px 0;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.activity-requirements h4,
.activity-contact h4 {
  font-size: 16px;
  color: #333;
  margin: 0 0 12px;
}

.activity-requirements ul {
  margin: 0;
  padding-left: 20px;
}

.activity-requirements li {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.6;
}

.participants-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.participants-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.participant-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}

.participant-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.participant-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.participant-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.participant-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.participant-time {
  font-size: 12px;
  color: #999;
}

@media (max-width: 768px) {
  .activity-header {
    grid-template-columns: 1fr;
  }
  
  .activity-image {
    height: 250px;
  }
}
</style>