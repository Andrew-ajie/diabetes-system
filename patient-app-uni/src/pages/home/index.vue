<template>
  <view class="container">
    <!-- 欢迎卡片 -->
    <view class="welcome-card">
      <view class="welcome-left">
        <text class="welcome-name">你好，{{ patient.name || '患者' }} 👋</text>
        <text class="welcome-sub">{{ today }} | {{ patient.diabetes_type || '糖尿病管理' }}</text>
      </view>
      <view class="avatar">{{ (patient.name || '?')[0] }}</view>
    </view>

    <!-- 最近血糖 -->
    <view class="card">
      <view class="section-title">📊 最近血糖</view>
      <view v-if="latestGlucose" class="stat-row">
        <view class="stat-item">
          <text class="stat-value" :style="glucoseColor(latestGlucose.value)">
            {{ latestGlucose.value }}
          </text>
          <text class="stat-label">mmol/L</text>
        </view>
        <view class="stat-item">
          <text class="stat-value-sm">{{ latestGlucose.meal_status_label }}</text>
          <text class="stat-label">餐况</text>
        </view>
        <view class="stat-item">
          <text class="stat-value-sm">{{ formatTime(latestGlucose.measure_time) }}</text>
          <text class="stat-label">时间</text>
        </view>
      </view>
      <text v-else class="empty-tip">暂无血糖记录</text>
    </view>

    <!-- 快捷入口 -->
    <view class="section-title">快捷功能</view>
    <view class="quick-grid">
      <view
        v-for="item in quickItems"
        :key="item.path"
        class="quick-item"
        @click="navigate(item.path)"
      >
        <text class="quick-icon">{{ item.icon }}</text>
        <text class="quick-text">{{ item.text }}</text>
      </view>
    </view>

    <!-- 最近提醒 -->
    <view class="card" v-if="reminders.length">
      <view class="section-title">🔔 健康提醒</view>
      <view
        v-for="r in reminders"
        :key="r.id"
        class="reminder-item"
        :class="'level-' + r.level"
      >
        <text class="reminder-content">{{ r.content }}</text>
        <text class="reminder-time">{{ formatTime(r.created_at) }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import { get } from '@/utils/request.js';

const MEAL_LABELS = {
  before_meal: '餐前',
  after_meal: '餐后',
  fasting: '空腹',
  random: '随机',
};

export default {
  data() {
    return {
      patient: {},
      latestGlucose: null,
      reminders: [],
      today: new Date().toLocaleDateString('zh-CN'),
      quickItems: [
        { icon: '💬', text: '在线咨询', path: '/pages/consult/index' },
        { icon: '👨‍👩‍👧', text: '家属绑定', path: '/pages/family/index' },
        { icon: '🔔', text: '健康提醒', path: '/pages/reminders/index' },
        { icon: '📈', text: '数据统计', path: '/pages/data/index' },
        { icon: '✏️', text: '数据录入', path: '/pages/input/index' },
        { icon: '👤', text: '个人信息', path: '/pages/profile/index' },
      ],
    };
  },
  onLoad() {
    this.loadPatient();
  },
  onShow() {
    this.loadData();
  },
  methods: {
    async loadPatient() {
      try {
        const cached = uni.getStorageSync('patient');
        if (cached) this.patient = JSON.parse(cached);
        const res = await get('/me');
        this.patient = res;
        uni.setStorageSync('patient', JSON.stringify(res));
      } catch (e) {}
    },
    async loadData() {
      try {
        const g = await get('/glucose?page=1&page_size=1');
        if (g.items && g.items.length) {
          const item = g.items[0];
          item.meal_status_label = MEAL_LABELS[item.meal_status] || '-';
          this.latestGlucose = item;
        }
      } catch (e) {}
      try {
        const r = await get('/reminders?page=1&page_size=3');
        this.reminders = r.items || [];
      } catch (e) {}
    },
    glucoseColor(val) {
      if (val > 11.1) return 'color:#f44336';
      if (val < 3.9) return 'color:#ff9800';
      return 'color:#4caf50';
    },
    formatTime(iso) {
      if (!iso) return '-';
      return iso.replace('T', ' ').slice(0, 16);
    },
    navigate(path) {
      const tabPaths = [
        '/pages/home/index',
        '/pages/consult/index',
        '/pages/data/index',
        '/pages/input/index',
        '/pages/profile/index',
      ];
      if (tabPaths.includes(path)) {
        uni.switchTab({ url: path });
      } else {
        uni.navigateTo({ url: path });
      }
    },
  },
};
</script>

<style lang="scss">
.container {
  padding: 24rpx;
}

.welcome-card {
  background: linear-gradient(135deg, #4caf50, #81c784);
  border-radius: 20rpx;
  padding: 36rpx 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;

  .welcome-left {
    flex: 1;
  }

  .welcome-name {
    display: block;
    font-size: 34rpx;
    font-weight: 700;
    color: #fff;
  }

  .welcome-sub {
    display: block;
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.85);
    margin-top: 8rpx;
  }

  .avatar {
    width: 90rpx;
    height: 90rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40rpx;
    color: #fff;
    font-weight: 700;
  }
}

.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.section-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #333;
  margin-bottom: 20rpx;
}

.stat-row {
  display: flex;
  justify-content: space-around;

  .stat-item {
    text-align: center;

    .stat-value {
      display: block;
      font-size: 56rpx;
      font-weight: 700;
    }

    .stat-value-sm {
      display: block;
      font-size: 30rpx;
      font-weight: 600;
      color: #333;
    }

    .stat-label {
      display: block;
      font-size: 22rpx;
      color: #999;
      margin-top: 4rpx;
    }
  }
}

.empty-tip {
  display: block;
  text-align: center;
  color: #bbb;
  font-size: 28rpx;
  padding: 20rpx 0;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16rpx;
  margin-bottom: 24rpx;

  .quick-item {
    background: #fff;
    border-radius: 16rpx;
    padding: 28rpx 0;
    text-align: center;
    box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);

    .quick-icon {
      display: block;
      font-size: 52rpx;
    }

    .quick-text {
      display: block;
      font-size: 24rpx;
      color: #555;
      margin-top: 10rpx;
    }
  }
}

.reminder-item {
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }

  .reminder-content {
    display: block;
    font-size: 28rpx;
    color: #333;
  }

  .reminder-time {
    display: block;
    font-size: 22rpx;
    color: #aaa;
    margin-top: 6rpx;
  }

  &.level-urgent .reminder-content {
    color: #f44336;
  }

  &.level-high .reminder-content {
    color: #ff9800;
  }
}
</style>
