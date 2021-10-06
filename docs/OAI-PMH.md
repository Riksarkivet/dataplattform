![Riksarkivet](https://sok.riksarkivet.se/Administration/Images/Layout/logo2.png)

# OAI-PMH

Riksarkivet publicerar data till [Archives Portal Europe](https://www.archivesportaleurope.net/sv) via [OAI-PMH](https://www.openarchives.org/pmh/). OAI-PMH är ett standardprotokoll för *metadata harvesting*, dvs hämtning av metadata från olika källor. OAI-PMH använder HTTP för request och response, där response har XML-format (content-type: text/xml).

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

* [Encoded Archival Description (EAD)](https://www.loc.gov/ead/)
* [Encoded Archival Description, anpassad för Archives Portal Europe (apeEAD)](http://wiki.archivesportaleurope.net/index.php/apeEAD)
* [Encoded Archival Description, anpassad för Riksarkivet (raEAD)](?)

### List ?

https://oai-pmh.riksarkivet.se/OAI?verb=ListAllAuth

Svaret listar ? OBS! metoden ListAllAuth ingår inte i OAI-PMH-standarden.

### List sets

Tjänsten stöder inte metoden **ListSets**.

### List identifiers

https://oai-pmh.riksarkivet.se/OAI/[dataset]?verb=ListIdentifiers

t.ex.
https://oai-pmh.riksarkivet.se/OAI/SE_ULA?verb=ListIdentifiers

Svaret listar alla identifierare för poster i datasetet.

