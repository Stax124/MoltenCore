import { serverUrl } from "@/env";
import type { NotificationApiInjection } from "naive-ui/es/notification/src/NotificationProvider";
import { defineStore } from "pinia";
import { reactive } from "vue";
import type { NotificationMessage } from "./../websockets/websockets";

const data: NotificationMessage[] = await fetch(
  `${serverUrl}/api/notifications`
).then((r) => r.json());

console.info("notifications", data);

const notifications: NotificationMessage[] = reactive(data);

export const useNotificationState = defineStore("notification", {
  state: () => {
    return { notifications };
  },
  actions: {
    push(
      n: NotificationMessage,
      notification_effect: NotificationApiInjection
    ) {
      notifications.push(n);
      notification_effect[n.severity]({
        title: n.message,
        duration: n.timeout,
      });
    },
  },
});
