<template>
  <el-card class="detail-card">
    <h3>📄 用例详情</h3>

    <pre class="json">{{ formatted }}</pre>
  </el-card>
</template>

<script setup>
const props = defineProps(["detail"]);

const formatted = computed(() =>
  JSON.stringify(props.detail, null, 2)
);
</script>

<style scoped>
.detail-card {
  width: 65%;
  white-space: pre-wrap;
}
.json {
  background: #1e1e1e;
  color: #dcdcdc;
  padding: 15px;
  border-radius: 8px;
  height: 600px;
  overflow: auto;
}
</style>
