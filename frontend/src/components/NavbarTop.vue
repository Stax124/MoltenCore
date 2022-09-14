<template>
	<div class="navbar">
		<div class="icon-container">
			<router-link to="/">
				<CIconButton icon="" />
			</router-link>
		</div>
		<div class="content-container">
			<router-link to="/">
				<CButton variant="ghost">Home</CButton>
			</router-link>

			<router-link to="/plugins">
				<CButton variant="ghost">Plugins</CButton>
			</router-link>
		</div>
	</div>
</template>

<script lang="ts">
import { CButton, CFlex, CIconButton, CText } from "@chakra-ui/vue-next";

export default {
	name: "Navbar",
	components: {
		CFlex,
		CButton,
		CIconButton,
		CText,
	},
};
</script>

<style>
.navbar {
	box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
	padding: 0.5rem 1rem;
	display: flex;
	justify-content: space-between;
	width: 100%;
	height: min(65px);
	align-items: center;
}

.icon {
	height: 50px;
	width: auto;
}

.content-container {
	align-items: center;
}

.content-container:first-child {
	margin-right: 1rem;
}

.content-container:last-child {
	margin-left: 1rem;
}

.content-container > * {
	margin-left: var(--element-spacing);
	margin-right: var(--element-spacing);
}
</style>
