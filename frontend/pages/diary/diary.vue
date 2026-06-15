
<template>
  <div class="diary-container">
    <!-- 动态背景 - 根据情绪变化 -->
    <div class="dynamic-bg" :class="currentMoodType">
      <div class="bg-element sun" v-if="currentMoodType === 'happy'">☀️</div>
      <div class="bg-element cloud" v-if="currentMoodType === 'peaceful'">☁️</div>
      <div class="bg-element star" v-if="currentMoodType === 'thoughtful'">✨</div>
      <div class="bg-element rain" v-if="currentMoodType === 'sad'">🌧️</div>
      <div class="bg-element sparkle" v-if="currentMoodType === 'excited'">⚡</div>
    </div>

    <!-- 顶部问候区 -->
    <div class="greeting-section">
      <div class="greeting-text">
        <h1>{{ timeGreeting }}，{{ userName }} 🌱</h1>
        <p class="greeting-sub">今天想和我聊聊吗？</p>
      </div>
      <div class="pet-avatar" @click="interactWithPet">
        <div class="pet" :class="petAnimation">
          <span class="pet-emoji">{{ petEmoji }}</span>
        </div>
      </div>
    </div>

    <!-- 情绪泡泡选择 -->
    <div class="mood-bubbles">
      <div class="section-title">
        <div class="sparkle">✨</div>
        <h2>今天是什么心情泡泡？</h2>
        <div class="sparkle">✨</div>
      </div>
      
      <div class="bubbles-container">
        <div 
          v-for="mood in moodBubbles" 
          :key="mood.id"
          class="mood-bubble"
          :class="{ selected: selectedMood === mood.id, [mood.type]: true }"
          @click="selectMood(mood.id)"
          @mouseenter="playBubbleSound"
        >
          <div class="bubble-emoji">{{ mood.emoji }}</div>
          <div class="bubble-text">{{ mood.text }}</div>
          <div class="bubble-glow"></div>
        </div>
      </div>
      
      <!-- 动态提示语 -->
      <div class="mood-hint" :class="selectedMoodType">
        <div class="hint-icon">💭</div>
        <div class="hint-text">{{ selectedMoodHint }}</div>
      </div>
    </div>

    <!-- 日记罐子 - 拟物化设计 -->
    <div class="diary-jar">
      <div class="jar-header">
        <div class="jar-title">
          <span class="jar-icon">🫙</span>
          <h3>情绪收纳罐</h3>
        </div>
        <div class="jar-stats">
          <span class="stat">已收纳 {{ diaryCount }} 个心情</span>
          <span class="stat">连续记录 {{ streakDays }} 天 🔥</span>
        </div>
      </div>
      
      <div class="jar-body" @click="focusTextarea">
        <div class="liquid" :class="currentMoodType" :style="{ height: textFillHeight }"></div>
        <textarea
          v-model="diaryText"
          class="jar-textarea"
          placeholder="把心里的话轻轻倒进来..."
          maxlength="300"
          @input="updateLiquidLevel"
 
          @blur="stopFloatingAnimation"
	      @click="onTextareaClick"
		  @keydown="onKeydown"
		  @focus="onFocus"
        ></textarea>
        
        <!-- 漂浮的小元素 -->
        <div class="floating-element" v-for="(element, index) in floatingElements" 
             :key="index" :style="element.style">
          {{ element.emoji }}
        </div>
      </div>
      
      <div class="jar-footer">
        <div class="word-count">
          <span class="count">{{ diaryText.length }}</span>
          <span class="total">/300</span>
        </div>
        <div class="writing-tip" v-if="diaryText.length > 0">
          {{ getWritingEncouragement() }}
        </div>
      </div>
    </div>

    <!-- 魔法按钮 -->
    <div class="magic-button-section">
      <button 
        class="magic-button" 
        :class="{ active: diaryText.length > 0, brewing: isAnalyzing }"
        @click="castAnalysisSpell"
        :disabled="isAnalyzing"
      >
        <div class="button-sparkles">
          <span class="sparkle" v-for="n in 3" :key="n">✨</span>
        </div>
        <div class="button-content">
          <span class="button-icon">{{ isAnalyzing ? '🔮' : '✨' }}</span>
          <span class="button-text">
            {{ isAnalyzing ? '魔法分析中...' : '施展情绪魔法' }}
          </span>
        </div>
        <div class="button-sparkles">
          <span class="sparkle" v-for="n in 3" :key="n">✨</span>
        </div>
      </button>
      
      <!-- 树洞选项 -->
      <div class="treehole-option" @click="toggleTreehole">
        <div class="treehole-icon">🕳️</div>
        <div class="treehole-content">
          <div class="treehole-title">放入树洞</div>
          <div class="treehole-desc">
            {{ isTreeholeActive ? '已开启匿名分享' : '点击开启，让温暖流淌' }}
          </div>
        </div>
        <div class="treehole-switch" :class="{ active: isTreeholeActive }">
          <div class="switch-dot"></div>
        </div>
      </div>
    </div>

    <!-- 情绪花园入口 -->
    <div class="garden-entrance" v-if="hasEntries" @click="navigateToGarden">
      <div class="garden-icon">🌸</div>
      <div class="garden-content">
        <div class="garden-title">你的情绪花园</div>
        <div class="garden-desc">看看心情花朵如何生长</div>
      </div>
      <div class="garden-arrow">→</div>
    </div>

    <!-- 魔法分析结果 - 卡片弹出 -->
    <transition name="magic-card">
      <div class="magic-result-card" v-if="showResult">
        <div class="card-close" @click="closeResult">×</div>
        
        <div class="result-header">
          <div class="result-emoji">{{ analysisResult.emoji }}</div>
          <div class="result-title">
            <h3>{{ analysisResult.title }}</h3>
            <p class="result-subtitle">{{ analysisResult.subtitle }}</p>
          </div>
        </div>
        
        <!-- 情绪花朵 -->
        <div class="mood-flower">
          <div class="flower-center" :style="{ 
            background: moodFlowerColor,
            transform: `scale(${analysisResult.intensity})`
          }"></div>
          <div class="flower-petal" v-for="n in 8" :key="n" :style="getPetalStyle(n)"></div>
        </div>
        
        <div class="result-insight">
          <div class="insight-text">{{ analysisResult.insight }}</div>
          <div class="insight-tags">
            <span class="tag" v-for="tag in analysisResult.tags" :key="tag">{{ tag }}</span>
          </div>
        </div>
        
        <!-- 魔法建议 -->
        <div class="magic-suggestion">
          <div class="suggestion-icon">🪄</div>
          <div class="suggestion-content">
            <div class="suggestion-title">今日小魔法</div>
            <div class="suggestion-text">{{ analysisResult.suggestion }}</div>
          </div>
        </div>
        
        <button class="result-action" @click="plantMoodFlower">
          <span class="action-icon">🌱</span>
          <span class="action-text">种下这朵心情</span>
        </button>
      </div>
    </transition>

    <!-- 宠物互动反馈 -->
    <div class="pet-feedback" v-if="showPetFeedback" @click="showPetFeedback = false">
      <div class="feedback-bubble">
        <div class="bubble-content">{{ petFeedback }}</div>
        <div class="bubble-tail"></div>
      </div>
    </div>

    <!-- 音效控制 -->
    <div class="sound-control" @click="toggleSound">
      <div class="sound-icon">{{ soundEnabled ? '🔊' : '🔇' }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// ==================== 原有状态 ====================
const userName = ref('旅人')
const streakDays = ref(7)
const diaryCount = ref(23)

// 时间问候语
const timeGreeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 5) return '深夜好'
  if (hour < 12) return '早晨好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  return '晚上好'
})

// 情绪泡泡
const moodBubbles = ref([
  { id: 1, emoji: '🌈', text: '闪闪发光', type: 'happy', hint: '像彩虹一样美好的一天！' },
  { id: 2, emoji: '🌻', text: '温暖生长', type: 'peaceful', hint: '像向日葵般静静生长～' },
  { id: 3, emoji: '🎐', text: '微风思绪', type: 'thoughtful', hint: '思绪如风铃般轻盈' },
  { id: 4, emoji: '☔', text: '雨滴心情', type: 'sad', hint: '没关系，雨滴也会唱歌' },
  { id: 5, emoji: '🎪', text: '马戏团日', type: 'excited', hint: '今天像马戏团一样精彩！' },
  { id: 6, emoji: '🧩', text: '拼图时刻', type: 'confused', hint: '慢慢拼凑，答案会出现' }
])

const selectedMood = ref(1)
const selectedMoodType = computed(() => {
  const mood = moodBubbles.value.find(m => m.id === selectedMood.value)
  return mood ? mood.type : 'peaceful'
})
const selectedMoodHint = computed(() => {
  const mood = moodBubbles.value.find(m => m.id === selectedMood.value)
  return mood ? mood.hint : ''
})

// 日记内容
const diaryText = ref('')
const textFillHeight = ref('0%')
const floatingElements = ref([])

// 交互状态
const isAnalyzing = ref(false)
const showResult = ref(false)
const isTreeholeActive = ref(false)
const hasEntries = ref(true)
const soundEnabled = ref(true)

// 宠物互动
const petAnimation = ref('idle')
const petEmoji = ref('🐇')
const showPetFeedback = ref(false)
const petFeedback = ref('')

// 分析结果
const analysisResult = ref({
  emoji: '🌸',
  title: '心情花朵',
  subtitle: '正在绽放中...',
  insight: '检测到温暖的思绪在发芽',
  tags: ['温暖', '成长', '期待'],
  suggestion: '对着窗外深呼吸三次，感受阳光的味道',
  intensity: 0.7,
  mood_id: null
})

// ==================== 新增行为记录状态 ====================
const startTime = ref(null)
const clickCount = ref(0)
const deleteCount = ref(0)
const dailyWriteCount = ref(0)

// ==================== 原有方法 ====================
const currentMoodType = computed(() => {
  if (selectedMood.value === 1) return 'happy'
  if (selectedMood.value === 2) return 'peaceful'
  if (selectedMood.value === 3) return 'thoughtful'
  if (selectedMood.value === 4) return 'sad'
  if (selectedMood.value === 5) return 'excited'
  return 'neutral'
})

const selectMood = (moodId) => {
  selectedMood.value = moodId
  if (soundEnabled.value) playSound('bubble')
  const reactions = {
    happy: '🎉 闪闪发光的日子！',
    peaceful: '🌿 感受到平静的能量',
    thoughtful: '💭 思考让心灵更丰富',
    sad: '☔ 我在这里陪伴你',
    excited: '🎪 哇，听起来很有趣！',
    confused: '🧩 慢慢来，我会陪着你'
  }
  const moodType = moodBubbles.value.find(m => m.id === moodId).type
  showPetMessage(reactions[moodType])
}

const playSound = (type) => {
  console.log('播放音效:', type)
}

const playBubbleSound = () => {
  if (soundEnabled.value) playSound('hover')
}

const updateLiquidLevel = () => {
  const length = diaryText.value.length
  const percentage = Math.min((length / 300) * 100, 100)
  textFillHeight.value = `${percentage}%`
  if (length > 0 && length % 50 === 0 && floatingElements.value.length < 6) {
    addFloatingElement()
  }
}

const addFloatingElement = () => {
  const emojis = ['💭', '✨', '⭐', '🌼', '💧', '🫧']
  const emoji = emojis[Math.floor(Math.random() * emojis.length)]
  floatingElements.value.push({
    emoji: emoji,
    style: {
      left: `${Math.random() * 80 + 10}%`,
      animationDelay: `${Math.random() * 2}s`
    }
  })
}

const startFloatingAnimation = () => {
  floatingElements.value.forEach((element, index) => {
    element.style.animation = `float 3s ease-in-out infinite`
    element.style.animationDelay = `${index * 0.3}s`
  })
}

const stopFloatingAnimation = () => {
  floatingElements.value.forEach(element => {
    element.style.animation = 'none'
  })
}

const focusTextarea = () => {
  document.querySelector('.jar-textarea')?.focus()
}

const getWritingEncouragement = () => {
  const length = diaryText.value.length
  if (length < 50) return '开始倾诉吧...'
  if (length < 100) return '很好，继续流淌...'
  if (length < 200) return '思绪在生长呢 🌱'
  if (length < 250) return '快要填满罐子了！'
  return '罐子快要溢出来了！'
}

const toggleTreehole = () => {
  isTreeholeActive.value = !isTreeholeActive.value
  playSound('toggle')
  showPetMessage(isTreeholeActive.value 
    ? '🎁 你的秘密会被温柔接住' 
    : '🔒 心事只留在我们之间')
}

const toggleSound = () => {
  soundEnabled.value = !soundEnabled.value
  playSound('toggle')
}

const interactWithPet = () => {
  const interactions = [
    '🧸 我一直在听哦',
    '🌙 今天辛苦啦',
    '🍃 深呼吸一下吧',
    '🎈 你做得很好',
    '🫂 给你一个抱抱'
  ]
  petAnimation.value = 'jump'
  setTimeout(() => petAnimation.value = 'idle', 1000)
  const message = interactions[Math.floor(Math.random() * interactions.length)]
  showPetMessage(message)
}

const showPetMessage = (message) => {
  petFeedback.value = message
  showPetFeedback.value = true
  setTimeout(() => {
    showPetFeedback.value = false
  }, 3000)
}

// ==================== 情绪分析相关 ====================
const castAnalysisSpell = async () => {
  if (!diaryText.value.trim()) {
    showPetMessage('📝 先写点什么吧～')
    return
  }
  
  isAnalyzing.value = true
  
  const duration = startTime.value ? Math.floor((Date.now() - startTime.value) / 1000) : 0
  const behavior = {
    duration: duration,
    click_count: clickCount.value,
    delete_count: deleteCount.value,
    selected_mood: selectedMood.value,
    treehole: isTreeholeActive.value ? 1 : 0,
    streak_days: streakDays.value,
    hour: new Date().getHours(),
    daily_count: dailyWriteCount.value
  }

  try {
    const response = await fetch('http://localhost:8000/api/analyze-mood', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: diaryText.value,
        behavior: behavior
      })
    })
    
    const result = await response.json()
    console.log('情绪分析结果:', result)
    
    if (result.success) {
      analysisResult.value = {
        emoji: result.emoji,
        title: result.title,
        subtitle: result.mood_name,
        insight: result.insight,
        tags: result.tags,
        suggestion: result.suggestion,
        intensity: 0.7,
        mood_id: result.mood_id
      }
      showResult.value = true
      if (soundEnabled.value) playSound('magic')
    } else {
      generateAnalysisResult()
      showResult.value = true
    }
  } catch (error) {
    console.error('API调用失败:', error)
    generateAnalysisResult()
    showResult.value = true
  } finally {
    isAnalyzing.value = false
  }
}

// 生成分析结果（备用）
const generateAnalysisResult = () => {
  const mood = moodBubbles.value.find(m => m.id === selectedMood.value)
  const results = {
    happy: {
      emoji: '🌻',
      title: '向日葵时刻',
      subtitle: '阳光在文字间跳跃',
      insight: '发现3个快乐小种子，继续浇灌它们吧',
      tags: ['阳光', '能量', '绽放'],
      suggestion: '对着镜子说一句"今天我也很棒"',
      intensity: 0.8,
      mood_id: 1
    },
    peaceful: {
      emoji: '🍃',
      title: '微风日记',
      subtitle: '平静中藏着力量',
      insight: '思绪如溪流般清澈，保持这份宁静',
      tags: ['平和', '清晰', '自然'],
      suggestion: '闭眼倾听周围3种声音',
      intensity: 0.6,
      mood_id: 2
    },
    thoughtful: {
      emoji: '💭',
      title: '思考云朵',
      subtitle: '云中有彩虹',
      insight: '深度思考让心灵更丰富，已在成长路径上',
      tags: ['思考', '成长', '探索'],
      suggestion: '用不同颜色标注今天的思绪',
      intensity: 0.7,
      mood_id: 3
    },
    sad: {
      emoji: '☁️',
      title: '雨过天晴',
      subtitle: '云层后有阳光',
      insight: '倾诉让心情减轻了30%，明天会更好',
      tags: ['释放', '勇气', '希望'],
      suggestion: '给自己泡一杯温暖的茶',
      intensity: 0.5,
      mood_id: 4
    }
  }
  const baseResult = results[mood.type] || results.peaceful
  analysisResult.value = baseResult
}

// ==================== 保存日记相关 ====================
const saveDiary = async () => {  // 注意这里加了 async
  console.log('======== 开始保存日记 ========')
  
  const currentText = diaryText.value
  console.log('1. 日记内容:', currentText)
  
  if (!currentText || currentText.trim() === '') {
    console.warn('⚠️ 日记内容为空，不保存')
    showPetMessage('⚠️ 日记内容不能为空')
    return
  }
  
  let userId = 'test_user'
  try {
    const userInfo = uni.getStorageSync('user')
    if (userInfo) {
      userId = userInfo.id || userInfo.phone || 'test_user'
    }
  } catch (e) {
    console.error('获取用户ID失败:', e)
  }
  
  const diaryData = {
    user_id: userId,
    date: new Date().toISOString(),
    diary_text: currentText,
    manual_mood: selectedMood.value,
    predicted_mood: analysisResult.value?.mood_id || null,
    is_treehole: isTreeholeActive.value ? 1 : 0,
    analysis_result: analysisResult.value,
    behavior_data: {
      duration: startTime.value ? Math.floor((Date.now() - startTime.value) / 1000) : 0,
      click_count: clickCount.value,
      delete_count: deleteCount.value,
      hour: new Date().getHours(),
      daily_count: dailyWriteCount.value
    }
  }
  
  console.log('2. 准备保存的数据:', diaryData)
  
  // 保存到本地（备份）
  try {
    const diaries = JSON.parse(localStorage.getItem('infog-mood-diaries') || '[]')
    diaries.push(diaryData)
    localStorage.setItem('infog-mood-diaries', JSON.stringify(diaries))
    console.log('3. 本地保存成功，当前总数:', diaries.length)
    
    diaryCount.value = diaries.length
    streakDays.value = calculateStreak(diaries)
    updateDailyCount()
  } catch (e) {
    console.error('本地保存失败:', e)
  }
  
  // 保存到数据库
  try {
    console.log('4. 开始保存到数据库...')
    
    const response = await fetch('http://localhost:8000/api/save-diary', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(diaryData)
    })
    
    const result = await response.json()
    console.log('5. 数据库返回结果:', result)
    
    if (result.success) {
      console.log('✅ 数据库保存成功，ID:', result.id)
      showPetMessage('花园里已经开出了一朵小花🌸')
    } else {
      console.error('❌ 数据库保存失败:', result.error)
      showPetMessage('⚠️ 云端保存失败，已存到本地')
    }
  } catch (error) {
    console.error('❌ 数据库保存异常:', error)
    showPetMessage('⚠️ 网络异常，已存到本地')
  }
  
  console.log('======== 保存完成 ========')
}

// 更新今日计数
const updateDailyCount = () => {
  try {
    const diaries = JSON.parse(localStorage.getItem('infog-mood-diaries') || '[]')
    const today = new Date().toDateString()
    dailyWriteCount.value = diaries.filter(d => {
      const dDate = new Date(d.date).toDateString()
      return dDate === today
    }).length
  } catch (e) {
    console.error('更新今日计数失败:', e)
  }
}

// 计算连续天数
const calculateStreak = (diaries) => {
  if (!diaries || diaries.length === 0) return 0
  
  const sorted = [...diaries].sort((a, b) => 
    new Date(b.date) - new Date(a.date)
  )
  
  let streak = 1
  const oneDay = 24 * 60 * 60 * 1000
  
  for (let i = 0; i < sorted.length - 1; i++) {
    const current = new Date(sorted[i].date).setHours(0, 0, 0, 0)
    const next = new Date(sorted[i + 1].date).setHours(0, 0, 0, 0)
    
    if (current - next === oneDay) {
      streak++
    } else {
      break
    }
  }
  
  return streak
}

// ==================== 行为记录方法 ====================
const resetBehaviorCounters = () => {
  startTime.value = Date.now()
  clickCount.value = 0
  deleteCount.value = 0
}

const onTextareaClick = () => {
  clickCount.value++
}

const onKeydown = (e) => {
  if (e.key === 'Backspace' || e.key === 'Delete') {
    deleteCount.value++
  }
}

const onFocus = () => {
  if (!startTime.value) {
    startTime.value = Date.now()
  }
}

// ==================== 结果卡片相关 ====================
const plantMoodFlower = () => {
  console.log('🌱 种下心情花朵')
  // 先保存日记
  saveDiary()
  // 再显示消息
  showPetMessage('🌱 心情已种入花园，明天来看它生长')
  // 延迟清空
  setTimeout(() => {
    closeResult()
  }, 500)
}

const closeResult = () => {
  console.log('清空结果卡片')
  showResult.value = false
  diaryText.value = ''
  textFillHeight.value = '0%'
  floatingElements.value = []
  // 重置计数器，准备下一次
  resetBehaviorCounters()
}

// ==================== 花瓣样式 ====================
const getPetalStyle = (index) => {
  const angle = (index / 8) * 360
  const size = 20 + Math.random() * 15
  return {
    transform: `rotate(${angle}deg) translateY(-60rpx)`,
    width: `${size}rpx`,
    height: `${size}rpx`,
    opacity: 0.7 + Math.random() * 0.3
  }
}

const moodFlowerColor = computed(() => {
  const colors = {
    happy: 'linear-gradient(45deg, #FFD93D, #FF6B6B)',
    peaceful: 'linear-gradient(45deg, #6BCB77, #4D96FF)',
    thoughtful: 'linear-gradient(45deg, #845EC2, #FF9671)',
    sad: 'linear-gradient(45deg, #B5B9FF, #FFC75F)',
    excited: 'linear-gradient(45deg, #FF8066, #FFD166)'
  }
  return colors[currentMoodType.value] || colors.peaceful
})

// ==================== 导航 ====================
const navigateToGarden = () => {
  uni.navigateTo({
    url: '/pages/diary/EmotionGarden/EmotionGarden'
  })
}

// ==================== 初始化 ====================
onMounted(() => {
  console.log('日记页面初始化')
  
  // 初始化宠物动画
  setInterval(() => {
    if (petAnimation.value === 'idle') {
      petAnimation.value = Math.random() > 0.5 ? 'blink' : 'wiggle'
      setTimeout(() => petAnimation.value = 'idle', 1000)
    }
  }, 5000)

  // 初始化计时器和今日计数
  resetBehaviorCounters()
  updateDailyCount()
})
</script>

<style scoped>
.diary-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #fef6e4 0%, #f3d2c1 100%);
  padding: 40rpx 32rpx 120rpx;
  position: relative;
  overflow-x: hidden;
}

/* 动态背景 */
.dynamic-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
  transition: all 1s ease;
}

.bg-element {
  position: absolute;
  font-size: 60rpx;
  opacity: 0.1;
  animation: float 20s infinite linear;
}

.sun { top: 10%; left: 10%; animation-delay: 0s; }
.cloud { top: 20%; right: 15%; animation-delay: 4s; animation-duration: 25s; }
.star { top: 60%; left: 15%; animation-delay: 8s; animation-duration: 30s; }
.rain { top: 40%; right: 20%; animation-delay: 12s; }
.sparkle { top: 70%; left: 70%; animation-delay: 16s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-40rpx) rotate(90deg); }
  50% { transform: translateY(0) rotate(180deg); }
  75% { transform: translateY(40rpx) rotate(270deg); }
}

/* 问候区 */
.greeting-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 60rpx;
  position: relative;
  z-index: 1;
}

.greeting-text h1 {
  font-size: 48rpx;
  font-weight: 800;
  color: #5c6b73;
  margin-bottom: 12rpx;
  font-family: 'ZCOOL XiaoWei', serif;
}

.greeting-sub {
  font-size: 30rpx;
  color: #8d9195;
  opacity: 0.9;
}

.pet-avatar {
  cursor: pointer;
}

.pet {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #ffd6e7, #c1f0ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12rpx 32rpx rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.pet-emoji {
  font-size: 60rpx;
}

.pet.idle { animation: idle 3s ease-in-out infinite; }
.pet.blink { animation: blink 1s ease; }
.pet.wiggle { animation: wiggle 0.5s ease; }
.pet.jump { animation: jump 1s ease; }

@keyframes idle {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10rpx); }
}

@keyframes blink {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes wiggle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

@keyframes jump {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-40rpx); }
}

/* 情绪泡泡 */
.mood-bubbles {
  position: relative;
  z-index: 1;
  margin-bottom: 60rpx;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20rpx;
  margin-bottom: 48rpx;
}

.section-title h2 {
  font-size: 38rpx;
  font-weight: 700;
  color: #5c6b73;
  text-align: center;
  font-family: 'ZCOOL XiaoWei', serif;
}

.sparkle {
  font-size: 32rpx;
  opacity: 0.8;
  animation: sparkle 2s infinite;
}

@keyframes sparkle {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

.bubbles-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24rpx;
}

.mood-bubble {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.mood-bubble:not(.selected) {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10rpx);
  border: 2rpx solid rgba(255, 255, 255, 0.9);
}

.mood-bubble:hover {
  transform: translateY(-8rpx) scale(1.05);
}

.bubble-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.mood-bubble.selected .bubble-glow {
  opacity: 1;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 20rpx currentColor; }
  50% { box-shadow: 0 0 40rpx currentColor; }
}

/* 泡泡类型颜色 */
.mood-bubble.happy.selected { 
  background: linear-gradient(135deg, #FFD93D, #FF6B6B);
  color: white;
}

.mood-bubble.peaceful.selected { 
  background: linear-gradient(135deg, #6BCB77, #4D96FF);
  color: white;
}

.mood-bubble.thoughtful.selected { 
  background: linear-gradient(135deg, #845EC2, #FF9671);
  color: white;
}

.mood-bubble.sad.selected { 
  background: linear-gradient(135deg, #B5B9FF, #FFC75F);
  color: white;
}

.mood-bubble.excited.selected { 
  background: linear-gradient(135deg, #FF8066, #FFD166);
  color: white;
}

.mood-bubble.confused.selected { 
  background: linear-gradient(135deg, #A8E6CF, #FFAAA5);
  color: white;
}

.bubble-emoji {
  font-size: 48rpx;
  margin-bottom: 12rpx;
  transition: transform 0.3s ease;
}

.mood-bubble.selected .bubble-emoji {
  transform: scale(1.2);
}

.bubble-text {
  font-size: 26rpx;
  font-weight: 600;
  opacity: 0.9;
}

/* 动态提示 */
.mood-hint {
  margin-top: 40rpx;
  padding: 28rpx 32rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  gap: 20rpx;
  animation: fadeIn 0.5s ease;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
}

.hint-icon {
  font-size: 40rpx;
  flex-shrink: 0;
}

.hint-text {
  font-size: 30rpx;
  color: #5c6b73;
  line-height: 1.5;
  flex: 1;
}

/* 日记罐子 */
.diary-jar {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20rpx);
  border-radius: 40rpx;
  padding: 40rpx 32rpx;
  margin-bottom: 48rpx;
  box-shadow: 
    0 20rpx 60rpx rgba(0, 0, 0, 0.1),
    inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
  position: relative;
  z-index: 1;
  border: 2rpx solid rgba(255, 255, 255, 0.6);
}

.jar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
}

.jar-title {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.jar-icon {
  font-size: 44rpx;
}

.jar-title h3 {
  font-size: 36rpx;
  font-weight: 700;
  color: #5c6b73;
  margin: 0;
}

.jar-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8rpx;
}

.stat {
  font-size: 24rpx;
  color: #8d9195;
  background: rgba(255, 255, 255, 0.6);
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}

.jar-body {
  height: 400rpx;
  border-radius: 32rpx;
  background: rgba(248, 249, 250, 0.6);
  position: relative;
  overflow: hidden;
  border: 2rpx dashed rgba(92, 107, 115, 0.2);
  cursor: text;
}

.liquid {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  transition: height 1s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 1;
}

.liquid.happy { background: linear-gradient(to top, rgba(255, 215, 61, 0.3), rgba(255, 107, 107, 0.5)); }
.liquid.peaceful { background: linear-gradient(to top, rgba(107, 203, 119, 0.3), rgba(77, 150, 255, 0.5)); }
.liquid.thoughtful { background: linear-gradient(to top, rgba(132, 94, 194, 0.3), rgba(255, 150, 113, 0.5)); }
.liquid.sad { background: linear-gradient(to top, rgba(181, 185, 255, 0.3), rgba(255, 199, 95, 0.5)); }
.liquid.excited { background: linear-gradient(to top, rgba(255, 128, 102, 0.3), rgba(255, 209, 102, 0.5)); }

.jar-textarea {
  position: relative;
  z-index: 2;
  width: 88%;
  height: 100%;
  padding: 40rpx;
  font-size: 32rpx;
  line-height: 1.6;
  color: #5c6b73;
  background: transparent;
  border: none;
  outline: none;
  resize: none;
  font-family: 'Ma Shan Zheng', cursive;
}

.jar-textarea::placeholder {
  color: rgba(92, 107, 115, 0.5);
  font-style: italic;
}

.floating-element {
  position: absolute;
  z-index: 3;
  font-size: 28rpx;
  pointer-events: none;
  animation: floatUp 4s ease-in-out infinite;
  opacity: 0.8;
}

@keyframes floatUp {
  0%, 100% { 
    transform: translateY(0) rotate(0deg);
    opacity: 0; 
  }
  10% { opacity: 0.8; }
  90% { opacity: 0.8; }
  100% { 
    transform: translateY(-300rpx) rotate(360deg);
    opacity: 0; 
  }
}

.jar-footer {
  margin-top: 32rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.word-count {
  font-size: 28rpx;
  color: #8d9195;
}

.count {
  font-weight: 600;
  color: #5c6b73;
}

.writing-tip {
  font-size: 26rpx;
  color: #6BCB77;
  font-style: italic;
  opacity: 0.9;
}

/* 魔法按钮 */
.magic-button-section {
  margin-bottom: 48rpx;
}

.magic-button {
  width: 100%;
  padding: 36rpx;
  background: linear-gradient(135deg, #845EC2, #FF6B95);
  color: white;
  border: none;
  border-radius: 60rpx;
  font-size: 34rpx;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  margin-bottom: 32rpx;
  box-shadow: 0 16rpx 48rpx rgba(132, 94, 194, 0.3);
}

.magic-button:hover:not(:disabled) {
  transform: translateY(-4rpx) scale(1.02);
  box-shadow: 0 24rpx 64rpx rgba(132, 94, 194, 0.4);
}

.magic-button.active:not(:disabled) {
  animation: glow 2s infinite;
}

@keyframes glow {
  0%, 100% { box-shadow: 0 16rpx 48rpx rgba(132, 94, 194, 0.3); }
  50% { box-shadow: 0 16rpx 48rpx rgba(132, 94, 194, 0.6); }
}

.magic-button.brewing {
  animation: brewing 1s infinite;
}

@keyframes brewing {
  0%, 100% { 
    background: linear-gradient(135deg, #845EC2, #FF6B95);
    transform: scale(1);
  }
  50% { 
    background: linear-gradient(135deg, #FF6B95, #845EC2);
    transform: scale(1.02);
  }
}

.magic-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-sparkles {
  position: absolute;
  top: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  opacity: 0.8;
}

.button-sparkles:first-child {
  left: 20rpx;
}

.button-sparkles:last-child {
  right: 20rpx;
}

.sparkle {
  font-size: 24rpx;
  animation: twinkle 1.5s infinite;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20rpx;
}

.button-icon {
  font-size: 40rpx;
}

/* 树洞选项 */
.treehole-option {
  display: flex;
  align-items: center;
  gap: 24rpx;
  padding: 28rpx 32rpx;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 28rpx;
  cursor: pointer;
  transition: all 0.3s ease;
}

.treehole-option:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2rpx);
}

.treehole-icon {
  font-size: 44rpx;
  flex-shrink: 0;
}

.treehole-content {
  flex: 1;
}

.treehole-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #5c6b73;
  margin-bottom: 4rpx;
}

.treehole-desc {
  font-size: 26rpx;
  color: #8d9195;
  opacity: 0.9;
}

.treehole-switch {
  width: 72rpx;
  height: 36rpx;
  background: #e0e0e0;
  border-radius: 18rpx;
  position: relative;
  transition: background-color 0.3s ease;
}

.treehole-switch.active {
  background: #6BCB77;
}

.switch-dot {
  position: absolute;
  top: 4rpx;
  left: 4rpx;
  width: 28rpx;
  height: 28rpx;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
}

.treehole-switch.active .switch-dot {
  transform: translateX(36rpx);
}

/* 花园入口 */
.garden-entrance {
  display: flex;
  align-items: center;
  gap: 24rpx;
  padding: 32rpx;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 248, 225, 0.9));
  border-radius: 32rpx;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 48rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.08);
  border: 2rpx solid rgba(255, 215, 61, 0.3);
}

.garden-entrance:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 12rpx 40rpx rgba(0, 0, 0, 0.12);
}

.garden-icon {
  font-size: 52rpx;
  flex-shrink: 0;
}

.garden-content {
  flex: 1;
}

.garden-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #5c6b73;
  margin-bottom: 4rpx;
}

.garden-desc {
  font-size: 28rpx;
  color: #8d9195;
  opacity: 0.9;
}

.garden-arrow {
  font-size: 36rpx;
  color: #FFD93D;
  font-weight: bold;
}

/* 魔法结果卡片 */
.magic-result-card {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 600rpx;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(40rpx);
  border-radius: 48rpx;
  padding: 60rpx 48rpx;
  z-index: 9999;
  box-shadow: 
    0 40rpx 120rpx rgba(0, 0, 0, 0.2),
    inset 0 1rpx 0 rgba(255, 255, 255, 0.8);
  animation: cardAppear 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 2rpx solid rgba(255, 255, 255, 0.6);
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.8);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}

.card-close {
  position: absolute;
  top: 32rpx;
  right: 32rpx;
  font-size: 44rpx;
  color: #8d9195;
  cursor: pointer;
  width: 60rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.card-close:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #5c6b73;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 28rpx;
  margin-bottom: 48rpx;
}

.result-emoji {
  font-size: 72rpx;
  flex-shrink: 0;
}

.result-title h3 {
  font-size: 42rpx;
  font-weight: 800;
  color: #5c6b73;
  margin-bottom: 8rpx;
  font-family: 'ZCOOL XiaoWei', serif;
}

.result-subtitle {
  font-size: 30rpx;
  color: #8d9195;
  opacity: 0.9;
}

/* 情绪花朵 */
.mood-flower {
  width: 200rpx;
  height: 200rpx;
  position: relative;
  margin: 0 auto 48rpx;
}

.flower-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  z-index: 1;
  transition: all 1s ease;
}

.flower-petal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: left center;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  border-radius: 40rpx;
  animation: petalBloom 2s ease-out;
}

@keyframes petalBloom {
  from {
    transform: rotate(0deg) translateY(0) scale(0);
    opacity: 0;
  }
  to {
    transform: rotate(var(--rotate)) translateY(-60rpx) scale(1);
    opacity: 0.8;
  }
}

.result-insight {
  background: rgba(248, 249, 250, 0.8);
  border-radius: 28rpx;
  padding: 32rpx;
  margin-bottom: 40rpx;
}

.insight-text {
  font-size: 30rpx;
  color: #5c6b73;
  line-height: 1.6;
  margin-bottom: 24rpx;
}

.insight-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.tag {
  padding: 8rpx 20rpx;
  background: rgba(255, 255, 255, 0.9);
  color: #845EC2;
  font-size: 24rpx;
  border-radius: 20rpx;
  border: 1rpx solid rgba(132, 94, 194, 0.3);
}

/* 魔法建议 */
.magic-suggestion {
  display: flex;
  align-items: flex-start;
  gap: 24rpx;
  background: linear-gradient(135deg, rgba(255, 248, 225, 0.9), rgba(255, 241, 242, 0.9));
  border-radius: 28rpx;
  padding: 32rpx;
  margin-bottom: 48rpx;
  border-left: 8rpx solid #FFD93D;
}

.suggestion-icon {
  font-size: 44rpx;
  flex-shrink: 0;
}

.suggestion-content {
  flex: 1;
}

.suggestion-title {
  font-size: 28rpx;
  font-weight: 700;
  color: #5c6b73;
  margin-bottom: 12rpx;
}

.suggestion-text {
  font-size: 28rpx;
  color: #5c6b73;
  line-height: 1.5;
  opacity: 0.9;
}

.result-action {
  width: 100%;
  padding: 32rpx;
  background: linear-gradient(135deg, #6BCB77, #4D96FF);
  color: white;
  border: none;
  border-radius: 50rpx;
  font-size: 34rpx;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20rpx;
  transition: all 0.3s ease;
}

.result-action:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 16rpx 48rpx rgba(107, 203, 119, 0.3);
}

/* 宠物反馈 */
.pet-feedback {
  position: fixed;
  bottom: 200rpx;
  right: 32rpx;
  z-index: 9998;
  animation: feedbackAppear 0.5s ease;
}

@keyframes feedbackAppear {
  from {
    opacity: 0;
    transform: translateY(40rpx) scale(0.8);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.feedback-bubble {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20rpx);
  border-radius: 28rpx 28rpx 4rpx 28rpx;
  padding: 24rpx 32rpx;
  box-shadow: 0 12rpx 40rpx rgba(0, 0, 0, 0.15);
  position: relative;
  max-width: 300rpx;
}

.bubble-content {
  font-size: 28rpx;
  color: #5c6b73;
  line-height: 1.4;
}

.bubble-tail {
  position: absolute;
  bottom: -8rpx;
  right: 0;
  width: 0;
  height: 0;
  border-left: 16rpx solid transparent;
  border-right: 16rpx solid transparent;
  border-top: 16rpx solid rgba(255, 255, 255, 0.98);
}

/* 音效控制 */
.sound-control {
  position: fixed;
  bottom: 40rpx;
  right: 32rpx;
  width: 80rpx;
  height: 80rpx;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s ease;
  margin-bottom: 70rpx;
}

.sound-control:hover {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.1);
}

.sound-icon {
  font-size: 36rpx;
}

/* 响应式设计 */
@media (max-width: 750rpx) {
  .bubbles-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .jar-body {
    height: 350rpx;
  }
  
  .magic-result-card {
    width: 95%;
    padding: 48rpx 32rpx;
  }
  
  .result-header {
    flex-direction: column;
    text-align: center;
    gap: 20rpx;
  }
}
</style>