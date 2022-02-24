"use strict";

const TOP_COLLECTION_URL = "/iiif/collection/riksarkivet";

const getCollection = async (uri) => {
	console.log(`--- Getting ${uri} ---`);

	return (await fetch(uri)).json();
}

