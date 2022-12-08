<template>
  <NSpace justify="end" inline align="center" class="top-bar">
    <NButton
      :type="syncType"
      ghost
      icon-placement="left"
      :render-icon="syncIcon"
      @click="sync"
      :loading="syncLoading"
      >Sync</NButton
    >
    <NAvatar src="/api/bot/icon" size="large" circle class="logo" />
  </NSpace>
</template>

<script lang="ts" setup>
import { SyncSharp } from "@vicons/ionicons5";
import { NAvatar, NButton, NSpace } from "naive-ui";
import type { Type as ButtonType } from "naive-ui/es/button/src/interface";
import { h, ref } from "vue";

let syncType: ButtonType = "primary";

const syncLoading = ref(false);
const syncIcon = () => {
  return h(SyncSharp);
};

async function sync() {
  syncLoading.value = true;
  await fetch("/api/system/sync-slash-commands", {
    method: "POST",
  }).catch(() => {
    syncLoading.value = false;
    syncType = "error";
  });
  syncLoading.value = false;
}
</script>

<style scoped>
.top-bar {
  border-bottom: #505050 1px solid;
  padding-top: 10px;
  padding-bottom: 10px;
  width: 100%;
}

.logo {
  margin-right: 16px;
  margin-left: 16px;
}
</style>
