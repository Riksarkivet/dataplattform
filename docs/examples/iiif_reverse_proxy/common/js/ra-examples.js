"use strict";

const IIIF_COLLECTION_BASE_URL = "/iiif/collection/";
const IIIF_COLLECTION_BASE_ACC_URL = "/iiif-acc/collection/";
const TOP_COLLECTION_ID = "riksarkivet";

const prod = false;

const collectionPath = (uri) => {
	const regex = /https:\/\/lbiiif(?:-acc)?.riksarkivet.se\/collection\/(.*)/;
	const match = uri.match(regex);
	return !!match && match.length > 1 ? match[1] : uri;
}

const getCollection = async (uri) => {
	// For absolute URIs (including https://lbiiif.riksarkivet.se), extract the id part
	const url = uri.startsWith("https")
		? (prod ? IIIF_COLLECTION_BASE_URL : IIIF_COLLECTION_BASE_ACC_URL) + collectionPath(uri)
		: uri;
	console.log(`--- Getting ${uri} by way of ${url} ---`);

	return (await fetch(url)).json();
}

const collectionUrl = () => {
	const urlSearchParams = new URLSearchParams(window.location.search);
	const params = Object.fromEntries(urlSearchParams.entries());
	const urlPart = params.arkiv ? `arkiv/${params.arkiv}` : TOP_COLLECTION_ID;
	//const url = `${IIIF_COLLECTION_BASE_ACC_URL}${urlPart}`;
	const url = `${prod ? IIIF_COLLECTION_BASE_URL : IIIF_COLLECTION_BASE_ACC_URL}${urlPart}`;
	return url;
}

const itemLink = (item) => {
	return `${item.label.sv[0]}  <span class='oi' data-glyph='${item.type === "Collection" ? "arrow-right" : "eye"}' title='Link icon' aria-hidden='true'></span>`
}

const initBrowseContext = () => {
	Alpine.data('browseContext', () => ({
		trail: [],
		item: {},
		collection: {},

		toggleLoading() {
			this.loading = !this.loading;
		},
  
		async getItems() {
			if (this.item.type === 'Collection') {
				this.trail.push({
					id: this.collection.id,
					label: this.collection.label.sv[0]
				})
				this.loading = true;
				this.collection = await getCollection(this.item.id)
				this.loading = false;
			} else {
				this.image.present = true
				this.image.id = this.item.id
			}
		},

		async goBack(index) {
			const ancestor = this.trail[index];
			this.trail = this.trail.slice(0, index);
			this.loading = true;
			this.collection = await getCollection(ancestor.id);
			this.loading = false;
		}
	}))
}