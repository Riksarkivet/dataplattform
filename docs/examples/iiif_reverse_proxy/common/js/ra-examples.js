"use strict";

const IIIF_COLLECTION_BASE_URL = "/iiif/collection/";
const IIIF_COLLECTION_BASE_ACC_URL = "/iiif-acc/collection/";
const TOP_COLLECTION_ID = "riksarkivet";

const getCollection = async (uri) => {
	console.log(`--- Getting ${uri} ---`);

	return (await fetch(uri)).json();
}

const collectionUrl = () => {
	const urlSearchParams = new URLSearchParams(window.location.search);
	const params = Object.fromEntries(urlSearchParams.entries());
	const urlPart = params.arkiv ? `arkiv/${params.arkiv}` : TOP_COLLECTION_ID;
	const url = `${IIIF_COLLECTION_BASE_ACC_URL}${urlPart}`;
	return url;
}

const itemLink = (item) => {
	return `${item.label.sv[0]}  <span class='oi' data-glyph='${item.type === "Collection" ? "arrow-right" : "eye"}' title='Link icon' aria-hidden='true'></span>`
}
