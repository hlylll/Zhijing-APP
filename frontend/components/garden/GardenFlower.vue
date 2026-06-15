<template>
  <div 
    class="garden-flower"
    :class="[type, size]"
    :style="{ 
      '--flower-color': flowerColor,
      '--flower-intensity': intensity
    }"
    @click="$emit('click')"
  >
    <div class="flower-emoji">{{ flowerEmoji }}</div>
    <div class="flower-petal" v-for="n in petalCount" :key="n"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: String,       // 花朵类型：sunflower/raindrop等
  intensity: Number,  // 情绪强度：0-1
  size: String        // 花朵大小：small/medium/large
})

const moodTypes = {
  sunflower: { emoji: '🌻', color: '#FFD93D' },
  cloud: { emoji: '☁️', color: '#6BCB77' },
  raindrop: { emoji: '🌧️', color: '#B5B9FF' },
  fire: { emoji: '🔥', color: '#FF6B6B' },
  moon: { emoji: '🌙', color: '#845EC2' }
}

const flowerEmoji = computed(() => moodTypes[props.type]?.emoji || '🌸')
const flowerColor = computed(() => moodTypes[props.type]?.color || '#FFD93D')

// 根据强度计算花瓣数量
const petalCount = computed(() => {
  if (props.intensity < 0.3) return 4
  if (props.intensity < 0.6) return 6
  return 8
})
</script>

<style scoped>
.garden-flower {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.garden-flower.small {
  width: 60rpx;
  height: 60rpx;
}

.garden-flower.medium {
  width: 80rpx;
  height: 80rpx;
}

.garden-flower.large {
  width: 100rpx;
  height: 100rpx;
}

.flower-emoji {
  font-size: inherit;
  position: relative;
  z-index: 2;
  filter: brightness(calc(0.8 + var(--flower-intensity, 0.5) * 0.4));
}

.flower-petal {
  position: absolute;
  width: calc(var(--flower-intensity, 0.5) * 20rpx + 10rpx);
  height: calc(var(--flower-intensity, 0.5) * 20rpx + 10rpx);
  background: var(--flower-color);
  border-radius: 50%;
  opacity: calc(0.3 + var(--flower-intensity, 0.5) * 0.7);
}

/* 花瓣位置 - 围绕中心 */
.flower-petal:nth-child(1) { transform: rotate(0deg) translateY(-30rpx); }
.flower-petal:nth-child(2) { transform: rotate(45deg) translateY(-30rpx); }
.flower-petal:nth-child(3) { transform: rotate(90deg) translateY(-30rpx); }
.flower-petal:nth-child(4) { transform: rotate(135deg) translateY(-30rpx); }
.flower-petal:nth-child(5) { transform: rotate(180deg) translateY(-30rpx); }
.flower-petal:nth-child(6) { transform: rotate(225deg) translateY(-30rpx); }
.flower-petal:nth-child(7) { transform: rotate(270deg) translateY(-30rpx); }
.flower-petal:nth-child(8) { transform: rotate(315deg) translateY(-30rpx); }

/* 花朵动画 */
@keyframes flowerBloom {
  from {
    transform: scale(0.5);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.garden-flower {
  animation: flowerBloom 0.6s ease-out;
}
</style>