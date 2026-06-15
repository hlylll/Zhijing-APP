<!-- App.vue -->
<script setup lang="ts">
import { onLaunch } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('App onLaunch 开始执行')

  // 1. 检查是否已经看过引导页
  const hasSeenOnboarding = uni.getStorageSync('hasSeenOnboarding')

  // 2. 延迟执行跳转（小程序启动时最稳定的做法，避免白屏/卡顿）
  setTimeout(() => {
    if (!hasSeenOnboarding) {
      // 没看过 → 强制跳转到引导页
      console.log('未看过引导页 → 跳转 guide')
      uni.reLaunch({
        url: '/pages/guide/guide'   // 改成你的实际路径，例如 /pages/onboarding/onboarding
      })
    } else {
      // 看过引导页 → 去登录页（或判断是否登录再去首页）
      const hasLogin = uni.getStorageSync('hasLogin')  // 可选：如果你有登录状态

      if (!hasLogin) {
        console.log('已看过引导，但未登录 → 去登录页')
        uni.reLaunch({
          url: '/pages/login/login'
        })
      } else {
        console.log('已看过引导，已登录 → 去首页')
        uni.reLaunch({
          url: '/pages/home/home'   // 或你的 tabBar 首页
        })
      }
    }
  }, 100)  // 延迟 100ms 更稳
})
</script>

<template>
  <view>
    <!-- App 根节点，通常留空或放全局 loading 遮罩 -->
  </view>
</template>

<style>
/* 可选：全局样式 */
page {
  background-color: #f5f5f5;
}
</style>