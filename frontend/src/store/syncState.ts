import { defineStore } from "pinia";

export const useSyncState = defineStore("sync", {
  state: () => {
    return { syncState: "primary" };
  },
  actions: {
    setNeedsSync() {
      this.syncState = "warning";
    },
    clearSync() {
      this.syncState = "primary";
    },
    setError() {
      this.syncState = "error";
    },
  },
});
