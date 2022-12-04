<template>
  <NConfigProvider :theme="darkTheme">
    <NMessageProvider>
      <CollapsileNavbarVue />
      <routerContainerVue />
      <NBackTop :right="100" />
    </NMessageProvider>
  </NConfigProvider>
</template>

<script setup lang="ts">
import {
  darkTheme,
  NBackTop,
  NConfigProvider,
  NMessageProvider,
} from "naive-ui";
import CollapsileNavbarVue from "./components/CollapsileNavbar.vue";
import routerContainerVue from "./core/router-container.vue";
</script>
