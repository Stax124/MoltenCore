import { serverUrl } from "@/env";
import type { NotificationApiInjection } from "naive-ui/es/notification/src/NotificationProvider";
import { defineStore } from "pinia";
import { computed, reactive } from "vue";
import type { NotificationMessage } from "./../websockets/websockets";

export const useNotificationState = defineStore("notification", () => {
  const notifications: NotificationMessage[] = reactive(new Array());
  fetch(`${serverUrl}/api/notifications`, {
    cache: "no-store",
  }).then((r) => r.json().then((d) => notifications.push(...d)));

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

  const remove = (n: NotificationMessage) => {
    notifications.splice(notifications.indexOf(n), 1);
    fetch(`${serverUrl}/api/notifications/clear/${n.id}`, {
      method: "POST",
    });
    return true;
  };

  const lenght = computed(() => notifications.length);

  return { notifications, push, lenght, remove };
});
