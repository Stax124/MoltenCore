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
        <NSpace vertical justify="space-between" style="height: 100%">
          <n-menu
            :collapsed="collapsed"
            :collapsed-width="64"
            :collapsed-icon-size="22"
            :options="menuOptionsMain"
          />
        </NSpace>
      </n-layout-sider>
    </n-layout>
  </div>
</template>

<script lang="ts" setup>
import { useNotificationState } from "@/store/notificationState";
import {
  ExtensionPuzzle,
  Home,
  InformationCircle,
  Notifications,
  StatsChart,
  Warning,
} from "@vicons/ionicons5";
import type { MenuOption } from "naive-ui";
import { NBadge, NIcon, NLayout, NLayoutSider, NMenu, NSpace } from "naive-ui";
import type { Component } from "vue";
import { h, ref } from "vue";
import { RouterLink } from "vue-router";

const notificationState = useNotificationState();

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) });
}

function renderNotification() {
  return () =>
    h(
      NBadge,
      { value: notificationState.$state.notifications.length },
      {
        default: () =>
          h(NIcon, { color: "white" }, { default: () => h(Notifications) }),
      }
    );
}

const menuOptionsMain: MenuOption[] = [
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
    label: () => h(RouterLink, { to: "/test" }, { default: () => "Test" }),
    key: "test",
    icon: renderIcon(Warning),
  },
  {
    label: () =>
      h(
        RouterLink,
        { to: "/notifications" },
        { default: () => "Notifications" }
      ),
    key: "notifications",
    icon: renderNotification(),
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
