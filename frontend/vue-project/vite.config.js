import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  // 환경변수 로드
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [vue()],
    server: {
      port: parseInt(env.VITE_DEV_PORT) || 5173,
      host: env.VITE_DEV_HOST || 'localhost',
      open: env.VITE_DEV_HOST === '0.0.0.0' ? false : true, // 외부 호스트일 때는 브라우저 자동 열기 비활성화
      proxy: {
        '/api': {
          target: env.VITE_API_TARGET || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    }
  }
})