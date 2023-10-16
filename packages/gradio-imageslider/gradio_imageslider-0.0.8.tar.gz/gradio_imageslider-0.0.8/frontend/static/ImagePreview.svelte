<script lang="ts">
	import Slider from "../shared/Slider.svelte";
	import { createEventDispatcher } from "svelte";
	import type { SelectData } from "@gradio/utils";
	import { BlockLabel, Empty, IconButton, ShareButton } from "@gradio/atoms";
	import { get_coordinates_of_clicked_image } from "../shared/utils";

	import { Image } from "@gradio/icons";
	import { type FileData, normalise_file } from "@gradio/upload";
	import type { I18nFormatter } from "@gradio/utils";

	export let value: [null | FileData, null | FileData] = [null, null];
	let value_: [null | FileData, null | FileData] = [null, null];
	export let label: string | undefined = undefined;
	export let show_label: boolean;
	export let root: string;
	export let i18n: I18nFormatter;

	const dispatch = createEventDispatcher<{
		change: string;
		select: SelectData;
	}>();

	// $: value && dispatch("change", value.data);

	$: if (value !== value_) {
		value_ = value;
		normalise_file(value_, root, null);
	}

	const handle_click = (evt: MouseEvent): void => {
		let coordinates = get_coordinates_of_clicked_image(evt);
		if (coordinates) {
			dispatch("select", { index: coordinates, value: null });
		}
	};

	let position = 0.5;
</script>

<BlockLabel {show_label} Icon={Image} label={label || i18n("image.image")} />
{#if value_ === null}
	<Empty unpadded_box={true} size="large"><Image /></Empty>
{:else}
	<!-- <div class="icon-buttons">
		{#if show_download_button}
			<a
				href={value_.data}
				target={window.__is_colab__ ? "_blank" : null}
				download={"image"}
			>
				<IconButton Icon={Download} label={i18n("common.download")} />
			</a>
		{/if}
		{#if show_share_button}
			<ShareButton
				{i18n}
				on:share
				on:error
				formatter={async (value) => {
					if (!value) return "";
					let url = await uploadToHuggingFace(value, "base64");
					return `<img src="${url}" />`;
				}}
				{value}
			/>
		{/if}
	</div> -->
	<!-- TODO: fix -->
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-noninteractive-element-interactions-->

	<div class="slider-wrap">
		<Slider bind:position>
			<img src={value_?.[0].data} alt="" loading="lazy" />
			<img
				class="fixed"
				src={value_?.[1].data}
				alt=""
				loading="lazy"
				style="clip-path: inset(0 0 0 {position * 100}%)"
			/>
		</Slider>
	</div>
{/if}

<style>
	.slider-wrap {
		user-select: none;
		max-height: calc(100vh - 40px);
	}
	img {
		width: var(--size-full);
		height: var(--size-full);
		object-fit: contain;
	}

	.fixed {
		position: absolute;
		top: 0;
		left: 0;
	}

	.selectable {
		cursor: crosshair;
	}
</style>
