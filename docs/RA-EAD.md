![Riksarkivet](https://sok.riksarkivet.se/Administration/Images/Layout/logo2.png)

# Arkivenheter i Riksarkivets EAD-format

Hur dataelement i EAD-filen motsvarar presentationen i söktjänsten.

## Volym

[Exempelfil (SE/ULA/10012/A I/1)](examples/data/ra-ead-volym.xml)

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
        
### Bildvisningslänk
        
    <did>
        ...
        <dao xlink:role="IMAGE" xlink:href="https://sok-acc.riksarkivet.se/bildvisning/C0002787?partner=ape" />
        <dao xlink:role="MANIFEST" xlink:href="https://lbiiif-acc.riksarkivet.se/arkis!C0002787/manifest" xlink:title="manifest" />
        <dao xlink:role="SERVICE" xlink:href="https://lbiiif-acc.riksarkivet.se" xlink:title="service" xlink:arcrole="https://iiif.io/api/image/3/level1.json" />
    </did>

## Serie

## Arkiv
