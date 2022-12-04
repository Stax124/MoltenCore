<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <n-data-table
    :columns="columnsRef"
    :data="dataRef"
    :pagination="false"
    :bordered="false"
  />
  <NButton @click="updateData">Update</NButton>
</template>

<script lang="ts" setup>
import {
  NButton,
  NDataTable,
  useMessage,
  type DataTableColumns,
} from "naive-ui";
import { reactive } from "vue";

type Plugin = {
  id: number;
  enabled: boolean;
  repo_url: string;
  name: string;
  author: string;
  stars: number;
  forks: number;
  issues: number;
  license: string;
  traceback: string;
  short_traceback: string;
  exists: boolean;
  empty: boolean;
};

const data: Plugin[] = [
  {
    enabled: true,
    traceback: "Traceback",
    short_traceback: "Traceback",
    author: "Author",
    stars: 1,
    empty: false,
    exists: true,
    forks: 1,
    id: 1,
    issues: 1,
    license: "MIT",
    name: "Name",
    repo_url: "",
  },
  {
    enabled: true,
    traceback: "Traceback",
    short_traceback: "Traceback",
    author: "Author",
    stars: 1,
    empty: false,
    exists: true,
    forks: 1,
    id: 1,
    issues: 1,
    license: "MIT",
    name: "Name",
    repo_url: "",
  },
];

const message = useMessage();

function updateData() {
  message.info("Updating data");
  dataRef[0].name = "New Name";
}

const createColumns2 = (): DataTableColumns => [
  {
    title: "Name",
    key: "name",
  },
  {
    title: "Author",
    key: "author",
  },
  {
    title: "Stars",
    key: "stars",
  },
  {
    title: "Forks",
    key: "forks",
  },
  {
    title: "Issues",
    key: "issues",
  },
  {
    title: "License",
    key: "license",
  },
  {
    title: "Enabled",
    key: "enabled",
  },
];

let columns = createColumns2();

const columnsRef = reactive(columns);
const dataRef = reactive(data);
</script>
