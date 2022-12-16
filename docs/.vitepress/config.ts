import { defineConfig } from "vitepress";

export default defineConfig({
	title: "MoltenCore",
	description: "Easy to use Discord bot that can be extended with plugins",
	lang: "en-US",
	appearance: true,
	lastUpdated: true,
	base: "/MoltenCore/",
	themeConfig: {
		sidebar: [
			{
				text: "Introduction",
				items: [{ text: "Introduction", link: "/" }],
				collapsible: true,
			},
		],
		editLink: {
			pattern: "https://github.com/Stax124/MoltenCore/edit/main/docs/:path",
		},
		socialLinks: [
			{
				icon: "github",
				link: "https://github.com/Stax124/MoltenCore",
			},
		],
	},
});
