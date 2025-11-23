import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3001,      // 本地开发服务器端口
    open: true,      // 自动打开浏览器
  },
  resolve: {
    alias: {
      '@': '/src'    // 路径别名，@ 对应 src 文件夹
    }
  }
})
