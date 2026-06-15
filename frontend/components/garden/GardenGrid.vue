<template>
	<div class="garden-grid">
	    <!-- 星期标题 -->
	    <div class="weekdays">
	      <div v-for="day in ['日', '一', '二', '三', '四', '五', '六']" :key="day">
	        {{ day }}
	      </div>
	    </div>
	
	    <!-- 日期网格 -->
	    <div class="calendar-grid">
	      <!-- 空白填充（上月） -->
	      <div 
	        v-for="n in startDay" 
	        :key="`empty-${n}`"
	        class="empty-day"
	      ></div>
	
	      <!-- 本月日期 -->
	      <div
	        v-for="day in monthDays"
	        :key="day.date"
	        class="calendar-day"
	        :class="{
	          'has-entry': day.hasEntry,
	          'today': day.isToday
	        }"
	        @click="handleDayClick(day)"
	      >
	        <!-- 花朵显示 -->
	        <GardenFlower
	          v-if="day.hasEntry"
	          :type="day.flowerType"
	          :intensity="day.intensity"
	          :size="flowerSize(day.diaryLength)"
	        />
	        
	        <!-- 日期数字 -->
	        <div class="day-number">{{ day.day }}</div>
	      </div>
	    </div>
	  </div>
</template>

<script setup>
import { computed } from 'vue'
import GardenFlower from './GardenFlower.vue'

const props = defineProps({
  days: Array
})

const emit = defineEmits(['flower-click'])

// 计算花朵大小（基于日记长度）
const flowerSize = (length) => {
  if (!length) return 'small'
  if (length < 100) return 'small'
  if (length < 300) return 'medium'
  return 'large'
}

// 处理日期点击
const handleDayClick = (day) => {
  if (day.hasEntry) {
    emit('flower-click', day)
  }
}
</script>

<style scoped>
.garden-grid {
  margin: 20rpx;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  margin-bottom: 16rpx;
  color: #666;
  font-size: 24rpx;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8rpx;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 16rpx;
  background: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.calendar-day.has-entry {
  background: rgba(255, 255, 255, 0.9);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}

.calendar-day.has-entry:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
}

.calendar-day.today {
  border: 2rpx solid #FFD93D;
}

.day-number {
  position: absolute;
  top: 8rpx;
  right: 8rpx;
  font-size: 24rpx;
  color: #666;
  font-weight: 500;
}
</style>