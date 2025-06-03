<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-semibold text-primary">추천 종목</h3>
      <div class="flex space-x-2">
        <select v-model="selectedMarket" class="border rounded px-2 py-1">
          <option value="KOSPI">KOSPI</option>
          <option value="KOSDAQ">KOSDAQ</option>
        </select>
        <button @click="refreshRecommendations" 
                class="bg-primary text-white px-4 py-1 rounded">
          새로고침
        </button>
      </div>
    </div>
    
    <div v-for="stock in recommendations" :key="stock.stock_code" 
         class="p-4 border rounded-lg hover:bg-primary/5 cursor-pointer"
         @click="$emit('select-stock', stock.stock_code)">
      <div class="flex justify-between items-center">
        <div>
          <p class="font-medium">{{ stock.stock_name }}</p>
          <p class="text-sm text-secondary">{{ stock.stock_code }}</p>
        </div>
        <div class="text-right">
          <p class="text-primary font-semibold">{{ stock.recommendation_score }}점</p>
          <p class="text-xs text-secondary">추천 점수</p>
        </div>
      </div>
      <p class="mt-2 text-sm text-secondary">{{ stock.analysis_summary }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  recommendations: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['select-stock', 'refresh'])

const selectedMarket = ref('KOSPI')

const refreshRecommendations = () => {
  emit('refresh', selectedMarket.value)
}
</script> 