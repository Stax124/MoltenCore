<template>
	<div class="navbar-left">
		<ul>
			<li>
				<router-link to="/">
					<CIconButton icon="home" />
				</router-link>
			</li>
			<li>
				<router-link to="/">
					<CIconButton icon="home" />
				</router-link>
			</li>
			<li>
				<router-link to="/">
					<CIconButton icon="" />
				</router-link>
			</li>
			<li>
				<router-link to="/">
					<CIconButton icon="" />
				</router-link>
			</li>
		</ul>
	</div>
</template>

<script lang="ts">
import { CIconButton } from "@chakra-ui/vue-next";

export default {
	name: "NavbarLeft",
	components: {
		CIconButton,
	},
};
</script>

<style>
:root {
	--x-spacing: 0px;
	--y-spacing: 0px;
}

.navbar-left {
	display: flex;
	flex-direction: column;
	height: 100%;
	background-color: aqua;
}

li {
	margin-left: var(--x-spacing);
	margin-right: var(--x-spacing);
	margin-bottom: var(--y-spacing);
}

li:first {
	margin-top: 0px;
}

ul {
	list-style-type: none;
}
</style>
