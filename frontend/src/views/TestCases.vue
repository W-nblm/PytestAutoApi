<template>
  <div class="page-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h3>🧩 测试用例管理</h3>
      <div class="action-group">
        <el-button type="primary" @click="generate">生成测试用例</el-button>
      </div>
      <div class="filter-group">
        <!-- 文档筛选 -->
        <el-select v-model="sourceFile" placeholder="选择接口文档" clearable @change="refreshCases">
          <el-option
            v-for="item in docFiles"
            :key="item.file_name"
            :label="item.file_name"
            :value="item.file_name"
          />
        </el-select>

        <!-- 排序选择 -->
        <el-select v-model="sortBy" placeholder="排序字段" style="width: 250px" @change="refreshCases">
          <el-option label="文件名" value="file_name" />
          <el-option label="更新时间" value="update_time" />
        </el-select>

        <el-select v-model="order" placeholder="顺序" style="width: 200px" @change="refreshCases">
          <el-option label="升序" value="asc" />
          <el-option label="降序" value="desc" />
        </el-select>

        <el-button type="success" @click="refreshCases">刷新</el-button>
      </div>
    </div>

    <!-- 用例表格 -->
    <el-card shadow="hover" class="mt-4">
      <el-table :data="cases" border stripe>
        <el-table-column type="index" label="#" width="50" />

        <el-table-column prop="file_name" label="用例名称" min-width="180" />
        <el-table-column prop="source_file" label="来源文档" min-width="180" />
        <el-table-column prop="update_time_str" label="更新时间" width="180" />

        <el-table-column label="操作" width="200" align="center">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="viewCase(row)">查看</el-button>
            <el-button size="small" type="warning" @click="editCase(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          background
          layout="prev, pager, next, jumper"
          :current-page="page"
          :page-size="size"
          :total="total"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 查看 YAML 弹窗 -->
    <el-dialog v-model="viewDialogVisible" title="查看 YAML 内容" width="60%">
      <pre class="yaml-view">{{ currentContent }}</pre>
      <template #footer>
        <el-button @click="viewDialogVisible=false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 编辑 YAML 弹窗 -->
    <el-dialog v-model="editDialogVisible" title="编辑 YAML" width="60%">
      <el-input
        type="textarea"
        v-model="editContent"
        :rows="20"
        resize="vertical"
      />
      <template #footer>
        <el-button @click="editDialogVisible=false">取消</el-button>
        <el-button type="primary" @click="saveCase">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";

// 数据
const docFiles = ref([]);
const cases = ref([]);

const page = ref(1);
const size = ref(10);
const total = ref(0);

const sortBy = ref("update_time");
const order = ref("desc");
const sourceFile = ref("");

const viewDialogVisible = ref(false);
const editDialogVisible = ref(false);

const currentFilePath = ref("");
const currentContent = ref("");
const editContent = ref("");

// 生命周期
onMounted(() => {
  loadDocFiles();
  refreshCases();
});
async function generate() {
  const res = await fetch("http://127.0.0.1:5000/api/generate_case");
  const data = await res.json();
}
// 获取接口文档列表
async function loadDocFiles() {
  const res = await fetch("http://127.0.0.1:5000/api/files");
  const data = await res.json();
  docFiles.value = data?.data?.files || [];
}

// 获取测试用例（分页 + 排序 + 筛选）
async function refreshCases() {
  const url = new URL("http://127.0.0.1:5000/api/cases");

  url.searchParams.append("page", page.value);
  url.searchParams.append("size", size.value);
  url.searchParams.append("sort_by", sortBy.value);
  url.searchParams.append("order", order.value);

  if (sourceFile.value) {
    url.searchParams.append("source_file", sourceFile.value);
  }

  const res = await fetch(url);
  const data = await res.json();

  cases.value = data?.data?.cases || [];
  total.value = data?.data?.total || 0;
}

// 分页切换
function handlePageChange(newPage) {
  page.value = newPage;
  refreshCases();
}

// 查看内容
async function viewCase(row) {
  currentFilePath.value = row.file_path;

  const res = await fetch(
    `http://127.0.0.1:5000/api/case_content?file_path=${encodeURIComponent(row.file_path)}`
  );

  const data = await res.json();

  currentContent.value = data.data.content;
  viewDialogVisible.value = true;
}

// 编辑用例
async function editCase(row) {
  currentFilePath.value = row.file_path;

  const res = await fetch(
    `http://127.0.0.1:5000/api/case_content?file_path=${encodeURIComponent(row.file_path)}`
  );

  const data = await res.json();
  editContent.value = data.data.content;

  editDialogVisible.value = true;
}

// 保存编辑后的 YAML
async function saveCase() {
  const res = await fetch("http://127.0.0.1:5000/api/save_case", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      file_path: currentFilePath.value,
      content: editContent.value,
    }),
  });

  const data = await res.json();

  if (data?.success) {
    ElMessage.success("保存成功！");
    editDialogVisible.value = false;
    refreshCases();
  } else {
    ElMessage.error("保存失败");
  }
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
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.mt-4 {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.yaml-view {
  background: #1e1e1e;
  color: #dcdcdc;
  padding: 15px;
  border-radius: 6px;
  max-height: 500px;
  overflow: auto;
}
</style>
