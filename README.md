# ADI Communications: Open-Source Physical Security & Telecom Engineering Suite (2026)

[![Live Web Tools](https://img.shields.io/badge/Live%20Web%20Apps-GitHub%20Pages-FF5500?style=for-the-badge)](https://gazpearce.github.io/cctv-security-hub/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Standards](https://img.shields.io/badge/Standards-BS%20EN%2062676--4%20%7C%20BS%206701-emerald?style=for-the-badge)](https://adicommunications.co.uk/)
[![YouTube](https://img.shields.io/badge/YouTube-CCTV.services-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@CCTV.services)

Official open-source engineering suite, mathematical calculation models, and technical specifications created by **Gary Pearce** (Lead Physical Security & Telecoms Engineer, [ADI Communications](https://adicommunications.co.uk/), Direct Line: `07860 244 274`).

---

## 🛠️ Interactive Diagnostic Web Applications

All tools are client-side, zero-telemetry, and hosted 100% free on GitHub Pages:

### 1. [CCTV Optical Lens & Police Evidence DORI Calculator](https://gazpearce.github.io/cctv-security-hub/cctv-dori-lens-calculator.html)
* **British Standard**: Implements **BS EN 62676-4** surveillance performance standards.
* **Crown Prosecution Service Evidence Requirement**: Calculates the exact focal length ($f$) and optical sensor geometry required to achieve $\ge 250\text{ px/m}$ at property boundary targets for court-admissible facial identification:
  $$f = \frac{\text{Sensor Width (mm)} \times \text{Distance (m)}}{\text{Field Width (m)}}$$
* **Aperture & Low-Light Benchmarks**: Evaluates F1.0 super-apertures (Hikvision ColorVu G2) vs active deterrence dual-light systems (Dahua TiOC 2.0) vs 850nm IR arrays.

### 2. [Starlink Gen 3 & Mini Wind-Load & 90mph Storm Bracket Calculator](https://gazpearce.github.io/cctv-security-hub/starlink-wind-load-calculator.html)
* **Aerodynamic Drag Modeling**: Computes peak dynamic wind force ($F$) and bending moments ($M$) on flat-panel satellite phased arrays during severe UK winter gales:
  $$F = \frac{1}{2} \rho v^2 C_d A$$
  *Where $\rho = 1.225\text{ kg/m}^3$, $v$ is gust velocity in m/s, $C_d$ is drag coefficient ($1.15$), and $A$ is dish area ($0.24\text{ m}^2$ for Gen 3 Standard).*
* **Non-Drill Chimney Lashing Safety Factors**: Verifies that tensioned stainless steel wire cradles exceed British Standard masonry shear limits by $3.4\times$ without drilling into heritage stone or brick.

### 3. [Upstairs Ethernet & Home Network Diagnostic Calculator](https://gazpearce.github.io/cctv-security-hub/ethernet-upstairs-calculator.html)
* **Masonry Attenuation Modeling**: Evaluates 5GHz/6GHz Wi-Fi degradation across UK cavity walls, 9-inch solid brick, and stone barn masonry.
* **Consumer Unit Phase Noise**: Computes powerline speed loss across split-RCD consumer units vs 100% solid bare copper Cat6 cabling (CW1308 / BS 6701).

---

## 🎬 1080p Broadcast Masterclasses (YouTube)

Full unbroken single-take technical engineering breakdowns:

1. **[Starlink Gen 3 & Mini UK Installation: 90mph Gale Chimney Mounts, Bypass & Speed Test](https://youtu.be/dOFIxVqMxCM)** (3:47)
   * *Covers*: Gen 3 kickstand dish vs Mini USB-PD specs, non-drill chimney lashing cradles, 110° northern orbital cone obstruction mapping, and router bypass mode to whole-home Wi-Fi 7 mesh.
2. **[Ajax Smart Alarms UK Masterclass 2026: Why Legacy 433MHz Bells Fail & MotionCam PhOD](https://youtu.be/l-HN4BuzBGQ)** (3:49)
   * *Covers*: Jeweller 868MHz frequency hopping, anti-jamming cellular failover, MotionCam 9-second visual verification, and 113dB StreetSiren storm rigging.
3. **[Hikvision ColorVu vs Infrared CCTV UK: Night Vision, DORI Standards & 4K Police Evidence](https://youtu.be/50q89TsNN3w)** (3:50)
   * *Covers*: Why 850nm IR night vision fails court standards, F1.0 super-apertures, BS EN 62676-4 DORI 250 px/m facial identification targets, hardwired PoE vs Wi-Fi jammers, and AcuSense AI object filtering.

---

## 🎙️ Official Podcast RSS Feed

Direct syndication feed for Spotify, Apple Podcasts, and Google Podcasts:
* **Feed URL**: [`https://gazpearce.github.io/cctv-security-hub/podcast.xml`](https://gazpearce.github.io/cctv-security-hub/podcast.xml)
* **Host**: Gary Pearce (ADI Communications)
* **Audio Format**: 128 kbps Stereo MP3 / 48kHz

---

## 👨‍🔧 Trade E-E-A-T & Contact

* **Lead Engineer**: Gary Pearce
* **Company**: ADI Communications
* **Hands-On Experience**: 25+ Years Physical Security, Aerials & Data Cabling
* **Insurance**: £10 Million Public Liability Insurance
* **Direct Mobile**: `07860 244 274`
* **Website**: [adicommunications.co.uk](https://adicommunications.co.uk/)
* **Blog**: [tvandhomesecurity.blogspot.com](https://tvandhomesecurity.blogspot.com/)
