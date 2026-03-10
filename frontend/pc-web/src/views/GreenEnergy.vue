<template>
  <div class="green-energy">
    <div class="hero-section">
      <div class="hero-content">
        <h1>🌱 智慧绿能</h1>
        <p>探索绿色生活方式，共建可持续社区</p>
      </div>
    </div>

    <div class="content-section">
      <div class="module-grid">
        <router-link to="/green-energy/knowledge" class="module-card">
          <div class="module-icon">📚</div>
          <h3>绿色养生知识</h3>
          <p>了解绿色健康生活的各种知识和技巧</p>
        </router-link>

        <router-link to="/green-energy/garbage" class="module-card">
          <div class="module-icon">♻️</div>
          <h3>AI绿色垃圾分类</h3>
          <p>使用AI技术轻松识别和分类垃圾</p>
        </router-link>

        <router-link to="/green-energy/health" class="module-card">
          <div class="module-icon">🏥</div>
          <h3>健康管理</h3>
          <p>关注身心健康，拥抱绿色生活</p>
        </router-link>

        <router-link to="/green-energy/diet" class="module-card">
          <div class="module-icon">🥗</div>
          <h3>饮食养生</h3>
          <p>健康饮食，绿色生活</p>
        </router-link>

        <router-link to="/green-energy/carbon-footprint" class="module-card">
          <div class="module-icon">🌍</div>
          <h3>碳足迹计算器</h3>
          <p>计算您的日常生活碳排放量</p>
        </router-link>

        <router-link to="/green-energy/forum" class="module-card">
          <div class="module-icon">💬</div>
          <h3>绿色社区论坛</h3>
          <p>分享绿色生活经验，共同建设美好社区</p>
        </router-link>

        <router-link to="/green-energy/environment" class="module-card">
          <div class="module-icon">🌿</div>
          <h3>环保数据监测</h3>
          <p>实时监测社区环境数据，关注环境质量</p>
        </router-link>

        <router-link to="/green-energy/energy-tips" class="module-card">
          <div class="module-icon">💡</div>
          <h3>节能小贴士</h3>
          <p>根据您的生活习惯，获取个性化的节能建议</p>
        </router-link>

        <router-link to="/green-energy/shopping" class="module-card">
          <div class="module-icon">🛒</div>
          <h3>绿色购物指南</h3>
          <p>选择环保产品，为地球减负</p>
        </router-link>

        <router-link to="/green-energy/points" class="module-card">
          <div class="module-icon">🎯</div>
          <h3>绿色积分系统</h3>
          <p>通过环保行为获得积分，兑换丰富奖励</p>
        </router-link>

        <router-link to="/green-energy/ai-tips" class="module-card">
          <div class="module-icon">🤖</div>
          <h3>AI绿色生活建议</h3>
          <p>基于人工智能，为您提供个性化的绿色生活建议</p>
        </router-link>

        <router-link to="/green-energy/travel" class="module-card">
          <div class="module-icon">🚲</div>
          <h3>绿色出行规划</h3>
          <p>规划环保出行路线，减少碳排放</p>
        </router-link>

        <router-link to="/green-energy/home-energy" class="module-card">
          <div class="module-icon">🏠</div>
          <h3>家居节能优化</h3>
          <p>分析家居能耗，获取节能优化方案</p>
        </router-link>
      </div>
    </div>

    <div class="feature-section">
      <h2>🌿 绿色生活特色</h2>
      <div class="feature-grid">
        <div class="feature-item">
          <div class="feature-icon">🌍</div>
          <h3>环保意识</h3>
          <p>提高社区居民的环保意识，共同保护地球</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">💡</div>
          <h3>节能技巧</h3>
          <p>学习家庭节能技巧，减少能源消耗</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🚲</div>
          <h3>绿色出行</h3>
          <p>推广绿色出行方式，减少碳排放</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🌱</div>
          <h3>社区绿化</h3>
          <p>参与社区绿化活动，创造更美好的生活环境</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 智慧绿能模块主页面
</script>

<style scoped>
.green-energy {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}

.hero-section {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
}

.hero-content h1 {
  font-size: 48px;
  margin-bottom: 20px;
  font-weight: 600;
}

.hero-content p {
  font-size: 20px;
  opacity: 0.9;
}

.content-section {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.module-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.module-card {
  background: white;
  border-radius: 12px;
  padding: 40px 30px;
  text-align: center;
  text-decoration: none;
  color: #333;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.module-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.module-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.module-card h3 {
  font-size: 24px;
  margin-bottom: 15px;
  font-weight: 600;
  color: #10b981;
}

.module-card p {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
}

.feature-section {
  background: white;
  padding: 60px 20px;
  margin-top: 40px;
}

.feature-section h2 {
  text-align: center;
  font-size: 32px;
  margin-bottom: 40px;
  color: #10b981;
}

.feature-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.feature-item {
  text-align: center;
  padding: 30px;
  border-radius: 8px;
  background: #f8fafc;
  transition: all 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 36px;
  margin-bottom: 15px;
  color: #10b981;
}

.feature-item h3 {
  font-size: 20px;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.feature-item p {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 36px;
  }
  
  .hero-content p {
    font-size: 18px;
  }
  
  .content-section {
    padding: 40px 20px;
  }
  
  .module-grid {
    grid-template-columns: 1fr;
  }
  
  .feature-section {
    padding: 40px 20px;
  }
  
  .feature-section h2 {
    font-size: 28px;
  }
}
</style>