<template>
  <div class="dashboard">
    <!-- 左侧导航栏 -->
    <el-container>
      <!-- 主体内容 -->
      <el-container>
        
        <el-main class="main-area">
          <!-- 上传页面 -->
          <div v-if="activeView === 'upload'">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>📤 上传 OpenAPI 文件</span>
                </div>
              </template>

              <el-upload
                drag
                :action="`${apiBase}/upload`"
                accept=".yaml,.yml"
                :on-success="handleUploadSuccess"
                :show-file-list="false"
              >
                <el-icon><UploadFilled /></el-icon>
                <div class="el-upload__text">
                  拖拽文件到此或 <em>点击上传</em>
                </div>
              </el-upload>

              <el-divider>已上传文件</el-divider>

              <el-table
                :data="uploadedFiles"
                border
                stripe
                v-if="uploadedFiles.length"
              >
                <el-table-column prop="file_name" label="文件名" />
                <el-table-column prop="file_path" label="文件路径" />
                <el-table-column label="操作" width="200" align="center">
                  <template #default="scope">
                    <el-button
                      type="success"
                      circle
                      @click="generateCases(scope.row)"
                    >
                      <el-icon><DocumentChecked /></el-icon>
                    </el-button>
                    <el-button
                      type="danger"
                      circle
                      @click="deleteFile(scope.row)"
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>

              <el-empty description="暂无上传文件" v-else />
            </el-card>
          </div>

          <!-- 测试用例 -->
          <div v-if="activeView === 'cases'">
            <el-card shadow="hover">
              <template #header>
                <span>🧩 测试用例管理</span>
              </template>

              <el-table :data="testCases" border stripe v-if="testCases.length">
                <el-table-column prop="name" label="用例文件" />
                <el-table-column
                  prop="created_at"
                  label="生成时间"
                  width="200"
                />
                <el-table-column label="操作" width="280" align="center">
                  <template #default="scope">
                    <el-button
                      type="primary"
                      circle
                      @click="viewCase(scope.row)"
                    >
                      <el-icon><View /></el-icon>
                    </el-button>
                    <el-button
                      type="warning"
                      circle
                      @click="runCase(scope.row)"
                    >
                      <el-icon><VideoPlay /></el-icon>
                    </el-button>
                    <el-button
                      type="danger"
                      circle
                      @click="deleteCase(scope.row)"
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>

              <el-empty description="暂无用例" v-else />
            </el-card>
          </div>

          <!-- 测试报告 -->
          <div v-if="activeView === 'reports'">
            <el-card shadow="hover">
              <template #header>
                <span>📊 测试执行报告</span>
              </template>
              <el-empty description="暂无报告数据，执行后将自动生成" />
            </el-card>
          </div>
        </el-main>
      </el-container>
    </el-container>

    <!-- 弹窗：用例详情 -->
    <el-dialog v-model="caseDialogVisible" title="测试用例详情" width="60%">
      <pre class="case-detail">{{ caseDetail }}</pre>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import {
  UploadFilled,
  Document,
  Delete,
  DocumentChecked,
  View,
  Histogram,
  VideoPlay,
  UserFilled,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

const apiBase = "http://127.0.0.1:5000/api";
const activeView = ref("upload");

const uploadedFiles = ref([]);
const testCases = ref([]);
const caseDialogVisible = ref(false);
const caseDetail = ref("");

const viewTitle = computed(() => {
  switch (activeView.value) {
    case "upload":
      return "接口文档管理";
    case "cases":
      return "测试用例中心";
    case "reports":
      return "执行报告";
    default:
      return "";
  }
});

onMounted(() => {
  fetchUploadedFiles();
  fetchTestCases();
});

async function fetchUploadedFiles() {
  const res = await fetch(`${apiBase}/files`);
  const data = await res.json();
  uploadedFiles.value = data.data.files || [];
}

async function fetchTestCases() {
  const res = await fetch(`${apiBase}/cases`);
  const data = await res.json();
  testCases.value = data.cases || [];
}

function handleUploadSuccess() {
  ElMessage.success("✅ 上传成功");
  fetchUploadedFiles();
}

async function deleteFile(file) {
  await fetch(`${apiBase}/delete_file/${file.file_name}`, { method: "DELETE" });
  ElMessage.success("🗑️ 文件已删除");
  fetchUploadedFiles();
}

async function generateCases(file) {
  const res = await fetch(`${apiBase}/generate/${file.file_name}`, {
    method: "GET",
  });
  await res.json();
  ElMessage.success("✨ 用例生成成功");
  fetchTestCases();
}

async function viewCase(row) {
  const res = await fetch(`${apiBase}/case_detail/${row.name}`);
  const data = await res.json();
  caseDetail.value = JSON.stringify(data.detail, null, 2);
  caseDialogVisible.value = true;
}

async function deleteCase(row) {
  await fetch(`${apiBase}/delete_case/${row.name}`, { method: "DELETE" });
  ElMessage.success("✅ 用例已删除");
  fetchTestCases();
}

async function runCase(row) {
  const res = await fetch(`${apiBase}/execute?file=${row.name}`, {
    method: "POST",
  });
  await res.json();
  ElMessage.success("🚀 测试执行完成");
}
</script>

<style scoped>
.dashboard {
  height: 100vh;
  background: #f5f7fa;
}

.sidebar {
  background-color: #1f2d3d;
  color: white;
  height: 100vh;
  padding-top: 10px;
}

.logo {
  text-align: center;
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 15px;
  color: #fff;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 0 20px;
  border-bottom: 1px solid #eee;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #555;
}

.main-area {
  padding: 24px;
  overflow: auto;
}

.case-detail {
  background: #272822;
  color: #f8f8f2;
  padding: 1rem;
  border-radius: 8px;
  font-family: monospace;
  max-height: 500px;
  overflow: auto;
}
</style>
