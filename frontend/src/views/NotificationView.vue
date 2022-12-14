<template>
  <div class="alerts">
    <NAlert
      v-for="n in notificationState.$state.notifications"
      v-bind:key="n.id"
      :title="n.title"
      :type="n.severity"
      closable
      :bordered="false"
      :on-close="() => clearNotification(n.id)"
    >
      {{ n.message }}
    </NAlert>
  </div>
</template>

<script lang="ts" setup>
import { serverUrl } from "@/env";
import { useNotificationState } from "@/store/notificationState";
import { NAlert } from "naive-ui";

const notificationState = useNotificationState();

function clearNotification(id: number) {
  notificationState.notifications.filter((n) => n.id !== id);
  fetch(`${serverUrl}/api/notifications/clear/${id}`, {
    method: "POST",
  });
  return true;
}
</script>

<style scoped>
.alerts {
  margin: 16px;
}

.n-alert:not(:last-child) {
  margin-bottom: 8px;
}
</style>
