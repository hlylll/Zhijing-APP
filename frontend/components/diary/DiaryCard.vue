<template>
  <div class="diary-modal" @click="$emit('close')">
    <div class="modal-overlay"></div>
    <div class="modal-content" @click.stop>
      <!-- 关闭按钮 -->
      <div class="close-btn" @click="$emit('close')">×</div>
      
      <!-- 卡片内容 -->
      <div class="card-header">
        <div class="date">{{ formatDate(dayData.date) }}</div>
        <div class="mood-tag" :style="{ background: moodColor }">
          {{ moodName }}
        </div>
      </div>
      
      <div class="card-body">
        <!-- 情绪强度 -->
        <div class="mood-intensity">
          <div class="intensity-label">情绪强度</div>
          <div class="intensity-bar">
            <div 
              class="intensity-fill"
              :style="{ 
                width: `${dayData.intensity * 100}%`,
                background: moodColor 
              }"
            ></div>
          </div>
          <div class="intensity-value">{{ Math.round(dayData.intensity * 100) }}%</div>
        </div>
        
        <!-- 日记内容 -->
        <div class="diary-content">
          <div class="section-title">当日记录</div>
          <p class="diary-text">{{ dayData.diary }}</p>
        </div>
        
        <!-- 快速操作 -->
        <div class="card-actions">
          <button class="action-btn edit" @click="editDiary">
            <span>✏️</span>
            <span>编辑</span>
          </button>
          <button class="action-btn share" @click="shareDiary">
            <span>📤</span>
            <span>分享</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import dayjs from 'dayjs'

const props = defineProps({
  dayData: Object
})

const emit = defineEmits(['close', 'edit'])

// 获取情绪颜色
const moodColor = computed(() => {
  const colors = {
    happy: '#FFD93D',
    peaceful: '#6BCB77',
    sad: '#B5B9FF',
    excited: '#FF6B6B',
    thoughtful: '#845EC2'
  }
  return colors[props.dayData.mood] || '#666'
})

// 获取情绪名称
const moodName = computed(() => {
  const names = {
    happy: '开心',
    peaceful: '平静',
    sad: '难过',
    excited: '兴奋',
    thoughtful: '思考'
  }
  return names[props.dayData.mood] || '未知'
})

// 格式化日期
const formatDate = (dateStr) => {
  return dayjs(dateStr).format('YYYY年MM月DD日 dddd')
}

// 编辑日记
const editDiary = () => {
  emit('edit', props.dayData)
  emit('close')
}

// 分享日记
const shareDiary = () => {
  // 实现分享逻辑
  console.log('分享日记:', props.dayData)
}
</script>