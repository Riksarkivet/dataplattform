![Riksarkivet](https://sok.riksarkivet.se/Administration/Images/Layout/logo2.png)

# OAI-PMH

Riksarkivet publicerar data till [Archives Portal Europe](https://www.archivesportaleurope.net/sv) via [OAI-PMH](https://www.openarchives.org/pmh/). OAI-PMH är ett standardprotokoll för *metadata harvesting*, dvs hämtning av metadata från olika källor. OAI-PMH använder HTTP för request och response, där response har XML-format (content-type: text/xml).

OAI-PMH är tänkt för skördning, dvs masshämtning av data för bearbetning och lagring i egna system. Det finns inga sök- eller sorteringsfunktioner. Om man känner till identifierare för en enskild post kan man hämta dess fullständiga data med metoden **GetRecord** (se nedan).

## Riksarkivets OAI-PMH Repository

### Adress (URL)

https://oai-pmh.riksarkivet.se/OAI

### Metoder

Riksarkivets OAI-PMH Repository stöder följande OAI-PMH-metoder "verb":

#### Identify

https://oai-pmh.riksarkivet.se/OAI?verb=Identify

Svaret innehåller grundläggande information om tjänsten.



#### List metadata formats

https://oai-pmh.riksarkivet.se/OAI?verb=ListMetadataFormats

Svaret listar de XML-format för metadata som tjänsten stöder. 

OBS! tjänsten stöder inte query-parametern identifier={identifier} för att lista vilka metadataformat som är tillgängliga för en specifik post.

* [Encoded Archival Description, anpassad för Archives Portal Europe (apeEAD)](http://wiki.archivesportaleurope.net/index.php/apeEAD), [XML-schemat för apeEAD](https://www.archivesportaleurope.net/Portal/profiles/apeEAD.xsd) är ett subset av [XML-schemat för EAD2002](http://www.loc.gov/ead/ead.xsd)
* [Encoded Archival Description, anpassad för Riksarkivet (RA-EAD)](http://xml.ra.se/ead/RA_EAD.xsd), 

#### List datasets

https://oai-pmh.riksarkivet.se/OAI?verb=ListAllAuth

Svaret listar de dataset som finns tillgängliga för **ListIdentifier**. OBS! metoden ListAllAuth ingår inte i OAI-PMH-standarden, resultatet refererar till OAI-PMH:s XML-schema men validerar inte mot det.

#### List sets

Tjänsten stöder inte metoden **ListSets**.

#### List identifiers

https://oai-pmh.riksarkivet.se/OAI/{dataset}?verb=ListIdentifiers

t.ex.

https://oai-pmh.riksarkivet.se/OAI/SE_ULA?verb=ListIdentifiers

Svaret listar alla identifierare för poster i datasetet. Tjänsten stöder inte filtrering på posternas tidsstämplar med query-parametrarna **from** och **until**. Tidsstämplarna finns dock med i svaret så system som anropar **ListIdentifiers** kan göra motsvarande filtrering.

Notera att datasetets id måste anges i adressen (/SE_ULA i exemplet).

#### List records

Tjänsten stöder inte metoden **ListRecords**. För att hämta kompletta data om ett dataset, använd ListIdentifiers och ett anrop till GetRecord för varje identifierare.

#### Get record

https://oai-pmh.riksarkivet.se/OAI?verb=GetRecord&identifier={identifier}&metadataPrefix={metadata-prefix}

där **metadata-prefix** skall vara en av

|prefix     |metadataformat                     |
|-----------|-----------------------------------|
|oai_ape_ead|EAD XML, anpassning för APE        |
|oai_ra_ead |EAD XML, anpassning för Riksarkivet|

t.ex.

https://oai-pmh.riksarkivet.se/OAI?verb=GetRecord&identifier=SE/ULA/10012&metadataPrefix=oai_ape_ead

Svaret innehåller fullständiga data för en post i angivet dataformat (apeEAD eller RA-EAD).
