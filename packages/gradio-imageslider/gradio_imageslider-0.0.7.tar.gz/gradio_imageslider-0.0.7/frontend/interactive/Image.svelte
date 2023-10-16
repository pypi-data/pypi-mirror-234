<script lang="ts">
	import Slider from "../shared/Slider.svelte";
	import { createEventDispatcher, tick, onMount } from "svelte";
	import { BlockLabel } from "@gradio/atoms";
	import { Image, Sketch as SketchIcon } from "@gradio/icons";
	import type { SelectData, I18nFormatter } from "@gradio/utils";
	import { get_coordinates_of_clicked_image } from "../shared/utils";

	import {
		Upload,
		ModifyUpload,
		type FileData,
		normalise_file
	} from "@gradio/upload";

	export let value: [FileData | null, FileData | null];

	export let label: string | undefined = undefined;
	export let show_label: boolean;
	export let pending = false;
	export let root: string;
	export let i18n: I18nFormatter;

	function handle_upload({ detail }: CustomEvent<string[]>, n: number): void {
		if (detail.length > 1) {
			value[0] = normalise_file(detail[0], root, null);
			value[1] = normalise_file(detail[1], root, null);
		} else {
			value[n] = normalise_file(detail[0], root, null);
		}

		dispatch("upload", value[n]);
	}

	const dispatch = createEventDispatcher<{
		change: string | null;
		stream: string | null;
		edit: undefined;
		clear: undefined;
		drag: boolean;
		upload: FileData;
		select: SelectData;
	}>();

	let dragging = false;

	$: dispatch("drag", dragging);

	$: console.log(value);
</script>

<BlockLabel {show_label} Icon={Image} label={label || "Image"} />

<div data-testid="image" class="image-container">
	<Slider position={0.5} disabled>
		<div class="upload-wrap">
			{#if !value[0]}
				<Upload
					bind:dragging
					filetype="image/*"
					on:load={(e) => handle_upload(e, 0)}
					disable_click={!!value?.[0]}
					{root}
					file_count="multiple"
				>
					<slot />
				</Upload>
			{:else}
				<img src={value[0].data} alt="" />
			{/if}

			{#if !value[1]}
				<Upload
					bind:dragging
					filetype="image/*"
					on:load={(e) => handle_upload(e, 1)}
					disable_click={!!value?.[1]}
					{root}
					file_count="multiple"
				>
					<slot />
				</Upload>
			{:else}
				<img src={value[1].data} alt="" />
			{/if}
		</div>
	</Slider>
</div>

<style>
	.upload-wrap {
		display: flex;
		justify-content: center;
		height: 100%;
		width: 100%;
	}
	.image-container,
	img {
		width: var(--size-full);
		height: var(--size-full);
	}
	img {
		object-fit: cover;
	}
</style>
