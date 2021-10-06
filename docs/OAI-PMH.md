![Riksarkivet](https://sok.riksarkivet.se/Administration/Images/Layout/logo2.png)

# OAI-PMH

Riksarkivet publicerar data till [Archives Portal Europe](https://www.archivesportaleurope.net/sv) via [OAI-PMH](https://www.openarchives.org/pmh/). OAI-PMH är ett standardprotokoll för *metadata harvesting*, dvs hämtning av metadata från olika källor. OAI-PMH använder HTTP för request och response, där response har XML-format (content-type: text/xml).

## Riksarkivets OAI-PMH Repository

### Adress (URL)

https://oai-pmh.riksarkivet.se/OAI

### Metoder

Riksarkivets OAI-PMH Repository stöder följande OAI-PMH-metoder "verb":

#### List metadata formats

https://oai-pmh.riksarkivet.se/OAI?verb=listmetadataformats

Svaret listar de XML-format för metadata som tjänsten stöder.

* [Encoded Archival Description (EAD)](https://www.loc.gov/ead/)
* [Encoded Archival Description, anpassad för Archives Portal Europe (apeEAD)](http://wiki.archivesportaleurope.net/index.php/apeEAD)
* [Encoded Archival Description, anpassad för Riksarkivet (raEAD)](?)

