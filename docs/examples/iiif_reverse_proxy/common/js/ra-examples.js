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
	const url = `${prod ? IIIF_COLLECTION_BASE_URL : IIIF_COLLECTION_BASE_ACC_URL}${urlPart}`;
	return url;
}

const itemLink = (item) => {
	return `${item.label.sv[0]}  <span class='oi' data-glyph='${item.type === "Collection" ? "arrow-right" : "eye"}' title='Link icon' aria-hidden='true'></span>`;
}

const backLink = (prev) => {
	return `${prev.label} <span class='oi' data-glyph='arrow-left' title='Arrow left' aria-hidden='true'></span>`;
}

const initBrowseContext = () => {
	Alpine.store("browseContext", {
		trail: [],
		loading: false,

		toggleLoading() {
			this.loading = !this.loading;
		},
  
		async goBack(index) {
			const store = Alpine.store("browseContext");
			const ancestor = store.trail[index];
			store.trail = store.trail.slice(0, index);
			store.toggleLoading();
			this.collection = await getCollection(ancestor.id);
			store.toggleLoading();
		},
		
		async handleNavigation(event) {
			if (event.state) {
				const store = Alpine.store("browseContext");
				for (index = store.trail.length -1; index >= 0; index--) {
					if (store.trail[index].id === event.state.collection) {
						await store.goBack(index);
					}
				}
			}
		}
	});

	Alpine.data('browseContext', () => ({
		item: {},
		collection: {},

		async selectItem() {
			if (this.item.type === 'Collection') {
				const store = Alpine.store("browseContext");
				store.trail.push({
					id: this.collection.id,
					label: this.collection.label.sv[0]
				})
				store.toggleLoading;
				this.collection = await getCollection(this.item.id)
				console.log(`--- Pushing state ${this.collection.id} ---`);
				history.pushState({
					collection: this.collection.id
				}, null);
				store.toggleLoading;
			} else {
				this.image.present = true
				this.image.id = this.item.id
			}
		}
	}))
}
