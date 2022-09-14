<template>
	<NavbarTop />
	<div class="view-container">
		<NavbarLeft />
		<router-view />
	</div>
</template>

<script lang="ts">
import NavbarLeft from "./components/NavbarLeft.vue";
import NavbarTop from "./components/NavbarTop.vue";

export default {
	name: "App",
	components: {
		NavbarTop,
		NavbarLeft,
	},
};
</script>

<style>
:root {
	--element-spacing: 0.5rem;
}

.view-container {
	display: flex;
	flex-direction: row;
}
</style>
