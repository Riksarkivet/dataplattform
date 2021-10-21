# IIIF

Riksarkivet tillgängliggör publika digitiserade arkivhandlingar via IIIF (International Image Interoperability Framework). IIIF innehåller en serie protokoll för hantering och publicering av digitala bilder. Riksarkivet stöder [IIIF Image 3.0](https://iiif.io/api/image/3.0/) för bildhantering och [IIIF Presentation 3.0](https://iiif.io/api/presentation/3.0/) för presentation. Utöver dessa finns [IIIF Authentication 1.0](https://iiif.io/api/auth/1.0/) för autenticering av bildresurser, [IIIF Search 1.0](https://iiif.io/api/search/1.0/) för sökning inom IIIF-resurser och [IIIF Change Discovery 1.0](https://iiif.io/api/discovery/1.0/) för publicering av ändringar i IIIF-resurser.

Dessa används i Riksarkivets tjänst [Sök i arkiven](https://sok.riksarkivet.se/), t.ex. [uppslag ur Bergshammars vapenbok](https://sok.riksarkivet.se/bildvisning/R0001216_00005#?c=&m=&s=&cv=4&xywh=-533%2C0%2C4333%2C2574). I och med användningen av IIIF-APIerna kan bilderna visas i andra bildvisningstjänster, t.ex. [Universal Viewer exempel](https://universalviewer.io/uv.html?manifest=https://lbiiif.riksarkivet.se/arkis!R0001216/manifest#?c=0&m=0&s=0&cv=0&xywh=-577%2C-137%2C4657%2C2739). IIIF Image ger möjlighet att zooma och panorera bilderna, IIIF Presentation ger bläddring mellan relaterade bilder och presentation av metadata med hjälp av bildvisaren [Universal Viewer](https://universalviewer.io/). 

## IIIF Image

Image-APIet har metoder för att bearbeta källbilder. Riksarkivets IIIF-tjänst når [compliance level 1](https://iiif.io/api/image/3.0/compliance/), och stöder de metoder som inte är kursiverade nedan:

* Utsnitt (fullständig, kvadratisk, x/y/bredd/höjd, *procent x/y/bredd/höjd*) 
* Skalning (max, bredd, höjd, bredd & höjd, *bredd/höjd med uppskalning*, *bredd/höjd med begränsning*)
* Rotation (0, "rotationBy90s", *godtycklig*, spegelvändning)
* Färgkvalitet (original, *färg*, *gråskala*, *bitonal*)
* Bildformat (jpeg, *png*, *tif*, *gif*, *pdf*, *jp2*, *webp*)

## IIIF Presentation

