"use strict";

const IIIF_BASE_URL = "/iiif/";

const IIIF_COLLECTION_BASE_URL = `${IIIF_BASE_URL}collection/`;
const TOP_COLLECTION_ID = "riksarkivet";

/**
 * Get id part of collection URI (name or arkiv/<pid>)
 * @param {*} uri Absolute or relative URI
 * @returns id part 
 */
const collectionPath = (uri) => {
	const regex = /https:\/\/lbiiif(?:-acc)?.riksarkivet.se\/collection\/(.*)/;
	const match = uri.match(regex);
	return !!match && match.length > 1 ? match[1] : uri;
}

/**
 * Get collection resource (JSON-LD). 
 * NB: this is very simplistic, without error handling
 * @param {*} uri Collection URI
 * @returns Resource in JSON-LD format
 */
const getCollection = async (uri) => {
	// For absolute URIs (including https://lbiiif.riksarkivet.se), extract the id part
	const url = uri.startsWith("https") ? `${IIIF_COLLECTION_BASE_URL}${collectionPath(uri)}` : uri;
	console.log(`--- Getting ${uri} by way of ${url} ---`);

	return (await fetch(url)).json();
}

/**
 * Get id part of manifest URI
 * @param {*} uri Absolute or relative URI
 * @returns id part 
 */
 const manifestPath = (uri) => {
	const regex = /https:\/\/lbiiif(?:-acc)?.riksarkivet.se\/(.*)/;
	const match = uri.match(regex);
	return !!match && match.length > 1 ? match[1] : uri;
}

/**
 * Get manifest resource (JSON-LD). 
 * NB: this is very simplistic, without error handling
 * @param {*} uri Manifest URI
 * @returns Resource in JSON-LD format
 */
 const getManifest = async (uri) => {
	// For absolute URIs (including https://lbiiif.riksarkivet.se), extract the id part
	const url = uri.startsWith("https") ? `${IIIF_BASE_URL}${manifestPath(uri)}` : uri;
	console.log(`--- Getting ${uri} by way of ${url} ---`);

	return (await fetch(url)).json();
}

/**
 * Get collection proxy URL, from query parameter ?arkiv if present, top collection id otherwise
 * @returns Proxy URL
 */
const collectionUrl = () => {
	const urlSearchParams = new URLSearchParams(window.location.search);
	const params = Object.fromEntries(urlSearchParams.entries());
	const urlPart = params.arkiv ? `arkiv/${params.arkiv}` : TOP_COLLECTION_ID;
	const url = `${IIIF_COLLECTION_BASE_URL}${urlPart}`;
	return url;
}

/**
 * Get IIIF image proxy URL
 * @param {*} uri Image URI
 * @param {*} v2 Use IIIF Image v2?
 * @returns Proxy URL
 */
const imageUrl = (uri, v2 = false) => {
	const regex = /https:\/\/lbiiif(?:-acc)?.riksarkivet.se\/(.*)/;
	const match = uri.match(regex);
	return !!match && match.length > 1 
		? `${IIIF_BASE_URL}${v2 ? "v2/" : ""}${match[1]}`
		: uri;
}

/**
 * Get HTML for link to collection or image presentation
 * @param {*} item Item object
 * @returns HTML for link component
 */
const itemLink = (item) => {
	return `${item.label.sv[0]}  <span class='oi' data-glyph='${item.type === "Collection" ? "arrow-right" : "eye"}' title='Link icon' aria-hidden='true'></span>`;
}

/**
 * Get HTML for back link to parent collection
 * @param {*} prev Item object
 * @returns HTML for back link component
 */
 const backLink = (prev) => {
	return `${prev.label} <span class='oi' data-glyph='arrow-left' title='Arrow left' aria-hidden='true'></span>`;
}

const stepImage = (imageIndex, forward) => {
	const store = Alpine.store("browseContext")
	if (forward) {
		return (imageIndex < store.image.urls.length - 1) ? imageIndex + 1 : 0;
	} else {
		return (imageIndex > 0) ? imageIndex - 1 : store.image.urls.length - 1;
	}
}

/**
 * Alpine.js initialization
 */
const initBrowseContext = () => {
	// Use store rather than data in order to access state from the browser
	// navigation handler
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
		 * @param {*} event Navigation event
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

	// And some data too, for state which is only used in the collection browsing
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
			}
		}
	}));
}
