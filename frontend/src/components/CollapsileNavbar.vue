<template>
  <nav class="vertical-nav">
    <ul>
      <li v-for="item in items" :key="item.id">
        <a :href="item.url" class="nav-toplevel">{{ item.name }}</a>
        <ul v-if="item.children">
          <li v-for="child in item.children" :key="child.id">
            <a :href="child.url">{{ child.name }}</a>
          </li>
        </ul>
      </li>
    </ul>
  </nav>
</template>

<script lang="ts">
import type { PropType } from "vue";

interface Item {
  id: number;
  name: string;
  url: string;
  children?: Item[];
}

export default {
  name: "VerticalNav",
  props: {
    items: {
      type: Array as PropType<Item[]>,
      required: true,
    },
  },
};
</script>

<style>
.vertical-nav {
  /* Set the width and height of the navigation bar */
  width: 200px;
  height: 100%;

  /* Add a background color and some padding */
  padding: 20px;

  /* Green box around it */
  border-right: 1px solid #109f7e;

  position: fixed;
  top: 0;
  left: 0;

  overflow: hidden;

  z-index: 1;
}

.vertical-nav ul {
  /* Reset the default list styles */
  list-style: none;
  margin: 0;
  padding: 0;
}

.vertical-nav a {
  /* Add some styles for the navigation links */
  text-decoration: none;
  font-size: 20px;
  font-weight: 450;
}

.vertical-nav li {
  margin: 5px 0px;
}

.vertical-nav .nav-toplevel {
  /* Add some styles for the top-level navigation links */
  display: block;
  padding: 10px 3px;
}

.vertical-nav .nav-toplevel:hover {
  border-radius: 8px;
  border: 1px;
}
</style>
