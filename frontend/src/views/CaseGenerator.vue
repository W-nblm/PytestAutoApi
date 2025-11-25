<template>
  <div class="page-container">
    <!-- ======================= 顶部标题 ======================= -->
    <div class="header-box">
      <div>
        <h2 class="page-title">🤖 AI 测试用例生成平台</h2>
        <p class="text-muted">上传需求文档，自动生成可导出的测试用例集</p>
      </div>
      <el-button type="primary" @click="dialogVisible = true">
        ➕ 新建用例集
      </el-button>
    </div>

    <!-- ======================= 用例列表 ======================= -->
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>📂 测试用例列表</span>

          <el-input
            v-model="search"
            placeholder="🔍 搜索用例集标题"
            clearable
            class="search-box"
            size="small"
          />
        </div>
      </template>

      <el-table
        :data="filteredCases"
        border
        stripe
        style="width: 100%"
        v-loading="loadingCases"
      >
        <el-table-column label="#" type="index" width="60" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="timestamp" label="创建时间" width="200" />
        <el-table-column label="操作" width="260">
          <template #default="scope">
            <el-button size="small" type="info" @click="viewCase(scope.row)"
              >查看</el-button
            >

            <el-button
              size="small"
              type="success"
              @click="downloadCase(scope.row)"
              >下载</el-button
            >

            <el-button
              size="small"
              type="danger"
              @click="deleteCase(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!cases.length && !loadingCases" description="暂无用例" />
    </el-card>

    <!-- ======================= 新建用例集 弹窗 ======================= -->
    <el-dialog v-model="dialogVisible" title="📄 生成测试用例" width="600px">
      <div class="dialog-body">
        <!-- 标题 -->
        <el-form label-width="90px">
          <el-form-item label="标题">
            <el-input v-model="title" placeholder="如：登录功能测试" />
          </el-form-item>

          <!-- 上传文件 -->
          <el-form-item label="上传文件">
            <el-upload
              drag
              :auto-upload="false"
              :on-change="handleFileChange"
              :show-file-list="true"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">拖拽至此或 <em>点击上传</em></div>
              <template #tip>
                <div class="el-upload__tip">支持 .txt / .docx</div>
              </template>
            </el-upload>
          </el-form-item>

          <!-- 文本 -->
          <el-form-item label="文本内容">
            <el-input
              v-model="text"
              type="textarea"
              :rows="6"
              placeholder="可以直接粘贴需求说明文档内容..."
            />
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="generating" @click="generate">
          🚀 生成
        </el-button>
      </template>
    </el-dialog>

    <!-- ======================= 用例详情对话框 ======================= -->
    <el-dialog v-model="caseDetailDialog" title="测试用例详情" width="60%">
      <pre class="case-detail">{{ detailText }}</pre>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import * as api from "@/api/case";

const dialogVisible = ref(false);
const caseDetailDialog = ref(false);

const title = ref("");
const text = ref("");
const file = ref(null);

const loadingCases = ref(false);
const generating = ref(false);
const cases = ref([]);
const detailText = ref("");
const search = ref("");

// ------------------ 初始化加载 ------------------
onMounted(fetchCases);

async function fetchCases() {
  loadingCases.value = true;
  try {
    const res = await api.getCaseList();
    console.log(res);
    cases.value = res.data.data || [];
  } finally {
    loadingCases.value = false;
  }
}

const filteredCases = computed(() =>
  cases.value.filter((c) =>
    c.title.toLowerCase().includes(search.value.toLowerCase())
  )
);

// ------------------ 上传文件 ------------------
function handleFileChange(uploadFile) {
  file.value = uploadFile.raw; // ⚠ 关键修复点！
}

// ------------------ 生成测试用例 ------------------
async function generate() {
  if (!title.value) {
    return ElMessage.warning("请输入用例集标题");
  }
  if (!file.value && !text.value) {
    return ElMessage.warning("请上传文件或输入文本");
  }

  const formData = new FormData();
  formData.append("title", title.value);
  if (file.value) formData.append("file", file.value);
  if (text.value) formData.append("text", text.value);

  generating.value = true;

  try {
    const res = await api.generateCase(formData);
    ElMessage.success(`生成成功：共 ${res.data.count} 条`);
    dialogVisible.value = false;
    fetchCases();
  } catch {
    ElMessage.error("生成失败");
  } finally {
    generating.value = false;
  }
}

// ------------------ 查看详情 ------------------
async function viewCase(row) {
  const res = await api.getCaseDetail(row.timestamp);
  detailText.value = JSON.stringify(res.data.data, null, 2);
  caseDetailDialog.value = true;
}

// ------------------ 下载 ------------------
function downloadCase(row) {
  api.downloadCase(row.timestamp).then((res) => {
    const blob = new Blob([res.data]);
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${row.title}.xlsx`;
    link.click();
  });
}

// ------------------ 删除 ------------------
async function deleteCase(row) {
  await ElMessageBox.confirm(`确定删除 "${row.title}"？`, "警告");
  await api.deleteCase(row.timestamp);
  ElMessage.success("删除成功");
  fetchCases();
}
</script>

<style scoped>
.page-container {
  padding: 24px;
  background: #f7f8fa;
}

.header-box {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.page-title {
  font-weight: 600;
  margin: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-box {
  width: 220px;
}

.case-detail {
  background: #262626;
  color: #e6e6e6;
  padding: 12px;
  border-radius: 6px;
  max-height: 600px;
  overflow: auto;
}
</style>
