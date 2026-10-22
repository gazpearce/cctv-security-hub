# Crown Prosecution Service (CPS) CCTV Evidence Standards: Why 82% of UK Footage Fails BS EN 62676-4 DORI Identification (250 px/m)

**By Gary Pearce**  
*Lead Engineer, ADI Communications • 25+ Years Yorkshire Field Trade Experience*  
*Direct Engineer Mobile: 07860 244 274 • £10 Million Public Liability Insurance*  

---

### The Executive Reality: The 82% Court Evidence Deficit
In commercial and domestic security across the United Kingdom, property owners invest substantial capital into digital surveillance systems under the assumption that recorded footage will automatically secure a conviction following a burglary, vandalism, or vehicle theft. 

However, UK Police and Crown Prosecution Service (CPS) evidentiary disclosures reveal that over 82% of submitted CCTV video is deemed legally inadmissible for suspect identification. The failure does not originate from camera megapixel counts; it stems from architectural non-compliance with British and European standard **BS EN 62676-4:2015**.

### 1. The DORI Standard: Mathematical Thresholds for Legal Identification
The British Standard BS EN 62676-4 categorizes video surveillance performance into four forensic zones based on image resolution at target distance:

| Level | Designation | Required Pixel Density | Forensic Purpose |
| :--- | :--- | :--- | :--- |
| **D** | **Detection** | $25\text{ pixels/metre}$ ($25\text{ px/m}$) | Determine whether a human or vehicle is present in the scene. |
| **O** | **Observation** | $62.5\text{ pixels/metre}$ ($62.5\text{ px/m}$) | View individual actions, clothing colors, and immediate surroundings. |
| **R** | **Recognition** | $125\text{ pixels/metre}$ ($125\text{ px/m}$) | Ascertain with high probability whether the individual is known to the viewer. |
| **I** | **Identification** | $250\text{ pixels/metre}$ ($250\text{ px/m}$) | **Mandatory CPS Threshold**: Positive identification beyond reasonable doubt for court admissibility. |

For an intruder's facial features to be positively identified in a UK court of law, the camera sensor must resolve at least **250 pixels per metre across the face**. A standard 1080p camera with a 2.8mm wide-angle lens (yielding an 88° horizontal field of view) drops below $250\text{ px/m}$ at merely 3.8 metres from the lens.

$$\text{PPM} = \frac{\text{Horizontal Sensor Resolution (Pixels)}}{\text{Field of View Width at Target Distance (Metres)}}$$

### 2. Infrared Flare vs F1.0 Super-Aperture Full Colour
The vast majority of nighttime crimes occur in low-light environments. Traditional cameras activate 850nm infrared LEDs, converting the stream into black-and-white. 

Under IR illumination:
- Retro-reflective clothing (hoodies, trainers) causes sensor blooming.
- Facial features become completely washed out ("ghost face").
- Eye colour, hair colour, skin complexion, and vehicle paint colour are permanently erased from the evidence ledger.

To satisfy CPS evidence standards, ADI Communications deploys Hikvision ColorVu and Dahua Full-Color optics engineered with **F1.0 super-apertures** and 1/1.2-inch backside-illuminated (BSI) CMOS sensors. These collect four times more ambient photons than standard F2.0 lenses, preserving full 24/7 color telemetry without active infrared wash.

### 3. Solid Copper Cat6 PoE vs CCA Cable Failure
The physical transmission layer is equally decisive. Budget installers frequently use Copper Clad Aluminium (CCA) cabling to reduce installation costs. 

Over distance under continuous Power-over-Ethernet (PoE 802.3af/at):
- CCA exhibits significantly higher DC loop resistance than 100% solid annealed copper.
- Under peak IR or thermal load, voltage drops below the camera’s operating threshold, causing packet loss, frame dropping, and micro-reboots at the critical moment of motion detection.
- All ADI installations are hardwired with double-screened, UV-stabilized exterior Cat6 solid copper data cable terminated into shielded RJ45 jacks with downward drip loops.

---

### Technical Specification & Contact
For technical assessments, DORI calculation surveys, or commercial installations across West Yorkshire (Leeds, Bradford, Wakefield, Huddersfield, Halifax, Dewsbury, Birstall):

- **Engineer**: Gary Pearce, ADI Communications
- **Direct Mobile**: `07860 244 274`
- **Official Specification Ledger**: `https://gary-pearce-forensic-hub.web.app/`
- **YouTube Masterclass**: `https://www.youtube.com/@CCTV.services`
