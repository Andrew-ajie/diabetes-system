<!--
  SimpleChart — 轻量柱状图/折线图组件（无外部依赖，兼容 H5 + App）
  Props:
    labels: string[]     — X 轴标签
    values: number[]     — 数据数组
    color: string        — 柱颜色（默认绿）
    unit: string         — 数值单位
    type: 'bar'|'line'   — 目前固定用柱状图实现
-->
<template>
  <view class="chart-wrap">
    <view v-if="!labels || !labels.length" class="empty-tip">暂无图表数据</view>
    <view v-else>
      <!-- 柱状图 -->
      <view class="bars-area">
        <view
          v-for="(val, idx) in values"
          :key="idx"
          class="bar-col"
        >
          <text class="bar-val">{{ val }}</text>
          <view class="bar-bg">
            <view
              class="bar-fill"
              :style="{ height: barHeight(val) + '%', background: color || '#4caf50' }"
            />
          </view>
          <text class="bar-label">{{ labels[idx] }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'SimpleChart',
  props: {
    labels: { type: Array, default: () => [] },
    values: { type: Array, default: () => [] },
    color: { type: String, default: '#4caf50' },
    unit: { type: String, default: '' },
  },
  computed: {
    maxVal() {
      const max = Math.max(...this.values, 0);
      return max === 0 ? 1 : max;
    },
  },
  methods: {
    barHeight(val) {
      return Math.round((val / this.maxVal) * 90) + 5;
    },
  },
};
</script>

<style lang="scss">
.chart-wrap {
  width: 100%;
  overflow-x: auto;
}

.bars-area {
  display: flex;
  align-items: flex-end;
  gap: 8rpx;
  min-height: 200rpx;
  padding: 10rpx 0;

  .bar-col {
    flex: 1;
    min-width: 60rpx;
    display: flex;
    flex-direction: column;
    align-items: center;

    .bar-val {
      font-size: 18rpx;
      color: #666;
      margin-bottom: 4rpx;
    }

    .bar-bg {
      width: 100%;
      height: 160rpx;
      background: #f0f0f0;
      border-radius: 6rpx;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      overflow: hidden;

      .bar-fill {
        width: 100%;
        border-radius: 6rpx 6rpx 0 0;
        transition: height 0.3s;
      }
    }

    .bar-label {
      font-size: 18rpx;
      color: #aaa;
      margin-top: 6rpx;
      transform: rotate(-30deg);
    }
  }
}

.empty-tip {
  text-align: center;
  color: #ccc;
  font-size: 26rpx;
  padding: 40rpx 0;
}
</style>
