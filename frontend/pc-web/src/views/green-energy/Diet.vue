<template>
  <div class="diet-health">
    <div class="page-header">
      <h1>🥗 饮食养生</h1>
      <p>健康饮食，绿色生活</p>
    </div>

    <div class="content-section">
      <div class="diet-guide">
        <div class="guide-card">
          <div class="guide-icon">🍎</div>
          <h3>均衡饮食</h3>
          <p>合理搭配各类食物，保证营养均衡</p>
          <ul class="guide-list">
            <li>🍅 多吃新鲜蔬菜水果</li>
            <li>🥩 适量摄入蛋白质</li>
            <li>🍞 选择全谷物食品</li>
            <li>🥛 保证钙质摄入</li>
          </ul>
        </div>

        <div class="guide-card">
          <div class="guide-icon">🌱</div>
          <h3>绿色饮食</h3>
          <p>选择绿色、有机、环保的食物</p>
          <ul class="guide-list">
            <li>🥬 选择当季蔬菜</li>
            <li>🍓 选择有机水果</li>
            <li>🐔 选择散养家禽</li>
            <li>🌾 选择有机谷物</li>
          </ul>
        </div>

        <div class="guide-card">
          <div class="guide-icon">💧</div>
          <h3>健康饮水</h3>
          <p>保持充足的水分摄入</p>
          <ul class="guide-list">
            <li>💦 每天喝够8杯水</li>
            <li>🍵 适量饮用茶水</li>
            <li>🥤 减少含糖饮料</li>
            <li>🧊 避免过量饮用冰水</li>
          </ul>
        </div>
      </div>

      <div class="seasonal-recipes">
        <h2>🍲 季节养生食谱</h2>
        <div class="recipe-grid">
          <div 
            v-for="recipe in seasonalRecipes" 
            :key="recipe.id"
            class="recipe-card"
          >
            <div class="recipe-image">
              <div class="image-placeholder">{{ recipe.icon }}</div>
            </div>
            <div class="recipe-content">
              <h3>{{ recipe.name }}</h3>
              <p class="recipe-season">{{ recipe.season }}</p>
              <p class="recipe-description">{{ recipe.description }}</p>
              <div class="recipe-ingredients">
                <h4>主要食材</h4>
                <div class="ingredient-list">
                  <span v-for="(ingredient, index) in recipe.ingredients" :key="index" class="ingredient-tag">
                    {{ ingredient }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="nutrition-tips">
        <h2>💡 营养小贴士</h2>
        <div class="tip-grid">
          <div class="tip-card">
            <div class="tip-icon">🥗</div>
            <h3>膳食纤维</h3>
            <p>多吃富含膳食纤维的食物，有助于消化健康</p>
          </div>
          <div class="tip-card">
            <div class="tip-icon">🍊</div>
            <h3>维生素C</h3>
            <p>多吃富含维生素C的食物，增强免疫力</p>
          </div>
          <div class="tip-card">
            <div class="tip-icon">🥜</div>
            <h3>健康脂肪</h3>
            <p>适量摄入健康脂肪，如坚果、橄榄油等</p>
          </div>
          <div class="tip-card">
            <div class="tip-icon">🥛</div>
            <h3>钙质</h3>
            <p>保证足够的钙质摄入，维持骨骼健康</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const seasonalRecipes = [
  {
    id: 1,
    name: '春季养生粥',
    season: '春季',
    icon: '🌸',
    description: '春季养生粥，具有养肝明目、健脾开胃的功效',
    ingredients: ['大米', '小米', '枸杞', '红枣', '山药']
  },
  {
    id: 2,
    name: '夏季清凉汤',
    season: '夏季',
    icon: '☀️',
    description: '夏季清凉汤，具有清热解暑、生津止渴的功效',
    ingredients: ['西瓜', '荷叶', '绿豆', '冰糖', '银耳']
  },
  {
    id: 3,
    name: '秋季润燥茶',
    season: '秋季',
    icon: '🍂',
    description: '秋季润燥茶，具有润肺止咳、养阴润燥的功效',
    ingredients: ['梨', '百合', '银耳', '蜂蜜', '枸杞']
  },
  {
    id: 4,
    name: '冬季温补汤',
    season: '冬季',
    icon: '❄️',
    description: '冬季温补汤，具有温阳散寒、益气补血的功效',
    ingredients: ['羊肉', '生姜', '红枣', '当归', '枸杞']
  }
]
</script>

<style scoped>
.diet-health {
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

.diet-guide {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.guide-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  text-align: center;
}

.guide-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.guide-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.guide-card h3 {
  font-size: 20px;
  margin-bottom: 15px;
  font-weight: 600;
  color: #10b981;
}

.guide-card p {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 20px;
}

.guide-list {
  text-align: left;
  padding-left: 20px;
}

.guide-list li {
  font-size: 14px;
  line-height: 1.8;
  color: #666;
  list-style: none;
  position: relative;
  padding-left: 10px;
}

.guide-list li:before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  width: 4px;
  height: 4px;
  background: #10b981;
  border-radius: 50%;
}

.seasonal-recipes {
  margin-bottom: 60px;
}

.seasonal-recipes h2 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 30px;
  color: #10b981;
}

.recipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.recipe-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.recipe-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.recipe-image {
  height: 200px;
  background: #f0fdf4;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder {
  font-size: 64px;
}

.recipe-content {
  padding: 25px;
}

.recipe-content h3 {
  font-size: 18px;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.recipe-season {
  font-size: 12px;
  padding: 4px 12px;
  background: #d1fae5;
  color: #065f46;
  border-radius: 12px;
  display: inline-block;
  margin-bottom: 15px;
}

.recipe-description {
  font-size: 14px;
  line-height: 1.5;
  color: #666;
  margin-bottom: 20px;
}

.recipe-ingredients h4 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
}

.ingredient-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ingredient-tag {
  padding: 4px 12px;
  background: #f3f4f6;
  color: #666;
  border-radius: 12px;
  font-size: 12px;
}

.nutrition-tips {
  background: white;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nutrition-tips h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  color: #10b981;
}

.tip-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.tip-card {
  text-align: center;
  padding: 25px;
  background: #f8fafc;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tip-icon {
  font-size: 36px;
  margin-bottom: 15px;
  color: #10b981;
}

.tip-card h3 {
  font-size: 16px;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.tip-card p {
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
  
  .diet-guide {
    grid-template-columns: 1fr;
  }
  
  .recipe-grid {
    grid-template-columns: 1fr;
  }
  
  .nutrition-tips {
    padding: 20px;
  }
  
  .tip-grid {
    grid-template-columns: 1fr;
  }
}
</style>