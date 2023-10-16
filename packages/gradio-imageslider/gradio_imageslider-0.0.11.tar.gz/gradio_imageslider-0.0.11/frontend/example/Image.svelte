<script lang="ts">
	export let value: [string, string];
	export let samples_dir: string;
	export let type: "gallery" | "table";
	export let selected = false;

	$: console.log(value, samples_dir);
</script>

<!-- TODO: fix -->
<!-- svelte-ignore a11y-missing-attribute -->
<img
	src={samples_dir + value[0]}
	class:table={type === "table"}
	class:gallery={type === "gallery"}
	class:selected
/>

<img
	src={samples_dir + value[1]}
	class:table={type === "table"}
	class:gallery={type === "gallery"}
	class:selected
/>

<style>
	img {
		border-radius: var(--radius-lg);
		max-width: none;
	}

	img.selected {
		border-color: var(--border-color-accent);
	}

	.table {
		margin: 0 auto;
		border: 2px solid var(--border-color-primary);
		border-radius: var(--radius-lg);
		width: var(--size-20);
		height: var(--size-20);
		object-fit: cover;
	}

	.gallery {
		border: 2px solid var(--border-color-primary);
		max-height: var(--size-20);
		object-fit: cover;
	}
</style>
