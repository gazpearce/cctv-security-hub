const assert = require('assert');
const math = require('./cctv-engineering-math.js');

console.log('--- RUNNING CCTV ENGINEERING MATH TEST SUITE ---');

// 1. DORI Test
const dori = math.calculateDori({ resolutionMp: 4, sensorWidthMm: 5.37, focalLengthMm: 2.8, distanceM: 10 });
console.log('1. DORI Test: PPM =', dori.ppm, 'Identify =', dori.isIdentify);
assert(dori.ppm > 0, 'DORI PPM should be greater than 0');
assert(typeof dori.hfovDeg === 'number', 'DORI HFOV should be a number');

// 2. Wind Load Test
const wind = math.calculateWindLoad({ dishAreaM2: 0.231, windSpeedMph: 90, mastHeightM: 0.6 });
console.log('2. Wind Load Test: Force =', wind.totalForceN, 'N, Moment =', wind.bendingMomentNm, 'Nm');
assert(wind.totalForceN > 200, 'Total force at 90mph should be > 200N');
assert(wind.bendingMomentNm > 150, 'Bending moment should be > 150Nm');

// 3. Ethernet Upstairs Test
const eth = math.evaluateEthernetUpstairs({ floorType: 'chipboard', hasExistingCoax: true });
console.log('3. Ethernet Test: Cat6 throughput =', eth.exteriorCat6.maxThroughputMbps, 'Mbps');
assert(eth.exteriorCat6.recommended === true, 'Exterior Cat6 should be recommended');

// 4. Ajax Grade Test
const ajax = math.determineAjaxGrade({ hasHighValueRisk: false, pingIntervalSec: 36 });
console.log('4. Ajax Grade Test: Grade =', ajax.recommendedGrade, 'Battery =', ajax.estimatedBatteryLifeYears, 'years');
assert(ajax.recommendedGrade === 2, 'Default should be Grade 2');

// 5. TV Fireplace Thermal Test
const tv = math.calculateTvFireplaceThermal({ fireOutputKw: 3.5, mantelDepthCm: 15, isOled: true });
console.log('5. TV Thermal Test: Temp =', tv.estimatedSurfaceTempC, 'C, Safe =', tv.isThermalSafe);
assert(typeof tv.estimatedSurfaceTempC === 'number', 'Surface temp should be a number');

// 6. CCTV Storage Test
const storage = math.calculateCctvStorage({ cameraCount: 4, resolutionMp: 4, fps: 20, compression: 'H265', retentionDays: 30 });
console.log('6. CCTV Storage Test: HDD =', storage.recommendedHddSizeTb, 'TB');
assert(storage.recommendedHddSizeTb >= 1, 'Storage size should be >= 1TB');

// 7. PoE Voltage Drop Test
const poeSolid = math.calculatePoeVoltageDrop({ cableLengthM: 50, isSolidCopper: true, deviceWatts: 15.4, supplyVoltage: 48 });
const poeCca = math.calculatePoeVoltageDrop({ cableLengthM: 50, isSolidCopper: false, deviceWatts: 15.4, supplyVoltage: 48 });
console.log('7. PoE Test: Solid Copper Volts =', poeSolid.voltageAtDeviceVolts, 'CCA Volts =', poeCca.voltageAtDeviceVolts);
assert(poeSolid.isPass === true, 'Solid copper at 50m should pass');
assert(poeCca.voltageAtDeviceVolts < poeSolid.voltageAtDeviceVolts, 'CCA should drop more voltage than solid copper');

// 8. Starlink vs 5G TCO Test
const tco = math.calculateStarlinkVs5gTco({ years: 3 });
console.log('8. TCO Test: Starlink Year 3 = £', tco.year3.starlink, '5G Year 3 = £', tco.year3.fiveG);
assert(tco.year3.starlink > 0, 'Year 3 cost should be positive');

// 9. Garden Office Bridge Test
const bridge = math.calculateGardenOfficeBridge({ distanceM: 75, freqGhz: 5, antennaHeightM: 3.5, maxObstacleHeightM: 2.0 });
console.log('9. Bridge Test: Fresnel radius =', bridge.fresnelRadiusM, 'm, Clear =', bridge.isLineOfSightClear);
assert(bridge.fresnelRadiusM > 0, 'Fresnel radius should be positive');

// 10. Doorbell Transformer Test
const doorbell = math.calculateDoorbellTransformer({ doorbellType: 'Ring Pro 2', existingVoltage: 8 });
console.log('10. Doorbell Test: Compatible =', doorbell.isExistingTransformerCompatible, 'Recommended =', doorbell.recommendedTransformer);
assert(doorbell.isExistingTransformerCompatible === false, '8V should be incompatible with Ring Pro 2');

console.log('--- ALL 10 TESTS PASSED (100% VERIFIED) ---');
