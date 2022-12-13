<template>
  <div class="container">
    <NCard title="System" hoverable class="layout-card">
      <NSpace>
        <NCard
          class="content-card"
          hoverable
          :segmented="{ content: true }"
          title="Uptime"
          style="--n-title-text-color: hsla(160, 100%, 37%, 1)"
        >
          <NSkeleton v-if="loading" text />
          <template v-else>
            <p>{{ systemStats.uptime }}</p>
          </template>
        </NCard>
      </NSpace>
    </NCard>
    <NCard title="Plugins" hoverable class="layout-card">
      <NSpace>
        <NCard
          class="content-card"
          hoverable
          :segmented="{ content: true }"
          title="Enabled"
          style="--n-title-text-color: hsla(160, 100%, 37%, 1)"
        >
          <NSkeleton v-if="loading" text />
          <template v-else>
            <p>{{ pluginStats.enabled }}</p>
          </template>
        </NCard>
        <NCard
          class="content-card"
          hoverable
          :segmented="{ content: true }"
          title="Disabled"
          style="--n-title-text-color: rgb(255, 150, 0)"
        >
          <NSkeleton v-if="loading" text />
          <template v-else>
            <p>{{ pluginStats.disabled }}</p>
          </template>
        </NCard>
        <NCard
          class="content-card"
          hoverable
          :segmented="{ content: true }"
          title="Total"
        >
          <NSkeleton v-if="loading" text />
          <template v-else>
            <p>{{ pluginStats.total }}</p>
          </template>
        </NCard>
      </NSpace>
    </NCard>
  </div>
</template>

<script setup lang="ts">
import { serverUrl } from "@/env";
import { NCard, NSkeleton, NSpace } from "naive-ui";
import { ref } from "vue";

interface PluginStats {
  total: number;
  enabled: number;
  disabled: number;
}

interface SystemStats {
  uptime: string;
}

const pluginStats = ref<PluginStats>({
  total: 0,
  enabled: 0,
  disabled: 0,
});
const systemStats = ref<SystemStats>({
  uptime: "",
});

const loading = ref(true);

fetch(`${serverUrl}/api/system/uptime`)
  .then((res) => res.json())
  .then((data: string) => {
    systemStats.value.uptime = data;
    loading.value = false;
  });

fetch(`${serverUrl}/api/plugins/stats`)
  .then((res) => res.json())
  .then((data: PluginStats) => {
    pluginStats.value = data;
    loading.value = false;
  });
</script>

<style scoped>
.content-card {
  max-width: 400px;
  min-width: 200px;
}
.container {
  margin: 24px;
}

.layout-card:not(:last-child) {
  margin-bottom: 24px;
}

p {
  margin: 0;
}
</style>
