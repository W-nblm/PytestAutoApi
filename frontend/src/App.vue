<template>
  <el-container style="height:100vh">
    <el-aside width="200px" class="sidebar">
      <div class="logo">AI 测试平台</div>
      <el-menu
        router
        default-active="/"
        background-color="#1f2937"
        text-color="#fff"
        active-text-color="#42b883"
      >
        <el-menu-item index="/">🏠 仪表盘</el-menu-item>
        <el-menu-item index="/docs">📘 接口文档</el-menu-item>
        <el-menu-item index="/cases">🧩 测试用例</el-menu-item>
        <el-menu-item index="/run">🚀 执行测试</el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <h2>AI 自动化测试平台</h2>
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
