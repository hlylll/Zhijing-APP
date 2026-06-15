import App from './App'
import * as echarts from 'echarts'
// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
  ...App
})
app.$mount()
const routes = [
  { path: '/', component: Home },
  { path: '/login', component: LoginPage },  // ← 确保有这个路由
  // ...
]

// #endif

// #ifdef VUE3
import { createSSRApp } from 'vue'
export function createApp() {
  const app = createSSRApp(App)
  return {
    app
  }
}
// #endif