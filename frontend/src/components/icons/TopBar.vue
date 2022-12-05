<template>
  <NSpace vertical class="top-bar">
    <NAvatar
      src="http://localhost:8080/api/bot/icon"
      size="large"
      circle
      class="logo"
    />
  </NSpace>
</template>

<script lang="ts" setup>
import { NAvatar, NSpace } from "naive-ui";
</script>

<style scoped>
.top-bar {
  background-color: #18181c;
  border-bottom: #505050 1px solid;
  align-items: flex-end;
  padding-right: 16px;
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>
