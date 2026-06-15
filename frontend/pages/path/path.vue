<template>
  <view class="magic-path-page">
    <!-- 魔法星星背景 -->
    <view class="stars-background">
      <view 
        v-for="(star, index) in magicStars" 
        :key="index"
        class="magic-star"
        :style="{
          left: star.left + '%',
          top: star.top + '%',
          width: star.size + 'rpx',
          height: star.size + 'rpx',
          opacity: star.opacity,
          animationDuration: star.duration + 's',
          animationDelay: star.delay + 's'
        }"
      ></view>
    </view>

    <!-- 顶部区域 -->
    <view class="header-section" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="greeting-container">
        <text class="greeting-text">嗨，{{ userName }}！</text>
        <text class="goal-text">你的魔法之路：{{ currentGoal }}</text>
      </view>
      
      <view class="progress-summary">
        <view class="progress-capsule">
          <view class="progress-item">
            <text class="progress-icon">📍</text>
            <view class="progress-info">
              <text class="progress-number">{{ currentStep }}/{{ totalSteps }}</text>
              <text class="progress-label">当前进度</text>
            </view>
          </view>
          
          <view class="progress-item">
            <text class="progress-icon">⏱️</text>
            <view class="progress-info">
              <text class="progress-number">{{ estimatedTime }}</text>
              <text class="progress-label">预计达成</text>
            </view>
          </view>
          
          <view class="progress-item">
            <text class="progress-icon">🔥</text>
            <view class="progress-info">
              <text class="progress-number">{{ streakDays }}</text>
              <text class="progress-label">连续成长</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 心情小组件 -->
      <view class="mood-widget" v-if="recentMood">
        <view class="mood-content">
          <text class="mood-emoji">{{ recentMood.emoji }}</text>
          <view class="mood-text">
            <text class="mood-title">最近情绪：{{ recentMood.label }}</text>
            <text class="mood-encouragement">{{ recentMood.encouragement }}</text>
          </view>
        </view>
        <view class="mood-flower">🌸</view>
      </view>
    </view>

    <!-- 路径视图切换 -->
    <view class="view-switcher">
      <view 
        class="view-tab" 
        :class="{ active: activeView === 'timeline' }"
        @click="switchView('timeline')"
      >
        <text class="tab-icon">✨</text>
        <text class="tab-text">魔法时间轴</text>
      </view>
      <view 
        class="view-tab" 
        :class="{ active: activeView === 'cards' }"
        @click="switchView('cards')"
      >
        <text class="tab-icon">📋</text>
        <text class="tab-text">激励卡片</text>
      </view>
    </view>

    <!-- 魔法时间轴视图 -->
    <scroll-view 
      v-if="activeView === 'timeline'" 
      class="timeline-container"
      scroll-y
      scroll-with-animation
      @scroll="handleScroll"
    >
      <view class="timeline-path">
        <!-- 发光路径 -->
        <view class="path-line">
          <view class="path-glow"></view>
        </view>
        
        <!-- 时间轴节点 -->
        <view 
          v-for="(step, index) in timelineSteps" 
          :key="index"
          class="timeline-node"
          :class="getNodeClass(step)"
          :style="{ top: (index * 120) + 'rpx' }"
          @click="showStepDetail(step)"
        >
          <!-- 节点连接点 -->
          <view class="node-connector"></view>
          
          <!-- 节点内容 -->
          <view class="node-content">
            <!-- 状态图标 -->
            <view class="node-status">
              <text v-if="step.status === 'completed'" class="status-icon">✓</text>
              <text v-else-if="step.status === 'in-progress'" class="status-icon">●</text>
              <text v-else class="status-icon">?</text>
            </view>
            
            <!-- 节点主体 -->
            <view class="node-body">
              <view class="node-header">
                <text class="node-icon">{{ step.icon }}</text>
                <view class="node-title-container">
                  <text class="node-title">{{ step.title }}</text>
                  <text class="node-tag" :style="{ background: getTagColor(step.type) }">
                    {{ getTypeLabel(step.type) }}
                  </text>
                </view>
              </view>
              
              <view class="node-info">
                <text class="node-duration">{{ step.duration }}</text>
                <text class="node-difficulty">
                  难度：<text v-for="n in 3" :key="n" 
                    class="difficulty-star"
                    :class="{ active: n <= step.difficulty }"
                  >★</text>
                </text>
              </view>
              
              <!-- 进行中的进度环 -->
              <view v-if="step.status === 'in-progress'" class="progress-ring">
                <view class="ring-background"></view>
                <view 
                  class="ring-progress" 
                  :style="{ transform: `rotate(${step.progress * 360}deg)` }"
                ></view>
                <text class="ring-text">{{ Math.round(step.progress * 100) }}%</text>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 路径终点 -->
      <view class="path-destination">
        <text class="destination-icon">🎯</text>
        <text class="destination-text">{{ goalDestination }}</text>
      </view>
    </scroll-view>

    <!-- 激励卡片视图 -->
    <scroll-view 
      v-else 
      class="cards-container"
      scroll-y
    >
      <view class="cards-grid">
        <view 
          v-for="(step, index) in cardSteps" 
          :key="index"
          class="motivation-card"
          :class="step.status"
          @click="showStepDetail(step)"
        >
          <view class="card-header">
            <text class="card-icon">{{ step.icon }}</text>
            <view class="card-title-container">
              <text class="card-title">{{ step.title }}</text>
              <text class="card-tag" :style="{ background: getTagColor(step.type) }">
                {{ getTypeLabel(step.type) }}
              </text>
            </view>
          </view>
          
          <view class="card-body">
            <text class="card-description">{{ step.description }}</text>
            
            <view class="card-meta">
              <view class="meta-item">
                <text class="meta-icon">⏱️</text>
                <text class="meta-text">{{ step.duration }}</text>
              </view>
              <view class="meta-item">
                <text class="meta-icon">⭐</text>
                <text class="meta-text">难度：{{ '★'.repeat(step.difficulty) }}</text>
              </view>
            </view>
            
            <!-- 进度条 -->
            <view v-if="step.status !== 'pending'" class="card-progress">
              <view class="progress-track">
                <view 
                  class="progress-fill"
                  :style="{ width: step.progress * 100 + '%' }"
                ></view>
              </view>
              <text class="progress-text">
                {{ step.status === 'completed' ? '已完成' : Math.round(step.progress * 100) + '%' }}
              </text>
            </view>
          </view>
          
          <view class="card-footer">
            <view 
              class="action-button"
              @click.stop="handleStepAction(step)"
              :class="step.status"
            >
              <text class="button-text">{{ getActionText(step.status) }}</text>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 底部操作栏 -->
    <view class="bottom-actions">
      <view class="action-buttons">
        <view class="action-button primary" @click="showPathTemplates">
          <text class="button-icon">🔄</text>
          <text class="button-text">切换路径</text>
        </view>
        
        <view 
          class="action-button success" 
          @click="markCurrentStepComplete"
          v-if="currentActiveStep"
        >
          <text class="button-icon">🎉</text>
          <text class="button-text">标记完成</text>
        </view>
        
        <view class="action-button secondary" @click="addCustomStep">
          <text class="button-icon">➕</text>
          <text class="button-text">添加步骤</text>
        </view>
        
        <view class="action-button info" @click="showResources">
          <text class="button-icon">📚</text>
          <text class="button-text">查看资源</text>
        </view>
      </view>
    </view>

    <!-- 路径模板选择弹窗 -->
    <view class="modal-overlay" v-if="showPathModal" @click="closePathModal">
      <view class="modal-content path-modal" @click.stop>
        <view class="modal-header">
          <text class="modal-title">选择魔法路径</text>
          <view class="modal-close" @click="closePathModal">×</view>
        </view>
        
        <scroll-view class="modal-body" scroll-y>
          <view 
            v-for="(template, index) in pathTemplates" 
            :key="index"
            class="template-card"
            :class="{ recommended: template.recommended }"
            @click="selectPathTemplate(template)"
          >
            <view class="template-icon">{{ template.icon }}</view>
            <view class="template-info">
              <text class="template-title">{{ template.title }}</text>
              <text class="template-subtitle">{{ template.subtitle }}</text>
              <view class="template-meta">
                <text class="meta-item">⏱️ {{ template.duration }}</text>
                <text class="meta-item">🎯 {{ template.steps }} 个步骤</text>
                <text v-if="template.matchScore" class="match-score">
                  匹配度 {{ template.matchScore }}%
                </text>
              </view>
            </view>
            <text v-if="template.recommended" class="recommended-badge">推荐</text>
          </view>
        </scroll-view>
      </view>
    </view>

    <!-- 步骤详情弹窗 -->
    <view class="modal-overlay" v-if="showStepModal" @click="closeStepModal">
      <view class="modal-content step-modal" @click.stop>
        <view class="modal-header">
          <text class="step-status-tag" :class="selectedStep.status">
            {{ getStatusLabel(selectedStep.status) }}
          </text>
          <view class="modal-close" @click="closeStepModal">×</view>
        </view>
        
        <scroll-view class="modal-body" scroll-y>
          <view class="step-detail-header">
            <text class="step-icon">{{ selectedStep.icon }}</text>
            <text class="step-title">{{ selectedStep.title }}</text>
            <text class="step-tag" :style="{ background: getTagColor(selectedStep.type) }">
              {{ getTypeLabel(selectedStep.type) }}
            </text>
          </view>
          
          <view class="step-detail-content">
            <view class="detail-section">
              <text class="section-title">📝 步骤描述</text>
              <text class="section-text">{{ selectedStep.description }}</text>
            </view>
            
            <view class="detail-section">
              <text class="section-title">🎯 预期成果</text>
              <view class="outcomes-list">
                <view v-for="(outcome, idx) in selectedStep.outcomes" :key="idx" class="outcome-item">
                  <text class="outcome-icon">✓</text>
                  <text class="outcome-text">{{ outcome }}</text>
                </view>
              </view>
            </view>
            
            <view class="detail-section">
              <text class="section-title">📊 进度追踪</text>
              <view class="progress-section">
                <view class="progress-stats">
                  <view class="stat-item">
                    <text class="stat-value">{{ Math.round(selectedStep.progress * 100) }}%</text>
                    <text class="stat-label">完成进度</text>
                  </view>
                  <view class="stat-item">
                    <text class="stat-value">{{ selectedStep.duration }}</text>
                    <text class="stat-label">预计时间</text>
                  </view>
                  <view class="stat-item">
                    <text class="stat-value">{{ '★'.repeat(selectedStep.difficulty) }}</text>
                    <text class="stat-label">难度</text>
                  </view>
                </view>
                
                <view v-if="selectedStep.status === 'in-progress'" class="progress-controls">
                  <text class="progress-label">更新进度：</text>
                  <view class="progress-slider-container">
                    <slider 
                      :value="selectedStep.progress * 100" 
                      @change="updateStepProgress"
                      activeColor="#F98C53"
                      backgroundColor="#F9F2EF"
                      block-size="24"
                    />
                  </view>
                </view>
              </view>
            </view>
            
            <view v-if="selectedStep.resources && selectedStep.resources.length" class="detail-section">
              <text class="section-title">📚 学习资源</text>
              <view class="resources-list">
                <view v-for="(resource, idx) in selectedStep.resources" :key="idx" class="resource-item">
                  <text class="resource-icon">{{ resource.type === 'article' ? '📖' : '🎬' }}</text>
                  <view class="resource-info">
                    <text class="resource-title">{{ resource.title }}</text>
                    <text class="resource-source">{{ resource.source }}</text>
                  </view>
                  <view class="resource-action" @click="openResource(resource)">查看</view>
                </view>
              </view>
            </view>
          </view>
        </scroll-view>
        
        <view class="modal-footer">
          <view class="action-buttons">
            <view 
              class="action-button"
              :class="selectedStep.status"
              @click="toggleStepStatus"
            >
              <text class="button-text">{{ getActionText(selectedStep.status) }}</text>
            </view>
            <view class="action-button secondary" @click="closeStepModal">
              <text class="button-text">关闭</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 完成庆祝动画 -->
    <view class="celebration-overlay" v-if="showCelebration">
      <view class="celebration-content">
        <view class="confetti-container">
          <view 
            v-for="(confetti, index) in confettiPieces" 
            :key="index"
            class="confetti-piece"
            :style="{
              left: confetti.left + '%',
              backgroundColor: confetti.color,
              animationDelay: confetti.delay + 's',
              animationDuration: confetti.duration + 's'
            }"
          ></view>
        </view>
        
        <view class="celebration-message">
          <text class="celebration-icon">🎉</text>
          <text class="celebration-title">恭喜！</text>
          <text class="celebration-text">你又向前迈了一大步！✨</text>
          <text class="celebration-subtext">{{ celebrationMessage }}</text>
        </view>
        
        <view class="celebration-actions">
          <view class="celebration-button" @click="closeCelebration">
            <text class="button-text">继续前进 →</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 首次引导 -->
    <view class="guide-overlay" v-if="showFirstGuide" @click="closeGuide">
      <view class="guide-content" @click.stop>
        <view class="guide-animation">
          <view class="seed-plant"></view>
          <view class="seed-grow"></view>
          <view class="seed-bloom">🌱</view>
        </view>
        
        <view class="guide-message">
          <text class="guide-title">欢迎来到魔法成长之路！</text>
          <text class="guide-text">让我们种下第一颗魔法种子，开启你的成长旅程</text>
          <text class="guide-tip">✨ 每个完成的步骤都会让路径更加明亮 ✨</text>
        </view>
        
        <view class="guide-actions">
          <view class="guide-button" @click="startFirstStep">
            <text class="button-text">种下种子 🌱</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 状态栏高度
const statusBarHeight = ref(44)

// 用户信息
const userName = ref('小萌')
const currentGoal = ref('软件工程 → AI产品经理')
const goalDestination = ref('成为AI产品经理')
const streakDays = ref(12)
const estimatedTime = ref('6个月后')

// 路径数据
const currentStep = ref(3)
const totalSteps = ref(8)
const currentActiveStep = ref(null)

// 视图状态
const activeView = ref('timeline')
const showPathModal = ref(false)
const showStepModal = ref(false)
const showCelebration = ref(false)
const showFirstGuide = ref(true)

// 选中的步骤
const selectedStep = ref({})

// 最近情绪
const recentMood = ref({
  emoji: '🌧️',
  label: '有点压力',
  encouragement: '最近有点小压力？这条路会陪你一起走哦～'
})

// 魔法星星
const magicStars = ref([])

// 庆祝彩纸
const confettiPieces = ref([])

// 时间轴步骤数据
const timelineSteps = ref([
  {
    id: 1,
    title: '掌握 React & Vue',
    icon: '⚛️',
    type: 'skill',
    status: 'completed',
    duration: '2个月',
    difficulty: 2,
    progress: 1,
    description: '掌握现代前端框架，构建交互式Web应用',
    outcomes: [
      '能够独立开发SPA应用',
      '理解组件化开发思想',
      '掌握状态管理方案'
    ],
    resources: [
      { type: 'article', title: 'React官方文档', source: 'reactjs.org' },
      { type: 'video', title: 'Vue3入门教程', source: 'Bilibili' }
    ]
  },
  {
    id: 2,
    title: '数据结构与算法',
    icon: '📊',
    type: 'foundation',
    status: 'completed',
    duration: '3个月',
    difficulty: 3,
    progress: 1,
    description: '夯实计算机基础，提升编程思维',
    outcomes: [
      '掌握常用数据结构',
      '熟悉经典算法',
      '提升编程思维能力'
    ]
  },
  {
    id: 3,
    title: '机器学习基础',
    icon: '🤖',
    type: 'skill',
    status: 'in-progress',
    duration: '3个月',
    difficulty: 3,
    progress: 0.65,
    description: '学习机器学习基本原理和常用算法',
    outcomes: [
      '理解机器学习基本概念',
      '掌握常见ML算法',
      '能够使用scikit-learn'
    ],
    resources: [
      { type: 'course', title: '吴恩达机器学习', source: 'Coursera' }
    ]
  },
  {
    id: 4,
    title: '参加AI Hackathon',
    icon: '🏆',
    type: 'competition',
    status: 'pending',
    duration: '1个月',
    difficulty: 3,
    progress: 0,
    description: '参加AI竞赛，积累实战经验',
    outcomes: [
      '获得项目经验',
      '积累竞赛经历',
      '扩展行业人脉'
    ]
  },
  {
    id: 5,
    title: '产品设计思维',
    icon: '🎨',
    type: 'skill',
    status: 'pending',
    duration: '2个月',
    difficulty: 2,
    progress: 0,
    description: '学习产品设计方法和用户研究',
    outcomes: [
      '掌握用户研究技巧',
      '能够进行产品原型设计',
      '理解用户体验原则'
    ]
  },
  {
    id: 6,
    title: 'AI产品实习',
    icon: '💼',
    type: 'internship',
    status: 'pending',
    duration: '3个月',
    difficulty: 3,
    progress: 0,
    description: '在AI公司进行产品实习',
    outcomes: [
      '积累实际产品经验',
      '了解AI产品开发流程',
      '建立行业联系'
    ]
  },
  {
    id: 7,
    title: '作品集完善',
    icon: '📁',
    type: 'portfolio',
    status: 'pending',
    duration: '1个月',
    difficulty: 2,
    progress: 0,
    description: '整理和完善个人作品集',
    outcomes: [
      '完整的作品集展示',
      '项目文档和演示',
      '个人品牌建立'
    ]
  },
  {
    id: 8,
    title: '求职准备与面试',
    icon: '🎯',
    type: 'job',
    status: 'pending',
    duration: '2个月',
    difficulty: 3,
    progress: 0,
    description: '准备简历、面试和求职策略',
    outcomes: [
      '专业的简历和LinkedIn',
      '面试技巧提升',
      '获得理想工作offer'
    ]
  }
])

// 卡片视图步骤数据（与时间轴数据同步）
const cardSteps = computed(() => timelineSteps.value)

// 路径模板
const pathTemplates = ref([
  {
    id: 'ai-product-manager',
    icon: '🤖',
    title: 'AI产品经理',
    subtitle: '从技术到产品的转型之路',
    duration: '12-18个月',
    steps: 8,
    recommended: true,
    matchScore: 95
  },
  {
    id: 'frontend-expert',
    icon: '💻',
    title: '前端技术专家',
    subtitle: '深入前端技术栈，成为领域专家',
    duration: '10-15个月',
    steps: 7,
    matchScore: 70
  },
  {
    id: 'fullstack-engineer',
    icon: '🔧',
    title: '全栈工程师',
    subtitle: '掌握前后端，独立开发完整产品',
    duration: '12-20个月',
    steps: 9,
    matchScore: 65
  },
  {
    id: 'data-scientist',
    icon: '📈',
    title: '数据科学家',
    subtitle: '数据分析与机器学习专家',
    duration: '15-24个月',
    steps: 10,
    matchScore: 60
  },
  {
    id: 'startup-founder',
    icon: '🚀',
    title: '创业公司创始人',
    subtitle: '从0到1打造自己的产品',
    duration: '18-36个月',
    steps: 12,
    matchScore: 50
  },
  {
    id: 'product-designer',
    icon: '🎨',
    title: '产品设计师',
    subtitle: '专注于用户体验和界面设计',
    duration: '10-16个月',
    steps: 7,
    matchScore: 45
  }
])

// 庆祝消息
const celebrationMessage = ref('')

// 初始化魔法星星
const generateMagicStars = () => {
  const stars = []
  const starCount = 15
  
  for (let i = 0; i < starCount; i++) {
    stars.push({
      left: Math.random() * 100,
      top: Math.random() * 50,
      size: 4 + Math.random() * 6,
      opacity: 0.3 + Math.random() * 0.5,
      duration: 3 + Math.random() * 4,
      delay: Math.random() * 2
    })
  }
  
  magicStars.value = stars
}

// 生成庆祝彩纸
const generateConfetti = () => {
  const pieces = []
  const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#FF9A9E', '#A1C4FD', '#D4FC79']
  
  for (let i = 0; i < 50; i++) {
    pieces.push({
      left: Math.random() * 100,
      color: colors[Math.floor(Math.random() * colors.length)],
      delay: Math.random() * 0.5,
      duration: 1 + Math.random() * 2
    })
  }
  
  confettiPieces.value = pieces
}

// 获取节点类名
const getNodeClass = (step) => {
  const classes = ['node-' + step.status]
  if (step.id === currentActiveStep.value) {
    classes.push('active')
  }
  return classes.join(' ')
}

// 获取标签颜色
const getTagColor = (type) => {
  const colors = {
    skill: 'rgba(249, 140, 83, 0.2)',
    foundation: 'rgba(106, 176, 76, 0.2)',
    competition: 'rgba(255, 107, 107, 0.2)',
    internship: 'rgba(66, 153, 225, 0.2)',
    portfolio: 'rgba(159, 122, 234, 0.2)',
    job: 'rgba(249, 140, 83, 0.2)'
  }
  return colors[type] || 'rgba(200, 200, 200, 0.2)'
}

// 获取类型标签
const getTypeLabel = (type) => {
  const labels = {
    skill: '技能',
    foundation: '基础',
    competition: '竞赛',
    internship: '实习',
    portfolio: '作品集',
    job: '求职'
  }
  return labels[type] || '其他'
}

// 获取状态标签
const getStatusLabel = (status) => {
  const labels = {
    completed: '已完成',
    'in-progress': '进行中',
    pending: '未开始'
  }
  return labels[status] || '未知'
}

// 获取行动文本
const getActionText = (status) => {
  const texts = {
    completed: '重新开始',
    'in-progress': '更新进度',
    pending: '开始进行'
  }
  return texts[status] || '操作'
}

// 切换视图
const switchView = (view) => {
  activeView.value = view
}

// 显示路径模板
const showPathTemplates = () => {
  showPathModal.value = true
}

// 关闭路径模板弹窗
const closePathModal = () => {
  showPathModal.value = false
}

// 选择路径模板
const selectPathTemplate = (template) => {
  currentGoal.value = template.title
  goalDestination.value = template.subtitle
  closePathModal()
  
  // 这里可以添加更多逻辑，比如加载模板对应的步骤
}

// 添加自定义步骤
const addCustomStep = () => {
  uni.showToast({
    title: '添加自定义步骤功能开发中',
    icon: 'none'
  })
}

// 显示资源
const showResources = () => {
  uni.navigateTo({
    url: '/pages/resources/index'
  })
}

// 显示步骤详情
const showStepDetail = (step) => {
  selectedStep.value = { ...step }
  showStepModal.value = true
}

// 关闭步骤详情
const closeStepModal = () => {
  showStepModal.value = false
}

// 更新步骤进度
const updateStepProgress = (e) => {
  const progress = e.detail.value / 100
  selectedStep.value.progress = progress
  
  // 更新原始数据
  const index = timelineSteps.value.findIndex(s => s.id === selectedStep.value.id)
  if (index !== -1) {
    timelineSteps.value[index].progress = progress
  }
}

// 切换步骤状态
const toggleStepStatus = () => {
  const step = selectedStep.value
  const index = timelineSteps.value.findIndex(s => s.id === step.id)
  
  if (index !== -1) {
    if (step.status === 'pending') {
      timelineSteps.value[index].status = 'in-progress'
      timelineSteps.value[index].progress = 0.1
      currentActiveStep.value = step.id
    } else if (step.status === 'in-progress') {
      timelineSteps.value[index].status = 'completed'
      timelineSteps.value[index].progress = 1
      currentActiveStep.value = null
      celebrateStepCompletion(step)
    } else if (step.status === 'completed') {
      timelineSteps.value[index].status = 'pending'
      timelineSteps.value[index].progress = 0
    }
    
    // 更新选中步骤状态
    selectedStep.value = { ...timelineSteps.value[index] }
    updateProgressStats()
  }
}

// 标记当前步骤完成
const markCurrentStepComplete = () => {
  const activeStep = timelineSteps.value.find(step => step.status === 'in-progress')
  if (activeStep) {
    activeStep.status = 'completed'
    activeStep.progress = 1
    currentActiveStep.value = null
    updateProgressStats()
    celebrateStepCompletion(activeStep)
  }
}

// 庆祝步骤完成
const celebrateStepCompletion = (step) => {
  celebrationMessage.value = `完成了 "${step.title}"！`
  generateConfetti()
  showCelebration.value = true
  
  // 播放庆祝音效（需要用户交互后）
  setTimeout(() => {
    // 这里可以添加音效播放代码
  }, 300)
}

// 关闭庆祝动画
const closeCelebration = () => {
  showCelebration.value = false
}

// 更新进度统计
const updateProgressStats = () => {
  const completedSteps = timelineSteps.value.filter(step => step.status === 'completed').length
  const inProgressSteps = timelineSteps.value.filter(step => step.status === 'in-progress').length
  
  currentStep.value = completedSteps + inProgressSteps
  currentActiveStep.value = timelineSteps.value.find(step => step.status === 'in-progress')?.id || null
}

// 处理滚动
const handleScroll = (e) => {
  // 可以添加滚动时的视差效果
  const scrollTop = e.detail.scrollTop
  // 这里可以添加滚动交互逻辑
}

// 处理步骤行动
const handleStepAction = (step) => {
  if (step.status === 'pending') {
    step.status = 'in-progress'
    step.progress = 0.1
    currentActiveStep.value = step.id
  } else if (step.status === 'in-progress') {
    showStepDetail(step)
  } else if (step.status === 'completed') {
    showStepDetail(step)
  }
}

// 打开资源
const openResource = (resource) => {
  uni.showModal({
    title: '打开资源',
    content: `将在浏览器中打开：${resource.title}`,
    success: (res) => {
      if (res.confirm) {
        // 这里可以实现打开链接的逻辑
        uni.showToast({
          title: '正在打开资源...',
          icon: 'none'
        })
      }
    }
  })
}

// 开始第一步
const startFirstStep = () => {
  showFirstGuide.value = false
  // 自动开始第一个步骤
  if (timelineSteps.value[0].status === 'pending') {
    timelineSteps.value[0].status = 'in-progress'
    timelineSteps.value[0].progress = 0.1
    currentActiveStep.value = timelineSteps.value[0].id
    updateProgressStats()
  }
}

// 关闭引导
const closeGuide = () => {
  showFirstGuide.value = false
}

// 生命周期
onMounted(() => {
  generateMagicStars()
  updateProgressStats()
})

onUnmounted(() => {
  // 清理逻辑
})
</script>

<style scoped>
.magic-path-page {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    #F98C53 0%, 
    #FCCEB4 30%, 
    #F9F2EF 50%, 
    #F0F8FF 70%, 
    #ABD7FB 100%);
  position: relative;
  overflow: hidden;
}

/* 魔法星星背景 */
.stars-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.magic-star {
  position: absolute;
  background: linear-gradient(135deg, #FFFFFF 0%, #FFFACD 100%);
  border-radius: 50%;
  filter: blur(1px);
  animation: starTwinkle ease-in-out infinite alternate;
}

@keyframes starTwinkle {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

/* 顶部区域 */
.header-section {
  position: relative;
  z-index: 1;
  padding: 40rpx 30rpx 20rpx;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.9), transparent);
  backdrop-filter: blur(10px);
  border-bottom-left-radius: 40rpx;
  border-bottom-right-radius: 40rpx;
  margin-bottom: 20rpx;
}

.greeting-container {
  margin-bottom: 40rpx;
}

.greeting-text {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
}

.goal-text {
  display: block;
  font-size: 28rpx;
  color: #666;
  line-height: 1.4;
}

/* 进度胶囊 */
.progress-summary {
  margin-bottom: 30rpx;
}

.progress-capsule {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 40rpx;
  padding: 30rpx;
  display: flex;
  justify-content: space-between;
  box-shadow: 0 8rpx 32rpx rgba(249, 140, 83, 0.15);
  border: 1rpx solid rgba(249, 140, 83, 0.1);
}

.progress-item {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 0 10rpx;
}

.progress-item:not(:last-child) {
  border-right: 1rpx solid rgba(0, 0, 0, 0.05);
}

.progress-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.progress-info {
  display: flex;
  flex-direction: column;
}

.progress-number {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 4rpx;
}

.progress-label {
  font-size: 22rpx;
  color: #888;
}

/* 心情小组件 */
.mood-widget {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 248, 240, 0.9));
  backdrop-filter: blur(20px);
  border-radius: 30rpx;
  padding: 24rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
  border: 1rpx solid rgba(249, 140, 83, 0.1);
}

.mood-content {
  display: flex;
  align-items: center;
  flex: 1;
}

.mood-emoji {
  font-size: 48rpx;
  margin-right: 20rpx;
}

.mood-text {
  flex: 1;
}

.mood-title {
  display: block;
  font-size: 26rpx;
  font-weight: 500;
  color: #333;
  margin-bottom: 6rpx;
}

.mood-encouragement {
  display: block;
  font-size: 22rpx;
  color: #666;
  line-height: 1.3;
}

.mood-flower {
  font-size: 36rpx;
  animation: flowerFloat 3s ease-in-out infinite;
}

@keyframes flowerFloat {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-10rpx) rotate(10deg); }
}

/* 视图切换器 */
.view-switcher {
  position: relative;
  z-index: 1;
  display: flex;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 40rpx;
  padding: 8rpx;
  margin: 0 30rpx 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.view-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20rpx 0;
  border-radius: 32rpx;
  transition: all 0.3s ease;
}

.view-tab.active {
  background: linear-gradient(135deg, #F98C53, #FFB347);
  box-shadow: 0 4rpx 16rpx rgba(249, 140, 83, 0.3);
}

.tab-icon {
  font-size: 32rpx;
  margin-right: 12rpx;
}

.tab-text {
  font-size: 26rpx;
  font-weight: 500;
}

.view-tab.active .tab-text {
  color: white;
  font-weight: 600;
}

.view-tab:not(.active) .tab-text {
  color: #666;
}

/* 魔法时间轴容器 */
.timeline-container {
  height: 65vh;
  position: relative;
  padding: 0 30rpx;
  margin-bottom: 20rpx;
}

.timeline-path {
  position: relative;
  min-height: 1200rpx;
  padding: 40rpx 0;
}

/* 发光路径 */
.path-line {
  position: absolute;
  left: 120rpx;
  top: 0;
  bottom: 0;
  width: 6rpx;
  background: linear-gradient(to bottom, 
    rgba(249, 140, 83, 0.3) 0%,
    rgba(249, 140, 83, 0.6) 30%,
    rgba(249, 140, 83, 0.8) 50%,
    rgba(210, 224, 170, 0.8) 70%,
    rgba(210, 224, 170, 0.4) 100%);
  z-index: 1;
}

.path-glow {
  position: absolute;
  left: -20rpx;
  top: 0;
  right: -20rpx;
  bottom: 0;
  background: linear-gradient(to bottom, 
    rgba(249, 140, 83, 0.1) 0%,
    rgba(249, 140, 83, 0.2) 50%,
    rgba(210, 224, 170, 0.2) 100%);
  filter: blur(20rpx);
  animation: pathGlow 2s ease-in-out infinite alternate;
}

@keyframes pathGlow {
  0% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* 时间轴节点 */
.timeline-node {
  position: absolute;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  z-index: 2;
  transition: all 0.3s ease;
}

.node-connector {
  width: 120rpx;
  height: 6rpx;
  background: rgba(249, 140, 83, 0.5);
  position: relative;
}

.node-connector::before {
  content: '';
  position: absolute;
  left: -4rpx;
  top: -4rpx;
  width: 14rpx;
  height: 14rpx;
  background: #F98C53;
  border-radius: 50%;
  box-shadow: 0 0 10rpx rgba(249, 140, 83, 0.8);
}

.node-content {
  flex: 1;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24rpx;
  padding: 24rpx;
  margin-left: 20rpx;
  box-shadow: 0 6rpx 24rpx rgba(0, 0, 0, 0.08);
  border: 1rpx solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.timeline-node.completed .node-content {
  background: linear-gradient(135deg, rgba(210, 224, 170, 0.95), rgba(255, 255, 255, 0.95));
  border: 1rpx solid rgba(210, 224, 170, 0.3);
  box-shadow: 0 6rpx 24rpx rgba(210, 224, 170, 0.2);
}

.timeline-node.in-progress .node-content {
  background: linear-gradient(135deg, rgba(249, 140, 83, 0.1), rgba(255, 255, 255, 0.95));
  border: 1rpx solid rgba(249, 140, 83, 0.2);
  box-shadow: 0 6rpx 24rpx rgba(249, 140, 83, 0.15);
  animation: pulseBreathing 2s ease-in-out infinite;
}

.timeline-node.pending .node-content {
  background: rgba(249, 242, 239, 0.9);
  border: 1rpx dashed rgba(0, 0, 0, 0.1);
}

@keyframes pulseBreathing {
  0%, 100% { transform: scale(1); box-shadow: 0 6rpx 24rpx rgba(249, 140, 83, 0.15); }
  50% { transform: scale(1.02); box-shadow: 0 8rpx 32rpx rgba(249, 140, 83, 0.25); }
}

.node-status {
  margin-right: 20rpx;
}

.status-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  font-size: 24rpx;
  font-weight: bold;
}

.timeline-node.completed .status-icon {
  background: rgba(106, 176, 76, 0.2);
  color: #6AB04C;
}

.timeline-node.in-progress .status-icon {
  background: rgba(249, 140, 83, 0.2);
  color: #F98C53;
  animation: dotPulse 1.5s ease-in-out infinite;
}

.timeline-node.pending .status-icon {
  background: rgba(200, 200, 200, 0.2);
  color: #999;
}

@keyframes dotPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(0.9); }
}

.node-body {
  flex: 1;
}

.node-header {
  display: flex;
  align-items: center;
  margin-bottom: 12rpx;
}

.node-icon {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.node-title-container {
  flex: 1;
}

.node-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 6rpx;
}

.node-tag {
  display: inline-block;
  font-size: 20rpx;
  color: #666;
  padding: 4rpx 12rpx;
  border-radius: 16rpx;
}

.node-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.node-duration {
  font-size: 24rpx;
  color: #888;
}

.node-difficulty {
  font-size: 22rpx;
  color: #666;
}

.difficulty-star {
  color: #DDD;
  margin-left: 4rpx;
}

.difficulty-star.active {
  color: #FFD700;
}

/* 进度环 */
.progress-ring {
  position: relative;
  width: 60rpx;
  height: 60rpx;
  margin-left: auto;
}

.ring-background {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 6rpx solid #F9F2EF;
  border-radius: 50%;
}

.ring-progress {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 6rpx solid transparent;
  border-top-color: #F98C53;
  border-radius: 50%;
  clip: rect(0, 30rpx, 60rpx, 0);
  transform-origin: center;
  transition: transform 0.5s ease;
}

.ring-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 20rpx;
  font-weight: 600;
  color: #F98C53;
}

/* 路径终点 */
.path-destination {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx;
  z-index: 3;
}

.destination-icon {
  font-size: 60rpx;
  margin-right: 20rpx;
  animation: destinationGlow 2s ease-in-out infinite alternate;
}

@keyframes destinationGlow {
  0% { filter: drop-shadow(0 0 5rpx rgba(249, 140, 83, 0.5)); }
  100% { filter: drop-shadow(0 0 20rpx rgba(249, 140, 83, 0.8)); }
}

.destination-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  text-align: center;
  background: linear-gradient(135deg, #F98C53, #FFB347);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 激励卡片视图 */
.cards-container {
  height: 65vh;
  padding: 0 30rpx;
  margin-bottom: 20rpx;
  
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320rpx, 1fr));
  gap: 24rpx;
  padding: 20rpx 0;
  margin-right: 60rpx;
}

.motivation-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24rpx;
  padding: 24rpx;
  box-shadow: 0 6rpx 24rpx rgba(0, 0, 0, 0.08);
  border: 1rpx solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.motivation-card.completed {
  background: linear-gradient(135deg, rgba(210, 224, 170, 0.95), rgba(255, 255, 255, 0.95));
  border: 1rpx solid rgba(210, 224, 170, 0.3);
}

.motivation-card.in-progress {
  background: linear-gradient(135deg, rgba(249, 140, 83, 0.1), rgba(255, 255, 255, 0.95));
  border: 1rpx solid rgba(249, 140, 83, 0.2);
  animation: cardPulse 3s ease-in-out infinite;
}

.motivation-card.pending {
  background: rgba(249, 242, 239, 0.9);
  border: 1rpx dashed rgba(0, 0, 0, 0.1);
  opacity: 0.8;
}

@keyframes cardPulse {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5rpx); }
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.card-icon {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.card-title-container {
  flex: 1;
}

.card-title {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 6rpx;
}

.card-tag {
  display: inline-block;
  font-size: 20rpx;
  color: #666;
  padding: 2rpx 10rpx;
  border-radius: 12rpx;
}

.card-body {
  margin-bottom: 20rpx;
}

.card-description {
  display: block;
  font-size: 24rpx;
  color: #666;
  line-height: 1.4;
  margin-bottom: 16rpx;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-icon {
  font-size: 24rpx;
  margin-right: 6rpx;
}

.meta-text {
  font-size: 22rpx;
  color: #888;
}

.card-progress {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.progress-track {
  flex: 1;
  height: 8rpx;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #F98C53, #FFB347);
  border-radius: 4rpx;
  transition: width 0.5s ease;
}

.motivation-card.completed .progress-fill {
  background: linear-gradient(90deg, #D2E0AA, #B8D8A6);
}

.progress-text {
  font-size: 22rpx;
  font-weight: 600;
  color: #F98C53;
  min-width: 80rpx;
  text-align: right;
}

.motivation-card.completed .progress-text {
  color: #6AB04C;
}

.card-footer {
  margin-top: 20rpx;
}

.action-button {
  width: 100%;
  padding: 16rpx 0;
  border-radius: 20rpx;
  text-align: center;
  font-size: 26rpx;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-button.in-progress {
  background: linear-gradient(135deg, #F98C53, #FFB347);
  color: white;
}

.action-button.completed {
  background: rgba(210, 224, 170, 0.2);
  color: #6AB04C;
}

.action-button.pending {
  background: rgba(200, 200, 200, 0.2);
  color: #999;
  border: 1rpx dashed rgba(0, 0, 0, 0.1);
}

/* 底部操作栏 */
.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-top: 1rpx solid rgba(0, 0, 0, 0.05);
  padding: 20rpx 30rpx;
  z-index: 100;
  margin-bottom: 100rpx;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16rpx;
}

.action-buttons .action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20rpx 0;
  border-radius: 24rpx;
  background: rgba(249, 140, 83, 0.1);
  border: 1rpx solid rgba(249, 140, 83, 0.2);
  transition: all 0.3s ease;
}

.action-buttons .action-button:active {
  transform: scale(0.95);
}

.action-buttons .action-button.primary {
  background: linear-gradient(135deg, rgba(249, 140, 83, 0.2), rgba(255, 179, 71, 0.2));
  border-color: rgba(249, 140, 83, 0.3);
}

.action-buttons .action-button.success {
  background: linear-gradient(135deg, rgba(210, 224, 170, 0.2), rgba(184, 216, 166, 0.2));
  border-color: rgba(210, 224, 170, 0.3);
}

.action-buttons .action-button.secondary {
  background: rgba(249, 242, 239, 0.8);
  border-color: rgba(0, 0, 0, 0.1);
}

.action-buttons .action-button.info {
  background: rgba(171, 215, 251, 0.2);
  border-color: rgba(171, 215, 251, 0.3);
}

.button-icon {
  font-size: 36rpx;
  margin-bottom: 8rpx;
}

.button-text {
  font-size: 22rpx;
  font-weight: 500;
  color: #333;
}

.action-buttons .action-button.primary .button-text {
  color: #F98C53;
  font-weight: 600;
}

.action-buttons .action-button.success .button-text {
  color: #6AB04C;
  font-weight: 600;
}

.action-buttons .action-button.info .button-text {
  color: #2B6CB0;
}

/* 弹窗通用样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 40rpx;
}

.modal-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 250, 240, 0.98));
  backdrop-filter: blur(30px);
  border-radius: 40rpx;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20rpx 80rpx rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
  border: 1rpx solid rgba(255, 255, 255, 0.3);
}

.modal-header {
  padding: 40rpx 40rpx 20rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1rpx solid rgba(0, 0, 0, 0.05);
}

.modal-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.modal-close {
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  color: #666;
  transition: all 0.3s ease;
}

.modal-close:active {
  background: rgba(0, 0, 0, 0.1);
}

.modal-body {
  flex: 1;
  padding: 0 40rpx;
  overflow-y: auto;
}

.modal-footer {
  padding: 30rpx 40rpx 40rpx;
}

/* 路径模板弹窗 */
.path-modal .modal-body {
  padding: 20rpx 40rpx;
}

.template-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  border: 1rpx solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
}

.template-card:active {
  transform: scale(0.98);
}

.template-card.recommended {
  background: linear-gradient(135deg, rgba(249, 140, 83, 0.1), rgba(255, 255, 255, 0.9));
  border: 1rpx solid rgba(249, 140, 83, 0.2);
  box-shadow: 0 8rpx 32rpx rgba(249, 140, 83, 0.15);
}

.template-icon {
  font-size: 60rpx;
  margin-right: 24rpx;
}

.template-info {
  flex: 1;
}

.template-title {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 8rpx;
}

.template-subtitle {
  display: block;
  font-size: 24rpx;
  color: #666;
  margin-bottom: 12rpx;
}

.template-meta {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.meta-item {
  font-size: 22rpx;
  color: #888;
}

.match-score {
  font-size: 22rpx;
  color: #F98C53;
  font-weight: 600;
  background: rgba(249, 140, 83, 0.1);
  padding: 4rpx 12rpx;
  border-radius: 16rpx;
  margin-left: auto;
}

.recommended-badge {
  position: absolute;
  top: -10rpx;
  right: 20rpx;
  background: linear-gradient(135deg, #F98C53, #FFB347);
  color: white;
  font-size: 20rpx;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  font-weight: 600;
}

/* 步骤详情弹窗 */
.step-modal {
  max-height: 85vh;
}

.step-status-tag {
  font-size: 26rpx;
  font-weight: 600;
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
}

.step-status-tag.completed {
  background: rgba(106, 176, 76, 0.1);
  color: #6AB04C;
}

.step-status-tag.in-progress {
  background: rgba(249, 140, 83, 0.1);
  color: #F98C53;
}

.step-status-tag.pending {
  background: rgba(200, 200, 200, 0.1);
  color: #999;
}

.step-detail-header {
  padding: 30rpx 0;
  border-bottom: 1rpx solid rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 20rpx;
}

.step-icon {
  font-size: 60rpx;
}

.step-title {
  flex: 1;
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  min-width: 300rpx;
}

.step-tag {
  font-size: 24rpx;
  color: #666;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}

.step-detail-content {
  padding: 30rpx 0;
}

.detail-section {
  margin-bottom: 40rpx;
}

.section-title {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
  margin-bottom: 16rpx;
}

.section-text {
  display: block;
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

.outcomes-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.outcome-item {
  display: flex;
  align-items: flex-start;
}

.outcome-icon {
  color: #6AB04C;
  font-size: 24rpx;
  margin-right: 12rpx;
  margin-top: 2rpx;
}

.outcome-text {
  flex: 1;
  font-size: 26rpx;
  color: #666;
  line-height: 1.5;
}

.progress-section {
  background: rgba(0, 0, 0, 0.02);
  border-radius: 20rpx;
  padding: 24rpx;
}

.progress-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.stat-value {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 4rpx;
}

.stat-label {
  font-size: 22rpx;
  color: #888;
}

.progress-controls {
  margin-top: 20rpx;
}

.progress-label {
  display: block;
  font-size: 26rpx;
  color: #666;
  margin-bottom: 20rpx;
}

.progress-slider-container {
  padding: 0 20rpx;
}

.resources-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.resource-item {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16rpx;
  padding: 20rpx;
  border: 1rpx solid rgba(0, 0, 0, 0.05);
}

.resource-icon {
  font-size: 36rpx;
  margin-right: 20rpx;
}

.resource-info {
  flex: 1;
}

.resource-title {
  display: block;
  font-size: 26rpx;
  font-weight: 500;
  color: #333;
  margin-bottom: 4rpx;
}

.resource-source {
  display: block;
  font-size: 22rpx;
  color: #888;
}

.resource-action {
  font-size: 24rpx;
  color: #F98C53;
  font-weight: 500;
  padding: 8rpx 20rpx;
  background: rgba(249, 140, 83, 0.1);
  border-radius: 16rpx;
}

.step-modal .action-buttons {
  display: flex;
  gap: 20rpx;
}

.step-modal .action-button {
  flex: 1;
  padding: 24rpx 0;
  border-radius: 24rpx;
  text-align: center;
  font-size: 28rpx;
  font-weight: 600;
}

.step-modal .action-button.in-progress {
  background: linear-gradient(135deg, #F98C53, #FFB347);
  color: white;
}

.step-modal .action-button.completed {
  background: rgba(210, 224, 170, 0.2);
  color: #6AB04C;
}

.step-modal .action-button.pending {
  background: rgba(249, 140, 83, 0.1);
  color: #F98C53;
}

.step-modal .action-button.secondary {
  background: rgba(0, 0, 0, 0.05);
  color: #666;
}

/* 庆祝动画 */
.celebration-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 40rpx;
}

.celebration-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 248, 240, 0.95));
  backdrop-filter: blur(30px);
  border-radius: 40rpx;
  padding: 60rpx 40rpx;
  width: 100%;
  max-width: 600rpx;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20rpx 80rpx rgba(249, 140, 83, 0.3);
  border: 2rpx solid rgba(249, 140, 83, 0.2);
}

.confetti-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.confetti-piece {
  position: absolute;
  width: 12rpx;
  height: 12rpx;
  border-radius: 2rpx;
  animation: confettiFall linear forwards;
}

@keyframes confettiFall {
  0% {
    transform: translateY(-100rpx) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(1000rpx) rotate(720deg);
    opacity: 0;
  }
}

.celebration-message {
  position: relative;
  z-index: 2;
}

.celebration-icon {
  display: block;
  font-size: 100rpx;
  margin-bottom: 20rpx;
  animation: celebrationBounce 1s ease-in-out infinite alternate;
}

@keyframes celebrationBounce {
  0% { transform: scale(1); }
  100% { transform: scale(1.1); }
}

.celebration-title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.celebration-text {
  display: block;
  font-size: 32rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.celebration-subtext {
  display: block;
  font-size: 28rpx;
  color: #F98C53;
  font-weight: 500;
  margin-bottom: 40rpx;
}

.celebration-actions {
  position: relative;
  z-index: 2;
}

.celebration-button {
  background: linear-gradient(135deg, #F98C53, #FFB347);
  border-radius: 40rpx;
  padding: 28rpx 0;
  text-align: center;
  box-shadow: 0 8rpx 32rpx rgba(249, 140, 83, 0.3);
}

.celebration-button .button-text {
  color: white;
  font-size: 32rpx;
  font-weight: 600;
}

/* 首次引导 */
.guide-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  padding: 40rpx;
}

.guide-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 248, 240, 0.95));
  backdrop-filter: blur(30px);
  border-radius: 40rpx;
  padding: 60rpx 40rpx;
  width: 100%;
  max-width: 600rpx;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20rpx 80rpx rgba(0, 0, 0, 0.3);
}

.guide-animation {
  position: relative;
  height: 200rpx;
  margin-bottom: 40rpx;
}

.seed-plant {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40rpx;
  height: 40rpx;
  background: #8B4513;
  border-radius: 50%;
  animation: seedPlant 2s ease-in-out forwards;
}

@keyframes seedPlant {
  0% { transform: translateX(-50%) scale(0); opacity: 0; }
  100% { transform: translateX(-50%) scale(1); opacity: 1; }
}

.seed-grow {
  position: absolute;
  bottom: 40rpx;
  left: 50%;
  transform: translateX(-50%);
  width: 4rpx;
  height: 0;
  background: #6AB04C;
  animation: seedGrow 2s ease-in-out 1s forwards;
}

@keyframes seedGrow {
  0% { height: 0; }
  100% { height: 120rpx; }
}

.seed-bloom {
  position: absolute;
  bottom: 160rpx;
  left: 50%;
  transform: translateX(-50%);
  font-size: 80rpx;
  opacity: 0;
  animation: seedBloom 1s ease-in-out 2s forwards;
}

@keyframes seedBloom {
  0% { opacity: 0; transform: translateX(-50%) scale(0.5); }
  100% { opacity: 1; transform: translateX(-50%) scale(1); }
}

.guide-message {
  margin-bottom: 40rpx;
}

.guide-title {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.guide-text {
  display: block;
  font-size: 28rpx;
  color: #666;
  margin-bottom: 10rpx;
  line-height: 1.5;
}

.guide-tip {
  display: block;
  font-size: 24rpx;
  color: #F98C53;
  font-style: italic;
}

.guide-button {
  background: linear-gradient(135deg, #F98C53, #FFB347);
  border-radius: 40rpx;
  padding: 28rpx 0;
  text-align: center;
  box-shadow: 0 8rpx 32rpx rgba(249, 140, 83, 0.3);
}

.guide-button .button-text {
  color: white;
  font-size: 32rpx;
  font-weight: 600;
}

/* 响应式调整 */
@media (max-width: 750rpx) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
  }
  
  .progress-capsule {
    flex-direction: column;
    gap: 20rpx;
  }
  
  .progress-item:not(:last-child) {
    border-right: none;
    border-bottom: 1rpx solid rgba(0, 0, 0, 0.05);
    padding-bottom: 20rpx;
  }
}
</style>