<template>
  <div class="services-container">
    <div class="page-header">
      <h1>社区服务</h1>
      <p>便民服务，贴心周到</p>
    </div>
    
    <div class="service-categories">
      <div 
        v-for="category in categories" 
        :key="category.id"
        :class="['category-card', { active: selectedCategory === category.id }]"
        @click="selectedCategory = category.id"
      >
        <div class="category-icon">{{ category.icon }}</div>
        <div class="category-name">{{ category.name }}</div>
      </div>
    </div>
    
    <div class="services-list">
      <div 
        v-for="service in filteredServices" 
        :key="service.id" 
        class="service-card"
      >
        <div class="service-image">
          <img :src="service.image" :alt="service.name" />
        </div>
        <div class="service-info">
          <h3 class="service-name">{{ service.name }}</h3>
          <p class="service-desc">{{ service.description }}</p>
          <div class="service-meta">
            <span class="price">¥{{ service.price }}</span>
            <span class="rating">⭐ {{ service.rating }}</span>
          </div>
          <div class="service-contact">
            <span class="contact-item">📞 {{ service.phone }}</span>
            <span class="contact-item">📍 {{ service.location }}</span>
          </div>
          <button class="book-btn" @click="bookService(service)">预约服务</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const selectedCategory = ref('')

const categories = [
  { id: '', name: '全部', icon: '🏠' },
  { id: 'repair', name: '维修服务', icon: '🔧' },
  { id: 'clean', name: '清洁服务', icon: '🧹' },
  { id: 'care', name: '家政服务', icon: '👨‍👩‍👧' },
  { id: 'delivery', name: '配送服务', icon: '📦' }
]

const services = ref([
  {
    id: 1,
    name: '水电维修',
    description: '专业水电维修师傅，快速响应，质量保证',
    image: 'https://via.placeholder.com/300x200?text=水电维修',
    price: 50,
    rating: 4.8,
    phone: '138-0000-0001',
    location: '社区维修中心',
    category: 'repair'
  },
  {
    id: 2,
    name: '家电维修',
    description: '空调、冰箱、洗衣机等家电专业维修',
    image: 'https://via.placeholder.com/300x200?text=家电维修',
    price: 80,
    rating: 4.7,
    phone: '138-0000-0002',
    location: '社区维修中心',
    category: 'repair'
  },
  {
    id: 3,
    name: '家庭清洁',
    description: '专业清洁团队，让您的家焕然一新',
    image: 'https://via.placeholder.com/300x200?text=家庭清洁',
    price: 100,
    rating: 4.9,
    phone: '138-0000-0003',
    location: '社区服务中心',
    category: 'clean'
  },
  {
    id: 4,
    name: '老人照护',
    description: '专业照护人员，贴心服务老人',
    image: 'https://via.placeholder.com/300x200?text=老人照护',
    price: 150,
    rating: 4.8,
    phone: '138-0000-0004',
    location: '社区养老中心',
    category: 'care'
  },
  {
    id: 5,
    name: '快递代收',
    description: '便捷快递代收服务，安全可靠',
    image: 'https://via.placeholder.com/300x200?text=快递代收',
    price: 2,
    rating: 4.6,
    phone: '138-0000-0005',
    location: '社区快递点',
    category: 'delivery'
  }
])

const filteredServices = computed(() => {
  if (!selectedCategory.value) {
    return services.value
  }
  return services.value.filter(s => s.category === selectedCategory.value)
})

const bookService = (service) => {
  alert(`预约服务：${service.name}`)
}
</script>

<style scoped>
.services-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
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

.service-categories {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.category-card {
  flex: 1;
  min-width: 120px;
  background: white;
  border: 2px solid #e8e8e8;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.category-card:hover {
  border-color: #2196F3;
  transform: translateY(-2px);
}

.category-card.active {
  border-color: #2196F3;
  background: #E3F2FD;
}

.category-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.category-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.services-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.service-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.service-image {
  height: 180px;
  overflow: hidden;
}

.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-info {
  padding: 20px;
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
  margin: 0 0 16px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.service-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.price {
  font-size: 20px;
  font-weight: 600;
  color: #FF5722;
}

.rating {
  font-size: 14px;
  color: #FFC107;
}

.service-contact {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #666;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.book-btn {
  width: 100%;
  padding: 12px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s;
}

.book-btn:hover {
  background: #1976D2;
}

@media (max-width: 768px) {
  .service-categories {
    flex-wrap: wrap;
  }
  
  .category-card {
    min-width: calc(50% - 10px);
  }
}
</style>