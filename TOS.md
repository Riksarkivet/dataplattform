# Användningsvillkor - Riksarkivets publika APIer

Genom att använda Riksarkivets publika API-er går du med på att följa de villkor som beskrivs nedan.

## APIer

Riksarkivet tillhandahåller följande APIer:

* [OAI-PMH](https://www.openarchives.org/pmh/) för skördning av metadata om arkiv och arkivhandlingar
* [IIIF Image](https://iiif.io/api/image/3.0/) och [IIIF Presentation](https://iiif.io/api/presentation/3.0/) för hantering och presentation av digitiserat arkivmaterial
* [Riksarkivets sök-API](docs/Sök-API.md) för sökning i Riksarkivets datakällor, motsvarande [söktjänstens samsökning](https://sok.riksarkivet.se/?Sok=true)
* [docs/LOD.md](Länkade data/RDF) läsning av enstaka poster i RDF-format

## Rättigheter och personskydd

Riksarkivets publika API-er returnerar data som är äldre än 110 år samt data som är uttryckligen förenliga med GDPR.

Merparten av arkivhandlingarna är offentliga handlingar, där det inte föreligger någon upphovsrätt. Digitiserat material är mestadels rättighetsmärkt med [Public Domain Mark 1.0](https://creativecommons.org/publicdomain/mark/1.0/). Det finns undantag, där annan aktör än Riksarkivet gjort digitiseringen. Dessa data har en Creative Commons-licens. Posternas metadata är huvudsakligen rättighetsmärkta med [CC0 1.0 universell](https://creativecommons.org/publicdomain/zero/1.0/deed.sv). Eventuella undantag har annan Creative Commons-licens.

## Autenticering och auktorisering

Riksarkivets publika API-er kräver ingen autenticering eller api-nyckel. I och med att alla tillgängliga data är öppna enligt ovanstående stycke om rättigheter och personskydd finns inget behov av auktorisering.

## Tillgänglighet och begränsningar

API-ernas tillgängligheten beror på tillgänglig server- och nätvekskapacitet. Riksarkivet kan vid behov sätta mängdbegränsning på åtkomst till API-er ([rate limiting](https://nordicapis.com/everything-you-need-to-know-about-api-rate-limiting/)). Om en enskild klient utnyttjar tillgängliga resurser så intensivt att det försämrar tillgängligheten till Riksarkivets tjänster för andra användare har Riksarkivet möjligheten att blockera den klienten tills vidare, medan en utredning och dialog om nyttjandet pågår.
