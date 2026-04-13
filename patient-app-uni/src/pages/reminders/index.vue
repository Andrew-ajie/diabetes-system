<template>
  <view class="container">
    <view class="card">
      <view class="section-title">🔔 健康提醒</view>
      <view v-if="!reminders.length" class="empty-tip">暂无健康提醒</view>
      <view
        v-for="r in reminders"
        :key="r.id"
        class="reminder-item"
        :class="'level-' + r.level"
      >
        <view class="level-badge" :class="'badge-' + r.level">
          {{ levelLabel(r.level) }}
        </view>
        <view class="reminder-body">
          <text class="reminder-content">{{ r.content }}</text>
          <text class="reminder-time">{{ formatTime(r.created_at) }}</text>
        </view>
      </view>
    </view>

    <!-- 加载更多 -->
    <view v-if="hasMore" class="load-more" @click="loadMore">加载更多</view>
    <view v-else-if="reminders.length > 0" class="no-more">已显示全部提醒</view>
  </view>
</template>

<script>
import { get } from '@/utils/request.js';

const LEVEL_LABELS = {
  low: '一般',
  medium: '重要',
  high: '紧急',
  urgent: '非常紧急',
};

export default {
  data() {
    return {
      reminders: [],
      page: 1,
      pageSize: 20,
      total: 0,
    };
  },
  computed: {
    hasMore() {
      return this.reminders.length < this.total;
    },
  },
  onLoad() {
    this.loadReminders(true);
  },
  onShow() {
    this.loadReminders(true);
  },
  methods: {
    async loadReminders(reset = false) {
      if (reset) {
        this.page = 1;
        this.reminders = [];
      }
      try {
        const res = await get(`/reminders?page=${this.page}&page_size=${this.pageSize}`);
        this.reminders = [...this.reminders, ...(res.items || [])];
        this.total = res.total || 0;
      } catch (e) {}
    },
    loadMore() {
      this.page += 1;
      this.loadReminders(false);
    },
    levelLabel(l) {
      return LEVEL_LABELS[l] || '提醒';
    },
    formatTime(iso) {
      if (!iso) return '';
      return iso.replace('T', ' ').slice(0, 16);
    },
  },
};
</script>

<style lang="scss">
.container {
  padding: 20rpx;
}

.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.section-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #333;
  margin-bottom: 20rpx;
}

.empty-tip {
  display: block;
  text-align: center;
  color: #bbb;
  font-size: 28rpx;
  padding: 60rpx 0;
}

.reminder-item {
  display: flex;
  align-items: flex-start;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
  gap: 16rpx;

  &:last-child {
    border-bottom: none;
  }

  .level-badge {
    flex-shrink: 0;
    padding: 6rpx 16rpx;
    border-radius: 20rpx;
    font-size: 20rpx;
    color: #fff;
    margin-top: 4rpx;

    &.badge-low {
      background: #9e9e9e;
    }

    &.badge-medium {
      background: #2196f3;
    }

    &.badge-high {
      background: #ff9800;
    }

    &.badge-urgent {
      background: #f44336;
    }
  }

  .reminder-body {
    flex: 1;

    .reminder-content {
      display: block;
      font-size: 28rpx;
      color: #333;
      line-height: 1.5;
    }

    .reminder-time {
      display: block;
      font-size: 22rpx;
      color: #aaa;
      margin-top: 8rpx;
    }
  }
}

.load-more {
  text-align: center;
  color: #4caf50;
  font-size: 28rpx;
  padding: 30rpx 0;
}

.no-more {
  text-align: center;
  color: #bbb;
  font-size: 24rpx;
  padding: 24rpx 0;
}
</style>
