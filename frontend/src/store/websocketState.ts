import { webSocketUrl } from "@/env";
import {
  processWebSocket,
  type WebSocketMessage,
} from "@/websockets/websockets";
import { useWebSocket } from "@vueuse/core";
import type { NotificationApiInjection } from "naive-ui/es/notification/src/NotificationProvider";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useWebsocket = defineStore("websocket", () => {
  let useNotification: NotificationApiInjection | null = null;
  const websocket = useWebSocket(`${webSocketUrl}/api/websockets/master`, {
    autoReconnect: true,
    heartbeat: {
      message: "ping",
      interval: 30000,
    },
    onConnected: () => {
      console.log("MASTER Websocket connected");
    },
    onMessage: (ws: WebSocket, event: MessageEvent) => {
      console.info(event.data);
      if (event.data === "pong") {
        return;
      }
      const data = JSON.parse(event.data) as WebSocketMessage;
      if (useNotification === null) {
        console.error("Notification handler not injected");
        return;
      }
      processWebSocket(data, useNotification);
    },
    onError: (ws: WebSocket, event: Event) => {
      console.error("MASTER Websocket error");
      console.error(event);
    },
    onDisconnected: (ws: WebSocket, event: CloseEvent) => {
      console.log("MASTER Websocket disconnected");
      console.log(event);
    },
  });
  console.log("MASTER Websocket created");

  function ws_text() {
    switch (readyState.value) {
      case "CLOSED":
        return "Closed";
      case "CONNECTING":
        return "Connecting";
      case "OPEN":
        return "Connected";
    }
  }

  function injectNotificationHanler(
    notification_effect: NotificationApiInjection
  ) {
    useNotification = notification_effect;
  }

  function get_color() {
    switch (readyState.value) {
      case "CLOSED":
        return "error";
      case "CONNECTING":
        return "warning";
      case "OPEN":
        return "success";
    }
  }

  const readyState = ref(websocket.status);
  const loading = computed(() => readyState.value === "CONNECTING");
  const text = computed(() => ws_text());
  const color = computed(() => get_color());

  return {
    websocket,
    readyState,
    loading,
    text,
    ws_open: websocket.open,
    injectNotificationHanler,
    color,
  };
});
