<template>
	<table>
		<thead>
			<tr>
				<th>Name</th>
				<th>Author</th>
				<th>License</th>
				<th>URL</th>
				<th>Path</th>
				<th>Enabled</th>
				<th>Actions</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="plugin of plugins" :key="plugin.name">
				<td>{{ plugin.name }}</td>
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
		</tbody>
	</table>
</template>

<script lang="ts">
import { PluginInterface } from "../interfaces/plugin";
const plugins: PluginInterface[] = [];

fetch("http://localhost:8080/plugins")
	.then((response) => response.json())
	.then((data: string[]) => {
		for (const plugin of data) {
			fetch(`http://localhost:8080/plugins/plugin/${plugin}`)
				.then((response) => response.json())
				.then((data: PluginInterface) => {
					plugins.push(data);
				});
		}
	});
// .then((data: PluginInterface[]) => {
// 	for (const plugin of data) {
// 		plugins.push(plugin);
// 	}

console.log(plugins);

export default {
	name: "Plugins",
	data() {
		return {
			plugins,
		};
	},
};
</script>
