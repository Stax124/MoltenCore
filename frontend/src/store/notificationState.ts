import { serverUrl } from "@/env";
import type { NotificationApiInjection } from "naive-ui/es/notification/src/NotificationProvider";
import { defineStore } from "pinia";
import { reactive } from "vue";
import type { NotificationMessage } from "./../websockets/websockets";

const data: NotificationMessage[] = [];
fetch(`${serverUrl}/api/notifications`, {
  cache: "no-store",
}).then((r) => r.json().then((d) => data.push(...d)));

const notifications: NotificationMessage[] = reactive(data);

export const useNotificationState = defineStore("notification", () => {
  const push = (
    n: NotificationMessage,
    notification_effect: NotificationApiInjection
  ) => {
    notifications.push(n);
    notification_effect[n.severity]({
      title: n.message,
      duration: n.timeout,
    });
  };

  return { notifications, push };
});
