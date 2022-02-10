# IIIF

Riksarkivet tillgängliggör publika digitiserade arkivhandlingar via IIIF (International Image Interoperability Framework). IIIF innehåller en serie protokoll för hantering och publicering av digitala bilder. Riksarkivet stöder [IIIF Image 3.0](https://iiif.io/api/image/3.0/) och [IIIF Image 2.0](https://iiif.io/api/image/2.0/) för bildhantering och [IIIF Presentation 3.0](https://iiif.io/api/presentation/3.0/) för presentation. Utöver dessa finns [IIIF Authentication 1.0](https://iiif.io/api/auth/1.0/) för autenticering av bildresurser, [IIIF Search 1.0](https://iiif.io/api/search/1.0/) för sökning inom IIIF-resurser och [IIIF Change Discovery 1.0](https://iiif.io/api/discovery/1.0/) för publicering av ändringar i IIIF-resurser.

Dessa används i Riksarkivets tjänst [Sök i arkiven](https://sok.riksarkivet.se/), t.ex. [uppslag ur Bergshammars vapenbok](https://sok.riksarkivet.se/bildvisning/R0001216_00005#?c=&m=&s=&cv=4&xywh=-533%2C0%2C4333%2C2574). I och med användningen av IIIF-APIerna kan bilderna visas i andra bildvisningstjänster, t.ex. [Universal Viewer exempel](https://universalviewer.io/uv.html?manifest=https://lbiiif.riksarkivet.se/arkis!R0001216/manifest#?c=0&m=0&s=0&cv=0&xywh=-577%2C-137%2C4657%2C2739). IIIF Image ger möjlighet att zooma och panorera bilderna, IIIF Presentation ger bläddring mellan relaterade bilder och presentation av metadata med hjälp av bildvisaren [Universal Viewer](https://universalviewer.io/). 


## IIIF Image

Image-APIet har metoder för att bearbeta källbilder. Riksarkivets IIIF-tjänst når [compliance level 1](https://iiif.io/api/image/3.0/compliance/), och stöder de metoder som inte är kursiverade nedan:

* Utsnitt (fullständig, kvadratisk, x/y/bredd/höjd, *procent x/y/bredd/höjd*) 
* Skalning (max, bredd, höjd, bredd & höjd, *bredd/höjd med uppskalning*, *bredd/höjd med begränsning*)
* Rotation (0, "rotationBy90s", *godtycklig*, spegelvändning)
* Färgkvalitet (original, *färg*, *gråskala*, *bitonal*)
* Bildformat (jpeg, *png*, *tif*, *gif*, *pdf*, *jp2*, *webp*)

Riksarkivets IIIF-tjänst stöder även IIIF Image 2.0, t.ex. för användning i bildvisare som inte stöder IIIF Image 3.0, som [Universal Viewer](https://universalviewer.io/).

##### Alla anrop (request) sker med Http-Get.

##### Svaret/response för alla IIIF-anrop är av typen: content-type: "image/jpeg". Om något är fel i anropet kommer främst svar av typen 400 "BadRequest" samt 501 "Not Implemented" att användas.

### Version 3.0

https://lbiiif.riksarkivet.se/{bild-id}/{region}/{storlek}/{rotation}/{färgmodell}.jpg
https://lbiiif.riksarkivet.se/v3/{bild-id}/{region}/{storlek}/{rotation}/{färgmodell}.jpg

För en fullständig beskrivning av URI-syntax se [version 3.0](https://iiif.io/api/image/3.0/#4-image-requests)

| Parameter  | Beskrivning |
| -----------| ------------- |
| region     | Önskat utsnitt av bilden: "*full*" eller "*x-start,y-start,bredd,höjd*"  |
| storlek    | Önskad storlek i pixlar på bilden: "*max*", "*bredd, höjd*", "*bredd,*" eller "*,höjd*"  |
| rotation   | Önskad rotation av bilden: "*0*", "*!0*", "*90*", "*!90*", "*180*", "*!180*", "*270*" eller "*!270*", där talet anger vinkel (i jämna 90-gradersintervall) och ! anger spegelvändning |
| färgmodell | Tjänsten stöder endast "*default*" |

### Version 2.0

https://lbiiif.riksarkivet.se/v2/{bild-id}/{region}/{storlek}/{rotation}/{färgmodell}.jpg

För en fullständig beskrivning av URI-syntax se [version 2.0](https://iiif.io/api/image/2.0/#image-request-parameters).

| Parameter  | Beskrivning |
| -----------| ------------- |
| region     | Önskat utsnitt av bilden: "*full*" eller "*x-start,y-start,bredd,höjd*"  |
| storlek    | Önskad storlek i pixlar på bilden: "*full*", "*bredd, höjd*", "*bredd,*" eller "*,höjd*"  |
| rotation   | Önskad rotation av bilden: "*0*", "*!0*", "*90*", "*!90*", "*180*", "*!180*", "*270*" eller "*!270*", där talet anger vinkel (i jämna 90-gradersintervall) och ! anger spegelvändning |
| färgmodell | Tjänsten stöder endast "*default*" |

### Exempel på IIIF Image-anrop

##### Bildformat (format): Endast stöd för "jpg"
##### Färgmodell (quality): Endast stöd för "default"

#### "Region" / Utsnitt
		
Exempel på "full" (fullständig): 
http://lbiiif.riksarkivet.se/arkis!C0002787_00008/full/max/0/default.jpg

Exempel på "square" (kvadratisk): 
http://lbiiif.riksarkivet.se/arkis!C0002787_00030/square/max/0/default.jpg

Exempel på utsnitt baserat på absoluta pixelvärden: 
http://lbiiif.riksarkivet.se/arkis!C0002787_00008/300,300,100,100/max/0/default.jpg


#### "Size" / Skalning

Skala på bredd: http://lbiiif.riksarkivet.se/arkis!C0002787_00030/full/300,/0/default.jpg

Skala på höjd: http://lbiiif.riksarkivet.se/arkis!C0002787_00030/full/,500/0/default.jpg

Skala på bredd samt höjd: http://lbiiif.riksarkivet.se/arkis!C0002787_00030/full/!500,300/0/default.jpg

#### Rotation

Ingen rotation (0): http://lbiiif.riksarkivet.se/arkis!C0002787_00008/full/max/0/default.jpg

Rotation 90 grader medurs: https://lbiiif.riksarkivet.se/arkis!C0002787_00030/full/max/90/default.jpg

Rotation 90 grader medurs och speglad: https://lbiiif.riksarkivet.se/arkis!C0002787_00030/full/max/!90/default.jpg


## IIIF Presentation

Presentation-APIet servar *resurser* som gör det möjligt att presentera bilder och audiovisuella media (ljud och film) med tillhörande metadata i en klienttillämpning (webbsida, app, etc.) Det finns två typer av resurser på den yttersta nivån:

* Manifest, som innehåller referenser till bilder/audiovisuella filer och metadata
* Collection, som innehåller referenser till underliggande Collections och Manifest för en hierarkisk gruppering

Svaren (response) är [JSON-LD-dokument](https://json-ld.org/), dvs [RDF](https://www.w3.org/RDF/)-modeller, serialiserade i JSON-format, se ett exempel här: https://iiif.io/api/presentation/3.0/#b-example-manifest-response. 
Det finns flera visningstillämpningar för IIIF-manifest, t.ex.

* [Universal Viewer](https://universalviewer.io/)
* [Mirador](https://projectmirador.org/)

##### Alla anrop (request) sker med Http-Get.

Presentation-APIet har en enkel URL-syntax.

### Manifest

https://lbiiif.riksarkivet.se/{identifierare}/manifest

### Collection

Riksarkivet tillhandahåller en Collection-struktur för att externa klienter skall kunna bläddra sig fram till manifesten.

https://lbiiif.riksarkivet.se/collection/riksarkivet

Collection på toppnivån innehåller referenser till följande parallella sorteringar/hierarkier:

<details>
  <summary><strong>Ämnesområde</strong> - https://lbiiif.riksarkivet.se/collection/amnesomrade</summary>
  <dl>
    <dt>Brott och straff</dt>
    <dd>https://lbiiif.riksarkivet.se/collection/brott-och-straff</dd>
    <dt>Emigration</dt>
    <dd>https://lbiiif.riksarkivet.se/collection/emigration</dd>
    <dt>Fastigheter och gårdar</dt>
    <dd>https://lbiiif.riksarkivet.se/collection/fastigheter-och-gardar</dd>
    <dt>Fotografier</dt>
    <dd>https://lbiiif.riksarkivet.se/collection/fotografier</dd>
    <dt>Gästgiveri och skjutsväsen</dt>
    <dd>https://lbiiif.riksarkivet.se/collection/gastgiveri-och-skjutsvasen</dd>
    <dt>Heraldik</dt>
    <dd>https://lbiiif.riksarkivet.se/collection/heraldik</dd>
    <dt>Idrott</dt>
    <dd>https://lbiiif.riksarkivet.se/collection/idrott</dd>
    <dt>Kartor och ritningar</dt>
    <dd>https://lbiiif.riksarkivet.se/collection/kartor-och-ritningar</dd>
  </dl>
</details>
<hr>

<details>
  <summary><strong>Register</strong> - https://lbiiif.riksarkivet.se/collection/register</summary>
</details>
<hr>

<details>
  <summary><strong>Arkivinstitution</strong> - https://lbiiif.riksarkivet.se/collection/arkivinstitution</summary>
</details>
<hr>

<details>
  <summary><strong>Ort</strong> - https://lbiiif.riksarkivet.se/collection/ort</summary>
</details>
<hr>

<details>
  <summary><strong>Tid</strong> - https://lbiiif.riksarkivet.se/collection/tid</summary>
</details>

#### Interna referenser

På nedersta nivå, som normalt motsvarar arkivenheter av typen **serie**, innehåller en Collection referenser till Manifest, som normalt motsvarar arkivenheter av typen **volym**. Interna referenser, till volymer i andra serier (**Se:** i Riksarkivets söktjänst), är inkluderade i **items**-listan om de hänvisar inom samma arkiv. Referenser till volymer i andra arkiv visas i söktjänsten men följer inte med i IIIF Collections på grund av tekniska begränsningar.

Presentationsresursernas innehåll och struktur finns beskrivna i [specifikation för Presentation API](https://iiif.io/api/presentation/3.0/).
