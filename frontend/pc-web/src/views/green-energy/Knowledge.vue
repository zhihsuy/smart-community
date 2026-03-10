<template>
  <div class="green-knowledge">
    <div class="page-header">
      <h1>📚 绿色养生知识</h1>
      <p>探索绿色健康生活的各种知识和技巧</p>
    </div>

    <div class="content-section">
      <div class="knowledge-categories">
        <button 
          v-for="category in categories" 
          :key="category.id"
          :class="{ active: selectedCategory === category.id }"
          @click="selectedCategory = category.id"
        >
          {{ category.icon }} {{ category.name }}
        </button>
      </div>

      <div class="knowledge-articles">
        <div 
          v-for="article in filteredArticles" 
          :key="article.id"
          class="article-card"
        >
          <div class="article-header">
            <h3>{{ article.title }}</h3>
            <span class="article-date">{{ article.date }}</span>
          </div>
          <div class="article-content">
            <p>{{ article.summary }}</p>
          </div>
          <div class="article-footer">
            <span class="article-tag">{{ article.category }}</span>
            <button class="read-more-btn">阅读更多</button>
          </div>
        </div>
      </div>

      <div class="tips-section">
        <h2>💡 绿色生活小贴士</h2>
        <div class="tips-grid">
          <div class="tip-item" v-for="tip in greenTips" :key="tip.id">
            <div class="tip-icon">{{ tip.icon }}</div>
            <p>{{ tip.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const selectedCategory = ref('all')

const categories = [
  { id: 'all', name: '全部', icon: '📋' },
  { id: 'diet', name: '饮食健康', icon: '🥗' },
  { id: 'exercise', name: '运动养生', icon: '🏃' },
  { id: 'environment', name: '环境健康', icon: '🌱' },
  { id: 'mental', name: '心理健康', icon: '🧠' }
]

const articles = [
  {
    id: 1,
    title: '如何打造绿色健康的家居环境',
    summary: '绿色家居环境对身体健康至关重要。本文将介绍如何通过简单的方法打造一个健康、环保的家居环境，包括选择环保材料、合理布置绿植、保持通风等方面。',
    category: '环境健康',
    date: '2026-03-01'
  },
  {
    id: 2,
    title: '春季养生食谱推荐',
    summary: '春季是养生的好时节，本文推荐几款适合春季食用的健康食谱，帮助您调理身体，增强免疫力。',
    category: '饮食健康',
    date: '2026-02-28'
  },
  {
    id: 3,
    title: '适合中老年人的绿色运动方式',
    summary: '中老年人适当的运动对健康非常重要。本文介绍几种适合中老年人的低强度绿色运动方式，帮助他们保持身体健康。',
    category: '运动养生',
    date: '2026-02-25'
  },
  {
    id: 4,
    title: '如何在现代生活中保持心理健康',
    summary: '现代生活节奏快，压力大，保持心理健康尤为重要。本文分享一些实用的方法，帮助您在忙碌的生活中保持心理平衡。',
    category: '心理健康',
    date: '2026-02-20'
  },
  {
    id: 5,
    title: '绿色出行方式及其 benefits',
    summary: '绿色出行不仅有利于环境保护，也对个人健康有益。本文介绍几种绿色出行方式及其好处，鼓励大家选择更环保的交通方式。',
    category: '环境健康',
    date: '2026-02-15'
  },
  {
    id: 6,
    title: '夏季养生注意事项',
    summary: '夏季天气炎热，养生需要特别注意。本文介绍夏季养生的注意事项，帮助您安全度过炎热的夏天。',
    category: '饮食健康',
    date: '2026-02-10'
  }
]

const greenTips = [
  { id: 1, icon: '💧', content: '每天喝够8杯水，保持身体水分平衡' },
  { id: 2, icon: '🌞', content: '适当晒太阳，促进维生素D的合成' },
  { id: 3, icon: '🌱', content: '在室内摆放绿植，改善空气质量' },
  { id: 4, icon: '🚶', content: '每天步行30分钟，保持身体健康' },
  { id: 5, icon: '😴', content: '保证充足的睡眠时间，有利于身体恢复' },
  { id: 6, icon: '🍎', content: '多吃新鲜蔬菜水果，补充维生素和矿物质' }
]

const filteredArticles = computed(() => {
  if (selectedCategory.value === 'all') {
    return articles
  }
  return articles.filter(article => article.category === categories.find(c => c.id === selectedCategory.value)?.name)
})
</script>

<style scoped>
.green-knowledge {
  min-height: 100vh;
  background: #f8fafc;
}

.page-header {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
}

.page-header h1 {
  font-size: 36px;
  margin-bottom: 10px;
  font-weight: 600;
}

.page-header p {
  font-size: 18px;
  opacity: 0.9;
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.knowledge-categories {
  display: flex;
  gap: 10px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.knowledge-categories button {
  padding: 10px 20px;
  border: 1px solid #10b981;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.knowledge-categories button:hover {
  background: #10b981;
  color: white;
}

.knowledge-categories button.active {
  background: #10b981;
  color: white;
}

.knowledge-articles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.article-card {
  background: white;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.article-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
  flex: 1;
}

.article-date {
  font-size: 12px;
  color: #999;
}

.article-content p {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  margin-bottom: 20px;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-tag {
  font-size: 12px;
  padding: 4px 12px;
  background: #d1fae5;
  color: #065f46;
  border-radius: 12px;
}

.read-more-btn {
  padding: 6px 16px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.read-more-btn:hover {
  background: #059669;
}

.tips-section {
  background: white;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.tips-section h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #10b981;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 15px;
  background: #f8fafc;
  border-radius: 6px;
}

.tip-icon {
  font-size: 24px;
  flex-shrink: 0;
  color: #10b981;
}

.tip-item p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin: 0;
}

@media (max-width: 768px) {
  .page-header {
    padding: 40px 20px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .content-section {
    padding: 20px;
  }
  
  .knowledge-articles {
    grid-template-columns: 1fr;
  }
  
  .tips-section {
    padding: 20px;
  }
  
  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>