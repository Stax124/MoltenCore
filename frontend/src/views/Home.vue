<script lang="ts">
import { CBadge, CBox, CFlex, CIcon, CText } from "@chakra-ui/vue-next";
export default {
	name: "Home",
	components: {
		CBadge,
		CBox,
		CFlex,
		CIcon,
		CText,
	},
};
</script>

<template>
	<CBox
		w="300px"
		font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';"
	>
		<CBox w="100%" shadow="md" rounded="lg" p="5">
			<chakra.img rounded="md" w="100%" src="https://bit.ly/2k1H1t6" />
			<CFlex align="baseline" mt="2">
				<CBadge color-scheme="purple"> Plus </CBadge>
				<CText
					ml="2"
					text-transform="uppercase"
					font-size="sm"
					font-weight="bold"
					color="pink.800"
				>
					Verified &bull; Cape Town
				</CText>
			</CFlex>
			<CText mt="2" font-size="xl" font-weight="semibold" line-height="short">
				Modern, Chic Penthouse with Mountain, City & Sea Views
			</CText>
			<CText mt="2"> $119/night </CText>
			<CFlex mt="2" align="center">
				<CIcon name="star" color="orange.400" />
				<CText ml="1" font-size="sm"> <b>4.84</b> $ </CText>
			</CFlex>
		</CBox>
	</CBox>
</template>
