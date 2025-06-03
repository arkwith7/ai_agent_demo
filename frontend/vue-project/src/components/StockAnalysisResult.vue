<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-semibold text-primary">종목 상세 분석</h3>
      <button @click="$emit('back')" class="text-sm text-primary">
        ← 추천 목록으로
      </button>
    </div>
    
    <!-- 기본 정보 -->
    <div class="p-4 border rounded-lg">
      <h4 class="font-medium mb-2">기본 정보</h4>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-sm text-secondary">종목명</p>
          <p class="font-medium">{{ analysis.stock_name }}</p>
        </div>
        <div>
          <p class="text-sm text-secondary">종목코드</p>
          <p class="font-medium">{{ analysis.stock_code }}</p>
        </div>
      </div>
    </div>
    
    <!-- 워런 버핏 기준 점수 -->
    <div class="p-4 border rounded-lg">
      <h4 class="font-medium mb-2">워런 버핏 투자 기준 평가</h4>
      <div class="space-y-2">
        <div v-for="(score, criteria) in analysis.buffett_criteria_scores" 
             :key="criteria"
             class="flex items-center">
          <div class="w-32 text-sm text-secondary">{{ getCriteriaName(criteria) }}</div>
          <div class="flex-1 h-2 bg-gray-200 rounded-full">
            <div class="h-2 bg-primary rounded-full" 
                 :style="{ width: `${score}%` }"></div>
          </div>
          <div class="w-12 text-right text-sm font-medium">{{ score }}%</div>
        </div>
      </div>
    </div>
    
    <!-- ESG 분석 -->
    <div v-if="showESG" class="p-4 border rounded-lg">
      <h4 class="font-medium mb-2">ESG 분석</h4>
      <div class="space-y-2">
        <div v-for="(score, category) in analysis.esg_scores" 
             :key="category"
             class="flex items-center">
          <div class="w-32 text-sm text-secondary">{{ getESGCategoryName(category) }}</div>
          <div class="flex-1 h-2 bg-gray-200 rounded-full">
            <div class="h-2 bg-green-500 rounded-full" 
                 :style="{ width: `${score}%` }"></div>
          </div>
          <div class="w-12 text-right text-sm font-medium">{{ score }}%</div>
        </div>
      </div>
    </div>
    
    <!-- 리스크 분석 -->
    <div v-if="showRisk" class="p-4 border rounded-lg">
      <h4 class="font-medium mb-2">리스크 분석</h4>
      <div class="space-y-2">
        <div v-for="(score, risk) in analysis.risk_scores" 
             :key="risk"
             class="flex items-center">
          <div class="w-32 text-sm text-secondary">{{ getRiskName(risk) }}</div>
          <div class="flex-1 h-2 bg-gray-200 rounded-full">
            <div class="h-2 bg-red-500 rounded-full" 
                 :style="{ width: `${score}%` }"></div>
          </div>
          <div class="w-12 text-right text-sm font-medium">{{ score }}%</div>
        </div>
      </div>
    </div>

    <!-- 투자 추천 -->
    <div class="p-4 border rounded-lg">
      <h4 class="font-medium mb-2">투자 추천</h4>
      <p class="text-secondary">{{ analysis.recommendation }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  analysis: {
    type: Object,
    required: true
  },
  showESG: {
    type: Boolean,
    default: true
  },
  showRisk: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['back'])

const getCriteriaName = (criteria) => {
  const criteriaNames = {
    market_cap_score: '시가총액',
    roe_score: 'ROE',
    profitability_score: '수익성',
    growth_score: '성장성',
    fcf_projection_score: '미래가치',
    valuation_score: '가치평가',
    esg_score: 'ESG',
    risk_score: '리스크'
  }
  return criteriaNames[criteria] || criteria
}

const getESGCategoryName = (category) => {
  const categoryNames = {
    environmental: '환경',
    social: '사회',
    governance: '지배구조'
  }
  return categoryNames[category] || category
}

const getRiskName = (risk) => {
  const riskNames = {
    market_risk: '시장 리스크',
    business_risk: '사업 리스크',
    financial_risk: '재무 리스크',
    operational_risk: '운영 리스크'
  }
  return riskNames[risk] || risk
}
</script> 