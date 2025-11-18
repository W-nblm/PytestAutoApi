<template>
  <div class="page-container">
    <div class="page-header">
      <h3>📘 接口文档管理</h3>

      <div class="action-group">
        <el-upload
          action="http://127.0.0.1:5000/api/upload"
          :on-success="handleUploadSuccess"
          :show-file-list="false"
          accept=".yaml,.yml"
        >
          <el-button type="primary">上传 OpenAPI 文件</el-button>
        </el-upload>
      </div>
    </div>

    <el-card shadow="hover" class="mt-4">
      <el-table :data="docs" border stripe style="width: 100%">
        <el-table-column type="index" label="#" width="50" />
        <el-table-column prop="file_name" label="文件名" />
        <el-table-column
          prop="upload_time"
          label="上传时间"
          width="180"
          :formatter="formatTime"
        />

        <!-- 操作栏 -->
        <el-table-column label="操作" width="180" align="center">
          <template #default="{ row }">
            <el-button size="small" type="success" @click="viewDetail(row)"
              >查看</el-button
            >

            <!-- 新增：生成测试用例 -->
            <el-button size="small" type="primary" @click="generateCases(row)">
              生成用例
            </el-button>

            <!-- 删除按钮已移除 -->
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

const router = useRouter();
const docs = ref([]);

// 初始化加载文件列表
onMounted(fetchDocs);

async function fetchDocs() {
  const res = await fetch("http://127.0.0.1:5000/api/files");
  const data = await res.json();
  docs.value = data?.data.files || [];
}

function handleUploadSuccess(res) {
  ElMessage.success("上传成功！");
  fetchDocs();
}

function viewDetail(row) {
  ElMessage.info(`查看文档: ${row.file_name}`);
}

// ⭐ 新增生成测试用例
async function generateCases(row) {
  ElMessage.info(`正在生成测试用例...`);

  const res = await fetch(
    `http://127.0.0.1:5000/api/generate/${row.file_name}`,
    {
      method: "GET",
    }
  );
  const data = await res.json();

  if (data?.success) {
    ElMessage.success("测试用例生成成功！");
  } else {
    ElMessage.error("生成失败");
  }
}

// 格式化时间
function formatTime(row, column, cellValue) {
  if (!cellValue) return "-";
  const date = new Date(cellValue * 1000);
  return date.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
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

.action-group {
  display: flex;
  gap: 10px;
}

.mt-4 {
  margin-top: 20px;
}
</style>
