import ChakraUIVuePlugin, { chakra } from "@chakra-ui/vue-next";
import { domElements } from "@chakra-ui/vue-system";
import { createApp } from "vue";
import { createRouter, createWebHashHistory } from "vue-router";
import Home from "./views/Home.vue";
import Plugins from "./views/Plugins.vue";
import App from "./App.vue";

const routes = [
	{ path: "/", component: Home, name: "Home" },
	{ path: "/plugins", component: Plugins, name: "Plugins" },
];

const router = createRouter({
	history: createWebHashHistory(),
	routes,
});

const app = createApp(App);

app.use(router);
app.use(ChakraUIVuePlugin);

domElements.forEach((tag) => {
	app.component(`chakra.${tag}`, chakra(tag));
});

app.mount("#app");
