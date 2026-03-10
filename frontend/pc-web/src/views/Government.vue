<template>
  <div class="government-container">
    <div class="page-header">
      <h1>政务服务</h1>
      <p>便民政务，高效便捷</p>
    </div>
    
    <div class="service-grid">
      <div 
        v-for="service in services" 
        :key="service.id" 
        class="service-card"
        @click="openService(service)"
      >
        <div class="service-icon">{{ service.icon }}</div>
        <h3 class="service-name">{{ service.name }}</h3>
        <p class="service-desc">{{ service.description }}</p>
        <button class="service-btn">办理</button>
      </div>
    </div>
    
    <div class="notice-section">
      <h2>政务公告</h2>
      <div class="notice-list">
        <div 
          v-for="notice in notices" 
          :key="notice.id" 
          class="notice-item"
          @click="viewNotice(notice)"
        >
          <div class="notice-date">{{ notice.date }}</div>
          <div class="notice-content">
            <h4 class="notice-title">{{ notice.title }}</h4>
            <p class="notice-summary">{{ notice.summary }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const services = ref([
  {
    id: 1,
    name: '社保查询',
    description: '查询个人社保缴费情况',
    icon: '📋'
  },
  {
    id: 2,
    name: '公积金查询',
    description: '查询个人公积金账户余额',
    icon: '💰'
  },
  {
    id: 3,
    name: '居住证办理',
    description: '在线申请办理居住证',
    icon: '🏠'
  },
  {
    id: 4,
    name: '身份证补办',
    description: '身份证丢失补办申请',
    icon: '🪪'
  },
  {
    id: 5,
    name: '户籍办理',
    description: '户籍相关业务办理',
    icon: '📝'
  },
  {
    id: 6,
    name: '证件预约',
    description: '各类证件办理预约',
    icon: '📅'
  }
])

const notices = ref([
  {
    id: 1,
    title: '关于开展社区安全检查的通知',
    summary: '为保障社区居民生命财产安全，将于近期开展安全检查工作...',
    date: '2026-03-05'
  },
  {
    id: 2,
    title: '社区疫苗接种点开放通知',
    summary: '为方便居民接种，社区疫苗接种点将于下周开放...',
    date: '2026-03-04'
  },
  {
    id: 3,
    title: '社区文化活动安排公告',
    summary: '为丰富居民文化生活，社区将举办一系列文化活动...',
    date: '2026-03-03'
  }
])

const openService = (service) => {
  alert(`打开服务：${service.name}`)
}

const viewNotice = (notice) => {
  alert(`查看公告：${notice.title}`)
}
</script>

<style scoped>
.government-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0 0 10px;
}

.page-header p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.service-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.service-card {
  background: white;
  border-radius: 8px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid #e8e8e8;
}

.service-card:hover {
  border-color: #2196F3;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.service-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.service-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px;
}

.service-desc {
  font-size: 14px;
  color: #666;
  margin: 0 0 20px;
  line-height: 1.6;
}

.service-btn {
  padding: 8px 24px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
}

.service-btn:hover {
  background: #1976D2;
}

.notice-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
}

.notice-section h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 24px;
}

.notice-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.notice-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.notice-item:hover {
  background: #f0f0f0;
}

.notice-date {
  min-width: 100px;
  font-size: 14px;
  color: #999;
  font-weight: 500;
}

.notice-content {
  flex: 1;
}

.notice-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px;
}

.notice-summary {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .service-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
  }
  
  .service-card {
    padding: 20px 16px;
  }
  
  .service-icon {
    font-size: 36px;
  }
  
  .notice-item {
    flex-direction: column;
    gap: 12px;
  }
}
</style>