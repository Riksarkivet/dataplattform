![Riksarkivet](https://sok.riksarkivet.se/Administration/Images/Layout/logo2.png)

# Arkivenheter i APE:s EAD-format

APE:s EAD-format har samma grundläggande struktur som [Riksarkivets EAD](RA-EAD.md), denna sida tar främst upp skillnaderna.

## Volym

[Exempelfil 1 (SE/ULA/10012/A I/2)](examples/data/ape-ead-volym-se-ula-10012-aI2.xml)

### Referenskod

    <eadheader ...>
      <eadid countrycode="SE" mainagencycode="SE-ULA" identifier="SE-ULA-10012-A I-2">SE/ULA/10012/AI/2</eadid>
      ...
    </eadheader>

Referenskoden är egentligen **SE/ULA/10012/A I/1**, mellanslaget försvinner i <eadid>-elementets innehåll. Notera också att attributen **mainagencycode** och **identifier** har en ganska strikt formatbegränsning, varför **"/"** i Riksarkivets referenskoder byts ut mot **"-"** i dessa. Attributet **identifier** förekommer i APE:s EAD men inte i Riksarkivets EAD.
    
## Allmän anmärkning
        
    <odd>
      <p>Med ortregister. Innehåller även längder över utflyttat tjänstefolk 1765-1771, 1773-1775 och uppbördslängd över "Åhrliga Påskepenningar af Alunda Sockns Ordinaira Soldater" 1753-1766.</p>
    </odd>

I APE:s EAD redovisas Allmän anmärkning i elementet <odd> i stället för <scopecontent>.
    
### Rättighetsmärkning
    
    <userestrict encodinganalog="3.4.5" type="dao">
      <p>
        <extref xlink:href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</extref>
      </p>
    </userestrict>
  
I APE:s EAD redovisas rättighetsmärkning med en Creative Commons-URI i elementet <userestrict>.

### Länk till posten

    <otherfindaid encodinganalog="3.4.5">
      <p>
        <extref xlink:href="https://sok-acc.riksarkivet.se/arkiv/4MgUgjX9rH6cxG02H087k3">Post i NAD</extref>
      </p>
    </otherfindaid>
  
APE:s EAD innehåller en länk till posten i söktjänsten.
  
### Bildvisningslänk
        
    <did>
      ...
      <dao xlink:role="IMAGE" xlink:href="https://sok.riksarkivet.se/bildvisning/C0002788?partner=ape" />
      <dao xlink:role="MANIFEST" xlink:href="https://lbiiif.riksarkivet.se/arkis!C0002788/manifest" xlink:title="manifest" />
      <dao xlink:role="SERVICE" xlink:href="https://lbiiif.riksarkivet.se" xlink:title="service" xlink:arcrole="https://iiif.io/api/image/3/level1.json" />
    </did>
        
Bildvisningslänkar förekommer i APE:s EAD men inte i Riksarkivets EAD.
