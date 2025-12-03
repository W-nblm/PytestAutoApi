<script setup lang="ts"></script>

<template>
  <el-container style="height: 100vh">
    <!-- ===================== 左侧菜单 ===================== -->
    <el-aside width="200px" class="sidebar">
      <div class="logo">AI 测试平台</div>

      <el-menu
        router
        :default-active="$route.path"
        background-color="#1f2937"
        text-color="#fff"
        active-text-color="#42b883"
      >
        <!-- 单菜单 -->
        <el-menu-item index="/">🏠 仪表盘</el-menu-item>
        <el-menu-item index="/docs">📘 接口文档</el-menu-item>
        <el-menu-item index="/run">🚀 执行测试</el-menu-item>

        <!-- 用例管理（含二级菜单） -->
        <el-sub-menu index="/case">
          <template #title>🧩 用例管理</template>
          <el-menu-item index="/case/func"> 🧪 功能测试用例 </el-menu-item>
          <el-menu-item index="/case/api"> 🔗 接口测试用例 </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <!-- ===================== 右侧内容区 ===================== -->
    <el-container>
      <el-header class="header">
        <h3>AI 自动化测试平台</h3>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.sidebar {
  background-color: #1f2937;
  color: white;
}
.logo {
  text-align: center;
  padding: 20px 0;
  font-weight: bold;
  font-size: 1.2rem;
  border-bottom: 1px solid #2469d8;
}
.header {
  background: #f9fafb;
  padding: 10px 20px;
  border-bottom: 1px solid #e5e7eb;
}
.main {
  padding: 20px;
  background-color: #f3f4f6;
  overflow-y: auto;
}
</style>
