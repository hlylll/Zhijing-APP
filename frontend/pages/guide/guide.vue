<template>
  <div class="guide-container">
    <!-- 滑动容器 -->
    <div
      class="slides"
      ref="slides"
      @touchstart="onTouchStart"
      @touchmove="onTouchMove"
      @touchend="onTouchEnd"
    >
      <!-- 第一页 -->
      <div class="slide" :class="{ active: current === 0 }">
        <img
          src="/static/bg/guide-1.png"
          alt="引导页1"
          class="guide-img"
        />
      </div>

      <!-- 第二页 -->
      <div class="slide" :class="{ active: current === 1 }">
        <img
          src="/static/bg/guide-2.png"
          alt="引导页2"
          class="guide-img"
        />
      </div>

      <!-- 第三页 -->
      <div class="slide" :class="{ active: current === 2 }">
        <img
          src="/static/bg/guide-3.png"
          alt="引导页3"
          class="guide-img"
        />

        <!-- 进入按钮 - 只在第三页显示，右下角，小巧设计 -->
        <button v-if="current === 2" class="enter-btn" @click="enter">
          <span>开启我的成长之旅</span>
          <span class="arrow">→</span>
        </button>
      </div>
    </div>

    <!-- 指示器 -->
    <div class="indicators">
      <span
        class="dot"
        :class="{ active: current === 0 }"
        @click="goTo(0)"
      ></span>
      <span
        class="dot"
        :class="{ active: current === 1 }"
        @click="goTo(1)"
      ></span>
      <span
        class="dot"
        :class="{ active: current === 2 }"
        @click="goTo(2)"
      ></span>
    </div>

    <!-- 跳过按钮（前两页显示） -->
    <button v-if="current < 2" class="skip-btn" @click="enter">
      跳过
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' // 如果使用 vue-router

const router = useRouter() // 如果不用 router，可替换为 window.location

const current = ref(0)
const slides = ref(null)
let touchStartX = 0

const goTo = (index) => {
  if (index >= 0 && index < 3) {
    current.value = index
    if (slides.value) {
      slides.value.style.transform = `translateX(-${index * 100}vw)`
    }
  }
}

const onTouchStart = (e) => {
  touchStartX = e.touches[0].clientX
}

const onTouchMove = (e) => {
  // 记录移动，但不在这里判断（防止抖动）
}

const onTouchEnd = (e) => {
  if (!touchStartX) return
  const touchEndX = e.changedTouches[0].clientX
  const diff = touchStartX - touchEndX

  // 阈值 50px，更稳定
  if (diff > 50 && current.value < 2) {
    goTo(current.value + 1)
  } else if (diff < -50 && current.value > 0) {
    goTo(current.value - 1)
  }

  touchStartX = 0
}

// 在 <script setup> 中
const enter = () => {
  uni.setStorageSync('guide-shown', 'true')  // 推荐用 uni.setStorageSync 代替 localStorage，更兼容 Uni-app 多端
  uni.navigateTo({
    url: '/pages/login/login'  // Uni-app 页面路径（不带 .vue）
  })
  // 或用 uni.redirectTo({ url: '/pages/login/login' }) 如果不想保留引导页在历史栈中
}
</script>

<style scoped>
.guide-container {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  background: #0f0e17;
  overflow: hidden;
  z-index: 9999;
}

.slides {
  display: flex;
  width: 300vw;
  height: 100%;
  transition: transform 0.6s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.slide {
  width: 100vw;
  height: 100vh;
  flex-shrink: 0;
  position: relative;
}

.guide-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 指示器 */
.indicators {
  position: absolute;
  bottom: 40px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 12px;
  z-index: 10;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  transition: all 0.3s ease;
  cursor: pointer;
}

.dot.active {
  width: 24px;
  background: linear-gradient(90deg, #a78bfa, #f6ad55);
  box-shadow: 0 0 12px rgba(167, 139, 250, 0.6);
}

/* 跳过按钮 */
.skip-btn {
  position: absolute;
  top: 32px;
  right: 24px;
  padding: 8px 20px;
  font-size: 15px;
  color: gray;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid gray;
  border-radius: 999px;
  backdrop-filter: blur(8px);
  z-index: 10;
  transition: all 0.3s;
}

.skip-btn:hover {
  color: white;
  background: rgba(255, 255, 255, 0.25);
}

/* 进入按钮 - 右下角、小巧、文字+箭头 */
.enter-btn {
  position: absolute;
  bottom: 60px;
  right: 40px;
  padding: 10px 24px;
  font-size: 35px;
  font-weight: 600;
  font-family: "Times New Roman", "Songti SC", serif;
  color: #f4c127; /* 温暖的金黄色，与渐变呼应 */
  background: transparent;
  border: #df8e0c;
  border-radius: 999px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
}

.enter-btn:hover {
  color: white;
  transform: translateY(-3px);
}

.enter-btn .arrow {
  font-size: 18px;
  font-weight: 300;
  transition: transform 0.3s ease;
}

.enter-btn:hover .arrow {
  transform: translateX(5px);
}

/* 手机端微调 */
@media (max-width: 480px) {
  .enter-btn {
    bottom: 50px;
    right: 30px;
    padding: 8px 20px;
    font-size: 14px;
    gap: 6px;
  }

  .enter-btn .arrow {
    font-size: 16px;
  }

  .skip-btn {
    top: 24px;
    right: 20px;
    padding: 7px 18px;
    font-size: 14px;
  }

  .indicators {
    bottom: 36px;
  }
}
</style>