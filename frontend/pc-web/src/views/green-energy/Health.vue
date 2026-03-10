<template>
  <div class="health-management">
    <div class="page-header">
      <h1>🏥 健康管理</h1>
      <p>关注身心健康，拥抱绿色生活</p>
    </div>

    <div class="content-section">
      <div class="health-dashboard">
        <div class="health-stats">
          <div class="stat-card">
            <div class="stat-icon">❤️</div>
            <div class="stat-info">
              <div class="stat-value">85</div>
              <div class="stat-label">健康指数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🏃</div>
            <div class="stat-info">
              <div class="stat-value">30</div>
              <div class="stat-label">今日运动(分钟)</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">💧</div>
            <div class="stat-info">
              <div class="stat-value">1500</div>
              <div class="stat-label">今日饮水(ml)</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">😴</div>
            <div class="stat-info">
              <div class="stat-value">7</div>
              <div class="stat-label">昨日睡眠(小时)</div>
            </div>
          </div>
        </div>
      </div>

      <div class="health-sections">
        <div class="section-card">
          <div class="section-header">
            <h3>🏃 运动建议</h3>
          </div>
          <div class="section-content">
            <div class="exercise-tips">
              <div class="tip-item">
                <div class="tip-icon">🚶</div>
                <div class="tip-text">
                  <h4>每日步行</h4>
                  <p>每天坚持步行30分钟，有助于保持身体健康</p>
                </div>
              </div>
              <div class="tip-item">
                <div class="tip-icon">🧘</div>
                <div class="tip-text">
                  <h4>瑜伽练习</h4>
                  <p>每周进行2-3次瑜伽练习，有助于放松身心</p>
                </div>
              </div>
              <div class="tip-item">
                <div class="tip-icon">🏊</div>
                <div class="tip-text">
                  <h4>游泳锻炼</h4>
                  <p>游泳是一种低冲击的全身运动，适合各个年龄段</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="section-card">
          <div class="section-header">
            <h3>😴 睡眠管理</h3>
          </div>
          <div class="section-content">
            <div class="sleep-tips">
              <div class="tip-item">
                <div class="tip-icon">🌙</div>
                <div class="tip-text">
                  <h4>规律作息</h4>
                  <p>保持固定的睡眠时间，有助于提高睡眠质量</p>
                </div>
              </div>
              <div class="tip-item">
                <div class="tip-icon">📵</div>
                <div class="tip-text">
                  <h4>睡前放松</h4>
                  <p>睡前1小时避免使用电子设备，可阅读或听轻音乐</p>
                </div>
              </div>
              <div class="tip-item">
                <div class="tip-icon">🌡️</div>
                <div class="tip-text">
                  <h4>舒适环境</h4>
                  <p>保持卧室温度适宜，光线柔和，有助于入睡</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="section-card">
          <div class="section-header">
            <h3>🧠 心理健康</h3>
          </div>
          <div class="section-content">
            <div class="mental-tips">
              <div class="tip-item">
                <div class="tip-icon">🧘</div>
                <div class="tip-text">
                  <h4>冥想练习</h4>
                  <p>每天进行10-15分钟的冥想，有助于减轻压力</p>
                </div>
              </div>
              <div class="tip-item">
                <div class="tip-icon">🗣️</div>
                <div class="tip-text">
                  <h4>积极沟通</h4>
                  <p>与家人朋友保持良好沟通，分享感受</p>
                </div>
              </div>
              <div class="tip-item">
                <div class="tip-icon">🎨</div>
                <div class="tip-text">
                  <h4>兴趣爱好</h4>
                  <p>培养兴趣爱好，丰富生活，缓解压力</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="section-card">
          <div class="section-header">
            <h3>🌱 绿色健康生活方式</h3>
          </div>
          <div class="section-content">
            <div class="green-lifestyle-tips">
              <div class="tip-item">
                <div class="tip-icon">🌿</div>
                <div class="tip-text">
                  <h4>亲近自然</h4>
                  <p>定期到户外接触自然，呼吸新鲜空气</p>
                </div>
              </div>
              <div class="tip-item">
                <div class="tip-icon">🚲</div>
                <div class="tip-text">
                  <h4>绿色出行</h4>
                  <p>尽量选择步行、骑行或公共交通出行</p>
                </div>
              </div>
              <div class="tip-item">
                <div class="tip-icon">🏡</div>
                <div class="tip-text">
                  <h4>绿色家居</h4>
                  <p>使用环保材料，减少化学物质的使用</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 健康管理页面
</script>

<style scoped>
.health-management {
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

.health-dashboard {
  margin-bottom: 40px;
}

.health-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 48px;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #10b981;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.health-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.section-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.section-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
}

.section-header {
  background: #10b981;
  color: white;
  padding: 20px;
}

.section-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.section-content {
  padding: 25px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.tip-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.tip-icon {
  font-size: 32px;
  flex-shrink: 0;
  color: #10b981;
}

.tip-text h4 {
  font-size: 16px;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.tip-text p {
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
  
  .health-stats {
    grid-template-columns: 1fr;
  }
  
  .health-sections {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .section-content {
    padding: 20px;
  }
}
</style>