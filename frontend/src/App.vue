<template>
  <CollapsileNavbarVue :items="navbarItems" />
  <NConfigProvider :theme="darkTheme">
    <routerContainerVue />
  </NConfigProvider>
</template>

<script setup lang="ts">
import { darkTheme, NConfigProvider } from "naive-ui";
import CollapsileNavbarVue from "./components/CollapsileNavbar.vue";
import routerContainerVue from "./core/router-container.vue";

const navbarItems = [
  {
    id: 1,
    name: "Home",
    url: "/",
  },
  {
    id: 2,
    name: "About",
    url: "/about",
  },
  {
    id: 3,
    name: "Contact",
    url: "/contact",
  },
  {
    id: 4,
    name: "Products",
    url: "/products",
  },
];
</script>
