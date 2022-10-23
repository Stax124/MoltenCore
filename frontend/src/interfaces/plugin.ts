export interface PluginInterface {
	id: number;
	enabled: boolean;
	repo_url: string;
	name: string;
	author: string;
	stars: number;
	forks: number;
	issues: number;
	license: string;
	traceback: string;
	short_traceback: string;
	exists: boolean;
	empty: boolean;
}
