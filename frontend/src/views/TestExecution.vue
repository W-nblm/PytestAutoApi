<template>
  <div class="page-container">
    <div class="page-header">
      <h3>🚀 测试执行</h3>
      <el-button type="danger" @click="runTests">执行所有测试</el-button>
    </div>

    <el-card shadow="hover" class="mt-4">
      <h5>执行结果：</h5>
      <el-table :data="results" border stripe>
        <el-table-column type="index" label="#" width="50" />
        <el-table-column prop="name" label="用例名称" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === '成功' ? 'success' : 'danger'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="耗时(ms)" width="120" />
        <el-table-column prop="message" label="结果详情" />
      </el-table>

      <div v-if="results.length" class="summary mt-3">
        <el-divider />
        <p><b>执行统计：</b> {{ summaryText }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";

const results = ref([]);
const summaryText = ref("");

async function runTests() {
  ElMessage.info("正在执行测试...");
  const res = await fetch("http://127.0.0.1:5000/api/execute", { method: "POST" });
  const data = await res.json();
  results.value = data?.data.test_files || [];
  summaryText.value = data?.data.total_files || "暂无统计信息";
  ElMessage.success("测试执行完毕！");
}
</script>

<style scoped>
.page-container {
  background: white;
  padding: 20px;
  border-radius: 10px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.mt-4 {
  margin-top: 20px;
}
.summary {
  background: #f9fafb;
  padding: 10px 15px;
  border-radius: 6px;
}
</style>
