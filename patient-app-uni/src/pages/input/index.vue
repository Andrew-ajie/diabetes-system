<template>
  <view class="container">
    <!-- 录入类型 Tab -->
    <view class="type-tabs">
      <view
        class="tab-item"
        :class="activeTab === 'glucose' ? 'active' : ''"
        @click="activeTab = 'glucose'"
      >血糖录入</view>
      <view
        class="tab-item"
        :class="activeTab === 'exercise' ? 'active' : ''"
        @click="activeTab = 'exercise'"
      >运动录入</view>
    </view>

    <!-- 血糖录入表单 -->
    <view v-if="activeTab === 'glucose'" class="card">
      <view class="section-title">📊 录入血糖数据</view>

      <view class="form-item">
        <text class="form-label">血糖值（mmol/L）*</text>
        <input
          v-model="glucose.value"
          class="form-input"
          type="digit"
          placeholder="例如：6.5"
        />
      </view>

      <view class="form-item">
        <text class="form-label">测量时间 *</text>
        <input
          v-model="glucose.measure_time"
          class="form-input"
          placeholder="格式：2024-01-15T08:30"
        />
      </view>

      <view class="form-item">
        <text class="form-label">餐况</text>
        <picker :range="mealOptions" :range-key="'label'" @change="onMealChange">
          <view class="picker-view">
            {{ selectedMealLabel || '请选择餐况' }}
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="form-label">备注</text>
        <textarea
          v-model="glucose.remark"
          class="form-textarea"
          placeholder="可选备注..."
        />
      </view>

      <button class="btn-submit" :disabled="submitting" @click="submitGlucose">
        {{ submitting ? '提交中...' : '✅ 提交血糖记录' }}
      </button>
    </view>

    <!-- 运动录入表单 -->
    <view v-if="activeTab === 'exercise'" class="card">
      <view class="section-title">🏃 录入运动数据</view>

      <view class="form-item">
        <text class="form-label">运动类型</text>
        <input
          v-model="exercise.exercise_type"
          class="form-input"
          placeholder="例如：步行、游泳、骑行"
        />
      </view>

      <view class="form-item">
        <text class="form-label">时长（分钟）</text>
        <input
          v-model="exercise.duration"
          class="form-input"
          type="number"
          placeholder="例如：30"
        />
      </view>

      <view class="form-item">
        <text class="form-label">卡路里消耗（千卡）</text>
        <input
          v-model="exercise.calories"
          class="form-input"
          type="number"
          placeholder="例如：150"
        />
      </view>

      <view class="form-item">
        <text class="form-label">运动强度</text>
        <picker :range="intensityOptions" :range-key="'label'" @change="onIntensityChange">
          <view class="picker-view">
            {{ selectedIntensityLabel || '请选择强度' }}
          </view>
        </picker>
      </view>

      <view class="form-item">
        <text class="form-label">运动时间 *</text>
        <input
          v-model="exercise.record_time"
          class="form-input"
          placeholder="格式：2024-01-15T08:30"
        />
      </view>

      <view class="form-item">
        <text class="form-label">备注</text>
        <textarea
          v-model="exercise.remark"
          class="form-textarea"
          placeholder="可选备注..."
        />
      </view>

      <button class="btn-submit" :disabled="submitting" @click="submitExercise">
        {{ submitting ? '提交中...' : '✅ 提交运动记录' }}
      </button>
    </view>
  </view>
</template>

<script>
import { post } from '@/utils/request.js';
import { formatLocalISO } from '@/utils/dateUtils.js';

export default {
  data() {
    const localISO = formatLocalISO();
    return {
      activeTab: 'glucose',
      submitting: false,
      glucose: {
        value: '',
        measure_time: localISO,
        meal_status: '',
        remark: '',
      },
      exercise: {
        exercise_type: '',
        duration: '',
        calories: '',
        intensity: '',
        record_time: localISO,
        remark: '',
      },
      mealOptions: [
        { label: '餐前', value: 'before_meal' },
        { label: '餐后', value: 'after_meal' },
        { label: '空腹', value: 'fasting' },
        { label: '随机', value: 'random' },
      ],
      intensityOptions: [
        { label: '低强度', value: 'low' },
        { label: '中强度', value: 'medium' },
        { label: '高强度', value: 'high' },
      ],
      selectedMealLabel: '',
      selectedIntensityLabel: '',
    };
  },
  methods: {
    onMealChange(e) {
      const idx = e.detail.value;
      this.glucose.meal_status = this.mealOptions[idx].value;
      this.selectedMealLabel = this.mealOptions[idx].label;
    },
    onIntensityChange(e) {
      const idx = e.detail.value;
      this.exercise.intensity = this.intensityOptions[idx].value;
      this.selectedIntensityLabel = this.intensityOptions[idx].label;
    },
    async submitGlucose() {
      if (!this.glucose.value || !this.glucose.measure_time) {
        uni.showToast({ title: '请填写血糖值和测量时间', icon: 'none' });
        return;
      }
      this.submitting = true;
      try {
        await post('/glucose', {
          value: parseFloat(this.glucose.value),
          measure_time: this.glucose.measure_time,
          meal_status: this.glucose.meal_status || null,
          remark: this.glucose.remark || null,
        });
        uni.showToast({ title: '血糖记录已保存', icon: 'success' });
        this.resetGlucose();
      } catch (e) {
      } finally {
        this.submitting = false;
      }
    },
    async submitExercise() {
      if (!this.exercise.record_time) {
        uni.showToast({ title: '请填写运动时间', icon: 'none' });
        return;
      }
      this.submitting = true;
      try {
        await post('/exercise', {
          exercise_type: this.exercise.exercise_type || null,
          duration: this.exercise.duration ? parseInt(this.exercise.duration) : null,
          calories: this.exercise.calories ? parseInt(this.exercise.calories) : null,
          intensity: this.exercise.intensity || null,
          record_time: this.exercise.record_time,
          remark: this.exercise.remark || null,
        });
        uni.showToast({ title: '运动记录已保存', icon: 'success' });
        this.resetExercise();
      } catch (e) {
      } finally {
        this.submitting = false;
      }
    },
    resetGlucose() {
      this.glucose.value = '';
      this.glucose.meal_status = '';
      this.glucose.remark = '';
      this.selectedMealLabel = '';
    },
    resetExercise() {
      this.exercise.exercise_type = '';
      this.exercise.duration = '';
      this.exercise.calories = '';
      this.exercise.intensity = '';
      this.exercise.remark = '';
      this.selectedIntensityLabel = '';
    },
  },
};
</script>

<style lang="scss">
.container {
  padding: 20rpx;
}

.type-tabs {
  display: flex;
  background: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  margin-bottom: 20rpx;

  .tab-item {
    flex: 1;
    height: 80rpx;
    line-height: 80rpx;
    text-align: center;
    font-size: 30rpx;
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
  margin-bottom: 24rpx;
}

.form-item {
  margin-bottom: 24rpx;

  .form-label {
    display: block;
    font-size: 26rpx;
    color: #666;
    margin-bottom: 10rpx;
  }

  .form-input {
    width: 100%;
    height: 84rpx;
    border: 2rpx solid #e0e0e0;
    border-radius: 10rpx;
    padding: 0 20rpx;
    font-size: 28rpx;
    color: #333;
    box-sizing: border-box;
  }

  .form-textarea {
    width: 100%;
    height: 140rpx;
    border: 2rpx solid #e0e0e0;
    border-radius: 10rpx;
    padding: 16rpx 20rpx;
    font-size: 28rpx;
    color: #333;
    box-sizing: border-box;
  }

  .picker-view {
    height: 84rpx;
    line-height: 84rpx;
    border: 2rpx solid #e0e0e0;
    border-radius: 10rpx;
    padding: 0 20rpx;
    font-size: 28rpx;
    color: #999;
  }
}

.btn-submit {
  background: #4caf50;
  color: #fff;
  border-radius: 44rpx;
  height: 90rpx;
  line-height: 90rpx;
  text-align: center;
  font-size: 32rpx;
  font-weight: 600;
  width: 100%;
  border: none;
  margin-top: 10rpx;
}
</style>
