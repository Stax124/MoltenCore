<template>
  <NSpace justify="end" inline align="center" class="top-bar">
    <NButton
      :type="(syncState.$state.syncState as ButtonType)"
      ghost
      icon-placement="left"
      :render-icon="syncIcon"
      @click="sync"
      :loading="syncLoading"
      >Sync</NButton
    >
    <NAvatar
      src="http://localhost:8080/api/bot/icon"
      size="large"
      circle
      class="logo"
    />
  </NSpace>
</template>

<script lang="ts" setup>
import { useSyncState } from "@/store/syncState";
import { SyncSharp } from "@vicons/ionicons5";
import { NAvatar, NButton, NSpace } from "naive-ui";
import type { Type as ButtonType } from "naive-ui/es/button/src/interface";
import { h, ref } from "vue";

const syncState = useSyncState();

const syncLoading = ref(false);
const syncIcon = () => {
  return h(SyncSharp);
};

async function sync() {
  syncLoading.value = true;
  await fetch("http://localhost:8080/api/system/sync-slash-commands", {
    method: "POST",
  })
    .catch((e) => {
      console.log(e);
      syncLoading.value = false;
      syncState.setError();
    })
    .then(() => {
      syncLoading.value = false;
      syncState.clearSync();
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
