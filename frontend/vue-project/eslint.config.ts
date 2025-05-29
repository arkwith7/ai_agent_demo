import { defineConfig } from 'eslint-define-config'
import vue from '@vitejs/plugin-vue'
import ts from '@vue/eslint-config-typescript'
import prettier from '@vue/eslint-config-prettier'

export default defineConfig({
  extends: [
    'plugin:vue/vue3-recommended',
    ts,
    prettier
  ],
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/no-v-html': 'off',
    'vue/require-default-prop': 'off',
    'vue/max-attributes-per-line': ['error', {
      singleline: 3,
      multiline: 1
    }],
    'vue/html-self-closing': ['error', {
      html: {
        void: 'always',
        normal: 'always',
        component: 'always'
      }
    }]
  }
})
