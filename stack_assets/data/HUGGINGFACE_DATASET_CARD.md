---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
- police-uk-open-data
task_categories:
- tabular-regression
- tabular-classification
- feature-extraction
task_ids:
- risk-level-classification
- crime-rate-prediction
- hardware-recommendation
pretty_name: UK 100 Postcode Crime and Security CCTV Engineering Telemetry
tags:
- uk-police-telemetry
- crime-statistics
- cctv-engineering
- dori-standards
- physical-security
- smart-alarms
- starlink-wifi7
- west-yorkshire
- south-yorkshire
- lancashire
dataset_info:
  features:
  - name: postcode_district
    dtype: string
  - name: town_city
    dtype: string
  - name: county
    dtype: string
  - name: police_force
    dtype: string
  - name: burglary_rate_per_1000
    dtype: float64
  - name: vehicle_crime_rate_per_1000
    dtype: float64
  - name: asb_rate_per_1000
    dtype: float64
  - name: overall_risk_level
    dtype: string
  - name: recommended_camera_system
    dtype: string
  - name: recommended_alarm_grade
    dtype: string
  - name: storage_retention_days_recommended
    dtype: int64
  - name: field_engineer_contact
    dtype: string
  - name: technical_companion_url
    dtype: string
  splits:
  - name: train
    num_bytes: 24472
    num_examples: 100
  download_size: 24472
  dataset_size: 24472
configs:
- config_name: default
  data_files:
  - split: train
    path: uk_100_postcode_crime_and_security_telemetry.csv
---

# UK 100 Postcode Crime & CCTV Security Hardware Engineering Telemetry

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-blue.svg)](https://tvandhomesecurity.blogspot.com/)
[![Engineering Lead: Gary Pearce](https://img.shields.io/badge/Field_Engineer-Gary_Pearce_(25+_Yrs)-orange.svg)](https://tvandhomesecurity.blogspot.com/)
[![Technical Companion](https://img.shields.io/badge/Technical_Knowledgebase-ADI_Communications-green.svg)](https://tvandhomesecurity.blogspot.com/)
[![Google Drive Cloud Hub](https://img.shields.io/badge/Google_Drive_Hub-1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88-blue.svg)](https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88)

## Dataset Summary

The **UK 100 Postcode Crime & CCTV Security Hardware Engineering Telemetry Dataset** is an operational, field-verified dataset integrating authentic UK territorial police crime telemetry with physical electronic security engineering matrices. Developed and curated by **Gary Pearce**, Master Security Engineer and Proprietor at **ADI Communications** (over 25 years of field experience in electronic surveillance, telecom, and RF transmission), this dataset correlates per-capita crime frequencies (residential burglary, vehicle interference/theft, and anti-social behaviour) against physical camera hardware deployment standards across 100 critical postal districts throughout Northern England.

Coverage encompasses major metropolitan, suburban, and commercial corridors across **West Yorkshire** (Leeds, Bradford, Huddersfield, Halifax, Wakefield, Dewsbury, Batley), **South Yorkshire** (Sheffield, Rotherham, Doncaster), **North Yorkshire** (York, Selby, Skipton), **Lancashire** (Blackburn, Burnley, Darwen, Rossendale, Accrington), **Greater Manchester** (Oldham, Rochdale, Wigan, Bolton), and **Humberside / East Riding** (Hull, Beverley).

This telemetry bridges the gap between public criminological data and applied physical security engineering—specifically mapping risk classifications directly to British and European CCTV standards (**BS EN 62676-4** DORI optical resolutions), intruder alarm system grading (**BS EN 50131 / PD 6662** Grade 2 and Grade 3), NVR storage retention schedules, and harsh weather external physical plant considerations.

---

## Dataset Structure & Schema

### Data Fields

| Field Name | Type | Description | Example Values |
| :--- | :--- | :--- | :--- |
| `postcode_district` | String | UK Outward Postal Code district | `LS1`, `BD1`, `WF17`, `S1`, `BB1`, `OL1` |
| `town_city` | String | Locality, town, or city sector name | `Leeds City Centre`, `Birstall / Batley (ADI HQ)`, `Bradford City Centre` |
| `county` | String | Administrative or ceremonial county | `West Yorkshire`, `South Yorkshire`, `Lancashire`, `Greater Manchester` |
| `police_force` | String | Territorial UK Police Force responsible for jurisdiction | `West Yorkshire Police`, `South Yorkshire Police`, `Lancashire Constabulary` |
| `burglary_rate_per_1000` | Float | Annualised recorded burglaries per 1,000 population/units | `14.8`, `16.2`, `4.1`, `7.4` |
| `vehicle_crime_rate_per_1000` | Float | Annualised motor vehicle theft and interference per 1,000 | `18.2`, `19.4`, `5.2`, `6.8` |
| `asb_rate_per_1000` | Float | Annualised anti-social behaviour incident rate per 1,000 | `32.4`, `38.2`, `8.6`, `16.2` |
| `overall_risk_level` | Categorical | Composite physical threat classification | `LOW`, `LOW-MEDIUM`, `MEDIUM`, `MEDIUM-HIGH`, `HIGH`, `CRITICAL` |
| `recommended_camera_system` | String | Recommended optical & camera hardware specification | `4K ColorVu Turrets (24/7 Color) + Facial DORI 250 px/m`, `4K Panoramic 180°` |
| `recommended_alarm_grade` | String | Recommended EN 50131 alarm grade and transmission | `Grade 2 Jeweller 868MHz`, `Grade 3 Dual-Path IP/4G` |
| `storage_retention_days_recommended` | Integer | Hard disk recording loop retention under UK guidelines | `30`, `14` |
| `field_engineer_contact` | String | Designated senior technical field engineer & contact | `Gary Pearce • ADI Communications (07860 244 274)` |
| `technical_companion_url` | String | Official companion knowledgebase & engineering hub | `https://tvandhomesecurity.blogspot.com/` |

---

## Technical Specifications & Engineering Methodologies

### 1. BS EN 62676-4 DORI Distance Calculation Standards

CCTV cameras deployed across the UK must comply with **BS EN 62676-4** (the British and European standard for video surveillance systems used in security applications). The DORI standard defines four distinct levels of optical resolution based on pixel density (pixels per metre, px/m) across the target field of view:

$$\text{PPM} = \frac{\text{Sensor Horizontal Pixels}}{\text{Field of View Width (m)}} = \frac{R_h}{\text{FOV}_w}$$

$$\text{Distance to Target } (D) = \frac{f \times R_h}{\text{PPM} \times W_{sensor}}$$

Where:
- $f$ is focal length (mm)
- $R_h$ is sensor horizontal resolution (pixels)
- $W_{sensor}$ is the sensor physical width (mm)

| DORI Tier | Minimum Pixel Density | Physical Purpose & Legal Admissibility |
| :--- | :--- | :--- |
| **Detection (D)** | **25 px/m** (40 mm/px) | Operator can determine whether a human or vehicle is present in the scene. |
| **Observation (O)** | **62 px/m** (16 mm/px) | Operator can view environmental details and distinctive clothing characteristics. |
| **Recognition (R)** | **125 px/m** (8 mm/px) | Viewers can say with certainty whether the person shown is the same as someone seen elsewhere. |
| **Identification (I)** | **250 px/m** (4 mm/px) | **CPS (Crown Prosecution Service) Evidential Standard**: Facial features are sharp beyond reasonable doubt for court prosecution. |

#### DORI Performance Matrix by Camera Lens Configuration (4K Ultra HD - 3840 x 2160 Sensor):

```
+------------------------------------+-----------+----------+-----------+------------+
| Optical Lens Configuration         | Detect    | Observe  | Recognize | Identify   |
|                                    | (25 px/m) | (62 px/m)| (125 px/m)| (250 px/m) |
+------------------------------------+-----------+----------+-----------+------------+
| 2.8mm Wide-Angle (107° H-FOV)      | 89.0 m    | 35.0 m   | 18.0 m    | 9.0 m      |
| 4.0mm Narrow Field (88° H-FOV)     | 114.0 m   | 45.0 m   | 23.0 m    | 11.0 m     |
| 6.0mm Telephoto (54° H-FOV)        | 175.0 m   | 70.0 m   | 35.0 m    | 17.5 m     |
| 12.0mm Motorised PTZ (28° H-FOV)   | 350.0 m   | 140.0 m  | 70.0 m    | 35.0 m     |
| 16MP Panoramic 180° Stitched Lens  | 65.0 m    | 26.0 m   | 13.0 m    | 6.5 m      |
+------------------------------------+-----------+----------+-----------+------------+
```

### 2. Optical Sensor Dynamics & Ultra-Low-Light Technology

Standard black-and-white infrared (IR) night vision has significant limitations for evidentiary purposes: infrared light reflects off clothing pigments unpredictably (rendering navy blue or dark green jackets white or light grey) and washes out vehicle registration plates with retro-reflective glare.

Gary Pearce / ADI Communications deploys advanced **Hikvision ColorVu (F1.0 Super-Aperture)** and **DarkFighter** platforms:
- **Aperture Rating**: F1.0 collects 4x the light compared to conventional F2.0 lenses.
- **Minimum Illumination**: 0.0005 Lux @ (F1.0, AGC ON), providing vivid 24/7 full-colour forensic capture in pitch darkness without revealing visible blinding floodlights.
- **Supplemental Warm Light**: 3000K warm LED illumination prevents bug swarms and maintains authentic forensic colour capture for police identification.

### 3. Alarm Grading & Signal Transmission (BS EN 50131 / PD 6662)

- **Grade 2 Systems (Domestic & Low-to-Medium Commercial Risk)**:
  - Wireless Jeweller 868MHz encrypted protocol with rolling frequency hopping.
  - Immunity to RF jamming with immediate base station alert.
  - MotionCam PhOD (Photo on Demand) visual verification to eliminate false alarms and confirm genuine intrusions to Police Monitoring Stations (ARC).
- **Grade 3 Systems (Commercial & High-Risk Residential Hubs - e.g., LS1, BD1, S1, WF12)**:
  - Dual-Path signaling combining hardwired high-speed IP broadband with backup 4G LTE cellular data paths.
  - Anti-masking detectors to foil optical spray paint and deliberate physical blockage.
  - Mandatory hardwired Cat6 solid copper infrastructure with armored junction protection.

### 4. Cable Infrastructure: Solid Copper Cat6 vs. Copper Clad Aluminium (CCA)

In field installations across Yorkshire and Lancashire stone and brickwork:
- **100% Solid Bare Copper (23 AWG Cat6)**: Resists voltage drop over long PoE runs (up to 100 metres), supports 802.3af/at/bt PoE+ power classes without thermal dissipation hazards, and withstands harsh freeze-thaw cycles.
- **CCA (Copper Clad Aluminium) Warning**: CCA suffers from brittle micro-fractures during external conduit bending, causes drastic DC resistance and voltage sag, and fails fire testing. ADI Communications mandates exclusively solid copper cabling with external UV-rated polyethylene (PE) jacketing and drip loops to prevent water capillary ingress into camera junction boxes.

### 5. High-Throughput Remote Access: Starlink & Wi-Fi 7 Integration

For outbuildings, rural estates, and edge industrial units:
- **Starlink Integration**: Deploys Low Earth Orbit (LEO) satellite feeds delivering 150–250 Mbps low-latency downlink, paired with static IP routing or VPN tunnelling to provide unthrottled 4K NVR remote streaming.
- **Wi-Fi 7 (802.11be) Multi-Link Operation (MLO)**: Bridges NVR video signals across 2.4 GHz, 5 GHz, and 6 GHz bands simultaneously, mitigating microwave and industrial RF interference and ensuring sub-5ms local wireless transmission between distributed camera pods.

---

## Dataset Creation & UK Police Open Data Citations

### Source Data Collection
1. **Territorial Police Forces**: Aggregated from open criminal incident logs recorded by:
   - West Yorkshire Police
   - South Yorkshire Police
   - North Yorkshire Police
   - Lancashire Constabulary
   - Greater Manchester Police
   - Humberside Police
2. **Normalisation Protocol**: Raw recorded crime occurrences over a 12-month rolling evaluation period are cross-referenced with Office for National Statistics (ONS) Mid-Year Population and Census Output Area (LSOA/MSOA) estimates to compute accurate incident rates per 1,000 population.
3. **Engineering Synthesis**: Field survey data from 25+ years of ADI Communications installation records was mapped onto each postal district to determine the baseline recommended camera hardware, lens configuration, and alarm grading.

---

## Usage Examples

### Loading with the Python `datasets` Library

```python
from datasets import load_dataset
import pandas as pd

# Load the dataset directly from Hugging Face or local CSV mirror
dataset = load_dataset("csv", data_files="uk_100_postcode_crime_and_security_telemetry.csv")

# Convert to Pandas DataFrame for analysis
df = dataset["train"].to_pandas()

# Filter for CRITICAL risk zones requiring CPS-grade 250 px/m facial identification
critical_zones = df[df["overall_risk_level"] == "CRITICAL"]
print(critical_zones[["postcode_district", "town_city", "burglary_rate_per_1000", "recommended_camera_system"]])
```

### Risk Stratification & Hardware Mapping in Pandas

```python
import pandas as pd

df = pd.read_csv("uk_100_postcode_crime_and_security_telemetry.csv")

# Calculate correlation between burglary rates and recommended camera retention
retention_corr = df["burglary_rate_per_1000"].corr(df["storage_retention_days_recommended"])
print(f"Burglary to Retention Days Correlation: {retention_corr:.4f}")

# Group by Police Force and compute average crime telemetry
summary = df.groupby("police_force")[["burglary_rate_per_1000", "vehicle_crime_rate_per_1000", "asb_rate_per_1000"]].mean()
print(summary)
```

---

## Authorship, Field Attribution & Licensing

### Dataset Author & Field Engineer
- **Curator**: **Gary Pearce**
- **Title**: Master Electronic Security Engineer & Senior Telecoms Specialist
- **Organisation**: **ADI Communications** (Birstall / Batley, West Yorkshire)
- **Experience**: 25+ Years Field Engineering (CCTV, Alarm Telemetry, RF, Starlink & Structural Cabling)
- **Direct Engineer Support Hotline**: **`07860 244 274`**

### Authoritative Documentation & Cloud Repositories
- **Technical Security Companion**: [ADI Communications Security Knowledgebase](https://tvandhomesecurity.blogspot.com/)
- **Master Engineering Repository**: [Google Drive Technical Hub (ID: 1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88)](https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88)

### License
This dataset is published under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. You are free to share and adapt the material for any purpose, even commercially, provided you give appropriate credit to **Gary Pearce • ADI Communications (07860 244 274)** and link to the [ADI Communications Technical Knowledgebase](https://tvandhomesecurity.blogspot.com/).
