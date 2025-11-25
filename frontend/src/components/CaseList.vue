<template>
  <el-card class="list-card">
    <h3>📂 历史用例集</h3>

    <el-scrollbar height="600px">
      <div
        v-for="item in cases"
        :key="item.timestamp"
        class="case-item"
        @click="$emit('select', item)"
      >
        <div>
          <strong>{{ item.title }}</strong>
          <div class="small">{{ item.timestamp }}</div>
        </div>

        <div>
          <el-tag type="info">{{ item.count }} 条</el-tag>
          <el-button
            type="danger"
            size="small"
            @click.stop="$emit('delete', item.timestamp)"
            >删除</el-button
          >
        </div>
      </div>
    </el-scrollbar>
  </el-card>
</template>

<script setup>
defineProps(["cases"]);
</script>

<style scoped>
.list-card {
  width: 35%;
}
.case-item {
  padding: 12px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
}
.case-item:hover {
  background: #f0f0f5;
}
.small {
  font-size: 12px;
  color: #999;
}
</style>
    