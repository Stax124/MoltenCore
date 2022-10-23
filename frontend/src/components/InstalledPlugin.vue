<template>
	<tr>
		<td>{{ plugin.name }}</td>
		<td>{{ plugin.version }}</td>
		<td>{{ plugin.description }}</td>
		<td>{{ plugin.author }}</td>
		<td>{{ plugin.license }}</td>
		<td>{{ plugin.url }}</td>
		<td>{{ plugin.path }}</td>
		<td>{{ plugin.enabled }}</td>
		<td>
			<button v-if="plugin.enabled" @click="disablePlugin(plugin)">
				Disable
			</button>
			<button v-else @click="enablePlugin(plugin)">Enable</button>
		</td>
	</tr>
</template>

<script lang="ts">
import { PluginInterface } from "../interfaces/Plugin";

export default {
	name: "InstalledPlugin",
	props: {
		plugin: Object as () => PluginInterface,
	},
	methods: {
		enablePlugin(plugin: PluginInterface) {
			//
		},
		disablePlugin(plugin: PluginInterface) {
			//
		},
		updatePlugin(plugin: PluginInterface) {
			//
		},
	},
};
</script>
