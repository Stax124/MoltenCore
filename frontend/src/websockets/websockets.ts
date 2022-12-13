import { useNotificationState } from "@/store/notificationState";
import type { NotificationApiInjection } from "naive-ui/es/notification/src/NotificationProvider";

export interface NotificationMessage {
  severity: "success" | "info" | "warning" | "error";
  title: string;
  timestamp: string;
  message: string;
  timeout: number;
  id: number;
}

export interface WebSocketMessage {
  type: string;
  data: any;
}

export function processWebSocket(
  message: WebSocketMessage,
  notification_effect: NotificationApiInjection
): void {
  if (message.type === "notification") {
    const notificationState = useNotificationState();
    const n = message.data as NotificationMessage;

    console.info("Received notification", n);

    notificationState.push(n, notification_effect);
  } else {
    console.log("Received unknown message", message);
    console.log("Type", message.type);
  }
}

// const x: WebSocketMessage = {
//   type: "notification",
//   data: {
//     severity: "success",
//     message: "Hello world from from test plugin",
//     timeout: 0,
//   },
// };
