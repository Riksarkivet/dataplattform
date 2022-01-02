![Riksarkivet](https://sok.riksarkivet.se/Administration/Images/Layout/logo2.png)

# Arkivenheter i Riksarkivets EAD-format

Hur dataelement i EAD-filen motsvarar presentationen i söktjänsten.

## Volym

[Exempelfil 1 (SE/ULA/10012/A I/1)](examples/data/ra-ead-volym-se-ula-10012-aI1.xml)

[Exempelfil 2 (SE/KrA/0414/0028/0006)](examples/data/ra-ead-volym-se-kra-0414-0028-0006.xml)

### Titel

    <filedesc>
      <titlestmt>
        <titleproper>5. Mariaeburgum. Ichnographice De Scriptum. A 1639. Tabula Explicans. [Marienburg/Malbork]</titleproper>
      </titlestmt>
    </filedesc>

och

    <did>
      <unittitle>5. Mariaeburgum. Ichnographice De Scriptum. A 1639. Tabula Explicans. [Marienburg/Malbork]</unittitle>
      ...
    </did

### Referenskod

    <eadheader ...>
      <eadid countrycode="SE" mainagencycode="SE-ULA" identifier="SE-ULA-10012-A I-1">SE/ULA/10012/AI/1</eadid>

Referenskoden är egentligen **SE/ULA/10012/A I/1**, mellanslaget försvinner i <eadid>-elementets innehåll. Notera också att attributen **mainagencycode** och **identifier** har en ganska strikt formatbegränsning, varför **"/"** i Riksarkivets referenskoder byts ut mot **"-"** i dessa.

    <did>
      <unitid encodinganalog="3.1.1" type="call number">SE/ULA/10012/A I/1</unitid>
      
Dvs, did/unitid innehåller referenskoden i originalformat.
  
### Länk till posten

    <otherfindaid encodinganalog="3.4.5">
      <p>
        <extref xlink:href="https://sok-acc.riksarkivet.se/arkiv/46gUgjX9rH6cxG02H087k3">Post i NAD</extref>
      </p>
    </otherfindaid>
  
### Omfång
      
    <physdesc encodinganalog="3.4.4">
      <extent unit="Kartor">1</extent>
    </physdesc>
      
### Datering
 
    <did>
      ...
      <unitdate calendar="gregorian" era="ce" normal="1752/1764" encodinganalog="3.1.3">1752--1764</unitdate>

unitdate-elementets textinnehåll är ustrukturerat, där kan förekomma kvalificerande förklaring ("osäker" etc.). Om arkivenheten har entydigt årtal i dateringsfälten innehåller attributet **normal** en standardrepresentation av tidpunkten eller tidsspannet **YYYY[/YYYY]**.
  
### Villkor
  
    <accessrestrict encodinganalog="3.4.1">
      <p>Delvis</p>
    </accessrestrict>
      
### Arkivinstitution

Referenskodens två första element anger arkivinstitution. I exemplet är det **SE/ULA** = Landsarkivet i Uppsala.
      
### Arkivbildare/upphov
      
    <origination encodinganalog="3.2.1">
      <name authfilenumber="SE/902002">Lokal upphovsman KARTIA (KrA) - Getkant, Friedrich</name>
    </origination>
        
### Bildvisningslänk
        
    <did>
      ...
      <dao xlink:role="IMAGE" xlink:href="https://sok-acc.riksarkivet.se/bildvisning/C0002787?partner=ape" />
      <dao xlink:role="MANIFEST" xlink:href="https://lbiiif-acc.riksarkivet.se/arkis!C0002787/manifest" xlink:title="manifest" />
      <dao xlink:role="SERVICE" xlink:href="https://lbiiif-acc.riksarkivet.se" xlink:title="service" xlink:arcrole="https://iiif.io/api/image/3/level1.json" />
    </did>
        
### Allmän anmärkning
        
    <scopecontent encodinganalog="summary">
      <p>Med ortregister. Innehåller även längder över utflyttat tjänstefolk 1765-1771, 1773-1775 och uppbördslängd över "Åhrliga Påskepenningar af Alunda Sockns Ordinaira Soldater" 1753-1766.</p>
    </scopecontent>
        
### Rättighetsmärkning
        
    <userestrict encodinganalog="3.4.5" type="dao">
      <p>
        <extref xlink:href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</extref>
      </p>
    </userestrict>
      
### Repr. anm.
      
    <altformavail>
      <p>Mediatyp enligt Kartia: Mikrofilm Mediatyp enligt Kartia: K 011 Mediatyp enligt Kartia: 471 </p>
    </altformavail>

### Senast ändrad
        
    <revisiondesc>
      ...
      <change>
        <date calendar="gregorian" era="ce">2021-11-18T13:53:13.173Z</date>
        <item>Senaste uppdatering i Arkis</item>
      </change>
    </revisiondesc>

## Serie

[Exempelfil (SE/ULA/10012/A I)](examples/data/ra-ead-serie.xml)

EAD-data för en serie har samma grundläggande uppbyggnad som för en volym. Data för volymerna i serien finns sedan som element nästade under 
        
    <dsc type="othertype">
      ...
    </dsc>
        
### Nästade volym-element
        
    <c level="otherlevel" otherlevel="volym" id="d2e101" encodinganalog="3.1.4">
      <did>
        <unitid encodinganalog="3.1.1" type="call number">SE/ULA/10012/A I/2</unitid>
        <unittitle>1772--1778</unittitle>
        <unitdate calendar="gregorian" era="ce" normal="1772/1778" encodinganalog="3.1.3">1772--1778</unitdate>
        <dao xlink:role="IMAGE" xlink:href="https://sok-acc.riksarkivet.se/bildvisning/C0002788?partner=ape" />
      </did>
      <scopecontent encodinganalog="summary">
        <p>Med ortregister.</p>
      </scopecontent>
      <accessrestrict encodinganalog="3.4.1">
        <p>Delvis</p>
      </accessrestrict>
      <otherfindaid encodinganalog="3.4.5">
        <p>
        <extref xlink:href="https://sok-acc.riksarkivet.se/arkiv/4MgUgjX9rH6cxG02H087k3">Post i NAD</extref>
        </p>
      </otherfindaid>
    </c>

## Arkiv
