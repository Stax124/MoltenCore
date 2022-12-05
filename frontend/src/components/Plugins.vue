<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <n-data-table
    :columns="columnsRef"
    :data="dataRef"
    :pagination="pagination"
    :bordered="false"
  />
</template>

<script lang="ts" setup>
import { NButton, NDataTable, type DataTableColumns } from "naive-ui";
import type { Type as ButtonType } from "naive-ui/es/button/src/interface";
import { h, reactive } from "vue";

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

const data: Plugin[] = [];

async function updateData() {
  const plugin_names = await (
    await fetch("http://localhost:8080/api/plugins")
  ).json();

  dataRef.splice(0, dataRef.length);

  for (const plugin_name of plugin_names) {
    const plugin = await (
      await fetch(`http://localhost:8080/api/plugins/status/${plugin_name}`)
    ).json();
    dataRef.push(plugin);
  }
}

const createColumns2 = ({
  openGitHub,
  togglePlugin,
  getStatusButtonType,
  getStatusText,
}: {
  openGitHub: (row: Plugin) => void;
  togglePlugin: (row: Plugin) => void;
  getStatusButtonType: (row: Plugin) => ButtonType;
  getStatusText: (row: Plugin) => string;
}): DataTableColumns<Plugin> => [
  {
    title: "Name",
    key: "name",
    sorter: "default",
  },
  {
    title: "Author",
    key: "author",
    sorter: "default",
  },
  {
    title: "GitHub",
    key: "repo_url",
    render(row) {
      return h(
        NButton,
        {
          type: "info",
          bordered: true,
          secondary: true,
          onClick: () => openGitHub(row),
          target: "_blank",
        },
        { default: () => "GitHub" }
      );
    },
    filter: "default",
  },
  {
    title: "Enabled",
    key: "enabled",
    render(row) {
      return h(
        NButton,
        {
          type: row.enabled ? "success" : "error",
          bordered: true,
          secondary: true,
          block: true,
          strong: true,
          onClick: () => togglePlugin(row),
        },
        { default: () => (row.enabled ? "Enabled" : "Disabled") }
      );
    },
  },
  {
    title: "Status",
    key: "status",
    render(row) {
      return h(
        NButton,
        {
          type: getStatusButtonType(row),
          bordered: true,
          secondary: true,
          block: true,
          style: "cursor: not-allowed",
        },
        { default: () => getStatusText(row) }
      );
    },
    filter: "default",
  },
];

let columns = createColumns2({
  openGitHub(row: Plugin) {
    window.open(row.repo_url);
  },
  togglePlugin(row: Plugin) {
    if (row.enabled) {
      fetch(`http://localhost:8080/api/plugins/disable-plugin/${row.name}`, {
        method: "POST",
      });
    } else {
      fetch(`http://localhost:8080/api/plugins/enable-plugin/${row.name}`, {
        method: "POST",
      });
    }

    fetch(`http://localhost:8080/api/plugins/status/${row.name}`)
      .then((res) => res.json())
      .then((plugin: Plugin) => {
        const index = dataRef.findIndex((p) => p.name === plugin.name);
        dataRef.splice(index, 1, plugin);
      });
  },
  getStatusButtonType(row: Plugin) {
    if (row.empty) {
      return "error";
    } else if (row.exists) {
      return "success";
    } else {
      return "warning";
    }
  },
  getStatusText(row: Plugin) {
    if (row.empty) {
      return "Empty";
    } else if (row.exists) {
      return "Exists";
    } else {
      return "Missing";
    }
  },
});

const columnsRef = reactive(columns);
const dataRef = reactive(data);
const pagination = reactive({ pageSize: 10 });
updateData();
</script>

<style>
/* .xxx {
  cursor: ;
} */
</style>
