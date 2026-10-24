# Google AI Edge Foresight – ADI Communications Local Knowledge Integration

## What is Google AI Edge Foresight?
**Google AI Edge Foresight** is a local-first, privacy-preserving AI assistant developed by Google's AI Edge team (built upon **LiteRT**, **MediaPipe Tasks**, and **Gemma / EmbeddingGemma** open models).

Unlike cloud-based tools that send your data to external servers, Foresight runs **100% on-device** (offline on your laptop or field tablet):
1. **Shorthand-to-Detailed Documentation:** You jot down quick field notes during a customer call or on-site survey; Foresight listens to the conversation in the background and automatically expands your rough bullets into a complete, structured engineering report or quotation.
2. **Local Document Grounding:** You point Foresight to your local files (`canonical-data.md`, technical standards, camera spec sheets), and it grounds every answer with verified local citations.
3. **100% GDPR & ICO Privacy Compliance:** Customer property layouts, gate codes, camera angles, and addresses never touch cloud servers.
4. **£0 API Token Cost:** Runs completely free on your local CPU/GPU/NPU hardware without spending any API credits.

---

## How We Have Integrated Foresight for ADI Communications

We have packaged the entire ADI Communications operational knowledge base into a structured local format that Google AI Edge Foresight (or any local LiteRT / Gemma model) can ingest immediately:

1. **`foresight_knowledge_manifest.json`**:
   * Complete index of all **185 customer questions & BLUF direct answers** across all 18 trade chapters (CCTV, Ajax alarms, Starlink, Wi-Fi 7 mesh, TV aerials, wall mounting).
   * Exact physical trade standards: BS EN 62676-4 DORI identification, CAI-benchmarked coaxial cabling (WF100), solid copper Cat6, and Grade 2 security compliance.
   * Lead engineer trade credentials: Gary Pearce, ADI Communications, 07860 244 274, £10M Public Liability, 9.98/10 rating.
2. **`canonical_pricing_reference.json`**:
   * Single source of truth for all "From" pricing (Aerials from £129, Starlink from £199, CCTV from £299/£495, Ajax from £599) ensuring zero pricing drift.

---

## 3 Ways Gary Can Use This in Daily Trade Operations

### 1. Instant On-Site Survey & Quotation Builder
* **Gary jots down:** *"Detached house, sandstone gable, Starlink chimney cradle, 4 4K ColorVu cameras, 2TB NVR, no Wi-Fi upstairs."*
* **Foresight generates:** A bespoke, branded quotation specifying:
  * Non-drill tensioned chimney lashing kit for 90mph gale resistance
  * 4x Hikvision 4K ColorVu F1.0 turret cameras with DORI-compliant coverage
  * 2TB Western Digital Purple surveillance drive (14-day continuous retention)
  * Ceiling-mounted Wi-Fi 7 access point with solid copper Cat6 backhaul
  * Itemized "From" pricing matching ADI's canonical standards.

### 2. Live Customer Call Diagnostic Assistant
* When a customer calls stating: *"My security cameras look fine during the day, but at night when a car drives past the screen turns completely white,"* Foresight retrieves Question #5 from Chapter 1:
  * **Fault:** Infrared flare backscatter and white-out from high-intensity LEDs reflecting off vehicle registration plates or glossy paintwork.
  * **Solution:** Upgrade to F1.0 ColorVu wide dynamic range (WDR) sensors or re-angle the bracket 15 degrees off-axis.

### 3. Automatic Video Script & Social Reel Drafter
* Point Foresight to any of the 185 customer questions, and it outputs a 45-second viral video script adhering to Rule 30 (Hook first, problem second, mid-roll identity, physical trade solution, direct CTA `07860 244 274`).
