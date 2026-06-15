<template>
  <div class="home-container">
    <!-- 顶部问候区 -->
    <div class="header">
      <div class="greeting">
        <h1>Hello, <span class="username">同学</span></h1>
        <p class="sub-greeting">今天有什么新计划？</p>
      </div>
      <div class="avatar-container">
        <div class="avatar">
          <img src="https://images.unsplash.com/photo-1519681393784-d120267933ba" alt="用户头像" />
        </div>
      </div>
    </div>

    <!-- 搜索框 -->
    <div class="search-bar" @tap="focusSearch">
      <input
        class="search-input"
        placeholder="搜竞赛、实习、考研资料..."
        v-model="searchKeyword"
        confirm-type="search"
        :focus="searchFocus"
        @focus="onSearchFocus"
        @blur="onSearchBlur"
        @confirm="doSearch"
      />
      <div class="search-button">
        <img src="/static/icons/res.png" alt="搜索" class="search-img" />
      </div>
    </div>

    <!-- 四宫格功能入口 -->
    <div class="quick-actions">
      <div class="action-item" v-for="item in actions" :key="item.id" @click="handleActionClick(item.id)">
        <div class="action-icon" :style="{ backgroundColor: item.color }">
          <span v-if="!item.image" class="icon">{{ item.icon }}</span>
          <img v-else :src="item.image" alt="icon" class="action-img" />
        </div>
        <div class="action-text">{{ item.text }}</div>
        <div class="action-badge" v-if="item.badge">{{ item.badge }}</div>
      </div>
    </div>
	
    <!-- 情绪卡片模块 -->
    <div class="mood-card-section">
      <div class="section-header">
        <div class="section-title">
          <div class="title-decoration"></div>
          <h2>今日心情</h2>
        </div>
        <div class="view-all" @click="goToDiary">
          写日记 >
        </div>
      </div>
	  
      <div class="mood-card" @click="goToDiary" :class="moodClass">
        <div class="mood-card-bg">
          <div class="mood-particles">
            <span class="particle" v-for="n in 8" :key="n">✨</span>
          </div>
        </div>
        
        <div class="mood-card-header">
          <div class="mood-emoji">{{ todayMood.emoji }}</div>
          <div class="mood-badge">{{ todayMood.moodName }}</div>
        </div>
        
        <div class="mood-message">
          <p class="message-text">{{ todayMood.message }}</p>
        </div>
        
        <div class="mood-footer">
          <div class="mood-suggestion">
            <span class="suggestion-icon">💡</span>
            <span class="suggestion-text">{{ todayMood.suggestion }}</span>
          </div>
          <div class="mood-action">
            <span class="action-arrow">→</span>
          </div>
        </div>
        
        <!-- 如果没有日记，显示提示 -->
        <div class="mood-empty" v-if="!hasTodayDiary">
          <div class="empty-icon">🌸</div>
          <div class="empty-text">今天还没有记录心情，</div>
          <div class="empty-subtext">点击写下你的第一篇日记</div>
        </div>
      </div>
    </div>

    <!-- 热门推荐区 -->
    <div class="recommendations">
      <div class="section-header">
        <div class="section-title">
          <div class="title-decoration"></div>
          <h2>热门推荐</h2>
        </div>
        <div class="view-all" @click="viewAllRecommendations">
          查看全部 >
        </div>
      </div>
      
      <div class="cards-container">
        <div class="cards-wrapper" ref="cardsWrapper">
          <div 
            class="card" 
            v-for="card in cards" 
            :key="card.id"
            :style="{ backgroundImage: `linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.2) 50%, transparent 100%), url(${card.image})` }"
            @click="viewCardDetail(card.id)"
          >
            <div class="card-badge" v-if="card.badge">{{ card.badge }}</div>
            <div class="card-content">
              <div class="card-tags" v-if="card.tags">
                <span class="tag" v-for="tag in card.tags" :key="tag">{{ tag }}</span>
              </div>
              <h3 class="card-title">{{ card.title }}</h3>
              <p class="card-subtitle">{{ card.subtitle }}</p>
              <div class="card-footer">
                <div class="card-stats">
                  <span class="stat">👤 {{ card.participants }}</span>
                  <span class="stat">⭐ {{ card.rating }}</span>
                </div>
                <div class="card-action">开始学习</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 滑动指示点 -->
        <div class="indicator-dots">
          <div 
            class="dot" 
            v-for="(card, index) in cards" 
            :key="index"
            :class="{ active: currentCardIndex === index }"
            @click="scrollToCard(index)"
          ></div>
        </div>
      </div>
    </div>

    <!-- 浮动操作按钮 -->
    <div class="floating-action-btn" @click="createNewPlan">
      <div class="fab-icon">+</div>
      <div class="fab-text">创建新计划</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { onPullDownRefresh, onShow } from '@dcloudio/uni-app'
const showGuide = ref(true)
const searchKeyword = ref('')
const searchFocus = ref(false)
const currentCardIndex = ref(0)

// 从后端获取的数据
const cards = ref([])
// 页面显示时刷新数据（例如从日记页返回）
onShow(() => {
  fetchTodayMood()
  fetchHomeCards()
})

// 下拉刷新
onPullDownRefresh(() => {
  fetchTodayMood()
  fetchHomeCards()
  // 停止下拉刷新动画
  uni.stopPullDownRefresh()
})
// 四宫格功能数据
const actions = ref([
  { 
    id: 1, 
    image: '/static/icons/wayy.png',
    text: '我的路径', 
    badge: '3' 
  },
  { 
    id: 2, 
    image: '/static/icons/right1.png',
    text: '今日打卡', 
    badge: '2' 
  },
  { 
    id: 3, 
    image: '/static/icons/studyy.png',
    text: '学习资源', 
  },
  { 
    id: 4, 
    image: '/static/icons/jiyu.png',
    text: '机会推荐', 
    badge: '新' 
  }
])

// ============ 情绪卡片相关 ============
const todayMood = ref({
  emoji: '🌸',
  moodName: '等待记录',
  message: '今天还没有记录心情日记，点击开始记录你的情绪吧',
  suggestion: '写日记能帮助整理思绪',
  type: 'peaceful'
})

const hasTodayDiary = ref(false)

// 情绪映射
const moodMap = {
  1: { emoji: '🌈', name: '闪闪发光', type: 'happy' },
  2: { emoji: '🌻', name: '温暖生长', type: 'peaceful' },
  3: { emoji: '🎐', name: '微风思绪', type: 'thoughtful' },
  4: { emoji: '☔', name: '雨滴心情', type: 'sad' },
  5: { emoji: '🎪', name: '马戏团日', type: 'excited' },
  6: { emoji: '🧩', name: '拼图时刻', type: 'confused' }
}

// 情绪鼓励语
const encouragementMessages = {
  1: [
    '今天的你像阳光一样耀眼，继续保持这份热情！',
    '快乐是会传染的，把今天的开心分享给身边的人吧',
    '每一个闪闪发光的日子都值得被记住'
  ],
  2: [
    '平静的日子里，藏着最温柔的力量',
    '像大树一样，在安静中生长',
    '今天的平静是为了明天更好的出发'
  ],
  3: [
    '思考让心灵更丰富，你的困惑会变成智慧',
    '慢慢来，答案会在思考中浮现',
    '每一次思考都是在给未来铺路'
  ],
  4: [
    '雨过总会天晴，给自己一个温暖的拥抱',
    '难过的时候，记得你并不孤单',
    '今天的眼泪会浇灌出明天的花朵'
  ],
  5: [
    '保持这份热情，它能带你到达任何地方',
    '兴奋的心情是最好的动力',
    '把今天的能量留给最重要的事'
  ],
  6: [
    '困惑是成长的开始，不要害怕提问',
    '每一个问题都在帮你看清方向',
    '慢慢来，答案就在不远处'
  ]
}

// 情绪建议
const moodSuggestions = {
  1: '对着镜子说一句"今天我也很棒"',
  2: '闭眼深呼吸三次，感受当下的平静',
  3: '把想法写下来，让思绪更清晰',
  4: '泡一杯热茶，给自己一些温暖',
  5: '把今天的能量分享给一个人',
  6: '把大问题拆成小问题，一步步解决'
}

// 计算情绪卡片类名
const moodClass = computed(() => {
  return todayMood.value.type || 'peaceful'
})

// 获取今天的情绪数据
const fetchTodayMood = () => {
  try {
    const diaries = uni.getStorageSync('infog-mood-diaries')
    if (diaries) {
      const diaryList = JSON.parse(diaries)
      const today = new Date().toDateString()
      
      const todayDiary = diaryList.find(d => {
        const diaryDate = new Date(d.date).toDateString()
        return diaryDate === today
      })
      
      if (todayDiary) {
        hasTodayDiary.value = true
        const moodId = todayDiary.predicted_mood || todayDiary.manual_mood || 2
        const moodInfo = moodMap[moodId] || moodMap[2]
        const messages = encouragementMessages[moodId] || encouragementMessages[2]
        const randomIndex = Math.floor(Math.random() * messages.length)
        
        todayMood.value = {
          emoji: moodInfo.emoji,
          moodName: moodInfo.name,
          message: messages[randomIndex],
          suggestion: moodSuggestions[moodId] || moodSuggestions[2],
          type: moodInfo.type
        }
      } else {
        hasTodayDiary.value = false
        todayMood.value = {
          emoji: '🌸',
          moodName: '等待记录',
          message: '今天还没有记录心情日记，点击开始记录你的情绪吧',
          suggestion: '写日记能帮助整理思绪',
          type: 'peaceful'
        }
      }
    }
  } catch (error) {
    console.error('获取今日情绪失败:', error)
  }
}

// 跳转到日记页面
const goToDiary = () => {
  uni.switchTab({
    url: '/pages/diary/diary',
    success: () => console.log('跳转到日记页面成功'),
    fail: (err) => console.error('跳转失败:', err)
  })
}

// 获取首页卡片数据
const fetchHomeCards = async () => {
  try {
    const res = await uni.request({
      url: 'http://127.0.0.1:8000/api/home-cards',
      method: 'GET'
    })
    console.log('首页卡片数据:', res.data)
    cards.value = res.data
  } catch (error) {
    console.error('获取首页卡片失败:', error)
    // 默认数据
    cards.value = [
      { 
        id: 1, 
        title: '前端工程师职业路径', 
        subtitle: '系统学习前端开发，掌握核心技能',
        image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4',
        badge: '热',
        tags: ['前端', '编程'],
        participants: '2.4k',
        rating: 4.8
      },
      { 
        id: 2, 
        title: '产品经理成长计划', 
        subtitle: '从0到1掌握产品思维',
        image: 'https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e',
        badge: '新',
        tags: ['产品', '管理'],
        participants: '1.8k',
        rating: 4.9
      }
    ]
  }
}

// 搜索相关函数
const focusSearch = () => {
  searchFocus.value = true
}

const onSearchFocus = () => {
  console.log('搜索框获得焦点')
  searchFocus.value = true
}

const onSearchBlur = () => {
  console.log('搜索框失焦')
}

const doSearch = () => {
  if (!searchKeyword.value.trim()) {
    uni.showToast({ title: '请输入搜索内容', icon: 'none' })
    return
  }
  console.log('执行搜索：', searchKeyword.value)
  uni.showToast({ title: `搜索：${searchKeyword.value}`, icon: 'none' })
}

// 处理功能入口点击
const handleActionClick = (id) => {
  console.log('点击功能入口:', id)
  
  if (id === 1) {
    uni.switchTab({
      url: '/pages/path2/path2',
      success: () => console.log('跳转到我的路径成功'),
      fail: (err) => console.error('跳转失败:', err)
    })
    return
  }
  
  const pages = {
    2: '/pages/checkin/checkin',
    3: '/pages/info/list',
    4: '/pages/opportunities/recommend'
  }
  
  const targetUrl = pages[id]
  if (targetUrl) {
    uni.navigateTo({
      url: targetUrl,
      success: () => console.log('跳转成功:', targetUrl),
      fail: (err) => console.error('跳转失败:', err)
    })
  } else {
    uni.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  }
}

// 查看卡片详情
const viewCardDetail = (id) => {
  console.log('查看卡片详情:', id)
  uni.showToast({ title: `查看卡片 ${id} 的详细内容`, icon: 'none' })
}

// 查看全部推荐
const viewAllRecommendations = () => {
  uni.navigateTo({
    url: '/pages/info/list',
  })
}

// 创建新计划
const createNewPlan = () => {
  console.log('创建新计划')
  uni.showToast({ title: '打开创建新计划页面', icon: 'none' })
}

// 滚动到指定卡片
const scrollToCard = (index) => {
  currentCardIndex.value = index
  const cardsWrapper = document.querySelector('.cards-wrapper')
  if (cardsWrapper) {
    const cardWidth = 500
    const gap = 32
    cardsWrapper.scrollTo({
      left: index * (cardWidth + gap),
      behavior: 'smooth'
    })
  }
}

// 卡片滑动相关
const cardsWrapper = ref(null)
let startX = 0
let isDragging = false

const handleTouchStart = (e) => {
  startX = e.touches[0].clientX
  isDragging = true
}

const handleTouchMove = (e) => {
  if (!isDragging) return
  const currentX = e.touches[0].clientX
  const diff = startX - currentX
  
  if (Math.abs(diff) > 50) {
    if (diff > 0 && currentCardIndex.value < cards.value.length - 1) {
      currentCardIndex.value++
    } else if (diff < 0 && currentCardIndex.value > 0) {
      currentCardIndex.value--
    }
    isDragging = false
    scrollToCard(currentCardIndex.value)
  }
}

const handleTouchEnd = () => {
  isDragging = false
}

const handleScroll = () => {
  if (cardsWrapper.value) {
    const scrollLeft = cardsWrapper.value.scrollLeft
    const cardWidth = 500
    const gap = 32
    const index = Math.round(scrollLeft / (cardWidth + gap))
    if (index >= 0 && index < cards.value.length) {
      currentCardIndex.value = index
    }
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchHomeCards()
  fetchTodayMood()
  
  if (cardsWrapper.value) {
    cardsWrapper.value.addEventListener('touchstart', handleTouchStart)
    cardsWrapper.value.addEventListener('touchmove', handleTouchMove)
    cardsWrapper.value.addEventListener('touchend', handleTouchEnd)
    cardsWrapper.value.addEventListener('scroll', handleScroll)
  }
})
</script>

<style scoped>
/* 这里保留您原来的所有样式，完全不变 */
/* 保留您原来的所有样式，只替换情绪卡片相关部分 */
body {
	overflow: auto; /* 改为 auto，允许滚动 */
	  -webkit-overflow-scrolling: touch; /* 添加平滑滚动 */

}

.app-container::before {
  display: none;
}

.home-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #FFFFFF 0%, #FFF8F3 100%);
  padding: 40rpx 32rpx 80rpx;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
 overflow-y: auto; /* 确保这里有这个属性 */
  -webkit-overflow-scrolling: touch;
}

/* 顶部问候区样式 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 48rpx;
}

.greeting h1 {
  font-size: 52rpx;
  font-weight: 800;
  color: #333333;
  margin: 0 0 12rpx;
  line-height: 1.2;
}

.sub-greeting {
  font-size: 30rpx;
  color: #666666;
  margin: 0;
  opacity: 0.8;
}

.username {
  font-style: italic;
  color: #F98C53;
  font-weight: 900;
}

.avatar-container {
  position: relative;
}

.avatar {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  border: 3rpx solid #F98C53;
  overflow: hidden;
  box-shadow: 0 8rpx 24rpx rgba(249, 140, 83, 0.25);
  transition: transform 0.3s ease;
}

.avatar:hover {
  transform: scale(1.05);
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 搜索框样式 */
.search-bar {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 50rpx;
  height: 100rpx;
  padding: 0 8rpx 0 40rpx;
  margin-bottom: 60rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.search-bar:focus-within {
  box-shadow: 0 12rpx 40rpx rgba(249, 140, 83, 0.2);
  transform: translateY(-2rpx);
}

.search-input {
  flex: 1;
  font-size: 30rpx;
  color: #333;
  background: transparent;
  border: none;
  outline: none;
}

.search-input::placeholder {
  color: #999999;
  font-size: 30rpx;
}

.search-button {
  width: 84rpx;
  height: 84rpx;
  background: #ffe3b4;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4rpx 16rpx rgba(249, 140, 83, 0.3);
  overflow: hidden;
}

.search-img {
  width: 45rpx;
  height: 45rpx;
  object-fit: contain;
}

.search-button:hover {
  transform: scale(1.08) rotate(5deg);
  background: #ff7c3a;
  box-shadow: 0 6rpx 20rpx rgba(249, 140, 83, 0.4);
}

/* 四宫格功能入口 - 极致清透版 */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20rpx;
  margin-bottom: 80rpx;
  padding: 0 12rpx;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.action-icon {
  width: 112rpx;
  height: 112rpx;
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16rpx;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.25);
  border: 1rpx solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.02);
  transition: all 0.2s ease;
}

.action-item:active .action-icon {
  background: rgba(255, 255, 255, 0.4);
  transform: scale(0.96);
}

.action-img {
  width: 72rpx;
  height: 72rpx;
  object-fit: contain;
  filter: drop-shadow(0 2rpx 4rpx rgba(0, 0, 0, 0.05));
}

.action-text {
  font-size: 26rpx;
  color: #4A4A4A;
  font-weight: 500;
  letter-spacing: 0.5rpx;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.action-item:active .action-text {
  opacity: 1;
}

.action-badge {
  position: absolute;
  top: -4rpx;
  right: 12rpx;
  background: #FF6B6B;
  color: white;
  font-size: 18rpx;
  font-weight: 600;
  padding: 2rpx 10rpx;
  border-radius: 20rpx;
  min-width: 24rpx;
  text-align: center;
  box-shadow: 0 2rpx 6rpx rgba(255, 107, 107, 0.2);
  border: 1rpx solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(2rpx);
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .action-icon {
    background: rgba(255, 255, 255, 0.1);
    border: 1rpx solid rgba(255, 255, 255, 0.15);
  }
  
  .action-text {
    color: #E0E0E0;
    opacity: 0.9;
  }
  
  .action-img {
    filter: drop-shadow(0 2rpx 4rpx rgba(0, 0, 0, 0.2));
  }
}

/* 可选：为不同图标添加微弱的个性化光晕（非常淡） */
.action-item:nth-child(1) .action-icon {
  background: rgba(255, 170, 0, 0.08);
}

.action-item:nth-child(2) .action-icon {
  background: rgba(173, 218, 254, 0.1);
}

.action-item:nth-child(3) .action-icon {
  background: rgba(255, 140, 200, 0.1);
}

.action-item:nth-child(4) .action-icon {
  background: rgba(163, 242, 120, 0.1);
}

/* ========== 情绪卡片模块 - 温暖治愈淡绿色风格 ========== */
.mood-card-section {
  margin-bottom: 80rpx;
  animation: fadeInUp 0.5s ease forwards;
  animation-delay: 0.25s;
}

.mood-card {
  background: rgba(235, 245, 235, 0.85);
  backdrop-filter: blur(10px);
  border-radius: 48rpx;
  padding: 48rpx 40rpx;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 20rpx 40rpx rgba(180, 210, 180, 0.25);
  transition: all 0.4s ease;
  min-height: 280rpx;
  border: 1rpx solid rgba(200, 225, 200, 0.5);
}

.mood-card:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 30rpx 60rpx rgba(160, 200, 160, 0.3);
  background: rgba(240, 250, 240, 0.9);
}

/* 不同情绪的渐变背景 - 都在淡绿色调上微调 */
.mood-card.happy {
  background: linear-gradient(145deg, rgba(235, 245, 235, 0.9), rgba(245, 250, 240, 0.9));
}

.mood-card.peaceful {
  background: linear-gradient(145deg, rgba(230, 245, 235, 0.9), rgba(240, 250, 240, 0.9));
}

.mood-card.thoughtful {
  background: linear-gradient(145deg, rgba(235, 245, 240, 0.9), rgba(240, 250, 240, 0.9));
}

.mood-card.sad {
  background: linear-gradient(145deg, rgba(235, 245, 240, 0.9), rgba(240, 250, 240, 0.9));
}

.mood-card.excited {
  background: linear-gradient(145deg, rgba(235, 245, 235, 0.9), rgba(245, 250, 235, 0.9));
}

.mood-card.confused {
  background: linear-gradient(145deg, rgba(235, 245, 235, 0.9), rgba(240, 250, 235, 0.9));
}

.mood-card-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.1;
}

.mood-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  animation: particleFloat 30s linear infinite;
}

.particle {
  position: absolute;
  font-size: 40rpx;
  color: #A8C9A8;
  animation: twinkle 3s ease-in-out infinite;
  opacity: 0.2;
}

.particle:nth-child(1) { top: 10%; left: 5%; animation-delay: 0s; }
.particle:nth-child(2) { top: 20%; right: 10%; animation-delay: 0.5s; }
.particle:nth-child(3) { bottom: 15%; left: 15%; animation-delay: 1s; }
.particle:nth-child(4) { bottom: 30%; right: 20%; animation-delay: 1.5s; }
.particle:nth-child(5) { top: 40%; left: 30%; animation-delay: 2s; }
.particle:nth-child(6) { top: 60%; right: 30%; animation-delay: 2.5s; }

@keyframes particleFloat {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(3deg); }
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.mood-card-content {
  position: relative;
  z-index: 2;
}

.mood-card-header {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 24rpx;
}

.mood-emoji {
  font-size: 48rpx;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(5px);
  width: 80rpx;
  height: 80rpx;
  border-radius: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1rpx solid rgba(180, 210, 180, 0.3);
}

.mood-badge {
  font-size: 28rpx;
  color: #5A715A;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(5px);
  padding: 8rpx 24rpx;
  border-radius: 36rpx;
  border: 1rpx solid rgba(180, 210, 180, 0.3);
}

.mood-message {
  margin-bottom: 32rpx;
}

.message-text {
  font-size: 36rpx;
  color: #4A5A4A;
  line-height: 1.5;
  font-weight: 450;
  margin: 0;
  letter-spacing: 0.5rpx;
}

.mood-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(5px);
  border-radius: 40rpx;
  padding: 20rpx 24rpx;
  border: 1rpx solid rgba(180, 210, 180, 0.3);
}

.mood-suggestion {
  display: flex;
  align-items: center;
  gap: 12rpx;
  flex: 1;
}

.suggestion-icon {
  font-size: 28rpx;
  color: #8BAF8B;
}

.suggestion-text {
  font-size: 26rpx;
  color: #5A6A5A;
  line-height: 1.4;
}

.mood-action {
  width: 56rpx;
  height: 56rpx;
  background: rgba(180, 210, 180, 0.3);
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.mood-card:hover .mood-action {
  transform: translateX(8rpx);
  background: rgba(160, 200, 160, 0.4);
}

.action-arrow {
  font-size: 32rpx;
  color: #7AA07A;
  font-weight: bold;
}

/* 空状态样式 */
.mood-empty {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200rpx;
}

.empty-icon {
  font-size: 64rpx;
  margin-bottom: 16rpx;
  animation: float 3s ease-in-out infinite;
}

.empty-text {
  font-size: 30rpx;
  color: #4A4A4A;
  font-weight: 500;
  margin-bottom: 8rpx;
}

.empty-subtext {
  font-size: 26rpx;
  color: #7A8A7A;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6rpx); }
}

/* 热门推荐区样式 */
.recommendations {
  margin-bottom: 80rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.title-decoration {
  width: 8rpx;
  height: 40rpx;
  background: #F98C53;
  border-radius: 4rpx;
}

.section-title h2 {
  font-size: 44rpx;
  font-weight: 800;
  color: #333333;
  margin: 0;
}

.view-all {
  font-size: 28rpx;
  color: #F98C53;
  font-weight: 600;
  cursor: pointer;
  padding: 8rpx 16rpx;
  border-radius: 20rpx;
  transition: all 0.3s ease;
}

.view-all:hover {
  background: rgba(249, 140, 83, 0.1);
  transform: translateX(4rpx);
}

.cards-container {
  position: relative;
}

.cards-wrapper {
  display: flex;
  gap: 32rpx;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding-bottom: 20rpx;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.cards-wrapper::-webkit-scrollbar {
  display: none;
}

.card {
  flex: 0 0 500rpx;
  height: 600rpx;
  border-radius: 40rpx;
  position: relative;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  box-shadow: 0 20rpx 60rpx rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.4s ease;
}

.card:hover {
  transform: translateY(-12rpx);
  box-shadow: 0 30rpx 80rpx rgba(0, 0, 0, 0.3);
}

.card-badge {
  position: absolute;
  top: 32rpx;
  right: 32rpx;
  width: 64rpx;
  height: 64rpx;
  background: #F98C53;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28rpx;
  font-weight: 800;
  z-index: 2;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.2);
}

.card-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 48rpx 40rpx 40rpx;
  background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.4) 50%, transparent 100%);
  z-index: 1;
}

.card-tags {
  display: flex;
  gap: 12rpx;
  margin-bottom: 24rpx;
  flex-wrap: wrap;
}

.tag {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 24rpx;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  backdrop-filter: blur(10rpx);
}

.card-title {
  font-size: 42rpx;
  font-weight: 800;
  color: white;
  margin: 0 0 16rpx;
  line-height: 1.3;
}

.card-subtitle {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 32rpx;
  line-height: 1.4;
  opacity: 0.95;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-stats {
  display: flex;
  gap: 24rpx;
}

.stat {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.85);
  display: flex;
  align-items: center;
  gap: 6rpx;
}

.card-action {
  background: #F98C53;
  color: white;
  font-size: 26rpx;
  font-weight: 600;
  padding: 12rpx 28rpx;
  border-radius: 30rpx;
  cursor: pointer;
  transition: all 0.3s ease;
}

.card-action:hover {
  background: #ff7c3a;
  transform: scale(1.05);
}

.indicator-dots {
  display: flex;
  justify-content: center;
  gap: 16rpx;
  margin-top: 40rpx;
}

.dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  cursor: pointer;
}

.dot.active {
  width: 40rpx;
  background: #F98C53;
  border-radius: 8rpx;
}

/* 浮动操作按钮 */
.floating-action-btn {
  position: fixed;
  bottom: 110rpx;
  right: 70rpx;
  background: linear-gradient(135deg, #F98C53, #FF7C3A);
  color: white;
  padding: 24rpx 36rpx;
  border-radius: 50rpx;
  display: flex;
  align-items: center;
  gap: 16rpx;
  cursor: pointer;
  box-shadow: 0 16rpx 48rpx rgba(249, 140, 83, 0.4);
  transition: all 0.3s ease;
  z-index: 1000;
  animation: float 3s ease-in-out infinite;
}

.floating-action-btn:hover {
  transform: translateY(-4rpx) scale(1.05);
  box-shadow: 0 24rpx 64rpx rgba(249, 140, 83, 0.5);
}

.fab-icon {
  font-size: 36rpx;
  font-weight: bold;
}

.fab-text {
  font-size: 30rpx;
  font-weight: 600;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10rpx);
  }
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header, .search-bar, .quick-actions, .recommendations, .mood-card-section {
  animation: fadeInUp 0.6s ease forwards;
}

.search-bar {
  animation-delay: 0.1s;
}

.quick-actions {
  animation-delay: 0.2s;
}

.mood-card-section {
  animation-delay: 0.25s;
}

.recommendations {
  animation-delay: 0.3s;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .card {
    flex: 0 0 450rpx;
    height: 540rpx;
  }
  
  .card-title {
    font-size: 38rpx;
  }
  
  .quick-actions {
    gap: 20rpx;
  }
  
  .action-icon {
    width: 100rpx;
    height: 100rpx;
  }
  
  .icon {
    font-size: 48rpx;
  }
  
  .floating-action-btn {
    bottom: 40rpx;
    right: 40rpx;
    padding: 20rpx 32rpx;
  }
}

/* 暗色模式适配 */
@media (prefers-color-scheme: dark) {
  .home-container {
    background: linear-gradient(to bottom, #1a1a1a 0%, #2a1e1a 100%);
  }
  
  .greeting h1, .section-title h2 {
    color: #ffffff;
  }
  
  .sub-greeting {
    color: #aaaaaa;
  }
  
  .search-bar {
    background: #2a2a2a;
    border: 1rpx solid #444444;
  }
  
  .search-placeholder {
    color: #888888;
  }
  
  .action-text {
    color: #dddddd;
  }
}
</style>