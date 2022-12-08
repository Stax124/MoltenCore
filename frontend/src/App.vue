<template>
  <NConfigProvider :theme="darkTheme">
    <NMessageProvider>
      <CollapsileNavbarVue />
      <TopBarVue />
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
import TopBarVue from "./components/TopBar.vue";
import routerContainerVue from "./core/router-container.vue";
</script>
