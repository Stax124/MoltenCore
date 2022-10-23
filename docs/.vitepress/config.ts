import { defineConfig } from "vitepress";

export default defineConfig({
	title: "Modular-Discord-Bot",
	description: "Easy to use Discord bot that can be extended with plugins",
	lang: "en-US",
	appearance: true,
	lastUpdated: true,
	base: "/Modular-Discord-Bot/",
	themeConfig: {
		sidebar: [
			{
				text: "Introduction",
				items: [{ text: "Introduction", link: "/" }],
				collapsible: true,
			},
		],
		editLink: {
			pattern:
				"https://github.com/Stax124/Modular-Discord-Bot/edit/main/docs/:path",
		},
		socialLinks: [
			{
				icon: "github",
				link: "https://github.com/Stax124/Modular-Discord-Bot",
			},
		],
	},
});
