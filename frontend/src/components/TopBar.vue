<template>
  <NSpace justify="end" inline align="center" class="top-bar">
    <NButton
      :type="(syncState.$state.syncState as ButtonType)"
      quaternary
      icon-placement="left"
      :render-icon="syncIcon"
      @click="sync"
      :loading="syncLoading"
      >{{
        syncState.$state.syncState == "primary" ? "Synced" : "Click to sync"
      }}</NButton
    >
    <NButton
      :type="(syncState.$state.syncState as ButtonType)"
      quaternary
      icon-placement="left"
      :render-icon="syncIcon"
      :loading="websocketState.loading"
      @click="websocketState.ws_open"
      >{{ websocketState.text }}</NButton
    >
    <NAvatar :src="iconLink" size="large" circle class="logo" />
  </NSpace>
</template>

<script lang="ts" setup>
import { useSyncState } from "@/store/syncState";
import { useWebsocket } from "@/store/websocketState";
import { SyncSharp } from "@vicons/ionicons5";
import { NAvatar, NButton, NSpace, useNotification } from "naive-ui";
import type { Type as ButtonType } from "naive-ui/es/button/src/interface";
import { h, ref } from "vue";
import { serverUrl } from "../env";

const iconLink = serverUrl + "/api/bot/icon";

const notification = useNotification();
const syncState = useSyncState();
const websocketState = useWebsocket();

const syncLoading = ref(false);
const syncIcon = () => {
  return h(SyncSharp);
};

async function sync() {
  syncLoading.value = true;
  await fetch(`${serverUrl}/api/system/sync-slash-commands`, {
    method: "POST",
  })
    .catch((e) => {
      console.log(e);
      syncLoading.value = false;
      syncState.setError();
      notification.error({
        title: "Error",
        description: "Error syncing slash commands",
        duration: 2000,
      });
    })
    .then(() => {
      syncLoading.value = false;
      syncState.clearSync();
      notification.success({
        title: "Success",
        description: "Successfully synced slash commands",
        duration: 2000,
      });
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
  background-color: rgb(24, 24, 28, 0.6);
}

.logo {
  margin-right: 16px;
  margin-left: 16px;
}
</style>
