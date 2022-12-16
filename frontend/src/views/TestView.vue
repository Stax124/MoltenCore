<template>
  <NButton @click="value">{{ len.length }}</NButton>
</template>

<script setup lang="ts">
import { NButton } from "naive-ui";
import { reactive } from "vue";
import { useNotificationState } from "../store/notificationState";
const state = useNotificationState();

const value = () => console.log(state.notifications.length);
const len = reactive(state.notifications);
</script>
