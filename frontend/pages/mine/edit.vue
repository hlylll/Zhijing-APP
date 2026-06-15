<template>
  <div class="edit-container">
    <!-- 顶部导航栏 -->
    <div class="nav-bar">
      <div class="nav-left" @click="handleBack">
        <div class="back-icon">←</div>
        <div class="back-text">返回</div>
      </div>
      <div class="nav-title">编辑个人信息</div>
      <div class="nav-right" @click="handleSave" :class="{ disabled: !isFormValid }">
        <div class="save-text">保存</div>
      </div>
    </div>

    <!-- 首次编辑提示 -->
    <div class="guide-card" v-if="isFirstEdit">
      <div class="guide-icon">✨</div>
      <div class="guide-content">
        <div class="guide-title">完善信息，Infog为你匹配专属成长路径</div>
        <div class="guide-desc">只需要2分钟，开启你的个性化成长之旅</div>
      </div>
    </div>

    <div class="scroll-content">
      <!-- 个人信息大卡片 -->
      <div class="info-card">
        <!-- 头像上传区域 -->
        <div class="avatar-section">
          <div class="avatar-upload" @click="handleAvatarUpload">
            <div class="avatar-preview" :style="{ backgroundImage: `url(${formData.avatar})` }">
              <div class="avatar-placeholder" v-if="!formData.avatar">
                <div class="placeholder-icon">😊</div>
              </div>
              <div class="avatar-mask">
                <div class="camera-icon">📷</div>
                <div class="mask-text">更换头像</div>
              </div>
            </div>
            <div class="upload-loading" v-if="uploading">
              <div class="loading-spinner"></div>
            </div>
          </div>
          <div class="avatar-tip">点击上传头像</div>
        </div>

        <!-- 基本信息表单 -->
        <div class="form-section">
          <div class="form-item" :class="{ 'has-error': errors.nickname }">
            <div class="form-label">
              <span class="required">*</span>
              昵称
            </div>
            <input
              v-model="formData.nickname"
              type="text"
              placeholder="请输入昵称（2-10个字符）"
              class="form-input"
              maxlength="10"
              @blur="validateField('nickname')"
              @input="handleNicknameInput"
            />
            <div class="word-count">{{ formData.nickname.length }}/10</div>
            <div class="error-msg" v-if="errors.nickname">{{ errors.nickname }}</div>
          </div>

          <div class="form-item" :class="{ 'has-error': errors.major }">
            <div class="form-label">
              <span class="required">*</span>
              专业
            </div>
            <div class="select-wrapper" @click="showMajorPicker = true">
              <input
                v-model="formData.major"
                type="text"
                placeholder="请选择或输入你的专业"
                class="form-input"
                readonly
              />
              <div class="select-arrow">▼</div>
            </div>
            <div class="major-suggestions" v-if="showMajorSuggestions">
              <div
                class="suggestion-item"
                v-for="major in filteredMajorSuggestions"
                :key="major"
                @click="selectMajorSuggestion(major)"
              >
                {{ major }}
              </div>
            </div>
            <div class="error-msg" v-if="errors.major">{{ errors.major }}</div>
          </div>

          <div class="form-item" :class="{ 'has-error': errors.grade }">
            <div class="form-label">
              <span class="required">*</span>
              年级
            </div>
            <div class="select-wrapper" @click="showGradePicker = true">
              <input
                v-model="formData.grade"
                type="text"
                placeholder="请选择年级"
                class="form-input"
                readonly
              />
              <div class="select-arrow">▼</div>
            </div>
            <div class="error-msg" v-if="errors.grade">{{ errors.grade }}</div>
          </div>

          <!-- 目标规划类型选择器 -->
          <div class="form-item" :class="{ 'has-error': errors.planType }">
            <div class="form-label">
              <span class="required">*</span>
              目标规划
            </div>
            <div class="plan-type-selector">
              <div
                v-for="type in planTypes"
                :key="type.value"
                class="plan-type-item"
                :class="{ active: formData.planType === type.value }"
                @click="selectPlanType(type.value)"
              >
                <div class="type-icon">{{ type.icon }}</div>
                <div class="type-text">{{ type.label }}</div>
              </div>
            </div>
            <div class="error-msg" v-if="errors.planType">{{ errors.planType }}</div>
          </div>

          <!-- 根据规划类型动态显示目标输入框 -->
          <div class="form-item" :class="{ 'has-error': errors.targetCareer }">
            <div class="form-label">
              <span class="required">*</span>
              {{ targetFieldLabel }}
            </div>
            
            <!-- 就业方向 -->
            <template v-if="formData.planType === 'job'">
              <input
                v-model="formData.targetCareer"
                type="text"
                placeholder="例如：前端工程师 / 数据分析师 / 产品经理"
                class="form-input"
                @blur="validateField('targetCareer')"
              />
              <div class="career-suggestions">
                <div class="suggestion-label">热门选择：</div>
                <div class="suggestion-tags">
                  <span
                    v-for="career in jobSuggestions"
                    :key="career"
                    class="suggestion-tag"
                    @click="selectCareerSuggestion(career)"
                  >
                    {{ career }}
                  </span>
                </div>
              </div>
            </template>

            <!-- 考研方向 -->
            <template v-if="formData.planType === 'postgraduate'">
              <div class="select-wrapper" @click="showPostgraduatePicker = true">
                <input
                  v-model="formData.targetCareer"
                  type="text"
                  placeholder="请选择考研方向"
                  class="form-input"
                  readonly
                />
                <div class="select-arrow">▼</div>
              </div>
              <div class="career-suggestions">
                <div class="suggestion-label">热门方向：</div>
                <div class="suggestion-tags">
                  <span
                    v-for="direction in postgraduateSuggestions"
                    :key="direction"
                    class="suggestion-tag"
                    @click="selectCareerSuggestion(direction)"
                  >
                    {{ direction }}
                  </span>
                </div>
              </div>
            </template>

            <!-- 考公方向 -->
            <template v-if="formData.planType === 'civilservant'">
              <div class="select-wrapper" @click="showCivilServantPicker = true">
                <input
                  v-model="formData.targetCareer"
                  type="text"
                  placeholder="请选择考公方向"
                  class="form-input"
                  readonly
                />
                <div class="select-arrow">▼</div>
              </div>
              <div class="career-suggestions">
                <div class="suggestion-label">热门类别：</div>
                <div class="suggestion-tags">
                  <span
                    v-for="category in civilServantSuggestions"
                    :key="category"
                    class="suggestion-tag"
                    @click="selectCareerSuggestion(category)"
                  >
                    {{ category }}
                  </span>
                </div>
              </div>
            </template>

            <!-- 考编方向 -->
            <template v-if="formData.planType === 'publicinstitution'">
              <div class="select-wrapper" @click="showInstitutionPicker = true">
                <input
                  v-model="formData.targetCareer"
                  type="text"
                  placeholder="请选择考编方向"
                  class="form-input"
                  readonly
                />
                <div class="select-arrow">▼</div>
              </div>
              <div class="career-suggestions">
                <div class="suggestion-label">热门类别：</div>
                <div class="suggestion-tags">
                  <span
                    v-for="category in institutionSuggestions"
                    :key="category"
                    class="suggestion-tag"
                    @click="selectCareerSuggestion(category)"
                  >
                    {{ category }}
                  </span>
                </div>
              </div>
            </template>

            <!-- 出国留学方向 -->
            <template v-if="formData.planType === 'abroad'">
              <div class="select-wrapper" @click="showAbroadPicker = true">
                <input
                  v-model="formData.targetCareer"
                  type="text"
                  placeholder="请选择留学方向"
                  class="form-input"
                  readonly
                />
                <div class="select-arrow">▼</div>
              </div>
              <div class="career-suggestions">
                <div class="suggestion-label">热门方向：</div>
                <div class="suggestion-tags">
                  <span
                    v-for="direction in abroadSuggestions"
                    :key="direction"
                    class="suggestion-tag"
                    @click="selectCareerSuggestion(direction)"
                  >
                    {{ direction }}
                  </span>
                </div>
              </div>
            </template>

            <div class="error-msg" v-if="errors.targetCareer">{{ errors.targetCareer }}</div>
          </div>
        </div>
      </div>

      <!-- 兴趣标签区 -->
      <div class="interest-card">
        <div class="section-header">
          <div class="section-title">
            <div class="title-decoration"></div>
            <h3>兴趣标签</h3>
          </div>
          <div class="section-subtitle">
            选择你的兴趣方向（可多选）- 当前规划：{{ getPlanTypeName(formData.planType) }}
          </div>
        </div>
        
        <div class="tags-container">
          <div
            v-for="tag in currentTags"
            :key="tag.id"
            class="tag-item"
            :class="{ selected: selectedTags.includes(tag.id) }"
            @click="toggleTag(tag.id)"
          >
            <div class="tag-icon">{{ tag.icon }}</div>
            <div class="tag-text">{{ tag.text }}</div>
            <div class="tag-check" v-if="selectedTags.includes(tag.id)">✓</div>
          </div>
        </div>
        
        <div class="tags-tip">已选择 {{ selectedTags.length }} 个兴趣标签</div>
      </div>
      
      <!-- 其他可选信息 -->
      <div class="optional-card">
        <div class="section-header">
          <h3>其他信息（可选）</h3>
          <div class="section-subtitle">帮助我们更好地了解你</div>
        </div>
        
        <div class="form-item">
          <div class="form-label">个人简介</div>
          <textarea
            v-model="formData.bio"
            class="form-textarea"
            placeholder="简单介绍一下自己"
            maxlength="100"
          ></textarea>
          <div class="word-count">{{ formData.bio.length }}/100</div>
        </div>

        <div class="form-item">
          <div class="form-label">期望城市/地区</div>
          <input
            v-model="formData.preferredCity"
            type="text"
            placeholder="例如：北京、上海、杭州"
            class="form-input"
          />
        </div>

        <div class="form-item">
          <div class="form-label">技能/特长</div>
          <div class="skills-input">
            <input
              v-model="newSkill"
              type="text"
              placeholder="输入技能后按回车添加"
              class="form-input"
              @keyup.enter="addSkill"
            />
          </div>
          <div class="skills-tags">
            <div
              v-for="(skill, index) in formData.skills"
              :key="index"
              class="skill-tag"
            >
              {{ skill }}
              <span class="remove-skill" @click="removeSkill(index)">×</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部保存按钮 -->
    <div class="bottom-action">
      <button
        class="save-button"
        :class="{ saving: isSaving, disabled: !isFormValid }"
        @click="handleSave"
        :disabled="!isFormValid || isSaving"
      >
        <div class="button-content">
          <span class="button-icon" v-if="!isSaving">💾</span>
          <div class="loading-spinner" v-if="isSaving"></div>
          <span class="button-text">
            {{ isSaving ? '保存中...' : '保存并更新路径' }}
          </span>
        </div>
      </button>
      <div class="save-tip">保存后系统将重新为你匹配成长路径</div>
    </div>

    <!-- 年级选择器 -->
    <div class="picker-modal" v-if="showGradePicker">
      <div class="picker-overlay" @click="showGradePicker = false"></div>
      <div class="picker-content" @click.stop>
        <div class="picker-header">
          <div class="picker-cancel" @click="showGradePicker = false">取消</div>
          <div class="picker-title">选择年级</div>
          <div class="picker-confirm" @click="confirmGrade">确定</div>
        </div>
        <div class="picker-body">
          <div
            v-for="grade in gradeOptions"
            :key="grade"
            class="picker-item"
            :class="{ selected: tempGrade === grade }"
            @click="tempGrade = grade"
          >
            {{ grade }}
          </div>
        </div>
      </div>
    </div>
  
    <!-- 专业选择器 -->
    <div class="picker-modal" v-if="showMajorPicker">
      <div class="picker-overlay" @click="showMajorPicker = false"></div>
      <div class="picker-content" @click.stop>
        <div class="picker-header">
          <div class="picker-cancel" @click="showMajorPicker = false">取消</div>
          <div class="picker-title">选择专业</div>
          <div class="picker-confirm" @click="confirmMajor">确定</div>
        </div>
        <div class="picker-body">
          <div class="major-search">
            <input
              v-model="majorSearch"
              type="text"
              placeholder="搜索专业"
              class="search-input"
            />
          </div>
          <div class="picker-list">
            <div
              v-for="major in filteredMajorList"
              :key="major"
              class="picker-item"
              :class="{ selected: tempMajor === major }"
              @click="tempMajor = major"
            >
              {{ major }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 考研方向选择器 -->
    <div class="picker-modal" v-if="showPostgraduatePicker">
      <div class="picker-overlay" @click="showPostgraduatePicker = false"></div>
      <div class="picker-content" @click.stop>
        <div class="picker-header">
          <div class="picker-cancel" @click="showPostgraduatePicker = false">取消</div>
          <div class="picker-title">选择考研方向</div>
          <div class="picker-confirm" @click="confirmPostgraduate">确定</div>
        </div>
        <div class="picker-body">
          <div class="major-search">
            <input
              v-model="postgraduateSearch"
              type="text"
              placeholder="搜索考研方向"
              class="search-input"
            />
          </div>
          <div class="picker-list">
            <div
              v-for="direction in filteredPostgraduateList"
              :key="direction"
              class="picker-item"
              :class="{ selected: tempPostgraduate === direction }"
              @click="tempPostgraduate = direction"
            >
              {{ direction }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 考公方向选择器 -->
    <div class="picker-modal" v-if="showCivilServantPicker">
      <div class="picker-overlay" @click="showCivilServantPicker = false"></div>
      <div class="picker-content" @click.stop>
        <div class="picker-header">
          <div class="picker-cancel" @click="showCivilServantPicker = false">取消</div>
          <div class="picker-title">选择考公方向</div>
          <div class="picker-confirm" @click="confirmCivilServant">确定</div>
        </div>
        <div class="picker-body">
          <div
            v-for="category in civilServantOptions"
            :key="category"
            class="picker-item"
            :class="{ selected: tempCivilServant === category }"
            @click="tempCivilServant = category"
          >
            {{ category }}
          </div>
        </div>
      </div>
    </div>

    <!-- 考编方向选择器 -->
    <div class="picker-modal" v-if="showInstitutionPicker">
      <div class="picker-overlay" @click="showInstitutionPicker = false"></div>
      <div class="picker-content" @click.stop>
        <div class="picker-header">
          <div class="picker-cancel" @click="showInstitutionPicker = false">取消</div>
          <div class="picker-title">选择考编方向</div>
          <div class="picker-confirm" @click="confirmInstitution">确定</div>
        </div>
        <div class="picker-body">
          <div
            v-for="category in institutionOptions"
            :key="category"
            class="picker-item"
            :class="{ selected: tempInstitution === category }"
            @click="tempInstitution = category"
          >
            {{ category }}
          </div>
        </div>
      </div>
    </div>

    <!-- 留学方向选择器 -->
    <div class="picker-modal" v-if="showAbroadPicker">
      <div class="picker-overlay" @click="showAbroadPicker = false"></div>
      <div class="picker-content" @click.stop>
        <div class="picker-header">
          <div class="picker-cancel" @click="showAbroadPicker = false">取消</div>
          <div class="picker-title">选择留学方向</div>
          <div class="picker-confirm" @click="confirmAbroad">确定</div>
        </div>
        <div class="picker-body">
          <div class="major-search">
            <input
              v-model="abroadSearch"
              type="text"
              placeholder="搜索国家/地区"
              class="search-input"
            />
          </div>
          <div class="picker-list">
            <div
              v-for="direction in filteredAbroadList"
              :key="direction"
              class="picker-item"
              :class="{ selected: tempAbroad === direction }"
              @click="tempAbroad = direction"
            >
              {{ direction }}
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <!-- 成功弹窗 -->
    <div class="success-modal" v-if="showSuccessModal">
      <div class="modal-overlay" @click="closeSuccessModal"></div>
      <div class="modal-content" @click.stop>
        <div class="modal-icon">🎉</div>
        <div class="modal-title">个人信息已更新</div>
        <div class="modal-desc">正在为你重新匹配成长路径...</div>
        <div class="modal-progress">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
          </div>
          <div class="progress-text">{{ progress }}%</div>
        </div>
        <div class="modal-tip">请稍候，即将跳转到路径页面</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'

// ==================== 配置 ====================
const API_BASE_URL = 'http://127.0.0.1:8000'

// ==================== 工具函数 ====================
const getPlanTypeName = (type) => {
  const map = {
    job: '就业',
    postgraduate: '考研',
    civilservant: '考公',
    publicinstitution: '考编',
    abroad: '出国'
  }
  return map[type] || '就业'
}

// ==================== 表单数据 ====================
const formData = reactive({
  avatar: '',
  nickname: '',
  major: '',
  grade: '',
  planType: 'job',
  targetCareer: '',
  bio: '',
  preferredCity: '',
  skills: []
})

// 错误信息
const errors = reactive({
  nickname: '',
  major: '',
  grade: '',
  planType: '',
  targetCareer: ''
})

// 状态管理
const isFirstEdit = ref(true)
const uploading = ref(false)
const isSaving = ref(false)
const showSuccessModal = ref(false)
const progress = ref(0)

// ==================== 兴趣标签数据 ====================
const interestTags = ref({
  common: [
    { id: 1, text: '实习经验', icon: '💼' },
    { id: 2, text: '科研项目', icon: '🔬' },
    { id: 3, text: '竞赛获奖', icon: '🏆' },
    { id: 4, text: '社团活动', icon: '👥' },
    { id: 5, text: '志愿服务', icon: '❤️' },
    { id: 6, text: '证书考取', icon: '📜' }
  ],
  job: [
    { id: 101, text: '前端开发', icon: '💻' },
    { id: 102, text: '后端开发', icon: '⚙️' },
    { id: 103, text: '移动开发', icon: '📱' },
    { id: 104, text: '数据分析', icon: '📊' },
    { id: 105, text: '人工智能', icon: '🤖' },
    { id: 106, text: '产品设计', icon: '🎨' },
    { id: 107, text: '运营增长', icon: '📈' }
  ],
  postgraduate: [
    { id: 201, text: '考研数学', icon: '🧮' },
    { id: 202, text: '考研英语', icon: '📝' },
    { id: 203, text: '考研政治', icon: '📜' },
    { id: 204, text: '专业课', icon: '📚' },
    { id: 205, text: '考研规划', icon: '🎯' }
  ],
  civilservant: [
    { id: 301, text: '行测', icon: '📊' },
    { id: 302, text: '申论', icon: '📋' },
    { id: 303, text: '面试', icon: '🎤' },
    { id: 304, text: '时政', icon: '📰' },
    { id: 305, text: '常识判断', icon: '💡' }
  ],
  publicinstitution: [
    { id: 401, text: '公共基础', icon: '📚' },
    { id: 402, text: '职业能力', icon: '💪' },
    { id: 403, text: '专业知识', icon: '🎓' },
    { id: 404, text: '教育综合', icon: '👩‍🏫' },
    { id: 405, text: '医疗基础', icon: '🏥' }
  ],
  abroad: [
    { id: 501, text: '雅思', icon: '🇬🇧' },
    { id: 502, text: '托福', icon: '🇺🇸' },
    { id: 503, text: 'GRE', icon: '📊' },
    { id: 504, text: 'GMAT', icon: '💼' },
    { id: 505, text: '留学文书', icon: '📝' }
  ]
})

// 当前显示的标签
const currentTags = computed(() => {
  const tags = [...interestTags.value.common]
  
  switch (formData.planType) {
    case 'job': tags.push(...interestTags.value.job); break
    case 'postgraduate': tags.push(...interestTags.value.postgraduate); break
    case 'civilservant': tags.push(...interestTags.value.civilservant); break
    case 'publicinstitution': tags.push(...interestTags.value.publicinstitution); break
    case 'abroad': tags.push(...interestTags.value.abroad); break
    default: tags.push(...interestTags.value.job)
  }
  
  return tags
})

// 选择的标签
const selectedTags = ref([])

// ==================== 选项数据 ====================
const planTypes = ref([
  { value: 'job', label: '就业', icon: '💼' },
  { value: 'postgraduate', label: '考研', icon: '📚' },
  { value: 'civilservant', label: '考公', icon: '🏛️' },
  { value: 'publicinstitution', label: '考编', icon: '🏫' },
  { value: 'abroad', label: '出国', icon: '✈️' }
])

const gradeOptions = ref([
  '大一', '大二', '大三', '大四',
  '研一', '研二', '研三', '博士生', '已毕业'
])

const majorSuggestions = ref([
  '软件工程', '计算机科学与技术', '人工智能', '数据科学与大数据技术',
  '电子信息工程', '通信工程', '自动化', '电气工程及其自动化',
  '金融学', '经济学', '会计学', '工商管理',
  '临床医学', '药学', '法学', '新闻学'
])

const jobSuggestions = ref([
  '前端工程师', '后端工程师', '全栈工程师', '数据分析师',
  '产品经理', 'UI设计师', '运营专员', '测试工程师'
])

const postgraduateSuggestions = ref([
  '计算机科学与技术', '软件工程', '人工智能', '金融学',
  '法律硕士', '新闻传播', '临床医学', '机械工程'
])

const civilServantOptions = ref([
  '综合管理类', '专业技术类', '行政执法类',
  '中央国家机关', '省级机关', '市级机关',
  '公安系统', '法院系统', '税务系统'
])

const civilServantSuggestions = computed(() => civilServantOptions.value.slice(0, 6))

const institutionOptions = ref([
  '教师编制', '医疗编制', '科研院所', '文化事业单位',
  '高校行政', '中小学教师', '医生', '护士'
])

const institutionSuggestions = computed(() => institutionOptions.value.slice(0, 6))

const abroadOptions = ref([
  '美国', '英国', '加拿大', '澳大利亚', '新加坡',
  '中国香港', '德国', '法国', '日本'
])

const abroadSuggestions = computed(() => abroadOptions.value.slice(0, 6))

// ==================== 选择器状态 ====================
const showGradePicker = ref(false)
const showMajorPicker = ref(false)
const showPostgraduatePicker = ref(false)
const showCivilServantPicker = ref(false)
const showInstitutionPicker = ref(false)
const showAbroadPicker = ref(false)

const tempGrade = ref('')
const tempMajor = ref('')
const tempPostgraduate = ref('')
const tempCivilServant = ref('')
const tempInstitution = ref('')
const tempAbroad = ref('')

const majorSearch = ref('')
const postgraduateSearch = ref('')
const abroadSearch = ref('')
const newSkill = ref('')

// ==================== 计算属性 ====================
const targetFieldLabel = computed(() => {
  const map = {
    job: '目标职业',
    postgraduate: '考研方向',
    civilservant: '考公类别',
    publicinstitution: '考编类别',
    abroad: '留学方向'
  }
  return map[formData.planType] || '目标方向'
})

const filteredMajorSuggestions = computed(() => {
  if (!formData.major) return []
  return majorSuggestions.value.filter(major =>
    major.includes(formData.major)
  ).slice(0, 3)
})

const filteredMajorList = computed(() => {
  if (!majorSearch.value) return majorSuggestions.value
  return majorSuggestions.value.filter(major =>
    major.includes(majorSearch.value)
  )
})

const filteredPostgraduateList = computed(() => {
  if (!postgraduateSearch.value) return postgraduateSuggestions.value
  return postgraduateSuggestions.value.filter(d =>
    d.includes(postgraduateSearch.value)
  )
})

const filteredAbroadList = computed(() => {
  if (!abroadSearch.value) return abroadOptions.value
  return abroadOptions.value.filter(d =>
    d.includes(abroadSearch.value)
  )
})

const showMajorSuggestions = computed(() => {
  return formData.major && filteredMajorSuggestions.value.length > 0
})

const isFormValid = computed(() => {
  return formData.nickname?.trim() && 
         formData.major?.trim() && 
         formData.grade && 
         formData.planType &&
         formData.targetCareer?.trim()
})

// ==================== 监听器 ====================
watch(() => formData.planType, () => {
  formData.targetCareer = ''
})

// ==================== 生命周期 ====================
onMounted(() => {
  loadUserData()
})

// ==================== 数据加载 ====================
// 加载用户数据
const loadUserData = () => {
  uni.showLoading({ title: '加载中...' })
  
  // 先从服务器获取
  uni.request({
    url: API_BASE_URL + '/user/profile',
    method: 'POST',
    success: (res) => {
      console.log('===== 服务器返回原始数据 =====')
      console.log('状态码:', res.statusCode)
      console.log('完整响应:', res)
      console.log('响应数据:', res.data)
      
      if (res.data && res.data.code === 200 && res.data.data) {
        const userData = res.data.data
        console.log('解析后的用户数据:', userData)
        
        try {
          // 逐个字段赋值并打印
          formData.avatar = userData.avatar || ''
          console.log('avatar:', formData.avatar)
          
          formData.nickname = userData.nickname || ''
          console.log('nickname:', formData.nickname)
          
          formData.major = userData.major || ''
          console.log('major:', formData.major)
          
          formData.grade = userData.grade || ''
          console.log('grade:', formData.grade)
          
          formData.planType = userData.plan_type || 'job'
          console.log('planType:', formData.planType)
          
          formData.targetCareer = userData.target_career || ''
          console.log('targetCareer:', formData.targetCareer)
          
          formData.bio = userData.bio || ''
          console.log('bio:', formData.bio)
          
          formData.preferredCity = userData.preferred_city || ''
          console.log('preferredCity:', formData.preferredCity)
          
          // 确保 skills 是数组
          formData.skills = Array.isArray(userData.skills) ? userData.skills : 
                           (typeof userData.skills === 'string' ? userData.skills.split(',') : [])
          console.log('skills:', formData.skills)
          
          // 确保 interest_tags 是数组
          selectedTags.value = Array.isArray(userData.interest_tags) ? userData.interest_tags : []
          console.log('selectedTags:', selectedTags.value)
          
          isFirstEdit.value = userData.is_first_edit === true || !formData.nickname
          console.log('isFirstEdit:', isFirstEdit.value)
          
          // 保存到本地
          uni.setStorageSync('userProfile', {
            ...formData,
            interestTags: selectedTags.value
          })
          
          console.log('===== 数据加载完成 =====')
        } catch (e) {
          console.error('解析数据时出错:', e)
          loadFromLocal()
        }
      } else {
        console.log('服务器返回数据格式不正确:', res.data)
        loadFromLocal()
      }
    },
    fail: (err) => {
      console.error('获取服务器数据失败:', err)
      loadFromLocal()
    },
    complete: () => {
      uni.hideLoading()
    }
  })
}

// 添加一个从本地加载的函数
const loadFromLocal = () => {
  try {
    const localData = uni.getStorageSync('userProfile')
    if (localData) {
      console.log('从本地加载数据:', localData)
      Object.assign(formData, localData)
      selectedTags.value = localData.interestTags || []
    }
  } catch (e) {
    console.error('加载本地数据失败:', e)
  }
}
// ==================== 头像上传 ====================
// 在 edit.vue 的 handleAvatarUpload 函数中
const handleAvatarUpload = () => {
  uni.chooseImage({
    count: 1,
    success: (res) => {
      const tempFilePath = res.tempFilePaths[0]
      console.log('选择的头像临时路径:', tempFilePath)
      
      // 显示预览
      formData.avatar = tempFilePath
      
      // 这里应该上传到服务器
      uploadAvatar(tempFilePath)
    }
  })
}

// 上传头像到服务器
const uploadAvatar = (tempFilePath) => {
  uni.uploadFile({
    url: API_BASE_URL + '/user/avatar',  // 需要后端提供这个接口
    filePath: tempFilePath,
    name: 'avatar',
    success: (uploadRes) => {
      const data = JSON.parse(uploadRes.data)
      if (data.code === 200) {
        // 保存服务器返回的永久 URL
        formData.avatar = data.data.url
        uni.showToast({ title: '头像上传成功', icon: 'success' })
      }
    },
    fail: (err) => {
      console.error('上传失败:', err)
      // 如果上传失败，暂时使用临时路径
      uni.showToast({ 
        title: '头像上传失败，将使用本地临时头像', 
        icon: 'none' 
      })
    }
  })
}

// ==================== 表单验证 ====================
const validateField = (field) => {
  switch (field) {
    case 'nickname':
      if (!formData.nickname?.trim()) {
        errors.nickname = '昵称不能为空'
      } else if (formData.nickname.length < 2) {
        errors.nickname = '昵称至少2个字符'
      } else if (formData.nickname.length > 10) {
        errors.nickname = '昵称不能超过10个字符'
      } else {
        errors.nickname = ''
      }
      break
    case 'major':
      errors.major = formData.major?.trim() ? '' : '专业不能为空'
      break
    case 'grade':
      errors.grade = formData.grade ? '' : '请选择年级'
      break
    case 'planType':
      errors.planType = formData.planType ? '' : '请选择规划类型'
      break
    case 'targetCareer':
      errors.targetCareer = formData.targetCareer?.trim() ? '' : `${targetFieldLabel.value}不能为空`
      break
  }
}

const handleNicknameInput = () => {
  formData.nickname = formData.nickname.trim()
  validateField('nickname')
}

// ==================== 选项选择 ====================
const selectPlanType = (type) => {
  formData.planType = type
  validateField('planType')
}

const selectMajorSuggestion = (major) => {
  formData.major = major
  validateField('major')
}

const selectCareerSuggestion = (career) => {
  formData.targetCareer = career
  validateField('targetCareer')
}

// ==================== 兴趣标签 ====================
const toggleTag = (tagId) => {
  const index = selectedTags.value.indexOf(tagId)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tagId)
  }
}

// ==================== 技能标签 ====================
const addSkill = () => {
  if (newSkill.value?.trim() && !formData.skills.includes(newSkill.value.trim())) {
    formData.skills.push(newSkill.value.trim())
    newSkill.value = ''
  }
}

const removeSkill = (index) => {
  formData.skills.splice(index, 1)
}

// ==================== 选择器确认 ====================
const confirmGrade = () => {
  formData.grade = tempGrade.value
  showGradePicker.value = false
  validateField('grade')
}

const confirmMajor = () => {
  formData.major = tempMajor.value
  showMajorPicker.value = false
  validateField('major')
}

const confirmPostgraduate = () => {
  formData.targetCareer = tempPostgraduate.value
  showPostgraduatePicker.value = false
  validateField('targetCareer')
}

const confirmCivilServant = () => {
  formData.targetCareer = tempCivilServant.value
  showCivilServantPicker.value = false
  validateField('targetCareer')
}

const confirmInstitution = () => {
  formData.targetCareer = tempInstitution.value
  showInstitutionPicker.value = false
  validateField('targetCareer')
}

const confirmAbroad = () => {
  formData.targetCareer = tempAbroad.value
  showAbroadPicker.value = false
  validateField('targetCareer')
}

// ==================== 保存数据 ====================
// 在 edit.vue 中修改 handleSave 函数

const handleSave = () => {
  // 验证所有字段
  validateField('nickname')
  validateField('major')
  validateField('grade')
  validateField('planType')
  validateField('targetCareer')
  
  if (!isFormValid.value) {
    uni.showToast({ title: '请填写必填信息', icon: 'none' })
    return
  }
  
  isSaving.value = true
  
  // 准备数据
  const userData = {
    nickname: formData.nickname,
    major: formData.major,
    grade: formData.grade,
    plan_type: formData.planType,
    target_career: formData.targetCareer,
    bio: formData.bio || '',
    preferred_city: formData.preferredCity || '',
    skills: formData.skills.join(','),
    avatar: formData.avatar || '',
    interest_tags: selectedTags.value
  }
  
  console.log('准备发送的数据:', userData)
  
  // 发送到服务器
  uni.request({
    url: API_BASE_URL + '/user/profile',
    method: 'PUT',
    data: userData,
    header: {
      'Content-Type': 'application/json'
    },
    success: (res) => {
      console.log('服务器返回:', res)
      
      if (res.data && res.data.code === 200) {
        // 更新本地存储的用户信息
        const updatedUserInfo = {
          name: formData.nickname,
          avatar: formData.avatar,
          major: formData.major,
          grade: formData.grade,
          target: formData.targetCareer
        }
        uni.setStorageSync('userInfo', updatedUserInfo)
        
        // 🔴 设置刷新标志，告诉首页需要刷新
        uni.setStorageSync('needRefreshHomePage', true)
        
        // 显示成功提示
        uni.showToast({
          title: '保存成功',
          icon: 'success',
          duration: 1500,
          success: () => {
            // 延迟后跳转到首页
            setTimeout(() => {
              // 使用 switchTab 跳转到首页（因为首页通常是 tab 页）
              uni.switchTab({
                url: '/pages/home/home',
                success: () => {
                  console.log('跳转到首页成功')
                },
                fail: (err) => {
                  console.error('跳转到首页失败:', err)
                  // 如果 switchTab 失败，尝试用 reLaunch
                  uni.reLaunch({
                    url: '/pages/home/home'
                  })
                }
              })
            }, 1500)
          }
        })
      } else {
        uni.showToast({ 
          title: res.data?.message || '保存失败', 
          icon: 'none' 
        })
        isSaving.value = false
      }
    },
    fail: (err) => {
      console.error('请求失败:', err)
      uni.showToast({ 
        title: '网络错误，但已保存到本地', 
        icon: 'none' 
      })
      
      // 即使网络错误，也更新本地存储并跳转
      const updatedUserInfo = {
        name: formData.nickname,
        avatar: formData.avatar,
        major: formData.major,
        grade: formData.grade,
        target: formData.targetCareer
      }
      uni.setStorageSync('userInfo', updatedUserInfo)
      uni.setStorageSync('needRefreshHomePage', true)
      
      setTimeout(() => {
        uni.switchTab({
          url: '/pages/home/home'
        })
      }, 1500)
      
      isSaving.value = false
    }
  })
  // 保存成功后
  uni.setStorageSync('userProfile', userData)
  // 清除路径页面的缓存，强制重新加载
  uni.setStorageSync('needRefresh', true)  // 添加一个标记
}
// 修改 startProgressSimulation 函数
const startProgressSimulation = () => {
  progress.value = 0
  const interval = setInterval(() => {
    progress.value += 10
    if (progress.value >= 100) {
      clearInterval(interval)
      setTimeout(() => {
        // 返回上一页并刷新
        const pages = getCurrentPages()
        const prevPage = pages[pages.length - 2]
        
        // 如果上一页存在且有刷新方法
        if (prevPage && prevPage.$vm) {
          // 触发上一页的数据刷新
          prevPage.$vm.fetchUserInfo && prevPage.$vm.fetchUserInfo()
          prevPage.$vm.fetchRealMoodData && prevPage.$vm.fetchRealMoodData()
        }
        
        uni.navigateBack()
      }, 500)
    }
  }, 200)
}

// ==================== 导航 ====================
const handleBack = () => {
  uni.navigateBack()
}

const closeSuccessModal = () => {
  showSuccessModal.value = false
}
</script>

<style scoped>
/* 基础样式重置 */
body, html {
  overflow: hidden;
  height: 100%;
}

.edit-container {
  min-height: 100vh;
  background: #F8F9FA;
  position: relative;
  padding-bottom: 200rpx;
}

/* 导航栏 */
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 40rpx 32rpx 20rpx;
  background: white;
  box-shadow: 0 2rpx 20rpx rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 12rpx 16rpx;
  border-radius: 25rpx;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.nav-left:hover {
  background-color: #f5f5f5;
}

.back-icon {
  font-size: 36rpx;
  color: #333333;
}

.back-text {
  font-size: 32rpx;
  color: #666666;
}

.nav-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
}

.nav-right {
  padding: 12rpx 24rpx;
  background: linear-gradient(to right, #F98C53, #FFAA6B);
  color: white;
  font-size: 32rpx;
  font-weight: 600;
  border-radius: 25rpx;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-right:hover {
  opacity: 0.9;
  transform: translateY(-2rpx);
}

.nav-right.disabled {
  background: #CCCCCC;
  cursor: not-allowed;
}

.nav-right.disabled:hover {
  transform: none;
}

/* 引导卡片 */
.guide-card {
  margin: 32rpx;
  padding: 32rpx;
  background: linear-gradient(135deg, #FFF8F3, #FFE8D6);
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  gap: 24rpx;
  box-shadow: 0 8rpx 32rpx rgba(249, 140, 83, 0.15);
  border: 2rpx solid rgba(249, 140, 83, 0.1);
}

.guide-icon {
  font-size: 48rpx;
  flex-shrink: 0;
}

.guide-content {
  flex: 1;
}

.guide-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #F98C53;
  margin-bottom: 8rpx;
}

.guide-desc {
  font-size: 28rpx;
  color: #666666;
  opacity: 0.9;
}

.scroll-content {
  padding: 0 32rpx 180rpx;
  overflow-y: auto;
  max-height: calc(100vh - 200rpx);
}

/* 卡片通用样式 */
.info-card,
.interest-card,
.optional-card {
  background: white;
  border-radius: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.06);
  margin-bottom: 32rpx;
  overflow: hidden;
}

/* 头像区域 */
.avatar-section {
  padding: 60rpx 0 40rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-upload {
  position: relative;
  cursor: pointer;
  margin-bottom: 20rpx;
}

.avatar-preview {
  width: 200rpx;
  height: 200rpx;
  border-radius: 50%;
  background-color: #FFE8D6;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  border: 6rpx solid white;
  box-shadow: 0 12rpx 40rpx rgba(0, 0, 0, 0.1);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 80rpx;
  opacity: 0.8;
}

.avatar-mask {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  padding: 24rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-upload:hover .avatar-mask {
  opacity: 1;
}

.camera-icon {
  font-size: 32rpx;
  color: white;
}

.mask-text {
  font-size: 24rpx;
  color: white;
}

.upload-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  width: 48rpx;
  height: 48rpx;
  border: 4rpx solid #f3f3f3;
  border-top: 4rpx solid #F98C53;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.avatar-tip {
  font-size: 28rpx;
  color: #999999;
}

/* 表单区域 */
.form-section {
  padding: 0 40rpx 40rpx;
}

.form-item {
  margin-bottom: 48rpx;
  position: relative;
}

.form-item:last-child {
  margin-bottom: 0;
}

.form-label {
  font-size: 32rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
}

.required {
  color: #FF4D4F;
  margin-right: 8rpx;
}

.form-input {
  width: 100%;
  padding: 24rpx 0;
  font-size: 32rpx;
  color: #333333;
  border: none;
  border-bottom: 2rpx solid #E0E0E0;
  outline: none;
  background: transparent;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  border-bottom-color: #F98C53;
}

.form-input::placeholder {
  color: #999999;
}

.form-input:readonly {
  cursor: pointer;
  color: #333333;
}

.form-item.has-error .form-input {
  border-bottom-color: #FF4D4F;
}

.error-msg {
  font-size: 26rpx;
  color: #FF4D4F;
  margin-top: 12rpx;
}

.word-count {
  position: absolute;
  right: 0;
  bottom: -36rpx;
  font-size: 26rpx;
  color: #999999;
}

/* 规划类型选择器 */
.plan-type-selector {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16rpx;
  margin-top: 16rpx;
}

.plan-type-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24rpx 16rpx;
  background: #F5F5F5;
  border-radius: 20rpx;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2rpx solid transparent;
}

.plan-type-item:hover {
  transform: translateY(-2rpx);
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.plan-type-item.active {
  background: linear-gradient(135deg, #FFF8F3, #FFE8D6);
  border-color: #F98C53;
}

.type-icon {
  font-size: 40rpx;
  margin-bottom: 12rpx;
}

.type-text {
  font-size: 28rpx;
  color: #333333;
  font-weight: 500;
}

.plan-type-item.active .type-text {
  color: #F98C53;
  font-weight: 600;
}

/* 选择器包装 */
.select-wrapper {
  position: relative;
  cursor: pointer;
}

.select-arrow {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  color: #999999;
  font-size: 24rpx;
}

/* 专业建议 */
.major-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border-radius: 16rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.1);
  z-index: 100;
  overflow: hidden;
  margin-top: 4rpx;
}

.suggestion-item {
  padding: 24rpx 32rpx;
  font-size: 30rpx;
  color: #333333;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.suggestion-item:hover {
  background-color: #f8f9fa;
}

/* 职业建议 */
.career-suggestions {
  margin-top: 24rpx;
}

.suggestion-label {
  font-size: 28rpx;
  color: #666666;
  margin-bottom: 16rpx;
}

.suggestion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.suggestion-tag {
  padding: 12rpx 24rpx;
  background: #F5F5F5;
  color: #666666;
  font-size: 28rpx;
  border-radius: 20rpx;
  cursor: pointer;
  transition: all 0.3s ease;
}

.suggestion-tag:hover {
  background: #F0F0F0;
  transform: translateY(-2rpx);
}

/* 兴趣标签区 */
.interest-card {
  padding: 40rpx 32rpx;
}

.section-header {
  margin-bottom: 40rpx;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin-bottom: 12rpx;
}

.title-decoration {
  width: 6rpx;
  height: 36rpx;
  background: #F98C53;
  border-radius: 3rpx;
}

.section-title h3 {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
  margin: 0;
}

.section-subtitle {
  font-size: 28rpx;
  color: #666666;
  opacity: 0.9;
}

.tags-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24rpx;
  margin-bottom: 32rpx;
}

.tag-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32rpx 20rpx;
  background: #F8F9FA;
  border-radius: 24rpx;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  border: 2rpx solid transparent;
}

.tag-item:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.08);
}

.tag-item.selected {
  background: linear-gradient(135deg, #FFF8F3, #FFE8D6);
  border-color: #F98C53;
  transform: translateY(-4rpx);
  box-shadow: 0 8rpx 24rpx rgba(249, 140, 83, 0.15);
}

.tag-icon {
  font-size: 48rpx;
  margin-bottom: 16rpx;
}

.tag-text {
  font-size: 28rpx;
  color: #333333;
  font-weight: 500;
  text-align: center;
}

.tag-item.selected .tag-text {
  color: #F98C53;
  font-weight: 600;
}

.tag-check {
  position: absolute;
  top: 12rpx;
  right: 12rpx;
  width: 32rpx;
  height: 32rpx;
  background: #F98C53;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: bold;
}

.tags-tip {
  font-size: 28rpx;
  color: #F98C53;
  text-align: center;
  font-weight: 500;
  padding: 16rpx;
  background: rgba(249, 140, 83, 0.1);
  border-radius: 16rpx;
}

/* 其他可选信息 */
.optional-card {
  padding: 40rpx 32rpx;
}

.form-textarea {
  width: 100%;
  min-height: 200rpx;
  padding: 24rpx;
  font-size: 32rpx;
  color: #333333;
  border: 2rpx solid #E0E0E0;
  border-radius: 16rpx;
  outline: none;
  background: transparent;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.form-textarea:focus {
  border-color: #F98C53;
}

.form-textarea::placeholder {
  color: #999999;
}

.skills-input {
  margin-bottom: 20rpx;
}

.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.skill-tag {
  padding: 12rpx 24rpx;
  background: #E8F4FF;
  color: #1890FF;
  font-size: 28rpx;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.remove-skill {
  cursor: pointer;
  font-size: 32rpx;
  color: #1890FF;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.remove-skill:hover {
  opacity: 1;
}

/* 底部保存按钮 */
.bottom-action {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 32rpx;
  background: white;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.05);
  z-index: 1000;
}

.save-button {
  width: 100%;
  padding: 32rpx;
  background: linear-gradient(to right, #F98C53, #FFAA6B);
  color: white;
  font-size: 36rpx;
  font-weight: 700;
  border: none;
  border-radius: 50rpx;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
  position: relative;
  overflow: hidden;
}

.save-button:hover {
  opacity: 0.95;
  transform: translateY(-2rpx);
  box-shadow: 0 8rpx 32rpx rgba(249, 140, 83, 0.3);
}

.save-button:active {
  transform: translateY(0);
}

.save-button.saving {
  cursor: not-allowed;
  opacity: 0.8;
}

.save-button.disabled {
  background: #CCCCCC;
  cursor: not-allowed;
}

.save-button.disabled:hover {
  transform: none;
  box-shadow: none;
}

.button-content {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.button-icon {
  font-size: 40rpx;
}

.button-text {
  font-size: 34rpx;
  font-weight: 700;
}

.save-tip {
  text-align: center;
  font-size: 26rpx;
  color: #666666;
  margin-top: 20rpx;
  opacity: 0.8;
}

/* 选择器弹窗样式 */
.picker-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  display: flex;
  align-items: flex-end;
}

.picker-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.picker-content {
  position: relative;
  width: 100%;
  background: white;
  border-radius: 40rpx 40rpx 0 0;
  z-index: 10000;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx 40rpx;
  border-bottom: 2rpx solid #F5F5F5;
}

.picker-cancel,
.picker-confirm {
  font-size: 32rpx;
  color: #666666;
  cursor: pointer;
  padding: 12rpx 24rpx;
  border-radius: 20rpx;
  transition: background-color 0.3s ease;
}

.picker-cancel:hover,
.picker-confirm:hover {
  background-color: #f5f5f5;
}

.picker-confirm {
  color: #F98C53;
  font-weight: 600;
}

.picker-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
}

.picker-body {
  flex: 1;
  overflow-y: auto;
  padding: 32rpx 40rpx;
  max-height: 60vh;
}

.picker-item {
  padding: 32rpx 0;
  font-size: 34rpx;
  color: #333333;
  border-bottom: 2rpx solid #F5F5F5;
  cursor: pointer;
  transition: all 0.3s ease;
}

.picker-item:last-child {
  border-bottom: none;
}

.picker-item:hover {
  background-color: #f8f9fa;
  transform: translateX(4rpx);
}

.picker-item.selected {
  color: #F98C53;
  font-weight: 600;
}

/* 专业搜索框 */
.major-search {
  margin-bottom: 32rpx;
}

.search-input {
  width: 100%;
  padding: 24rpx 32rpx;
  font-size: 32rpx;
  color: #333333;
  border: 2rpx solid #E0E0E0;
  border-radius: 24rpx;
  outline: none;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #F98C53;
}

.search-input::placeholder {
  color: #999999;
}

.picker-list {
  max-height: 50vh;
  overflow-y: auto;
}

/* 成功弹窗样式 */
.success-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: relative;
  width: 80%;
  max-width: 600rpx;
  background: white;
  border-radius: 40rpx;
  padding: 60rpx 48rpx;
  text-align: center;
  z-index: 10000;
  box-shadow: 0 20rpx 80rpx rgba(0, 0, 0, 0.15);
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(40rpx) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-icon {
  font-size: 80rpx;
  margin-bottom: 32rpx;
}

.modal-title {
  font-size: 40rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 16rpx;
}

.modal-desc {
  font-size: 32rpx;
  color: #666666;
  margin-bottom: 48rpx;
}

.modal-progress {
  margin-bottom: 40rpx;
}

.progress-bar {
  width: 100%;
  height: 16rpx;
  background: #F0F0F0;
  border-radius: 8rpx;
  overflow: hidden;
  margin-bottom: 20rpx;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #F98C53, #FFAA6B);
  border-radius: 8rpx;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 28rpx;
  color: #F98C53;
  font-weight: 600;
}

.modal-tip {
  font-size: 28rpx;
  color: #999999;
  padding: 16rpx;
  background: #F8F9FA;
  border-radius: 20rpx;
}

/* 响应式调整 */
@media (max-width: 750rpx) {
  .picker-content {
    max-height: 70vh;
  }
  
  .picker-body {
    max-height: 50vh;
  }
  
  .picker-item {
    padding: 28rpx 0;
    font-size: 32rpx;
  }
  
  .modal-content {
    width: 85%;
    padding: 48rpx 40rpx;
  }
  
  .tags-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .plan-type-selector {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>