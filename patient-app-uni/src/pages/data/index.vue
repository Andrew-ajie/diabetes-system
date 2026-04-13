<template>
  <view class="container">
    <!-- 范围切换 -->
    <view class="range-tabs">
      <view
        class="tab-item"
        :class="range === 'week' ? 'active' : ''"
        @click="setRange('week')"
      >近7天</view>
      <view
        class="tab-item"
        :class="range === 'month' ? 'active' : ''"
        @click="setRange('month')"
      >近30天</view>
    </view>

    <!-- 血糖统计 -->
    <view class="card">
      <view class="section-title">📊 血糖趋势（mmol/L）</view>
      <simple-chart
        :labels="glucoseStats.labels"
        :values="glucoseStats.averages"
        color="#4caf50"
        unit="mmol/L"
      />
      <view class="summary-row" v-if="glucoseStats.count > 0">
        <view class="summary-item">
          <text class="s-val">{{ glucoseStats.avg }}</text>
          <text class="s-label">平均值</text>
        </view>
        <view class="summary-item">
          <text class="s-val" style="color:#f44336">{{ glucoseStats.max }}</text>
          <text class="s-label">最高值</text>
        </view>
        <view class="summary-item">
          <text class="s-val" style="color:#ff9800">{{ glucoseStats.min }}</text>
          <text class="s-label">最低值</text>
        </view>
        <view class="summary-item">
          <text class="s-val">{{ glucoseStats.count }}</text>
          <text class="s-label">记录次数</text>
        </view>
      </view>
      <text v-else class="empty-tip">该时段暂无血糖数据</text>
    </view>

    <!-- 运动统计 -->
    <view class="card">
      <view class="section-title">🏃 运动趋势（分钟）</view>
      <simple-chart
        :labels="exerciseStats.labels"
        :values="exerciseStats.durations"
        color="#2196f3"
        unit="min"
      />
      <view class="summary-row" v-if="exerciseStats.count > 0">
        <view class="summary-item">
          <text class="s-val">{{ exerciseStats.total_duration }}</text>
          <text class="s-label">总时长(分)</text>
        </view>
        <view class="summary-item">
          <text class="s-val">{{ exerciseStats.total_calories }}</text>
          <text class="s-label">总卡路里</text>
        </view>
        <view class="summary-item">
          <text class="s-val">{{ exerciseStats.count }}</text>
          <text class="s-label">运动次数</text>
        </view>
      </view>
      <text v-else class="empty-tip">该时段暂无运动数据</text>
    </view>

    <!-- 血糖记录列表 -->
    <view class="card">
      <view class="section-title">📋 血糖记录</view>
      <view v-if="glucoseRecords.length">
        <view v-for="r in glucoseRecords" :key="r.id" class="record-item">
          <view class="record-left">
            <text class="record-val" :style="glucoseColor(r.value)">{{ r.value }} mmol/L</text>
            <text class="record-sub">{{ mealLabel(r.meal_status) }} · {{ formatTime(r.measure_time) }}</text>
          </view>
          <text class="record-remark">{{ r.remark || '' }}</text>
        </view>
      </view>
      <text v-else class="empty-tip">暂无血糖记录</text>
    </view>

    <!-- 运动记录列表 -->
    <view class="card">
      <view class="section-title">🏋️ 运动记录</view>
      <view v-if="exerciseRecords.length">
        <view v-for="r in exerciseRecords" :key="r.id" class="record-item">
          <view class="record-left">
            <text class="record-val">{{ r.exercise_type || '运动' }}</text>
            <text class="record-sub">
              {{ r.duration }}分钟 · {{ r.calories }}千卡 · {{ formatTime(r.record_time) }}
            </text>
          </view>
        </view>
      </view>
      <text v-else class="empty-tip">暂无运动记录</text>
    </view>
  </view>
</template>

<script>
import SimpleChart from '@/components/SimpleChart.vue';
import { get } from '@/utils/request.js';

const MEAL_LABELS = {
  before_meal: '餐前',
  after_meal: '餐后',
  fasting: '空腹',
  random: '随机',
};

export default {
  components: { SimpleChart },
  data() {
    return {
      range: 'week',
      glucoseStats: { labels: [], averages: [], count: 0 },
      exerciseStats: { labels: [], durations: [], count: 0 },
      glucoseRecords: [],
      exerciseRecords: [],
    };
  },
  onLoad() {
    this.loadAll();
  },
  onShow() {
    this.loadAll();
  },
  methods: {
    setRange(r) {
      this.range = r;
      this.loadAll();
    },
    async loadAll() {
      await Promise.all([
        this.loadGlucoseStats(),
        this.loadExerciseStats(),
        this.loadGlucoseRecords(),
        this.loadExerciseRecords(),
      ]);
    },
    async loadGlucoseStats() {
      try {
        const res = await get(`/stats/glucose?range=${this.range}`);
        this.glucoseStats = res;
      } catch (e) {}
    },
    async loadExerciseStats() {
      try {
        const res = await get(`/stats/exercise?range=${this.range}`);
        this.exerciseStats = res;
      } catch (e) {}
    },
    async loadGlucoseRecords() {
      try {
        const res = await get('/glucose?page=1&page_size=10');
        this.glucoseRecords = res.items || [];
      } catch (e) {}
    },
    async loadExerciseRecords() {
      try {
        const res = await get('/exercise?page=1&page_size=10');
        this.exerciseRecords = res.items || [];
      } catch (e) {}
    },
    glucoseColor(val) {
      if (val > 11.1) return 'color:#f44336';
      if (val < 3.9) return 'color:#ff9800';
      return 'color:#4caf50';
    },
    mealLabel(s) {
      return MEAL_LABELS[s] || '-';
    },
    formatTime(iso) {
      if (!iso) return '-';
      return iso.replace('T', ' ').slice(0, 16);
    },
  },
};
</script>

<style lang="scss">
.container {
  padding: 20rpx;
}

.range-tabs {
  display: flex;
  background: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  margin-bottom: 20rpx;

  .tab-item {
    flex: 1;
    height: 72rpx;
    line-height: 72rpx;
    text-align: center;
    font-size: 28rpx;
    color: #666;

    &.active {
      background: #4caf50;
      color: #fff;
      font-weight: 600;
    }
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

.summary-row {
  display: flex;
  justify-content: space-around;
  margin-top: 20rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid #f0f0f0;

  .summary-item {
    text-align: center;

    .s-val {
      display: block;
      font-size: 34rpx;
      font-weight: 700;
      color: #333;
    }

    .s-label {
      display: block;
      font-size: 22rpx;
      color: #aaa;
      margin-top: 4rpx;
    }
  }
}

.empty-tip {
  display: block;
  text-align: center;
  color: #bbb;
  font-size: 26rpx;
  padding: 30rpx 0;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }

  .record-left {
    flex: 1;

    .record-val {
      display: block;
      font-size: 30rpx;
      font-weight: 600;
    }

    .record-sub {
      display: block;
      font-size: 22rpx;
      color: #aaa;
      margin-top: 4rpx;
    }
  }

  .record-remark {
    font-size: 24rpx;
    color: #bbb;
    max-width: 160rpx;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>
