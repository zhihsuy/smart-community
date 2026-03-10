<template>
  <div class="building-manage-container">
    <div class="page-header">
      <h1>楼栋管理</h1>
      <p>运营人员楼栋管理界面</p>
    </div>
    
    <div class="building-list">
      <div class="building-item" v-for="building in buildings" :key="building.id">
        <div class="building-info">
          <h3>{{ building.name }}</h3>
          <p>单元数: {{ building.unit_count }}</p>
          <p>层数: {{ building.floor_count }}</p>
          <p>户数: {{ building.household_count }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 状态
const buildings = ref([])

// 方法
const fetchBuildings = async () => {
  try {
    const response = await axios.get('/api/v1/pc/building/op/list')
    
    if (response.data.code === 0) {
      buildings.value = response.data.data
    }
  } catch (error) {
    console.error('获取楼栋列表失败:', error)
  }
}

// 初始化
onMounted(() => {
  fetchBuildings()
})
</script>

<style scoped>
.building-manage-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 24px;
  margin: 0 0 10px;
}

.page-header p {
  color: #666;
  margin: 0;
}

.building-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.building-item {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.building-info h3 {
  margin: 0 0 15px;
  font-size: 18px;
  color: #333;
}

.building-info p {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
}
</style>