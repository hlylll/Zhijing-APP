<template>
  <view class="path-container">
    <!-- 调试按钮区域 - 开发时使用，发布时注释掉 -->
    <view class="debug-section" v-if="false">  <!-- 改为 false 隐藏调试按钮 -->
      <view class="debug-buttons">
        <button size="mini" type="default" @tap="debugCheckStorage">检查存储</button>
        <button size="mini" type="primary" @tap="setPlanType('job')">设为就业</button>
        <button size="mini" type="primary" @tap="setPlanType('postgraduate')">设为考研</button>
        <button size="mini" type="primary" @tap="setPlanType('civilservant')">设为考公</button>
      </view>
      <view class="debug-info">
        <text>当前规划: 
          <text style="font-weight: bold; color: #4A90E2;">
            {{ userInfo.planType === 'job' ? '就业' : 
               userInfo.planType === 'postgraduate' ? '考研' : 
               userInfo.planType === 'civilservant' ? '考公' : '未知' }}
          </text>
        </text>
        <text>目标: {{ userInfo.targetCareer || '未设置' }}</text>
      </view>
    </view>

    <!-- 顶部标题 -->
    <view class="header">
      <text class="title">🌱 我的成长之路 🌱</text>
      <view class="subtitle">每一步都通向更好的自己</view>
    </view>

    <!-- 核心信息大卡片 -->
    <view class="core-card">
      <!-- 欢迎语和用户画像 -->
      <view class="greeting-section">
        <view class="avatar-wrapper">
          <image src="/static/icons/grow.png" style="width: 85%; height: 85%;"></image>
        </view>
        <view class="greeting-text">
          <text class="hello">{{ greetingText }}，{{ userInfo.nickname || '小萌' }}！</text>
          <!-- 动态成长路径文案 -->
          <text class="path">
            <template v-if="userInfo.planType === 'job'">就业 → {{ userInfo.targetCareer || '未设置目标' }}</template>
            <template v-else-if="userInfo.planType === 'postgraduate'">考研 → {{ userInfo.targetCareer || '未设置目标专业' }}</template>
            <template v-else-if="userInfo.planType === 'civilservant'">考公 → {{ userInfo.targetCareer || '未设置目标岗位' }}</template>
            <template v-else>你的成长之路：{{ userInfo.major || '未知专业' }} → {{ userInfo.targetCareer || '未设置目标' }}</template>
          </text>
        </view>
      </view>

      <!-- 多模态情感感知卡片 -->
      <view class="emotion-card" v-if="todayMood">
        <view class="emotion-header">
          <text class="emotion-title">今日情感感知</text>
          <text class="emotion-emoji">{{ todayMood.emoji }}</text>
        </view>
        <view class="emotion-detail">
          <view class="emotion-item">
            <text class="label">文本情绪：</text>
            <text class="value">{{ todayMood.textEmotion }}</text>
          </view>
          <view class="emotion-item">
            <text class="label">行为特征：</text>
            <text class="value">{{ todayMood.behaviorText }}</text>
          </view>
        </view>
        <text class="emotion-text">{{ todayMood.suggestion }}</text>
      </view>
      <view class="emotion-card" v-else>
        <view class="emotion-header">
          <text class="emotion-title">今日情感感知</text>
          <text class="emotion-emoji">🌱</text>
        </view>
        <view class="emotion-detail">
          <text class="no-data">今天还没有记录情绪，去日记页面记录一下吧～</text>
        </view>
        <text class="emotion-text">记录情绪可以帮助我们更好地为你推荐合适的任务</text>
      </view>

      <!-- 进度三连击 -->
      <view class="progress-row">
        <view class="progress-item">
          <view class="icon-wrapper">
            <text class="icon">📍</text>
          </view>
          <text class="num">{{ completedTasksCount }}/{{ totalTasksCount }}</text>
          <text class="label">当前进度</text>
        </view>
        <view class="progress-item">
          <view class="icon-wrapper">
            <text class="icon">⏰</text>
          </view>
          <text class="num">{{ estimatedCompletion }}</text>
          <text class="label">预计达成</text>
        </view>
        <view class="progress-item">
          <view class="icon-wrapper">
            <text class="icon">🔥</text>
          </view>
          <text class="num">{{ streakDays }}天</text>
          <text class="label">连续成长</text>
        </view>
      </view>
    </view>

    <!-- 主推荐卡片 -->
    <view class="main-recommend-card">
      <view class="recommend-header">
        <text class="recommend-icon">✨</text>
        <text class="recommend-title">今日为你推荐</text>
        <view class="match-badge">{{ mainRecommendation.match }}% 匹配</view>
      </view>
      <view class="recommend-content">
        <view class="path-info">
          <text class="path-name">{{ mainRecommendation.name }}</text>
          <text class="path-desc">{{ mainRecommendation.desc }}</text>
          <view class="match-tags">
            <text 
              v-for="tag in mainRecommendation.matchTags" 
              :key="tag.text" 
              class="match-tag"
              :class="{ 'match-success': tag.matched }"
            >
              {{ tag.text }} {{ tag.matched ? '✅' : '❌' }}
            </text>
          </view>
          <view class="emotion-fit" v-if="todayMood">
            <text class="fit-icon">🌱</text>
            <text class="fit-text">{{ mainRecommendation.emotionFit }}</text>
          </view>
        </view>
        <view class="path-actions">
          <button class="action-btn" @tap="switchRecommendation">换一批</button>
          <button class="action-btn primary" @tap="viewPathDetail(mainRecommendation)">查看详情</button>
        </view>
      </view>
    </view>

    <!-- 备选路径 - 仅就业时显示 -->
    <view class="alternative-paths" v-if="userInfo.planType === 'job'">
      <view class="section-header">
        <text class="section-title">其他适合你的路径</text>
        <text class="section-more" @tap="viewAllPaths">查看全部 →</text>
      </view>
      <scroll-view scroll-x class="alt-scroll" show-scrollbar="false">
        <view class="alt-items">
          <view class="alt-item" v-for="path in alternativePaths" :key="path.id" @tap="selectPath(path)">
            <text class="alt-name">{{ path.name }}</text>
            <view class="alt-match">
              <text class="alt-match-value">{{ path.match }}%</text>
              <text class="alt-match-label">匹配</text>
            </view>
            <view class="alt-tags">
              <text class="alt-tag" v-for="tag in path.tags" :key="tag">{{ tag }}</text>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- Tab切换 -->
    <view class="tab-bar">
      <view class="tab-item" :class="{active: tabIndex === 0}" @tap="tabIndex = 0">
        <image class="tab-icon" src="/static/icons/time1.png" mode="widthFix" />
        <text class="tab-text">成长时间轴</text>
      </view>
      <view class="tab-item" :class="{active: tabIndex === 1}" @tap="tabIndex = 1">
        <image class="tab-icon" src="/static/icons/11.png" mode="widthFix" />
        <text class="tab-text">激励卡片</text>
      </view>
      <view class="tab-slider" :style="{transform: `translateX(${tabIndex * 100}%)`}"></view>
    </view>

    <!-- 成长时间轴 -->
    <view v-if="tabIndex === 0" class="timeline">
      <view class="timeline-header">
        <text class="timeline-title">当前阶段任务</text>
        <text class="timeline-subtitle">根据你的状态动态调整</text>
      </view>

      <!-- 情感提示条 -->
      <view class="mood-tip" v-if="todayMood">
        <text class="mood-tip-icon">💡</text>
        <text class="mood-tip-text">{{ todayMood.suggestion }}</text>
      </view>

      <!-- 任务列表 -->
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
          <view v-if="index < currentTasks.length - 1" class="line" :class="{ 
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
            <view class="step-type" :class="step.typeClass">{{ step.type }}</view>
          </view>
          <text class="step-desc">{{ step.desc }}</text>
          <view class="step-info">
            <view class="info-item">
              <text class="info-icon">⏳</text>
              <text class="info-text">{{ step.time }}</text>
            </view>
            <view class="info-item">
              <text class="info-icon">📊</text>
              <text class="info-text">{{ step.difficulty }}</text>
            </view>
          </view>
          <view class="mood-fit-tag" v-if="step.moodFit">
            <text class="fit-icon">🌱</text>
            <text class="fit-text">{{ step.moodFit }}</text>
          </view>
          <view v-if="step.current" class="current-indicator">
            <text class="sparkle">✨</text>
            <text class="current-text">进行中...</text>
          </view>
        </view>
      </view>

      <!-- 查看更多 -->
      <view class="more-btn" @tap="viewAllSteps">
        <text class="more-text">查看更多任务</text>
        <text class="more-arrow">→</text>
      </view>
    </view>

    <!-- 激励卡片 -->
    <view v-else class="incentive">
      <view class="incentive-card">
        <text class="incentive-title">💝 今日鼓励</text>
        <text class="incentive-text">{{ dailyEncouragement }}</text>
        <view class="incentive-stats">
          <view class="stat-item">
            <text class="stat-num">{{ streakDays }}</text>
            <text class="stat-label">连续成长</text>
          </view>
          <view class="stat-divider">|</view>
          <view class="stat-item">
            <text class="stat-num">{{ achievementsUnlocked }}</text>
            <text class="stat-label">成就解锁</text>
          </view>
          <view class="stat-divider">|</view>
          <view class="stat-item">
            <text class="stat-num">{{ nextMilestone }}</text>
            <text class="stat-label">下一个里程碑</text>
          </view>
        </view>
        <view class="incentive-nature">
          <text class="nature-element">🌿</text>
          <text class="nature-element">🌼</text>
          <text class="nature-element">🌱</text>
        </view>
      </view>
    </view>

    <!-- 悬浮加号菜单 -->
    <view class="float-menu">
      <view v-if="menuExpanded" class="menu-items">
        <view class="menu-item" @tap="openPathSelector">
          <view class="menu-item-icon">🔄</view>
          <text class="menu-item-text">路径</text>
        </view>
        <view class="menu-item" @tap="markComplete">
          <view class="menu-item-icon">✅</view>
          <text class="menu-item-text">完成</text>
        </view>
        <view class="menu-item" @tap="goToEditProfile">
          <view class="menu-item-icon">✏️</view>
          <text class="menu-item-text">画像</text>
        </view>
        <view class="menu-item" @tap="viewResources">
          <view class="menu-item-icon">📚</view>
          <text class="menu-item-text">资源</text>
        </view>
      </view>
      
      <view class="float-main-btn" @tap="toggleMenu">
        <text class="main-btn-icon" :class="{ rotated: menuExpanded }">＋</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onShow, onPullDownRefresh } from '@dcloudio/uni-app'

// ==================== 存储键名常量 ====================
const PATH_PROGRESS_KEY = 'user_path_progress'      // 存储当前路径完整数据（规划类型、目标、任务列表）
const TASKS_STORAGE_KEY = 'user_path_tasks'         // 存储简化任务进度，供我的页面同步

// ==================== 状态定义 ====================
const menuExpanded = ref(false)
const tabIndex = ref(0)

const userInfo = ref({
  nickname: '',
  major: '',
  grade: '',
  planType: 'job',
  targetCareer: '',
  bio: '',
  preferredCity: '',
  skills: [],
  avatar: ''
})

const userTags = ref([])
const todayMood = ref(null)
const currentTasks = ref([])
const streakDays = ref(0)
const achievementsUnlocked = ref(0)
const alternativePaths = ref([])

// ==================== 情绪映射 ====================
const moodMap = {
  1: { emoji: '☀️', name: '闪闪发光', textEmotion: '开心 80% · 能量 20%', behaviorText: '日间活跃度高', suggestion: '今天状态很好，可以挑战一些有难度的任务！' },
  2: { emoji: '🌱', name: '温暖生长', textEmotion: '平静 70% · 满足 30%', behaviorText: '节奏平稳', suggestion: '平和的心态最适合学习新知识～' },
  3: { emoji: '🍃', name: '微风思绪', textEmotion: '思考 50% · 专注 50%', behaviorText: '沉浸时间长', suggestion: '思绪清晰，适合做需要深度思考的任务' },
  4: { emoji: '🌧️', name: '雨滴心情', textEmotion: '焦虑 60% · 迷茫 30%', behaviorText: '深夜活跃度较高', suggestion: '今晚早点休息，明天精力会更充沛～' },
  5: { emoji: '✨', name: '马戏团日', textEmotion: '兴奋 70% · 期待 30%', behaviorText: '多任务切换', suggestion: '热情满满，可以尝试一些新领域！' },
  6: { emoji: '🫧', name: '拼图时刻', textEmotion: '困惑 50% · 探索 50%', behaviorText: '反复思考', suggestion: '困惑是成长的开始，慢慢来' }
}

// ==================== 问候语 ====================
const greetingText = computed(() => {
  const hour = new Date().getHours()
  if (hour < 6) return '凌晨好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  return '晚上好'
})

// ==================== 任务统计 ====================
const completedTasksCount = computed(() => currentTasks.value.filter(t => t.completed).length)
const totalTasksCount = computed(() => currentTasks.value.length)

// ==================== 预计达成时间 ====================
const estimatedCompletion = computed(() => {
  const remainingTasks = currentTasks.value.filter(t => !t.completed).length
  if (remainingTasks === 0) return '已完成'
  const totalMonths = currentTasks.value.reduce((sum, task) => sum + (parseInt(task.time) || 0), 0)
  const completedMonths = currentTasks.value.filter(t => t.completed).reduce((sum, task) => sum + (parseInt(task.time) || 0), 0)
  return `${totalMonths - completedMonths}个月后`
})

// ==================== 每日鼓励语 ====================
const dailyEncouragement = computed(() => {
  const encouragements = [
    '"每一小步都是通往梦想的一大步，今天的你已经很棒了！"',
    '"不要和别人比，要和昨天的自己比，你已经进步了！"',
    '"今天的努力，是明天的礼物，继续加油！"',
    '"成长的路上有起伏很正常，重要的是坚持走下去。"',
    '"你已经走了很远的路，不要轻易放弃。"'
  ]
  const dayOfYear = Math.floor(Date.now() / (1000 * 60 * 60 * 24))
  return encouragements[dayOfYear % encouragements.length]
})

// ==================== 下一个里程碑 ====================
const nextMilestone = computed(() => {
  const nextTask = currentTasks.value.find(t => !t.completed)
  return nextTask ? nextTask.title : '目标达成'
})

// ==================== 主推荐路径 ====================
const mainRecommendation = computed(() => {
  const planType = userInfo.value.planType || 'job'
  if (planType === 'job') {
    const basePath = {
      name: `${userInfo.value.major || '当前专业'} → ${userInfo.value.targetCareer || '目标职业'}`,
      desc: '',
      match: 85,
      matchTags: [],
      emotionFit: ''
    }
    if (userInfo.value.major?.includes('软件工程') || userInfo.value.major?.includes('计算机')) {
      basePath.desc = '适合有技术背景，想转型AI产品方向的同学'
      basePath.matchTags = [
        { text: `专业：${userInfo.value.major}`, matched: true },
        { text: '兴趣：AI', matched: userTags.value.includes('人工智能') },
        { text: '兴趣：产品', matched: userTags.value.includes('产品设计') }
      ]
    } else if (userInfo.value.major?.includes('金融') || userInfo.value.major?.includes('经济')) {
      basePath.desc = '金融背景转型数据分析，发挥你的专业优势'
      basePath.matchTags = [
        { text: `专业：${userInfo.value.major}`, matched: true },
        { text: '兴趣：数据分析', matched: userTags.value.includes('数据分析') },
        { text: '技能：Python', matched: userInfo.value.skills?.includes('Python') }
      ]
    } else {
      basePath.desc = '根据你的专业和兴趣定制的成长路径'
      basePath.matchTags = [
        { text: `专业：${userInfo.value.major || '未设置'}`, matched: !!userInfo.value.major },
        { text: '目标：' + (userInfo.value.targetCareer || '未设置'), matched: !!userInfo.value.targetCareer },
        { text: '兴趣标签', matched: userTags.value.length > 0 }
      ]
    }
    let matchPercentage = 85
    if (todayMood.value) {
      if (todayMood.value.emoji === '☀️' || todayMood.value.emoji === '✨') matchPercentage += 5
      else if (todayMood.value.emoji === '🌧️') matchPercentage -= 5
      basePath.emotionFit = todayMood.value.emoji === '🌧️' ? '根据你当前情绪，推荐从轻松的任务开始' : '根据你当前情绪，这个任务很适合你'
    }
    basePath.match = Math.min(100, matchPercentage)
    return basePath
  }
  if (planType === 'postgraduate') {
    return {
      name: '考研备考规划',
      desc: '根据你的目标专业和当前进度，为你定制每日学习计划',
      match: 90,
      matchTags: [
        { text: `目标专业：${userInfo.value.targetCareer || '未设置'}`, matched: !!userInfo.value.targetCareer },
        { text: '当前年级：' + (userInfo.value.grade || '未设置'), matched: !!userInfo.value.grade },
        { text: '备考时间：6个月', matched: true }
      ],
      emotionFit: todayMood.value ? '结合今日情绪，推荐从英语单词或政治背诵开始' : ''
    }
  }
  if (planType === 'civilservant') {
    return {
      name: '公务员备考计划',
      desc: '行测+申论系统学习，搭配历年真题训练',
      match: 88,
      matchTags: [
        { text: `目标岗位：${userInfo.value.targetCareer || '未设置'}`, matched: !!userInfo.value.targetCareer },
        { text: '当前阶段：基础学习', matched: true },
        { text: '备考时间：4个月', matched: true }
      ],
      emotionFit: todayMood.value ? '今日适合进行行测模块练习，保持专注' : ''
    }
  }
  return {
    name: '个性化成长路径',
    desc: '根据你的信息定制专属发展路线',
    match: 80,
    matchTags: [],
    emotionFit: ''
  }
})

// ==================== 生命周期 ====================
onShow(() => {
  loadUserData()
  loadMoodData()
})

onMounted(() => {
  loadUserData()
  loadMoodData()
})

onPullDownRefresh(() => {
  loadUserData()
  loadMoodData()
  setTimeout(() => uni.stopPullDownRefresh(), 500)
})

// ==================== 数据加载 ====================
const loadUserData = () => {
  try {
    const possibleKeys = ['userProfile', 'userInfo', 'currentUser', 'userData']
    let savedProfile = null
    for (const key of possibleKeys) {
      const data = uni.getStorageSync(key)
      if (data) {
        savedProfile = data
        break
      }
    }
    if (savedProfile) {
      userInfo.value = {
        id: savedProfile.id || '',
        open_id: savedProfile.open_id || '',
        phone: savedProfile.phone || '',
        nickname: savedProfile.nickname || savedProfile.username || '小萌',
        avatar: savedProfile.avatar || '',
        major: savedProfile.major || '',
        grade: savedProfile.grade || '',
        planType: savedProfile.plan_type || savedProfile.planType || 'job',
        targetCareer: savedProfile.target_career || savedProfile.targetCareer || '',
        bio: savedProfile.bio || '',
        preferredCity: savedProfile.preferred_city || savedProfile.preferredCity || '',
        skills: savedProfile.skills || [],
        is_first_edit: savedProfile.is_first_edit,
        created_at: savedProfile.created_at,
        updated_at: savedProfile.updated_at
      }
      if (savedProfile.interestTags || savedProfile.interest_tags) {
        convertTags(savedProfile.interestTags || savedProfile.interest_tags || [])
      }
      updateUIByPlanType(userInfo.value.planType)
    } else {
      userInfo.value = {
        nickname: '测试用户',
        major: '软件工程',
        grade: '大三',
        planType: 'postgraduate',
        targetCareer: '计算机科学与技术',
        bio: '',
        preferredCity: '',
        skills: [],
        avatar: ''
      }
      updateUIByPlanType(userInfo.value.planType)
    }
  } catch (error) {
    console.error('加载用户信息失败:', error)
    uni.showToast({ title: '加载用户信息失败', icon: 'none' })
  }
}

const loadMoodData = () => {
  try {
    const diaries = uni.getStorageSync('infog-mood-diaries')
    if (diaries) {
      const diaryList = JSON.parse(diaries)
      const today = new Date().toDateString()
      const todayDiary = diaryList.find(d => new Date(d.date).toDateString() === today)
      if (todayDiary) {
        const moodId = todayDiary.predicted_mood || todayDiary.manual_mood || 2
        const moodInfo = moodMap[moodId] || moodMap[2]
        todayMood.value = {
          emoji: moodInfo.emoji,
          textEmotion: moodInfo.textEmotion,
          behaviorText: moodInfo.behaviorText,
          suggestion: moodInfo.suggestion,
          moodId: moodId
        }
      } else {
        todayMood.value = null
      }
      calculateStreak(diaryList)
    } else {
      todayMood.value = null
    }

    // 优先恢复保存的进度（规划类型+目标匹配才恢复）
    const loaded = loadPathProgress()
    if (!loaded) {
      if (todayMood.value) generateTasksByMood(todayMood.value.moodId)
      else generateDefaultTasks()
      savePathProgress()
    }
    // 确保任务进度同步到 TASKS_STORAGE_KEY（供我的页面）
    saveTasksToStorage()
  } catch (error) {
    console.error('获取今日情绪失败:', error)
    generateDefaultTasks()
  }
}

// ==================== 工具函数 ====================
const convertTags = (interestTags) => {
  const tagMap = {
    1: '实习经验', 2: '科研项目', 3: '竞赛获奖', 4: '社团活动',
    5: '志愿服务', 6: '证书考取',
    101: '前端开发', 102: '后端开发', 103: '移动开发',
    104: '数据分析', 105: '人工智能', 106: '产品设计',
    107: '运营增长', 108: '测试开发', 109: '运维开发', 110: '网络安全',
    201: '考研数学', 202: '考研英语', 203: '考研政治', 204: '专业课',
    301: '行测', 302: '申论', 303: '面试', 304: '时政',
    401: '公共基础', 402: '职业能力', 403: '专业知识',
    501: '雅思', 502: '托福', 503: 'GRE', 504: 'GMAT'
  }
  userTags.value = interestTags.map(id => tagMap[id]).filter(tag => tag)
}

const calculateStreak = (diaries) => {
  if (!diaries || diaries.length === 0) {
    streakDays.value = 0
    return
  }
  const dates = diaries.map(d => new Date(d.date).toDateString()).sort((a, b) => new Date(b) - new Date(a))
  let streak = 1
  const today = new Date().toDateString()
  const startIndex = dates[0] === today ? 0 : 1
  for (let i = startIndex; i < dates.length - 1; i++) {
    const current = new Date(dates[i])
    const next = new Date(dates[i + 1])
    const diffDays = Math.round((current - next) / (1000 * 60 * 60 * 24))
    if (diffDays === 1) streak++
    else break
  }
  streakDays.value = streak
  achievementsUnlocked.value = Math.floor(streak / 7)
}

const updateUIByPlanType = (planType) => {
  if (planType === 'job') generateAlternativePaths()
  else alternativePaths.value = []
  if (todayMood.value) generateTasksByMood(todayMood.value.moodId)
  else generateDefaultTasks()
}

const generateAlternativePaths = () => {
  const paths = [
    { id: 2, name: '前端架构师', tags: ['计算机', '编程', '设计'], baseMatch: 75, condition: (user) => user.major?.includes('计算机') || user.skills?.includes('JavaScript') },
    { id: 3, name: '数据科学家', tags: ['数学', '统计', '机器学习'], baseMatch: 68, condition: (user) => user.major?.includes('数学') || user.skills?.includes('Python') },
    { id: 4, name: '全栈工程师', tags: ['前端', '后端', '数据库'], baseMatch: 70, condition: (user) => user.major?.includes('计算机') || user.skills?.length > 2 },
    { id: 5, name: '技术经理', tags: ['管理', '架构', '团队'], baseMatch: 62, condition: (user) => user.grade?.includes('研') || user.grade?.includes('毕业') }
  ]
  alternativePaths.value = paths.map(path => {
    let match = path.baseMatch
    if (path.condition(userInfo.value)) match += 10
    if (userInfo.value.targetCareer?.includes(path.name)) match += 15
    return { ...path, match: Math.min(100, match) }
  }).sort((a, b) => b.match - a.match)
}

const generateTasksByMood = (moodId) => {
  const planType = userInfo.value.planType || 'job'
  let baseTasks = []

  if (planType === 'job') {
    baseTasks = [
      { id: 1, title: userInfo.value.targetCareer ? `${userInfo.value.targetCareer}基础` : '目标职业基础', type: '技能', typeClass: 'skill', desc: '', time: '2个月', difficulty: '★★★', completed: false, current: true },
      { id: 2, title: '行业认知', type: '软技能', typeClass: 'soft', desc: '了解行业现状和发展趋势', time: '1个月', difficulty: '★★', completed: false, current: false },
      { id: 3, title: '实践项目', type: '技能', typeClass: 'skill', desc: '动手完成一个小型项目', time: '3个月', difficulty: '★★★★', completed: false, current: false }
    ]
    if (userInfo.value.targetCareer?.includes('产品')) {
      baseTasks[0].desc = '学习产品设计基础，掌握用户研究方法'
      baseTasks[1].desc = '分析优秀产品案例，理解产品思维'
      baseTasks[2].desc = '完成一个产品原型设计项目'
    } else if (userInfo.value.targetCareer?.includes('前端')) {
      baseTasks[0].desc = '掌握HTML/CSS/JavaScript基础'
      baseTasks[1].desc = '学习Vue/React框架'
      baseTasks[2].desc = '完成一个前端项目开发'
    } else if (userInfo.value.targetCareer?.includes('数据')) {
      baseTasks[0].desc = '学习Python和SQL基础'
      baseTasks[1].desc = '掌握数据分析工具'
      baseTasks[2].desc = '完成一个数据分析项目'
    } else {
      baseTasks[0].desc = '学习基础知识，建立知识体系'
      baseTasks[1].desc = '拓展行业视野'
      baseTasks[2].desc = '实践应用'
    }
  } else if (planType === 'postgraduate') {
    baseTasks = [
      { id: 1, title: '考研英语', type: '公共课', typeClass: 'soft', desc: '每日单词+阅读理解', time: '每天1.5h', difficulty: '★★★', completed: false, current: true },
      { id: 2, title: '考研政治', type: '公共课', typeClass: 'soft', desc: '马原+史纲基础', time: '每天1h', difficulty: '★★', completed: false, current: false },
      { id: 3, title: '专业课', type: '专业课', typeClass: 'skill', desc: userInfo.value.targetCareer ? `${userInfo.value.targetCareer}核心知识` : '专业课复习', time: '每天2h', difficulty: '★★★★', completed: false, current: false }
    ]
  } else if (planType === 'civilservant') {
    baseTasks = [
      { id: 1, title: '行测-言语理解', type: '行测', typeClass: 'soft', desc: '逻辑填空+片段阅读', time: '每天1h', difficulty: '★★★', completed: false, current: true },
      { id: 2, title: '行测-判断推理', type: '行测', typeClass: 'soft', desc: '图形推理+定义判断', time: '每天1h', difficulty: '★★★', completed: false, current: false },
      { id: 3, title: '申论', type: '申论', typeClass: 'skill', desc: '归纳概括+大作文', time: '每天1.5h', difficulty: '★★★★', completed: false, current: false }
    ]
  }

  switch(moodId) {
    case 1:
      baseTasks[0].desc += '，今天状态好可以挑战更难的内容'
      baseTasks[0].moodFit = '适合挑战性任务'
      break
    case 4:
      baseTasks[0].desc = '从轻松的内容开始，慢慢进入状态'
      baseTasks[0].moodFit = '适合轻松学习'
      baseTasks[1].current = true
      baseTasks[0].current = false
      break
    default:
      baseTasks[0].moodFit = '适合现在状态'
  }
  currentTasks.value = baseTasks
}

const generateDefaultTasks = () => {
  const planType = userInfo.value.planType || 'job'
  if (planType === 'postgraduate') {
    currentTasks.value = [{
      id: 1, title: '确定目标院校', type: '规划', typeClass: 'soft', desc: '先去编辑个人信息，设定你的考研目标', time: '10分钟', difficulty: '★', completed: false, current: true
    }]
  } else if (planType === 'civilservant') {
    currentTasks.value = [{
      id: 1, title: '了解考公流程', type: '规划', typeClass: 'soft', desc: '先去编辑个人信息，设定你的考公目标', time: '5分钟', difficulty: '★', completed: false, current: true
    }]
  } else {
    currentTasks.value = [{
      id: 1, title: '设定目标', type: '规划', typeClass: 'soft', desc: '先去编辑个人信息，设定你的目标吧', time: '5分钟', difficulty: '★', completed: false, current: true
    }]
  }
}

// ==================== 进度持久化（路径页内部） ====================
const savePathProgress = () => {
  const progressData = {
    planType: userInfo.value.planType,
    targetCareer: userInfo.value.targetCareer,
    tasks: currentTasks.value,
    savedAt: Date.now()
  }
  uni.setStorageSync(PATH_PROGRESS_KEY, JSON.stringify(progressData))
}

const loadPathProgress = () => {
  try {
    const saved = uni.getStorageSync(PATH_PROGRESS_KEY)
    if (saved) {
      const data = JSON.parse(saved)
      if (data.planType === userInfo.value.planType && data.targetCareer === userInfo.value.targetCareer) {
        currentTasks.value = data.tasks
        return true
      } else {
        uni.removeStorageSync(PATH_PROGRESS_KEY)
      }
    }
  } catch (e) {
    console.error('加载路径进度失败', e)
  }
  return false
}

// ==================== 同步任务进度到我的页面 ====================
const saveTasksToStorage = () => {
  const progressData = {
    tasks: currentTasks.value,
    totalSteps: totalTasksCount.value,
    completedSteps: completedTasksCount.value,
    progressPercent: (completedTasksCount.value / totalTasksCount.value) * 100 || 0,
    lastUpdate: Date.now()
  }
  uni.setStorageSync(TASKS_STORAGE_KEY, JSON.stringify(progressData))
  uni.setStorageSync('needRefreshMinePage', true)   // 通知我的页面刷新
}

// ==================== 菜单方法 ====================
const toggleMenu = () => { menuExpanded.value = !menuExpanded.value }

const switchRecommendation = () => {
  uni.showToast({ title: '换一批推荐', icon: 'none' })
  menuExpanded.value = false
}

const viewPathDetail = (path) => {
  uni.showToast({ title: `查看：${path.name}`, icon: 'none' })
  menuExpanded.value = false
}

const viewAllPaths = () => {
  uni.showToast({ title: '全部路径', icon: 'none' })
}

const selectPath = (path) => {
  uni.showToast({ title: `选择：${path.name}`, icon: 'none' })
}

const viewAllSteps = () => {
  uni.showToast({ title: '全部任务', icon: 'none' })
}

const openPathSelector = () => {
  uni.showToast({ title: '路径选择器', icon: 'none' })
  menuExpanded.value = false
}

// ==================== 完成任务 ====================
const markComplete = () => {
  const currentIndex = currentTasks.value.findIndex(task => task.current === true)
  if (currentIndex === -1) {
    uni.showToast({ title: '没有进行中的任务', icon: 'none' })
    menuExpanded.value = false
    return
  }

  const currentTask = currentTasks.value[currentIndex]
  currentTask.completed = true
  currentTask.current = false

  // 查找下一个未完成的任务
  const nextIndex = currentTasks.value.findIndex((task, idx) => idx > currentIndex && !task.completed)
  if (nextIndex !== -1) {
    currentTasks.value[nextIndex].current = true
    uni.showToast({
      title: `任务完成！下一任务：${currentTasks.value[nextIndex].title}`,
      icon: 'success'
    })
  } else {
    // 所有任务已完成，弹出对话框
    uni.showModal({
      title: '🎉 恭喜完成所有任务！',
      content: '你已经完成了当前阶段所有任务，是否重新开始？',
      confirmText: '重新开始',
      cancelText: '稍后再说',
      success: (res) => {
        if (res.confirm) {
          currentTasks.value.forEach(task => {
            task.completed = false
            task.current = false
          })
          currentTasks.value[0].current = true
          savePathProgress()
          saveTasksToStorage()
          uni.showToast({ title: '已重置，继续加油！', icon: 'success' })
        }
      }
    })
  }

  // 保存最新进度（路径页内部）
  savePathProgress()
  // 同步到我的页面
  saveTasksToStorage()
  menuExpanded.value = false
}

// ==================== 调试与跳转 ====================
const debugCheckStorage = () => {
  const keys = uni.getStorageInfoSync().keys
  console.log('所有存储key:', keys)
  keys.forEach(key => {
    console.log(`key: ${key}, value:`, uni.getStorageSync(key))
  })
  uni.showToast({ title: '请查看控制台日志', icon: 'none' })
}

const setPlanType = (type) => {
  userInfo.value.planType = type
  updateUIByPlanType(type)
  uni.showToast({ title: `已设为${type === 'job' ? '就业' : type === 'postgraduate' ? '考研' : '考公'}`, icon: 'success' })
}

const goToEditProfile = () => {
  uni.navigateTo({ url: '/pages/mine/edit' })
  menuExpanded.value = false
}

const viewResources = () => {
  uni.showToast({ title: '学习资源', icon: 'none' })
  menuExpanded.value = false
}
</script>

<style scoped>
/* 调试样式 */
.debug-section {
  background: #f5f5f5;
  padding: 20rpx;
  margin-bottom: 20rpx;
  border-radius: 16rpx;
  font-size: 24rpx;
}

.debug-buttons {
  display: flex;
  gap: 16rpx;
  margin-bottom: 16rpx;
  flex-wrap: wrap;
}

.debug-buttons button {
  font-size: 24rpx;
  padding: 8rpx 16rpx;
  line-height: 1.5;
}

.debug-info {
  display: flex;
  gap: 32rpx;
  color: #666;
}

/* 页面主要样式 - 保持不变 */
.path-container {
  padding: 32rpx 32rpx 60rpx;
  background: linear-gradient(135deg, #F0F8FF 0%, #E6F0FF 50%, #F0FFF4 100%);
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', sans-serif;
}

/* 头部 */
.header {
  padding: 40rpx 0 32rpx;
  text-align: center;
}

.title {
  font-size: 52rpx;
  font-weight: 700;
  background: linear-gradient(135deg, #4A90E2, #63B3ED);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-family: 'Brush Script MT', cursive;
  font-size: 28rpx;
  color: #7B8B9F;
  margin-top: 12rpx;
}

/* 核心卡片 */
.core-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 48rpx 40rpx;
  box-shadow: 0 20rpx 60rpx rgba(74, 144, 226, 0.1);
  margin-bottom: 48rpx;
  backdrop-filter: blur(20rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}

/* 欢迎区域 */
.greeting-section {
  display: flex;
  align-items: center;
  margin-bottom: 48rpx;
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

.greeting-text {
  flex: 1;
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
  display: block;
  margin-bottom: 12rpx;
}

/* 情感卡片 */
.emotion-card {
  background: linear-gradient(135deg, #E8F4FD, #F0FDF4);
  border-radius: 40rpx;
  padding: 32rpx;
  margin-bottom: 48rpx;
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
  font-size: 48rpx;
}

.emotion-detail {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 24rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
}

.emotion-item {
  display: flex;
  margin-bottom: 8rpx;
  font-size: 26rpx;
}

.emotion-item .label {
  color: #7B8B9F;
  width: 140rpx;
}

.emotion-item .value {
  color: #2D3748;
  flex: 1;
}

.emotion-text {
  font-size: 26rpx;
  color: #4A90E2;
  background: rgba(255, 255, 255, 0.4);
  padding: 16rpx 20rpx;
  border-radius: 24rpx;
  line-height: 1.5;
}

/* 进度三连击 */
.progress-row {
  display: flex;
  justify-content: space-between;
  gap: 20rpx;
}

.progress-item {
  flex: 1;
  text-align: center;
  background: rgba(240, 248, 255, 0.9);
  border-radius: 32rpx;
  padding: 32rpx 16rpx;
  border: 2rpx solid rgba(129, 212, 250, 0.3);
}

.icon-wrapper {
  margin-bottom: 16rpx;
}

.icon {
  font-size: 48rpx;
}

.num {
  font-size: 40rpx;
  font-weight: 700;
  color: #4A90E2;
  display: block;
  margin-bottom: 8rpx;
}

.label {
  font-size: 24rpx;
  color: #7B8B9F;
}

/* 主推荐卡片 */
.main-recommend-card {
  background: linear-gradient(135deg, #FFF9E6, #FFF3E0);
  border-radius: 48rpx;
  padding: 40rpx;
  margin-bottom: 48rpx;
  border: 2rpx solid rgba(255, 214, 102, 0.6);
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
  flex: 1;
}

.match-badge {
  background: #F6AD55;
  color: white;
  padding: 8rpx 24rpx;
  border-radius: 40rpx;
  font-size: 26rpx;
  font-weight: 600;
}

.recommend-content {
  display: flex;
  gap: 24rpx;
}

.path-info {
  flex: 1;
}

.path-name {
  font-size: 36rpx;
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

.match-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-bottom: 16rpx;
}

.match-tag {
  background: rgba(255, 214, 102, 0.2);
  padding: 6rpx 20rpx;
  border-radius: 30rpx;
  font-size: 24rpx;
  color: #D69E2E;
  border: 2rpx solid #FFD766;
}

.match-tag.match-success {
  background: rgba(104, 211, 145, 0.2);
  border-color: #68D391;
  color: #2F855A;
}

.emotion-fit {
  display: flex;
  align-items: center;
  gap: 12rpx;
  background: rgba(255, 255, 255, 0.6);
  padding: 16rpx 20rpx;
  border-radius: 40rpx;
}

.fit-icon {
  font-size: 32rpx;
}

.fit-text {
  font-size: 24rpx;
  color: #4A90E2;
  line-height: 1.4;
  flex: 1;
}

.path-actions {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  justify-content: center;
}

.action-btn {
  background: rgba(255, 255, 255, 0.9);
  border: 2rpx solid #FFD766;
  border-radius: 40rpx;
  padding: 16rpx 32rpx;
  font-size: 26rpx;
  color: #F6AD55;
  font-weight: 600;
  white-space: nowrap;
}

.action-btn.primary {
  background: linear-gradient(135deg, #FFD966, #FFB347);
  border: none;
  color: white;
}

/* 备选路径 */
.alternative-paths {
  margin-bottom: 48rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #4A90E2;
}

.section-more {
  font-size: 26rpx;
  color: #7B8B9F;
}

.alt-scroll {
  white-space: nowrap;
  overflow-x: auto;
  padding-bottom: 16rpx;
}

.alt-items {
  display: inline-flex;
  gap: 24rpx;
}

.alt-item {
  display: inline-block;
  width: 260rpx;
  background: white;
  border-radius: 32rpx;
  padding: 28rpx 20rpx;
  border: 2rpx solid rgba(129, 212, 250, 0.3);
}

.alt-name {
  font-size: 28rpx;
  font-weight: 700;
  color: #2D3748;
  display: block;
  margin-bottom: 12rpx;
  white-space: normal;
  word-break: break-word;
}

.alt-match {
  display: flex;
  align-items: baseline;
  gap: 8rpx;
  margin-bottom: 12rpx;
}

.alt-match-value {
  font-size: 36rpx;
  font-weight: 700;
  color: #F6AD55;
}

.alt-match-label {
  font-size: 22rpx;
  color: #7B8B9F;
}

.alt-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
}

.alt-tag {
  background: rgba(129, 212, 250, 0.1);
  padding: 4rpx 16rpx;
  border-radius: 30rpx;
  font-size: 20rpx;
  color: #4A90E2;
  border: 2rpx solid rgba(99, 179, 237, 0.2);
}

/* Tab栏 */
.tab-bar {
  display: flex;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50rpx;
  padding: 8rpx;
  margin-bottom: 48rpx;
  position: relative;
  border: 2rpx solid rgba(129, 212, 250, 0.2);
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 20rpx 0;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  border-radius: 42rpx;
  color: #7B8B9F;
}

.tab-item.active {
  color: #4A90E2;
  font-weight: 600;
}

.tab-icon {
  width: 60rpx;
  height: 45rpx;
  opacity: 0.6;
}

.tab-item.active .tab-icon {
  opacity: 1;
  transform: scale(1.1);
}

.tab-text {
  font-size: 26rpx;
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
}

/* 时间轴 */
.timeline {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 48rpx 40rpx;
  box-shadow: 0 20rpx 60rpx rgba(74, 144, 226, 0.1);
  margin-bottom: 48rpx;
}

.timeline-header {
  text-align: center;
  margin-bottom: 32rpx;
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

/* 情感提示条 */
.mood-tip {
  background: #FFF3E0;
  border-left: 8rpx solid #FFB347;
  padding: 24rpx;
  border-radius: 24rpx;
  margin-bottom: 32rpx;
  display: flex;
  align-items: flex-start;
  gap: 16rpx;
}

.mood-tip-icon {
  font-size: 40rpx;
}

.mood-tip-text {
  font-size: 26rpx;
  color: #2D3748;
  flex: 1;
  line-height: 1.5;
}

/* 步骤 */
.step {
  display: flex;
  margin-bottom: 48rpx;
}

.step-line {
  width: 80rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dot {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20rpx;
  z-index: 2;
}

.dot.completed {
  background: linear-gradient(135deg, #68D391, #38A169);
}

.dot.current {
  background: linear-gradient(135deg, #63B3ED, #4A90E2);
  animation: pulse 2s infinite;
}

.dot.pending {
  background: white;
  border: 4rpx solid #E8F4FD;
}

.dot-text {
  font-size: 32rpx;
  color: white;
}

.line {
  flex: 1;
  width: 6rpx;
  background: #E8F4FD;
  border-radius: 3rpx;
  margin: 8rpx 0;
}

.line.completed {
  background: #68D391;
}

/* 步骤卡片 */
.step-card {
  flex: 1;
  background: #F8FAFC;
  border-radius: 40rpx;
  padding: 32rpx;
  border: 2rpx solid #E8F4FD;
}

.step-card.current {
  background: #F0F8FF;
  border-color: #D4EDFA;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.step-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #2D3748;
}

.step-type {
  font-size: 22rpx;
  padding: 6rpx 20rpx;
  border-radius: 40rpx;
  font-weight: 600;
}

.step-type.skill {
  background: rgba(129, 212, 250, 0.3);
  color: #4A90E2;
}

.step-type.soft {
  background: rgba(251, 211, 141, 0.3);
  color: #D69E2E;
}

.step-desc {
  font-size: 26rpx;
  color: #718096;
  line-height: 1.5;
  margin-bottom: 20rpx;
}

.step-info {
  display: flex;
  gap: 32rpx;
  margin-bottom: 20rpx;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.info-icon {
  font-size: 26rpx;
  color: #7B8B9F;
}

.info-text {
  font-size: 24rpx;
  color: #7B8B9F;
}

/* 情感适配标签 */
.mood-fit-tag {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-bottom: 16rpx;
  padding: 8rpx 20rpx;
  background: rgba(129, 212, 250, 0.15);
  border-radius: 24rpx;
  width: fit-content;
}

.mood-fit-tag .fit-icon {
  font-size: 26rpx;
}

.mood-fit-tag .fit-text {
  font-size: 24rpx;
  color: #4A90E2;
}

.current-indicator {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 20rpx;
  background: rgba(99, 179, 237, 0.15);
  border-radius: 24rpx;
  width: fit-content;
}

.current-text {
  font-size: 24rpx;
  color: #4A90E2;
  font-weight: 600;
}

/* 查看更多 */
.more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  padding: 28rpx;
  background: #F8FAFC;
  border-radius: 40rpx;
  border: 2rpx dashed #D4EDFA;
  margin-top: 24rpx;
}

.more-text {
  font-size: 28rpx;
  color: #4A90E2;
  font-weight: 600;
}

.more-arrow {
  font-size: 32rpx;
  color: #4A90E2;
}

/* 激励卡片 */
.incentive {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 48rpx;
  padding: 48rpx 40rpx;
  margin-bottom: 48rpx;
}

.incentive-card {
  text-align: center;
  background: linear-gradient(135deg, #E8F4FD, #F0FDF4);
  border-radius: 40rpx;
  padding: 60rpx 40rpx;
  border: 2rpx solid rgba(129, 212, 250, 0.4);
}

.incentive-title {
  font-size: 40rpx;
  font-weight: 700;
  color: #4A90E2;
  display: block;
  margin-bottom: 32rpx;
}

.incentive-text {
  font-size: 32rpx;
  color: #2D3748;
  line-height: 1.5;
  margin-bottom: 48rpx;
  font-style: italic;
}

.incentive-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 32rpx;
  margin-bottom: 40rpx;
  padding: 32rpx;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 32rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.stat-num {
  font-size: 44rpx;
  font-weight: 700;
  color: #4A90E2;
}

.stat-label {
  font-size: 22rpx;
  color: #7B8B9F;
}

.stat-divider {
  font-size: 28rpx;
  color: #D4EDFA;
}

.incentive-nature {
  display: flex;
  justify-content: center;
  gap: 32rpx;
}

.incentive-nature .nature-element {
  font-size: 48rpx;
}

/* 悬浮加号菜单 */
.float-menu {
  position: fixed;
  right: 40rpx;
  bottom: 120rpx;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.menu-items {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 24rpx;
  margin-bottom: 24rpx;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20rpx);
  padding: 20rpx 32rpx 20rpx 24rpx;
  border-radius: 60rpx;
  box-shadow: 0 10rpx 30rpx rgba(74, 144, 226, 0.2);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
  animation: slideIn 0.2s ease;
}

.menu-item-icon {
  font-size: 40rpx;
  color: #4A90E2;
}

.menu-item-text {
  font-size: 28rpx;
  color: #2D3748;
  font-weight: 600;
}

.float-main-btn {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #4A90E2, #63B3ED);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 16rpx 40rpx rgba(74, 144, 226, 0.4);
  border: 4rpx solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.float-main-btn:active {
  transform: scale(0.95);
}

.main-btn-icon {
  font-size: 64rpx;
  color: white;
  font-weight: 300;
  transition: transform 0.3s ease;
}

.main-btn-icon.rotated {
  transform: rotate(45deg);
}

.no-data {
  font-size: 26rpx;
  color: #7B8B9F;
  padding: 20rpx 0;
  text-align: center;
  display: block;
}

/* 动画 */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20rpx);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(74, 144, 226, 0.4); }
  70% { box-shadow: 0 0 0 20rpx rgba(74, 144, 226, 0); }
  100% { box-shadow: 0 0 0 0 rgba(74, 144, 226, 0); }
}
</style>