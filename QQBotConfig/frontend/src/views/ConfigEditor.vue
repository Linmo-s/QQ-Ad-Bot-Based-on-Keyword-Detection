<template>
  <div>
    <h2>Bot 配置管理</h2>

    <!-- 加载中提示 -->
    <div v-if="loading" style="color: #999; margin-bottom: 20px;">
      加载中...
    </div>

    <!-- 请求失败提示 -->
    <div v-if="error" style="color: red; margin-bottom: 20px;">
      请求配置失败：{{ error }}
    </div>

    <!-- 配置表单 -->
    <el-form v-if="config" label-width="120px">

      <!-- triggerCount -->
      <el-form-item label="触发次数">
        <el-input-number v-model="config.global_config.triggerCount" />
      </el-form-item>

      <!-- keywords -->
      <el-form-item label="关键词(空格分隔)">
        <el-input v-model="config.global_config.keywords" />
      </el-form-item>

      <!-- textMessage -->
      <el-form-item label="文本内容">
        <el-input type="textarea" v-model="config.global_config.textMessage" />
      </el-form-item>

      <!-- imagePath -->
      <el-form-item label="图片路径">
        <el-input v-model="config.global_config.imagePath" />
      </el-form-item>

      <!-- 目标群组 -->
      <h3>目标群组</h3>
      <el-button type="success" size="small" @click="addGroup" style="margin-bottom: 10px;">添加群组</el-button>

      <el-table :data="config.target_groups || []" style="width: 100%">
        <!-- 群号列 -->
        <el-table-column prop="id" label="群号" width="180">
          <template #default="{ row }">
            <el-input
              v-model="row.id"
              placeholder="请输入群号"
              style="width: 160px;"
              @input="row.id = row.id.replace(/\D/g,'')"
            ></el-input>
          </template>
        </el-table-column>

        <!-- 启用列 -->
        <el-table-column label="启用" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.enabled"></el-switch>
          </template>
        </el-table-column>

        <!-- 操作列 -->
        <el-table-column label="操作" width="100">
          <template #default="{ $index }">
            <el-button type="danger" size="small" @click="removeGroup($index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 保存按钮 -->
      <el-button type="primary" @click="saveConfig" style="margin-top: 20px">
        保存配置
      </el-button>

    </el-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// 数据
const config = ref(null);
const loading = ref(true);
const error = ref(null);

// 获取配置
onMounted(async () => {
  try {
    const res = await axios.get("http://localhost:8080/api/config");
    config.value = res.data;
  } catch (err) {
    console.error(err);
    error.value = err.message || "未知错误";
  } finally {
    loading.value = false;
  }
});

// 保存配置
const saveConfig = async () => {
  // 校验群号
  const ids = config.value.target_groups.map(g => g.id.toString());
  const hasEmpty = ids.some(id => !id || id === "0");
  const hasDuplicate = new Set(ids).size !== ids.length;

  if (hasEmpty) {
    return alert("群号不能为空或0");
  }
  if (hasDuplicate) {
    return alert("群号不能重复");
  }

  try {
    await axios.post("http://localhost:8080/api/config", config.value);
    alert("保存成功");
  } catch (err) {
    console.error(err);
    alert("保存失败：" + (err.message || "未知错误"));
  }
};

// 添加群组
const addGroup = () => {
  if (!config.value.target_groups) {
    config.value.target_groups = [];
  }
  config.value.target_groups.push({
    id: "",
    enabled: true
  });
};

// 删除群组
const removeGroup = (index) => {
  config.value.target_groups.splice(index, 1);
};
</script>

<style scoped>
h2 {
  margin-bottom: 20px;
}
h3 {
  margin-top: 30px;
  margin-bottom: 10px;
}
</style>
