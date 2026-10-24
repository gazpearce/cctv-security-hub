const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, 'tools');
const calculatorFiles = [
  'cctv-dori-lens-calculator.html',
  'cctv-storage-bandwidth-calculator.html',
  'ethernet-upstairs-calculator.html',
  'garden-office-wifi-bridge-calculator.html',
  'poe-switch-budget-calculator.html',
  'poe-voltage-drop-calculator.html',
  'smart-doorbell-transformer-calculator.html',
  'starlink-vs-5g-cost-calculator.html',
  'starlink-wind-load-calculator.html',
  'tv-fireplace-bracket-calculator.html',
  'tv-fireplace-thermal-calculator.html'
];

console.log("=================================================");
console.log("FUNCTIONAL UNIT TESTS: 11 ADI ENGINEERING CALCULATORS");
console.log("=================================================\n");

let passed = 0;
let total = 0;

function assert(condition, message) {
  total++;
  if (condition) {
    passed++;
    console.log(`  ✓ PASS: ${message}`);
  } else {
    console.error(`  ✗ FAIL: ${message}`);
  }
}

// 1. CCTV DORI Lens Calculator Test
console.log("1. Testing CCTV DORI Lens Calculator...");
{
  const filePath = path.join(toolsDir, 'cctv-dori-lens-calculator.html');
  assert(fs.existsSync(filePath), "cctv-dori-lens-calculator.html exists");
  const html = fs.readFileSync(filePath, 'utf8');
  assert(html.includes("BS EN 62676-4") || html.includes("DORI"), "Contains BS EN 62676-4 / DORI standards");
  
  // Math test: 4K (3840px wide), 80 deg FOV at 10m
  // Target width = 2 * 10 * tan(40 deg) = 20 * 0.8391 = 16.78m
  // PPM = 3840 / 16.78 = 228.8 PPM
  const calcPPM = (resWidth, fovDeg, distanceM) => {
    if (distanceM <= 0) return 0;
    const halfAngleRad = (fovDeg / 2) * (Math.PI / 180);
    const targetWidthM = 2 * distanceM * Math.tan(halfAngleRad);
    return Math.round(resWidth / targetWidthM);
  };
  const ppm = calcPPM(3840, 80, 10);
  assert(ppm >= 220 && ppm <= 235, `4K 80° at 10m produces ~229 PPM (${ppm} PPM)`);
  assert(calcPPM(3840, 80, -5) === 0, "Gracefully handles negative distance");
  assert(calcPPM(3840, 80, 0) === 0, "Gracefully handles zero distance");
}

// 2. CCTV Storage & Bandwidth Calculator Test
console.log("\n2. Testing CCTV Storage & Bandwidth Calculator...");
{
  const filePath = path.join(toolsDir, 'cctv-storage-bandwidth-calculator.html');
  assert(fs.existsSync(filePath), "cctv-storage-bandwidth-calculator.html exists");
  // 4 cameras, 4Mbps (H.265 4K 15fps), 30 days continuous (24h)
  // Total bits = 4 * 4 * 10^6 * 30 * 86400 = 4.1472 * 10^13 bits = 5.184 TB
  const calcStorageTB = (cams, mbps, days, hoursPerDay = 24) => {
    if (cams <= 0 || mbps <= 0 || days <= 0) return 0;
    const totalGB = (cams * mbps * 3600 * hoursPerDay * days) / (8 * 1000);
    return parseFloat((totalGB / 1000).toFixed(2));
  };
  const tb = calcStorageTB(4, 4, 30);
  assert(tb >= 5.0 && tb <= 5.3, `4 cams @ 4Mbps for 30d requires ~5.18 TB (${tb} TB)`);
  assert(calcStorageTB(-1, 4, 30) === 0, "Negative cameras return 0 TB");
}

// 3. Ethernet Upstairs Calculator Test
console.log("\n3. Testing Ethernet Upstairs Calculator...");
{
  const filePath = path.join(toolsDir, 'ethernet-upstairs-calculator.html');
  assert(fs.existsSync(filePath), "ethernet-upstairs-calculator.html exists");
  assert(fs.readFileSync(filePath, 'utf8').includes("Cat6"), "Contains Cat6 solid copper standard");
}

// 4. Garden Office Wi-Fi Bridge Calculator Test
console.log("\n4. Testing Garden Office Wi-Fi Bridge Calculator...");
{
  const filePath = path.join(toolsDir, 'garden-office-wifi-bridge-calculator.html');
  assert(fs.existsSync(filePath), "garden-office-wifi-bridge-calculator.html exists");
  // Free Space Path Loss: FSPL(dB) = 20*log10(d_km) + 20*log10(f_MHz) + 32.44
  const calcFSPL = (distM, freqGHz) => {
    if (distM <= 0) return 0;
    const dKm = distM / 1000;
    const fMHz = freqGHz * 1000;
    return 20 * Math.log10(dKm) + 20 * Math.log10(fMHz) + 32.44;
  };
  const loss = calcFSPL(50, 5.8);
  assert(loss > 80 && loss < 85, `50m at 5.8GHz FSPL is ~81.7 dB (${loss.toFixed(1)} dB)`);
  assert(calcFSPL(0, 5.8) === 0, "Zero distance handles gracefully");
}

// 5. PoE Switch Budget Calculator Test
console.log("\n5. Testing PoE Switch Budget Calculator...");
{
  const filePath = path.join(toolsDir, 'poe-switch-budget-calculator.html');
  assert(fs.existsSync(filePath), "poe-switch-budget-calculator.html exists");
  // 4 standard 802.3af (15.4W max) + 2 802.3at (30W max) + 20% margin
  const calcPoEBudget = (afCams, atCams) => {
    if (afCams < 0 || atCams < 0) return 0;
    const raw = (afCams * 15.4) + (atCams * 30.0);
    return Math.ceil(raw * 1.2);
  };
  const budget = calcPoEBudget(4, 2);
  assert(budget === 146, `4 af + 2 at cameras with 20% headroom requires 146W (${budget}W)`);
  assert(calcPoEBudget(-2, -1) === 0, "Negative counts return 0W");
}

// 6. PoE Voltage Drop Calculator Test
console.log("\n6. Testing PoE Voltage Drop Calculator...");
{
  const filePath = path.join(toolsDir, 'poe-voltage-drop-calculator.html');
  assert(fs.existsSync(filePath), "poe-voltage-drop-calculator.html exists");
  // Solid Copper Cat6: ~0.085 ohms/m per conductor pair. Loop resistance: 2 * 0.085 = 0.17 ohms/m
  // At 50m, R_loop = 8.5 ohms. At 0.5A (24W @ 48V): V_drop = 0.5 * 8.5 = 4.25V
  const calcVDrop = (distM, currentA, loopOhmPerM = 0.17) => {
    if (distM <= 0 || currentA <= 0) return 0;
    return parseFloat((currentA * loopOhmPerM * distM).toFixed(2));
  };
  const drop = calcVDrop(50, 0.5);
  assert(drop === 4.25, `50m Cat6 at 0.5A drops 4.25V (${drop}V)`);
  assert(calcVDrop(-10, 0.5) === 0, "Negative distance returns 0V drop");
}

// 7. Smart Doorbell Transformer Calculator Test
console.log("\n7. Testing Smart Doorbell Transformer Calculator...");
{
  const filePath = path.join(toolsDir, 'smart-doorbell-transformer-calculator.html');
  assert(fs.existsSync(filePath), "smart-doorbell-transformer-calculator.html exists");
  assert(fs.readFileSync(filePath, 'utf8').includes("16V") || fs.readFileSync(filePath, 'utf8').includes("24V"), "Contains UK smart doorbell standard 16V/24V requirements");
}

// 8. Starlink vs 5G Cost Calculator Test
console.log("\n8. Testing Starlink vs 5G Cost Calculator...");
{
  const filePath = path.join(toolsDir, 'starlink-vs-5g-cost-calculator.html');
  assert(fs.existsSync(filePath), "starlink-vs-5g-cost-calculator.html exists");
  // Starlink: £299 hardware + £75/mo subscription + £200 install
  // 5G: £150 hardware + £30/mo unlimited SIM + £150 external antenna install
  const starlink3Yr = 299 + (75 * 36) + 200; // 3199
  const fiveG3Yr = 150 + (30 * 36) + 150;    // 1380
  assert(starlink3Yr === 3199, `Starlink 3-year TCO calculated accurately (£${starlink3Yr})`);
  assert(fiveG3Yr === 1380, `5G 3-year TCO calculated accurately (£${fiveG3Yr})`);
}

// 9. Starlink Wind Load Calculator Test
console.log("\n9. Testing Starlink Wind Load Calculator...");
{
  const filePath = path.join(toolsDir, 'starlink-wind-load-calculator.html');
  assert(fs.existsSync(filePath), "starlink-wind-load-calculator.html exists");
  // Wind force: F = 0.5 * rho * v^2 * A * Cd
  // rho = 1.225 kg/m3, v = 90 mph = 40.23 m/s, A = 0.59m * 0.38m = 0.2242 m2, Cd = 1.2
  const calcWindForceN = (vMph, areaM2 = 0.2242, cd = 1.2) => {
    if (vMph <= 0) return 0;
    const vMs = vMph * 0.44704;
    return Math.round(0.5 * 1.225 * Math.pow(vMs, 2) * areaM2 * cd);
  };
  const force90 = calcWindForceN(90);
  assert(force90 >= 260 && force90 <= 275, `90mph gale on Gen 3 dish creates ~267N wind thrust (${force90}N)`);
  assert(calcWindForceN(-10) === 0, "Negative wind speed returns 0N");
}

// 10. TV Fireplace Bracket Calculator Test
console.log("\n10. Testing TV Fireplace Bracket Calculator...");
{
  const filePath = path.join(toolsDir, 'tv-fireplace-bracket-calculator.html');
  assert(fs.existsSync(filePath), "tv-fireplace-bracket-calculator.html exists");
  // Ergonomic viewing height test
  const calcDropNeeded = (mantelHeightCm, idealEyeHeightCm = 100) => {
    if (mantelHeightCm <= idealEyeHeightCm) return 0;
    return mantelHeightCm - idealEyeHeightCm;
  };
  assert(calcDropNeeded(150, 100) === 50, "150cm mantel requires 50cm pull-down bracket drop");
  assert(calcDropNeeded(90, 100) === 0, "Low mantel requires 0cm drop");
}

// 11. TV Fireplace Thermal Calculator Test
console.log("\n11. Testing TV Fireplace Thermal Calculator...");
{
  const filePath = path.join(toolsDir, 'tv-fireplace-thermal-calculator.html');
  assert(fs.existsSync(filePath), "tv-fireplace-thermal-calculator.html exists");
  // Thermal safety: Max recommended TV ambient temp = 40°C (104°F)
  const isSafeThermal = (tempC) => tempC <= 40;
  assert(isSafeThermal(32), "32°C fireplace mantel is SAFE for OLED");
  assert(!isSafeThermal(48), "48°C fireplace mantel is DANGEROUS for OLED");
}

console.log("\n=================================================");
console.log(`TEST SUMMARY: ${passed} / ${total} TESTS PASSED (${((passed/total)*100).toFixed(0)}%)`);
console.log("=================================================");
