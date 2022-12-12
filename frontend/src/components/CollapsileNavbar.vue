<template>
  <div class="navbar">
    <n-layout style="height: 100%" has-sider>
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="240"
        :collapsed="collapsed"
        @collapse="collapsed = true"
        @expand="collapsed = false"
        style="height: 100%"
      >
        <n-menu
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="menuOptions"
          style="height: 100%"
        />
      </n-layout-sider>
    </n-layout>
  </div>
</template>

<script lang="ts" setup>
import {
  ExtensionPuzzle,
  Home,
  InformationCircle,
  StatsChart,
} from "@vicons/ionicons5";
import type { MenuOption } from "naive-ui";
import { NIcon, NLayout, NLayoutSider, NMenu } from "naive-ui";
import type { Component } from "vue";
import { h, ref } from "vue";
import { RouterLink } from "vue-router";

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) });
}

const menuOptions: MenuOption[] = [
  {
    label: () => h(RouterLink, { to: "/" }, { default: () => "Home" }),
    key: "home",
    icon: renderIcon(Home),
  },
  {
    label: () =>
      h(RouterLink, { to: "/plugins" }, { default: () => "Plugins" }),
    key: "plugins",
    icon: renderIcon(ExtensionPuzzle),
  },
  {
    label: () => h(RouterLink, { to: "/stats" }, { default: () => "Stats" }),
    key: "stats",
    icon: renderIcon(StatsChart),
  },
  {
    label: () => h(RouterLink, { to: "/about" }, { default: () => "About" }),
    key: "about",
    icon: renderIcon(InformationCircle),
  },
];

let collapsed = ref(true);
</script>

<style>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  z-index: 1000;
}
</style>