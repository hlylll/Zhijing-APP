<template>
  <view class="path-container">
    <!-- 顶部标题 -->
    <view class="header">
      <text class="title" >🌱 我的成长之路 🌱</text>
      <view class="subtitle">每一步都通向更好的自己</view>
    </view>
    
    <!-- 核心信息大卡片 -->
    <view class="core-card">
      <!-- 欢迎语和路径 -->
      <view class="greeting-section">
        <view class="avatar-wrapper">
			<image src="/static/icons/grow.png" style="width: 85%; height: 85%;"></image>
          <!-- <text class="avatar-emoji">🌿</text> -->
        </view>
        <view class="greeting-text">
          <text class="hello">下午好，小萌！</text>
          <text class="path">你的成长之路：软件工程 → AI产品经理</text>
          <view class="sparkle">✨</view>
        </view>
      </view>
      
      <!-- 进度三连击 -->
      <view class="progress-row">
        <view class="progress-item">
          <view class="icon-wrapper">
            <text class="icon">📍</text>
            <view class="icon-bg"></view>
          </view>
          <text class="num">3/8</text>
          <text class="label">当前进度</text>
        </view>
        <view class="progress-item">
          <view class="icon-wrapper">
            <text class="icon">⏰</text>
            <view class="icon-bg"></view>
          </view>
          <text class="num">6个月后</text>
          <text class="label">预计达成</text>
        </view>
        <view class="progress-item">
          <view class="icon-wrapper">
            <text class="icon">🔥</text>
            <view class="icon-bg"></view>
          </view>
          <text class="num">12天</text>
          <text class="label">连续成长</text>
        </view>
      </view>
      
      <!-- 情绪关怀卡片 -->
      <view class="emotion-card">
        <view class="emotion-header">
          <text class="emotion-title">最近情绪：有点压力</text>
          <text class="emotion-emoji">🌧️</text>
        </view>
        <text class="emotion-text">最近有点小压力？放轻松，成长的路需要耐心～</text>
        <view class="nature-elements">
          <text class="nature-element">☁️</text>
          <text class="nature-element">🌱</text>
          <text class="nature-element">💧</text>
          <text class="nature-element">☀️</text>
        </view>
        <view class="bubble"></view>
      </view>
    </view>
    
   <!-- Tab切换 -->
   <view class="tab-bar">
     <view class="tab-item" :class="{active: tabIndex === 0}" @tap="tabIndex = 0">
       <!-- 替换 📅 为 timeline.png -->
       <image 
         class="tab-icon"
         src="/static/icons/time1.png"
         mode="widthFix"
       />
       <text style="font-size: 28rpx;">成长时间轴</text>
     </view>
     <view class="tab-item" :class="{active: tabIndex === 1}" @tap="tabIndex = 1">
       <!-- 替换 💌 为 motivation.png -->
       <image 
         class="tab-icon"
         src="/static/icons/11.png"
         mode="widthFix"
       />
       <text style="font-size: 28rpx;">激励卡片</text>
     </view>
     <view class="tab-slider" :style="{transform: `translateX(${tabIndex * 100}%)`}"></view>
   </view>
    
	
	<!-- 在 path.vue 中修改推荐卡片部分 -->
	<view class="recommend-card" v-if="recommendedPath">
	  <view class="recommend-header">
	    <text class="recommend-icon">✨</text>
	    <text class="recommend-title">为您推荐的路径</text>
	  </view>
	  <view class="recommend-content">
	    <view class="path-info">
	      <text class="path-name">{{ recommendedPath.name }}</text>
	      <text class="path-desc">{{ recommendedPath.description }}</text>
	      <view class="match-details">
	        <view class="match-tag">
	          <text class="match-label">匹配度</text>
	          <text class="match-stars">{{ getMatchStars(recommendedPath) }}</text>
	        </view>
	        <view class="user-profile-tip" v-if="userProfile.major">
	          <text class="tip-icon">🎯</text>
	          <text class="tip-text">
	            基于：{{ userProfile.major }} · 
	            {{ userProfile.interestTexts?.slice(0,2).join('、') }} 
	            {{ userProfile.interestTexts?.length > 2 ? '等' : '' }}
	          </text>
	        </view>
	      </view>
	    </view>
	    <view class="path-actions">
	      <button class="action-btn" @tap="switchRecommendation">换一批</button>
	      <button class="action-btn primary" @tap="acceptRecommendation">查看详情</button>
	    </view>
	  </view>
	  <view class="recommend-footer">
	    <text>基于你的个人信息智能推荐</text>
	    <text class="update-time" v-if="userProfile.updatedAt">
	      更新于 {{ formatDate(userProfile.updatedAt) }}
	    </text>
	  </view>
	</view>


    <!-- Tab内容 -->
    <view class="tab-content">
      <!-- 成长时间轴 -->
      <view v-if="tabIndex === 0" class="timeline">
        <view class="timeline-header">
          <text class="timeline-title">今日任务</text>
          <text class="timeline-subtitle">慢慢来，比较快</text>
        </view>
        
        <view class="step" v-for="(step, index) in currentTasks" :key="step.id">
          <view class="step-line">
            <view class="dot" :class="{ 
              completed: step.completed, 
              current: step.current,
              pending: !step.completed && !step.current 
            }">
              <text v-if="step.completed" class="dot-text">✓</text>
              <text v-else-if="step.current" class="dot-text">🌱</text>
              <text v-else class="dot-text">○</text>
            </view>
            <view v-if="index < steps.length - 1" class="line" :class="{ 
              completed: step.completed,
              current: step.current
            }"></view>
          </view>
          <view class="step-card" :class="{ 
            completed: step.completed,
            current: step.current
          }">
            <view class="step-header">
              <text class="step-title">{{ step.title }}</text>
              <view class="step-type" :class="step.type.toLowerCase()">{{ step.type }}</view>
            </view>
            <text class="step-desc">{{ step.desc }}</text>
            <view class="step-info">
              <view class="info-item">
                <text class="info-icon">⏳</text>
                <text class="time">{{ step.time }}</text>
              </view>
              <view class="info-item">
                <text class="info-icon">📊</text>
                <text class="difficulty">{{ step.difficulty }}</text>
              </view>
            </view>
            <view v-if="step.current" class="current-indicator">
              <text class="sparkle">✨</text>
              <text class="current-text">进行中...</text>
            </view>
          </view>
        </view>
        
        <!-- 查看全部 -->
        <view class="more-btn" @tap="viewAllSteps">
          <text class="more-text">查看更多任务</text>
          <text class="more-arrow">→</text>
        </view>
      </view>

      <!-- 激励卡片 -->
      <view v-else class="incentive">
        <view class="incentive-card">
          <text class="incentive-title">💝 今日鼓励</text>
          <text class="incentive-text">"每一小步都是通往梦想的一大步，今天的你已经很棒了！"</text>
          <view class="incentive-stats">
            <view class="stat-item">
              <text class="stat-num">12</text>
              <text class="stat-label">连续成长</text>
            </view>
            <view class="stat-divider">|</view>
            <view class="stat-item">
              <text class="stat-num">23</text>
              <text class="stat-label">成就解锁</text>
            </view>
            <view class="stat-divider">|</view>
            <view class="stat-item">
              <text class="stat-num">∞</text>
              <text class="stat-label">可能性</text>
            </view>
          </view>
          <view class="incentive-nature">
            <text class="nature-element">🌿</text>
            <text class="nature-element">🌼</text>
            <text class="nature-element">🌱</text>
          </view>
        </view>
      </view>

      <!-- 思维导图部分 -->
      <view class="mindmap-section">
        <view class="mindmap-header">
          <text class="mindmap-title">🌳 你的完整成长路径</text>
          <text class="mindmap-desc">从软件工程到AI产品经理的全景图</text>
        </view>
        
        <!-- 思维导图容器 -->
        <scroll-view 
          scroll-x 
          scroll-y 
          class="mindmap-container"
          @touchstart="touchStart" 
          @touchmove="touchMove" 
          @touchend="touchEnd"
        >
          <view 
            class="mindmap-wrapper" 
            :style="{ 
              transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
              width: `${imageWidth}px`,
              height: `${imageHeight}px`
            }"
          >
            <image 
              class="mindmap-img"
              :src="mindmapUrl" 
              mode="widthFix"
              @load="onImageLoad"
            />
          </view>
        </scroll-view>
        
        <view class="zoom-controls">
          <view class="zoom-btn" @tap="zoomOut">−</view>
          <view class="zoom-value">{{ Math.round(scale * 100) }}%</view>
          <view class="zoom-btn" @tap="zoomIn">＋</view>
          <view class="reset-btn" @tap="resetMindmap">🔄 重置</view>
        </view>
        
        <view class="zoom-tips">双指捏合缩放 / 单指拖动查看全貌</view>
      </view>
    </view>
    
    <!-- 底部浮动操作栏 -->
    <view class="bottom-bar">
      <view class="btn" @tap="switchPath">
        <text class="btn-icon">🔄</text>
        <text class="btn-text">切换</text>
      </view>
      <view class="btn" @tap="markComplete">
        <text class="btn-icon">✅</text>
        <text class="btn-text">完成</text>
      </view>
      <view class="btn main-btn" @tap="addStep">
        <text class="main-btn-icon">＋</text>
      </view>
     <view class="btn" @tap="goToEditProfile">
       <text class="btn-icon">✏️</text>
       <text class="btn-text">编辑</text>
     </view>
      <view class="btn" @tap="viewResources">
        <text class="btn-icon">📚</text>
        <text class="btn-text">资源</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

function goToEditProfile() {
  uni.navigateTo({
    url: '/pages/mine/edit.vue' // 根据你的实际路径调整
  })
}

// ========== 1. 定义路径数据（包含任务列表） ==========
const pathList = ref([
  {
    id: 1,
    name: '软件工程 → AI产品经理',
    description: '适合有技术背景，想转型AI产品方向的同学',
    tags: ['计算机', '编程', 'AI', '产品', '逻辑思维'],
    tasks: [
      { id: 1, title: '掌握 React & Vue', type: '技能', desc: '构建现代Web交互式应用', time: '2个月', difficulty: '★★★', completed: true, current: false },
      { id: 2, title: '数据结构与算法', type: '基础', desc: '夯实计算机基础，提升编程思维', time: '3个月', difficulty: '★★★', completed: true, current: false },
      { id: 3, title: '机器学习基础', type: '技能', desc: '理解AI核心原理', time: '4个月', difficulty: '★★★★', completed: false, current: true },
      { id: 4, title: '产品设计思维', type: '软技能', desc: '培养产品设计思维与用户体验', time: '2个月', difficulty: '★★★', completed: false, current: false },
      { id: 5, title: '项目管理实践', type: '软技能', desc: '学习敏捷开发与项目管理', time: '3个月', difficulty: '★★★★', completed: false, current: false },
    ]
  },
  {
    id: 2,
    name: '前端架构师',
    description: '深入前端框架与用户体验，成为团队技术核心',
    tags: ['计算机', '编程', '设计', '交互', 'JavaScript'],
    tasks: [
      { id: 1, title: 'JavaScript 深度进阶', type: '技能', desc: '掌握闭包、原型、异步编程', time: '2个月', difficulty: '★★★', completed: true, current: false },
      { id: 2, title: 'React 源码分析', type: '技能', desc: '理解框架原理，提升调试能力', time: '3个月', difficulty: '★★★★', completed: false, current: true },
      { id: 3, title: '前端工程化', type: '技能', desc: 'Webpack、Vite、CI/CD', time: '2个月', difficulty: '★★★', completed: false, current: false },
      { id: 4, title: '用户体验设计', type: '软技能', desc: '交互设计与用户研究', time: '2个月', difficulty: '★★★', completed: false, current: false },
    ]
  },
  {
    id: 3,
    name: '数据科学家',
    description: '从数据中挖掘价值，掌握AI核心算法',
    tags: ['数学', '统计', '编程', '机器学习', '分析'],
    tasks: [
      { id: 1, title: 'Python 数据分析', type: '技能', desc: 'NumPy、Pandas、Matplotlib', time: '2个月', difficulty: '★★★', completed: true, current: false },
      { id: 2, title: '机器学习基础', type: '技能', desc: 'Scikit-learn 常用算法', time: '4个月', difficulty: '★★★★', completed: false, current: true },
      { id: 3, title: '统计学与概率论', type: '基础', desc: '夯实数学基础', time: '3个月', difficulty: '★★★', completed: false, current: false },
      { id: 4, title: '深度学习入门', type: '技能', desc: 'TensorFlow/PyTorch 基础', time: '4个月', difficulty: '★★★★', completed: false, current: false },
    ]
  }
])

// ========== 2. 从存储读取用户画像 ==========
const userProfile = ref({
  major: '计算机', // 默认值
  interests: ['AI', '产品'], // 默认兴趣标签
  targetCareer: 'AI产品经理',
  skills: []
})

// 加载用户画像
function loadUserProfile() {
  const savedProfile = uni.getStorageSync('userProfile')
  if (savedProfile) {
    userProfile.value = savedProfile
    
    // 将兴趣标签ID转换为文本（用于匹配）
    if (savedProfile.interestTagDetails) {
      userProfile.value.interestTexts = savedProfile.interestTagDetails.map(tag => tag.text)
    } else if (savedProfile.interestTags) {
      // 如果没有存储详情，需要从interestTags列表映射
      const allTags = [
        { id: 1, text: '前端开发' },
        { id: 2, text: '后端开发' },
        { id: 3, text: '移动开发' },
        { id: 4, text: '数据分析' },
        { id: 5, text: '人工智能' },
        { id: 6, text: '产品设计' },
        { id: 7, text: '运营增长' },
        { id: 8, text: '考研深造' },
        { id: 9, text: '公务员' },
        { id: 10, text: '心理健康' },
        { id: 11, text: '外语学习' },
        { id: 12, text: '创业创新' }
      ]
      userProfile.value.interestTexts = savedProfile.interestTags
        .map(id => allTags.find(t => t.id === id)?.text)
        .filter(Boolean)
    }
  }
}

// ========== 3. 当前状态 ==========
const currentPathId = ref(1)          // 当前展示的路径ID
const recommendedPath = ref(null)     // 推荐的路径对象
const matchInfo = ref({})             // 匹配信息

// ========== 4. 计算属性：当前路径的任务列表 ==========
const currentTasks = computed(() => {
  const path = pathList.value.find(p => p.id === currentPathId.value)
  return path ? path.tasks : []
})

// ========== 5. 增强推荐算法 ==========
function calculateRecommendation() {
  const profile = userProfile.value
  
  // 构建用户标签（结合专业、兴趣、目标职业）
  const userTags = [
    profile.major,
    ...(profile.interestTexts || []),
    profile.targetCareer
  ].filter(Boolean) // 过滤掉空值
  
  console.log('用户标签:', userTags) // 调试用
  
  // 计算每条路径的匹配度
  const pathScores = pathList.value.map(path => {
    // 计算标签匹配数
    const commonTags = path.tags.filter(tag => 
      userTags.some(userTag => 
        userTag.includes(tag) || tag.includes(userTag)
      )
    )
    
    // 计算匹配分数（可以增加权重）
    let score = commonTags.length
    
    // 如果有目标职业直接匹配，增加权重
    if (profile.targetCareer && 
        path.tags.some(tag => profile.targetCareer.includes(tag))) {
      score += 2
    }
    
    return {
      path,
      score,
      commonTags
    }
  })
  
  // 按分数排序
  pathScores.sort((a, b) => b.score - a.score)
  
  return {
    bestPath: pathScores[0]?.path,
    allScores: pathScores,
    userTags
  }
}

// 刷新推荐
function refreshRecommendation() {
  const result = calculateRecommendation()
  recommendedPath.value = result.bestPath
  matchInfo.value = {
    score: result.allScores[0]?.score,
    userTags: result.userTags
  }
}

// 换一批（随机选择其他路径）
function switchRecommendation() {
  const otherPaths = pathList.value.filter(p => p.id !== recommendedPath.value.id)
  if (otherPaths.length === 0) return
  const randomIndex = Math.floor(Math.random() * otherPaths.length)
  recommendedPath.value = otherPaths[randomIndex]
}

// 接受推荐：将当前路径切换为推荐路径
function acceptRecommendation() {
  if (recommendedPath.value) {
    currentPathId.value = recommendedPath.value.id
    uni.showToast({ title: '已切换至推荐路径', icon: 'success' })
  }
}

// ========== 6. 获取匹配度星标 ==========
function getMatchStars(path) {
  if (!path) return ''
  
  const profile = userProfile.value
  const userTags = [
    profile.major,
    ...(profile.interestTexts || []),
    profile.targetCareer
  ].filter(Boolean)
  
  const common = path.tags.filter(tag => 
    userTags.some(userTag => 
      userTag.includes(tag) || tag.includes(userTag)
    )
  ).length
  
  const total = path.tags.length
  const ratio = common / total
  const filled = Math.round(ratio * 5)
  
  return '★'.repeat(filled) + '☆'.repeat(5 - filled)
}

// ========== 7. 日期格式化 ==========
function formatDate(dateString) {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60 * 1000) return '刚刚'
  if (diff < 60 * 60 * 1000) return `${Math.floor(diff / (60 * 1000))}分钟前`
  if (diff < 24 * 60 * 60 * 1000) return `${Math.floor(diff / (60 * 60 * 1000))}小时前`
  return `${Math.floor(diff / (24 * 60 * 60 * 1000))}天前`
}

// ========== 8. 原有的变量和方法 ==========
const tabIndex = ref(0)
const steps = ref([
  { id: 1, title: '掌握 React & Vue', type: '技能', desc: '构建现代Web交互式应用', time: '2个月', difficulty: '★★★', completed: true, current: false },
  { id: 2, title: '数据结构与算法', type: '基础', desc: '夯实计算机基础，提升编程思维', time: '3个月', difficulty: '★★★', completed: true, current: false },
  { id: 3, title: '机器学习基础', type: '技能', desc: '理解AI核心原理', time: '4个月', difficulty: '★★★★', completed: false, current: true },
  { id: 4, title: '产品设计思维', type: '软技能', desc: '培养产品设计思维与用户体验', time: '2个月', difficulty: '★★★', completed: false, current: false },
  { id: 5, title: '项目管理实践', type: '软技能', desc: '学习敏捷开发与项目管理', time: '3个月', difficulty: '★★★★', completed: false, current: false },
])

// 思维导图相关
const scale = ref(1)
const translateX = ref(0)
const translateY = ref(0)
const imageWidth = ref(800)
const imageHeight = ref(600)
const startScale = ref(1)
const startX = ref(0)
const startY = ref(0)
const lastScale = ref(1)
const isMultiTouch = ref(false)
const startDistance = ref(0)
const initialTouches = ref([])
const mindmapUrl = ref('https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80')

// 方法
const viewAllSteps = () => {
  uni.showToast({ title: '查看全部步骤', icon: 'none', duration: 1500 })
}
const switchPath = () => uni.showToast({ title: '切换路径', icon: 'none' })
const markComplete = () => uni.showToast({ title: '任务完成！', icon: 'success' })
const addStep = () => uni.showToast({ title: '添加新任务', icon: 'none' })
const addNote = () => uni.showToast({ title: '记录心情', icon: 'none' })
const viewResources = () => uni.showToast({ title: '学习资源', icon: 'none' })

// 缩放控制
const zoomIn = () => { scale.value = Math.min(3, scale.value + 0.2) }
const zoomOut = () => { scale.value = Math.max(0.5, scale.value - 0.2) }
const resetMindmap = () => {
  scale.value = 1
  translateX.value = 0
  translateY.value = 0
}

// 触摸事件
const touchStart = (e) => {
  if (e.touches.length === 2) {
    isMultiTouch.value = true
    const touch1 = e.touches[0]
    const touch2 = e.touches[1]
    startScale.value = scale.value
    startDistance.value = Math.hypot(
      touch2.pageX - touch1.pageX,
      touch2.pageY - touch1.pageY
    )
    initialTouches.value = [touch1, touch2]
  } else if (e.touches.length === 1) {
    startX.value = e.touches[0].pageX - translateX.value
    startY.value = e.touches[0].pageY - translateY.value
  }
}

const touchMove = (e) => {
  if (e.touches.length === 2 && isMultiTouch.value) {
    const touch1 = e.touches[0]
    const touch2 = e.touches[1]
    const currentDistance = Math.hypot(
      touch2.pageX - touch1.pageX,
      touch2.pageY - touch1.pageY
    )
    const newScale = startScale.value * (currentDistance / startDistance.value)
    scale.value = Math.max(0.5, Math.min(3, newScale))
  } else if (e.touches.length === 1) {
    translateX.value = e.touches[0].pageX - startX.value
    translateY.value = e.touches[0].pageY - startY.value
  }
}

const touchEnd = () => { isMultiTouch.value = false }

const onImageLoad = (e) => {
  const { width, height } = e.detail
  imageWidth.value = width
  imageHeight.value = height
  console.log('思维导图加载完成，尺寸:', width, '×', height)
}

// ========== 9. 初始化 ==========
onMounted(() => {
  loadUserProfile()
  refreshRecommendation()
})
</script>

<style scoped>
.path-container {
  padding: 32rpx 32rpx 180rpx;
  background: linear-gradient(135deg, #F0F8FF 0%, #E6F0FF 50%, #F0FFF4 100%);
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
}

/* 头部 */
.header {
  padding: 40rpx 0 32rpx;
  text-align: center;
}

.title {

  font-size: 52rpx;
  font-weight: 700;
  color: #4A90E2;
  letter-spacing: 2rpx;
  text-shadow: 0 4rpx 12rpx rgba(74, 144, 226, 0.15);
  background: linear-gradient(135deg, #4A90E2, #63B3ED);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
 font-family: 'Brush Script MT', sans-serif;
  font-size: 28rpx;
  color: #7B8B9F;
  margin-top: 12rpx;
  font-weight: 400;
}

/* 核心卡片 */
.core-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 48rpx 40rpx;
  box-shadow: 
    0 20rpx 60rpx rgba(74, 144, 226, 0.1),
    0 4rpx 24rpx rgba(129, 212, 250, 0.2);
  margin-bottom: 48rpx;
  margin-top: -20rpx;
  backdrop-filter: blur(20rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}
/* ====== 新增推荐卡片样式 ====== */
.recommend-card {
  background: linear-gradient(135deg, #FFF9E6, #FFF3E0);
  border-radius: 48rpx;
  padding: 40rpx;
  margin: 32rpx 0 48rpx;
  box-shadow: 0 20rpx 60rpx rgba(255, 193, 7, 0.15);
  border: 2rpx solid rgba(255, 214, 102, 0.6);
  position: relative;
  overflow: hidden;
}

.recommend-card::before {
  content: '✨';
  position: absolute;
  top: -20rpx;
  right: -20rpx;
  font-size: 120rpx;
  opacity: 0.1;
  transform: rotate(15deg);
}

.recommend-header {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 24rpx;
}

.recommend-icon {
  font-size: 48rpx;
}

.recommend-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #F6AD55;
  text-shadow: 0 2rpx 4rpx rgba(255, 193, 7, 0.2);
}

.recommend-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24rpx;
  margin-bottom: 24rpx;
}

.path-info {
  flex: 1;
}

.path-name {
  font-size: 40rpx;
  font-weight: 700;
  color: #2D3748;
  display: block;
  margin-bottom: 8rpx;
}

.path-desc {
  font-size: 26rpx;
  color: #718096;
  display: block;
  margin-bottom: 16rpx;
  line-height: 1.4;
}

.match-tag {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.match-label {
  font-size: 26rpx;
  color: #7B8B9F;
}

.match-stars {
  font-size: 28rpx;
  color: #F6AD55;
  letter-spacing: 2rpx;
}

.path-actions {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.action-btn {
  background: rgba(255, 255, 255, 0.9);
  border: 2rpx solid #FFD766;
  border-radius: 40rpx;
  padding: 16rpx 32rpx;
  font-size: 28rpx;
  color: #F6AD55;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.action-btn.primary {
  background: linear-gradient(135deg, #FFD966, #FFB347);
  border: none;
  color: white;
  box-shadow: 0 8rpx 24rpx rgba(255, 193, 7, 0.4);
}

.action-btn:active {
  transform: scale(0.96);
}

.recommend-footer {
  font-size: 24rpx;
  color: #A0AEC0;
  text-align: right;
  border-top: 2rpx dashed #FFE5B4;
  padding-top: 20rpx;
  margin-top: 8rpx;
}

/* 欢迎区域 */
.greeting-section {
  display: flex;
  align-items: center;
  margin-bottom: 48rpx;
  position: relative;
}

.avatar-wrapper {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #d1f0f7, #98e5fa);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 32rpx;
  box-shadow: 0 12rpx 32rpx rgba(79, 195, 247, 0.3);
}

.avatar-emoji {
	
  font-size: 64rpx;
  filter: drop-shadow(0 4rpx 8rpx rgba(0,0,0,0.1));
}

.greeting-text {
  font-family: 'Courier New', Courier, monospace;
  flex: 1;
  position: relative;
  font-weight: 1700;
}

.hello {
  font-size: 40rpx;
  font-weight: 700;
  color: #2D3748;
  display: block;
  margin-bottom: 8rpx;
}

.path {
  font-size: 28rpx;
  color: #718096;
  line-height: 1.4;
}

.sparkle {
  position: absolute;
  right: -20rpx;
  top: -10rpx;
  font-size: 32rpx;
  animation: twinkle 2s infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.7; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}

/* 进度三连击 */
.progress-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 48rpx;
  gap: 20rpx;
}

.progress-item {
  flex: 1;
  text-align: center;
  background: rgba(240, 248, 255, 0.9);
  border-radius: 32rpx;
  padding: 36rpx 24rpx;
  position: relative;
  overflow: hidden;
  border: 2rpx solid rgba(129, 212, 250, 0.3);
  transition: all 0.3s ease;
}

.progress-item:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 16rpx 32rpx rgba(129, 212, 250, 0.25);
}

.icon-wrapper {
  position: relative;
  margin-bottom: 20rpx;
}

.icon {
  font-size: 48rpx;
  position: relative;
  z-index: 2;
}

.icon-bg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80rpx;
  height: 80rpx;
  background: rgba(129, 212, 250, 0.2);
  border-radius: 50%;
  z-index: 1;
}

.num {
  font-size: 44rpx;
  font-weight: 700;
  color: #4A90E2;
  display: block;
  margin-bottom: 8rpx;
  font-family: 'Arial Rounded MT Bold', sans-serif;
}

.label {
  font-size: 24rpx;
  color: #7B8B9F;
  font-weight: 500;
}

/* 情绪卡片 */
.emotion-card {
  background: linear-gradient(135deg, #E8F4FD, #F0FDF4);
  border-radius: 40rpx;
  padding: 40rpx;
  position: relative;
  overflow: hidden;
  border: 2rpx solid rgba(129, 212, 250, 0.4);
}

.emotion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.emotion-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #4A90E2;
}

.emotion-emoji {
  font-size: 40rpx;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10rpx); }
}

.emotion-text {
  font-size: 28rpx;
  color: #718096;
  line-height: 1.5;
  margin-bottom: 20rpx;
}

.nature-elements {
  display: flex;
  gap: 20rpx;
  margin-top: 20rpx;
}

.nature-element {
  font-size: 32rpx;
  animation: sway 4s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.5s);
}

.nature-element:nth-child(1) { --i: 1; }
.nature-element:nth-child(2) { --i: 2; }
.nature-element:nth-child(3) { --i: 3; }
.nature-element:nth-child(4) { --i: 4; }

@keyframes sway {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-8rpx) rotate(5deg); }
}

.bubble {
  position: absolute;
  bottom: -60rpx;
  right: -60rpx;
  width: 200rpx;
  height: 200rpx;
  background: radial-gradient(circle, rgba(129, 212, 250, 0.1) 0%, transparent 70%);
  border-radius: 50%;
}

/* Tab栏 */
.tab-bar {
  display: flex;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50rpx;
  padding: 8rpx;
  margin-bottom: 48rpx;
  position: relative;
  box-shadow: 0 8rpx 32rpx rgba(129, 212, 250, 0.15);
  border: 2rpx solid rgba(129, 212, 250, 0.2);
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 28rpx 0;
  font-size: 30rpx;
  color: #7B8B9F;
  background: transparent;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  transition: all 0.3s ease;
  border-radius: 42rpx;
}

.tab-item.active {
  color: #4A90E2;
  font-weight: 600;
}

/* 修改 tab-icon 为图片样式 */
.tab-icon {
  width: 70rpx;      /* 图片宽度 */
  height: 55rpx;     /* 图片高度 */
  margin-bottom: 8rpx;
  /* 非激活状态的样式 */
  opacity: 0.6;
  filter: grayscale(30%) brightness(0.9);
  transition: all 0.3s ease;
}

/* 激活状态下的图标样式 */
.tab-item.active .tab-icon {
  opacity: 1;
  filter: grayscale(0%) brightness(1);
  transform: scale(1.1);
}
.tab-slider {
  position: absolute;
  top: 8rpx;
  left: 8rpx;
  width: calc(50% - 8rpx);
  height: calc(100% - 16rpx);
  background: linear-gradient(135deg, #E8F4FD, #D4EDFA);
  border-radius: 42rpx;
  transition: transform 0.3s ease;
  z-index: 1;
  box-shadow: 0 4rpx 16rpx rgba(129, 212, 250, 0.3);
}

/* 时间轴 */
.timeline {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 48rpx 40rpx;
  box-shadow: 0 20rpx 60rpx rgba(74, 144, 226, 0.1);
  backdrop-filter: blur(20rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}

.timeline-header {
  text-align: center;
  margin-bottom: 48rpx;
}

.timeline-title {
  font-size: 40rpx;
  font-weight: 700;
  color: #4A90E2;
  display: block;
  margin-bottom: 8rpx;
}

.timeline-subtitle {
  font-size: 26rpx;
  color: #7B8B9F;
}

/* 步骤样式 */
.step {
  display: flex;
  margin-bottom: 48rpx;
  position: relative;
}

.step-line {
  width: 80rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.dot {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20rpx;
  z-index: 2;
  position: relative;
  border: 4rpx solid transparent;
  transition: all 0.3s ease;
}

.dot.completed {
  background: linear-gradient(135deg, #68D391, #38A169);
  border-color: rgba(104, 211, 145, 0.3);
  box-shadow: 0 8rpx 24rpx rgba(56, 161, 105, 0.3);
}

.dot.current {
  background: linear-gradient(135deg, #63B3ED, #4A90E2);
  border-color: rgba(99, 179, 237, 0.4);
  box-shadow: 0 8rpx 24rpx rgba(74, 144, 226, 0.4);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(74, 144, 226, 0.4); }
  70% { box-shadow: 0 0 0 20rpx rgba(74, 144, 226, 0); }
  100% { box-shadow: 0 0 0 0 rgba(74, 144, 226, 0); }
}

.dot.pending {
  background: rgba(255, 255, 255, 0.8);
  border: 4rpx solid #E8F4FD;
  box-shadow: 0 4rpx 16rpx rgba(129, 212, 250, 0.2);
}

.dot-text {
  font-size: 36rpx;
  color: white;
}

.line {
  flex: 1;
  width: 8rpx;
  background: linear-gradient(to bottom, #E8F4FD, #D4EDFA);
  border-radius: 4rpx;
  margin: 8rpx 0;
}

.line.completed {
  background: linear-gradient(to bottom, #68D391, #38A169);
}

/* 步骤卡片 */
.step-card {
  flex: 1;
  background: rgba(248, 250, 252, 0.9);
  border-radius: 40rpx;
  padding: 40rpx;
  border: 2rpx solid #E8F4FD;
  transition: all 0.3s ease;
}

.step-card.current {
  background: rgba(240, 248, 255, 0.95);
  border-color: #D4EDFA;
  box-shadow: 0 12rpx 32rpx rgba(129, 212, 250, 0.2);
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.step-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #2D3748;
}

.step-type {
  font-size: 24rpx;
  padding: 8rpx 20rpx;
  border-radius: 40rpx;
  font-weight: 600;
}

.step-type.技能 {
  background: rgba(129, 212, 250, 0.3);
  color: #4A90E2;
  border: 2rpx solid rgba(99, 179, 237, 0.4);
}

.step-type.基础 {
  background: rgba(104, 211, 145, 0.3);
  color: #38A169;
  border: 2rpx solid rgba(72, 187, 120, 0.4);
}

.step-type.软技能 {
  background: rgba(251, 211, 141, 0.3);
  color: #D69E2E;
  border: 2rpx solid rgba(246, 173, 85, 0.4);
}

.step-desc {
  font-size: 28rpx;
  color: #718096;
  line-height: 1.5;
  margin-bottom: 24rpx;
}

.step-info {
  display: flex;
  gap: 40rpx;
  font-size: 26rpx;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.info-icon {
  font-size: 28rpx;
  opacity: 0.8;
}

.time, .difficulty {
  color: #7B8B9F;
}

.current-indicator {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-top: 24rpx;
  padding: 12rpx 24rpx;
  background: linear-gradient(135deg, rgba(129, 212, 250, 0.3), rgba(99, 179, 237, 0.2));
  border-radius: 24rpx;
  width: fit-content;
}

.current-text {
  color: #4A90E2;
  font-size: 26rpx;
  font-weight: 600;
}

/* 查看更多按钮 */
.more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  padding: 28rpx;
  background: rgba(248, 250, 252, 0.9);
  border-radius: 40rpx;
  border: 2rpx dashed #D4EDFA;
  margin-top: 32rpx;
  transition: all 0.3s ease;
}

.more-btn:hover {
  background: rgba(240, 248, 255, 0.95);
  transform: translateY(-2rpx);
}

.more-text {
  font-size: 30rpx;
  color: #4A90E2;
  font-weight: 600;
}

.more-arrow {
  font-size: 32rpx;
  color: #4A90E2;
  transition: transform 0.3s ease;
}

.more-btn:hover .more-arrow {
  transform: translateX(8rpx);
}

/* 激励卡片 */
.incentive {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 48rpx 40rpx;
  box-shadow: 0 20rpx 60rpx rgba(74, 144, 226, 0.1);
  backdrop-filter: blur(20rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}

.incentive-card {
  text-align: center;
  background: linear-gradient(135deg, #E8F4FD, #F0FDF4);
  border-radius: 40rpx;
  padding: 60rpx 40rpx;
  position: relative;
  overflow: hidden;
  border: 2rpx solid rgba(129, 212, 250, 0.4);
}

.incentive-title {
  font-size: 44rpx;
  font-weight: 700;
  color: #4A90E2;
  display: block;
  margin-bottom: 32rpx;
}

.incentive-text {
  font-size: 36rpx;
  font-family: 'Papyrus', Courier, monospace;
  font-weight: 600;
  color: #2D3748;
  line-height: 1.5;
  margin-top: 20rpx;
  margin-bottom:60rpx;
  font-style: italic;
  quotes: "「" "」";
}

.incentive-text::before {
  content: open-quote;
}

.incentive-text::after {
  content: close-quote;
}

.incentive-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40rpx;
  margin-bottom: 40rpx;
  padding: 32rpx;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 32rpx;
  border: 2rpx solid rgba(129, 212, 250, 0.3);
  
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  
  gap: 8rpx;
}

.stat-num {
  font-size: 48rpx;
  font-weight: 700;
  color: #4A90E2;
  font-family: 'Arial Rounded MT Bold', sans-serif;
}

.stat-label {
  font-size: 24rpx;
  color: #7B8B9F;
  font-weight: 500;
}

.stat-divider {
  font-size: 32rpx;
  color: #D4EDFA;
  font-weight: 100;
}

.incentive-nature {
  display: flex;
  justify-content: center;
  gap: 32rpx;
  margin-top: 32rpx;
}

.incentive-nature .nature-element {
  font-size: 48rpx;
  animation: bounce 2s ease-in-out infinite;
  animation-delay: calc(var(--j) * 0.3s);
}

.incentive-nature .nature-element:nth-child(1) { --j: 1; }
.incentive-nature .nature-element:nth-child(2) { --j: 2; }
.incentive-nature .nature-element:nth-child(3) { --j: 3; }

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20rpx); }
}

/* 思维导图部分 */
.mindmap-section {
  margin-top: 48rpx;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 40rpx;
  box-shadow: 0 20rpx 60rpx rgba(74, 144, 226, 0.1);
  backdrop-filter: blur(20rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}

.mindmap-header {
  text-align: center;
  margin-bottom: 32rpx;
}

.mindmap-title {
  font-size: 44rpx;
  font-weight: 700;
  color: #4A90E2;
  display: block;
}

.mindmap-desc {
  font-size: 28rpx;
  color: #718096;
  margin-top: 12rpx;
}

.mindmap-container {
  width: 100%;
  height: 800rpx;
  overflow: hidden;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #E8F4FD, #F0FDF4);
  border: 2rpx solid rgba(129, 212, 250, 0.4);
  position: relative;
}

.mindmap-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.1s;
  position: absolute;
  top: 0;
  left: 0;
}

.mindmap-img {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 16rpx;
}

.zoom-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24rpx;
  margin-top: 32rpx;
  padding: 20rpx;
  background: rgba(248, 250, 252, 0.9);
  border-radius: 32rpx;
  border: 2rpx solid rgba(129, 212, 250, 0.3);
}

.zoom-btn {
  width: 80rpx;
  height: 80rpx;
  background: linear-gradient(135deg, #81D4FA, #4FC3F7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4rpx 16rpx rgba(79, 195, 247, 0.3);
}

.zoom-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 8rpx 24rpx rgba(79, 195, 247, 0.4);
}

.zoom-value {
  font-size: 32rpx;
  font-weight: 600;
  color: #4A90E2;
  min-width: 100rpx;
  text-align: center;
}

.reset-btn {
  padding: 16rpx 32rpx;
  background: linear-gradient(135deg, #68D391, #38A169);
  border-radius: 32rpx;
  font-size: 28rpx;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(56, 161, 105, 0.3);
}

.reset-btn:hover {
  transform: translateY(-2rpx);
  box-shadow: 0 8rpx 24rpx rgba(56, 161, 105, 0.4);
}

.zoom-tips {
  text-align: center;
  font-size: 24rpx;
  color: #7B8B9F;
  margin-top: 24rpx;
}

/* 透明风格底部浮动栏 - 更轻盈的设计 */
.bottom-bar {
  position: fixed;
  bottom: 120rpx;
  left: 32rpx;
  right: 32rpx;
  
  /* 透明背景：完全透明背景 + 强毛玻璃效果 */
  background: transparent;                /* 完全透明背景层 */
  backdrop-filter: blur(30rpx);           /* 更强的模糊，透出底层内容 */
  -webkit-backdrop-filter: blur(30rpx);   /* 兼容性 */
  
  /* 半透明白色遮罩层（模拟玻璃质感）通过伪元素实现，避免直接背景色覆盖 */
  border-radius: 80rpx;                   /* 更大的圆角，更柔和 */
  border: 3px solid rgba(220, 240, 251, 1.0); /* 半透明白色边框，增加玻璃边缘感 */
  
  /* 阴影调整：更轻盈、弥散，带一点蓝色光晕 */
  box-shadow: 
    0 20rpx 60rpx rgba(74, 144, 226, 0.15),
    0 8rpx 32rpx rgba(129, 212, 250, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.4) inset; /* 内发光增加玻璃深度 */
  
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 20rpx 0;                        /* 略减内边距，让栏更精致 */
  z-index: 1000;
  
  /* 如果希望更纯粹的透明，可以添加一层极淡的白色底色（几乎透明） */
  /* 这里通过伪元素来实现微妙的底色，而不是直接background，保持透明度灵活 */
}

/* 伪元素打造轻量底色，增强玻璃可视性，但保持透明感 */
.bottom-bar::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.15);   /* 极浅的白色底色，几乎透明但提升阅读性 */
  border-radius: 80rpx;
  z-index: -1;
  pointer-events: none;                     /* 确保点击穿透到按钮 */
}

/* 按钮样式调整，保持清晰可见 */
.bottom-bar .btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8rpx 16rpx;
  border-radius: 40rpx;
  transition: background 0.2s ease;
  /* 增加点击区域 */
  position: relative;
  min-width: 80rpx;
}

/* 按钮悬停/触摸反馈 */
.bottom-bar .btn:active {
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10rpx);
}

/* 主按钮特殊样式 (加号) 保持醒目，但透明融合 */SS
.bottom-bar .main-btn {
  background: rgba(173, 233, 248, 1.0);      /* 半透明背景，区别于其他按钮 */
  backdrop-filter: blur(20rpx);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 8rpx 24rpx rgba(74, 144, 226, 0.3);
  width: 100rpx;
  height: 100rpx;
  border-radius: 60rpx;
  margin-top: -40rpx;                         /* 略微上浮，突出主按钮 */
  transition: transform 0.2s;
}

.bottom-bar .main-btn:active {
  transform: scale(0.96);
  background: rgba(255, 255, 255, 0.7);
}

/* 图标和文字颜色微调，在透明背景上保持可读性 */
.bottom-bar .btn-icon {
  font-size: 36rpx;
  line-height: 1.2;
  color: #2c3e50;                           /* 深色文字，透明背景下依然清晰 */
  text-shadow: 0 2rpx 6rpx rgba(255,255,255,0.5); /* 轻微白边增强可读性 */
}

.bottom-bar .btn-text {
  font-size: 22rpx;
  color: #2c3e50;
  font-weight: 500;
  margin-top: 4rpx;
  text-shadow: 0 1rpx 4rpx rgba(255,255,255,0.6);
}

.bottom-bar .main-btn-icon {
  font-size: 60rpx;
  color: #ffffff;                           /* 主按钮图标颜色更深 */
  font-weight: 300;
  line-height: 1;
  text-shadow: 0 2rpx 8rpx rgba(255,255,255,0.8);
}

/* 可选：根据不同场景增加底部留白，让栏更透气 */
page {
  background: linear-gradient(145deg, #f0f7ff 0%, #e6f0fa 100%); /* 示例背景，可删除 */
  /* 实际使用中背景由上层决定，这里仅为预览效果 */
}

.btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  padding: 16rpx 32rpx;
  border-radius: 40rpx;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn:hover {
  background: rgba(240, 248, 255, 0.8);
  transform: translateY(-4rpx);
}

.btn-icon {
  font-size: 36rpx;
  color: #4A90E2;
}

.btn-text {
  font-size: 24rpx;
  color: #7B8B9F;
  font-weight: 600;
}

.main-btn {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #4A90E2, #63B3ED);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -40rpx 0;
  box-shadow: 0 16rpx 32rpx rgba(74, 144, 226, 0.4);
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.main-btn:hover {
  transform: translateY(-4rpx) scale(1.05);
  box-shadow: 0 24rpx 48rpx rgba(74, 144, 226, 0.5);
}

.main-btn::before {
  content: '';
  position: absolute;
  top: -10rpx;
  left: -10rpx;
  right: -10rpx;
  bottom: -10rpx;
  background: rgba(74, 144, 226, 0.1);
  border-radius: 50%;
  z-index: -1;
}

.main-btn-icon {
  font-size: 64rpx;
  color: white;
  font-weight: 300;
}
</style>