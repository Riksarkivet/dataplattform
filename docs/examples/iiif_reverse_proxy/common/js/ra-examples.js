"use strict";

const IIIF_BASE_URL = "/iiif/";
const IIIF_BASE_ACC_URL = "/iiif-acc/";

const IIIF_COLLECTION_BASE_URL = `${IIIF_BASE_URL}collection/`;
const IIIF_COLLECTION_BASE_ACC_URL = `${IIIF_BASE_ACC_URL}collection/`;
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

const manifestPath = (uri) => {
	const regex = /https:\/\/lbiiif(?:-acc)?.riksarkivet.se\/(.*)/;
	const match = uri.match(regex);
	return !!match && match.length > 1 ? match[1] : uri;
}

const getManifest = async (uri) => {
	// For absolute URIs (including https://lbiiif.riksarkivet.se), extract the id part
	const url = uri.startsWith("https")
		? (prod ? IIIF_BASE_URL : IIIF_BASE_ACC_URL) + manifestPath(uri)
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

const imageUrl = (uri, v2 = false) => {
	const regex = /https:\/\/lbiiif(?:-acc)?.riksarkivet.se\/(.*)/;
	const match = uri.match(regex);
	return !!match && match.length > 1 
		? `${prod ? IIIF_BASE_URL : IIIF_BASE_ACC_URL}${v2 ? "v2/" : ""}${match[1]}`
		: uri;
}

const itemLink = (item) => {
	return `${item.label.sv[0]}  <span class='oi' data-glyph='${item.type === "Collection" ? "arrow-right" : "eye"}' title='Link icon' aria-hidden='true'></span>`;
}

const backLink = (prev) => {
	return `${prev.label} <span class='oi' data-glyph='arrow-left' title='Arrow left' aria-hidden='true'></span>`;
}

const initBrowseContext = () => {
	Alpine.store("browseContext", {
		loading: false,
		trail: [],
		collection: {},
		image: {
			present: false,
			id: null,
			urls: []
		},

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

		closeImage() {
			const store = Alpine.store("browseContext");
			if (store.image.present) {
				store.image = {
					present: false,
					id: null
				};
			}
		},
		
		/**
		 * Handler for browser back/forward event. NB: only handles back, forward is
		 * too complex for this simple example
		 * 
		 * @param {*} event 
		 */
		async handleNavigation(event) {
			if (event.state) {
				const store = Alpine.store("browseContext");
				for (let index = store.trail.length -1; index >= 0; index--) {
					if (store.trail[index].id === event.state.collection) {
						await store.goBack(index);
					}
				}
			}
		}
	});

	Alpine.data("browseContext", () => ({
		item: {},

		async selectItem() {
			const store = Alpine.store("browseContext");
			if (this.item.type === 'Collection') {
				store.trail.push({
					id: store.collection.id,
					label: store.collection.label.sv[0]
				})
				store.loading = true;
				store.collection = await getCollection(this.item.id)
				console.log(`--- Pushing state ${store.collection.id} ---`);
				history.pushState({
					collection: store.collection.id
				}, null);
				store.loading = false;
			} else {
				store.image.present = true;
				store.image.id = this.item.id;
				const manifest = await getManifest(this.item.id);
				store.image.urls = manifest.items.map(element => imageUrl(element.items[0].items[0].body.id, true));
				// const tileSources = store.image.urls.map(url => ({
				// 	type: "image",
				// 	url: url
				// }));
				// const viewer = OpenSeadragon({
				// 	id: "viewer",
				// 	prefixUrl: "https://cdn.jsdelivr.net/npm/openseadragon/build/openseadragon/images/",
				// 	tileSources: tileSources
				// });
			}
		}
	}));
}
