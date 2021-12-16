![Riksarkivet](https://sok.riksarkivet.se/Administration/Images/Layout/logo2.png)

# Arkivenheter i Riksarkivets EAD-format

Hur dataelement i EAD-filen motsvarar presentationen i söktjänsten.

## Volym

[Exempelfil 1 (SE/ULA/10012/A I/1)](examples/data/ra-ead-volym-se-ula-10012-aI1.xml)
[Exempelfil 2 (SE/KrA/0414/0028/0006)](examples/data/ra-ead-volym-se-kra-0414-0028-0006.xml)

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

### Senast ändrad
        
    <revisiondesc>
			...
			<change>
				<date calendar="gregorian" era="ce">2021-11-18T13:53:13.173Z</date>
				<item>Senaste uppdatering i Arkis</item>
			</change>
    </revisiondesc>


## Serie

## Arkiv
