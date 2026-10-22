/**
 * CCTV & Telecom Engineering Mathematics Library (v1.0.0)
 * Open-source physics, electrical, and optical calculations for UK physical security & telecommunications.
 * Developed by Gary Pearce / ADI Communications (https://gary-pearce-forensic-hub.web.app/ | 07860 244 274)
 * License: MIT
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.CctvEngineeringMath = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var CctvEngineeringMath = {};

  /**
   * 1. BS EN 62676-4 DORI Lens & Pixel Density Calculator
   */
  CctvEngineeringMath.calculateDori = function (options) {
    var resolutionMp = Number(options.resolutionMp) || 4;
    var sensorWidthMm = Number(options.sensorWidthMm) || 5.37; // 1/2.8" standard
    var focalLengthMm = Number(options.focalLengthMm) || 2.8;
    var distanceM = Number(options.distanceM) || 10;

    var horizPixels = 1920;
    if (resolutionMp >= 8) horizPixels = 3840;
    else if (resolutionMp >= 5) horizPixels = 2880;
    else if (resolutionMp >= 4) horizPixels = 2560;

    var hfovRad = 2 * Math.atan(sensorWidthMm / (2 * focalLengthMm));
    var hfovDeg = hfovRad * (180 / Math.PI);
    var sceneWidthM = 2 * distanceM * Math.tan(hfovRad / 2);
    var ppm = horizPixels / sceneWidthM;

    return {
      hfovDeg: Math.round(hfovDeg * 10) / 10,
      sceneWidthM: Math.round(sceneWidthM * 100) / 100,
      ppm: Math.round(ppm * 10) / 10,
      isIdentify: ppm >= 250,
      isRecognize: ppm >= 125,
      isObserve: ppm >= 62,
      isDetect: ppm >= 25,
      maxIdentifyDistanceM: Math.round((horizPixels / (250 * 2 * Math.tan(hfovRad / 2))) * 10) / 10,
      maxRecognizeDistanceM: Math.round((horizPixels / (125 * 2 * Math.tan(hfovRad / 2))) * 10) / 10
    };
  };

  /**
   * 2. Starlink Wind Load & Aerodynamic Drag Calculator
   */
  CctvEngineeringMath.calculateWindLoad = function (options) {
    var dishAreaM2 = Number(options.dishAreaM2) || 0.231; // Gen 3 standard
    var windSpeedMph = Number(options.windSpeedMph) || 90; // UK Pennine gale
    var dragCoefficient = Number(options.dragCoefficient) || 1.15;
    var mastHeightM = Number(options.mastHeightM) || 0.6; // 600mm standoff

    var windSpeedMs = windSpeedMph * 0.44704;
    var airDensity = 1.225; // kg/m^3 at sea level, 15°C
    var dynamicPressurePa = 0.5 * airDensity * Math.pow(windSpeedMs, 2);
    var totalForceN = dynamicPressurePa * dishAreaM2 * dragCoefficient;
    var bendingMomentNm = totalForceN * mastHeightM;
    var shearKg = totalForceN / 9.80665;

    return {
      dynamicPressurePa: Math.round(dynamicPressurePa),
      totalForceN: Math.round(totalForceN * 10) / 10,
      bendingMomentNm: Math.round(bendingMomentNm * 10) / 10,
      shearForceKg: Math.round(shearKg * 10) / 10,
      isSafeSingleBracket: bendingMomentNm < 150,
      recommendedMounting: bendingMomentNm > 250 ? 'Heavy-Duty Chimney Cradle with 5-Metre Galvanised Wire Lashing' : 'Twin Galvanised Pennine Wall Brackets (18-Inch Spacing)'
    };
  };

  /**
   * 3. Ethernet Upstairs Transmission Evaluation
   */
  CctvEngineeringMath.evaluateEthernetUpstairs = function (options) {
    var floorType = options.floorType || 'chipboard'; // chipboard, floorboards, concrete
    var hasExistingCoax = Boolean(options.hasExistingCoax);
    var targetSpeedMbps = Number(options.targetSpeedMbps) || 500;

    return {
      exteriorCat6: {
        maxThroughputMbps: 1000,
        latencyMs: '< 1ms',
        reliabilityPercent: 99.9,
        difficulty: 'Requires external drilling, drip loops & silicone grommet sealing',
        recommended: true
      },
      mocaCoax: {
        maxThroughputMbps: hasExistingCoax ? 1000 : 0,
        latencyMs: '2-4ms',
        reliabilityPercent: hasExistingCoax ? 98.5 : 0,
        difficulty: hasExistingCoax ? 'Plug-and-play adapter at coax outlets' : 'N/A - No coax available',
        recommended: hasExistingCoax && targetSpeedMbps <= 1000
      },
      powerlineAv2: {
        maxThroughputMbps: floorType === 'concrete' ? 95 : 180,
        latencyMs: '8-25ms (jitter prone)',
        reliabilityPercent: 82.0,
        difficulty: 'Plug-in but vulnerable to RCD split-load consumer units & motor noise',
        recommended: false
      }
    };
  };

  /**
   * 4. BS EN 50131-1 Ajax Alarm Grade & Battery Drain Selector
   */
  CctvEngineeringMath.determineAjaxGrade = function (options) {
    var hasHighValueRisk = Boolean(options.hasHighValueRisk);
    var insuranceRequirement = options.insuranceRequirement || 'Grade2';
    var pingIntervalSec = Number(options.pingIntervalSec) || 36;

    var grade = (hasHighValueRisk || insuranceRequirement === 'Grade3') ? 3 : 2;
    var batteryLifeYears = 5;
    if (pingIntervalSec <= 12) batteryLifeYears = 3.2;
    else if (pingIntervalSec >= 60) batteryLifeYears = 6.5;

    return {
      recommendedGrade: grade,
      standardCode: 'BS EN 50131-1:2006+A3:2020',
      technology: grade === 3 ? 'Ajax Fibra (Hardwired Bus) + Jeweller Hybrid' : 'Ajax Jeweller (868MHz Wireless with Frequency Hopping)',
      estimatedBatteryLifeYears: batteryLifeYears,
      backupRuntimeHours: grade === 3 ? 60 : 16
    };
  };

  /**
   * 5. TV Fireplace Thermal & Anchor Calculator
   */
  CctvEngineeringMath.calculateTvFireplaceThermal = function (options) {
    var fireOutputKw = Number(options.fireOutputKw) || 3.5;
    var mantelDepthCm = Number(options.mantelDepthCm) || 15;
    var tvHeightAboveHearthCm = Number(options.tvHeightAboveHearthCm) || 90;
    var isOled = Boolean(options.isOled);

    var baseAmbient = 21;
    var heatRise = (fireOutputKw * 22) / (1 + (mantelDepthCm * 0.08) + (tvHeightAboveHearthCm * 0.015));
    var estimatedTempC = Math.round((baseAmbient + heatRise) * 10) / 10;
    var maxSafeTemp = isOled ? 40 : 45;

    return {
      estimatedSurfaceTempC: estimatedTempC,
      maxAllowableTempC: maxSafeTemp,
      isThermalSafe: estimatedTempC <= maxSafeTemp,
      warning: estimatedTempC > maxSafeTemp ? 'Risk of panel delamination and OLED thermal throttling. Install a deeper deflective mantelpiece.' : 'Thermal profile within manufacturer operating parameters.',
      recommendedFixing: 'Heavy-Duty Corefix 100 or Geebfix Cavity Anchors (Rated 90kg+ in 15mm plasterboard)'
    };
  };

  /**
   * 6. CCTV Storage & Bandwidth Calculator
   */
  CctvEngineeringMath.calculateCctvStorage = function (options) {
    var cameraCount = Number(options.cameraCount) || 4;
    var resolutionMp = Number(options.resolutionMp) || 4;
    var fps = Number(options.fps) || 20;
    var isH265 = options.compression !== 'H264';
    var motionDutyCycle = Number(options.motionDutyCycle) || 0.35; // 35% motion recording
    var retentionDays = Number(options.retentionDays) || 30;

    var baseBitrateKbps = resolutionMp * 1000 * (fps / 25);
    if (isH265) baseBitrateKbps *= 0.55; // 45% savings with H.265+

    var totalBitrateMbps = (baseBitrateKbps * cameraCount) / 1000;
    var totalDailyGb = (totalBitrateMbps * 3600 * 24 * motionDutyCycle) / (8 * 1024);
    var totalRequiredTb = (totalDailyGb * retentionDays) / 1024;
    var recommendedHddTb = Math.ceil(totalRequiredTb * 1.2); // 20% safety margin

    return {
      streamBitratePerCamMbps: Math.round((baseBitrateKbps / 1000) * 100) / 100,
      totalNetworkBandwidthMbps: Math.round(totalBitrateMbps * 100) / 100,
      dailyStorageGb: Math.round(totalDailyGb * 10) / 10,
      totalRawStorageTb: Math.round(totalRequiredTb * 100) / 100,
      recommendedHddSizeTb: recommendedHddTb <= 1 ? 1 : (recommendedHddTb <= 2 ? 2 : (recommendedHddTb <= 4 ? 4 : (recommendedHddTb <= 6 ? 6 : (recommendedHddTb <= 8 ? 8 : 12))))
    };
  };

  /**
   * 7. PoE IEEE 802.3 Voltage Drop Calculator
   */
  CctvEngineeringMath.calculatePoeVoltageDrop = function (options) {
    var cableLengthM = Number(options.cableLengthM) || 50;
    var isSolidCopper = Boolean(options.isSolidCopper !== false);
    var deviceWatts = Number(options.deviceWatts) || 15.4; // 802.3af (15.4W) or 802.3at (30W)
    var supplyVoltage = Number(options.supplyVoltage) || 48.0;

    // Resistance per loop meter (2 conductors)
    // 24 AWG Solid Bare Copper: ~0.17 ohm/loop meter
    // 24 AWG Copper Clad Aluminium (CCA): ~0.29 ohm/loop meter
    var loopResistancePerM = isSolidCopper ? 0.17 : 0.29;
    var totalLoopResistance = cableLengthM * loopResistancePerM;

    var currentAmps = deviceWatts / supplyVoltage;
    var voltageDrop = currentAmps * totalLoopResistance;
    var voltageAtDevice = supplyVoltage - voltageDrop;
    var minOperatingVoltage = 37.0; // IEEE 802.3af minimum at PD

    return {
      totalLoopResistanceOhms: Math.round(totalLoopResistance * 100) / 100,
      currentAmps: Math.round(currentAmps * 1000) / 1000,
      voltageDropVolts: Math.round(voltageDrop * 100) / 100,
      voltageAtDeviceVolts: Math.round(voltageAtDevice * 100) / 100,
      isPass: voltageAtDevice >= minOperatingVoltage,
      rebootLoopRisk: !isSolidCopper && cableLengthM > 40 && deviceWatts > 12,
      recommendation: isSolidCopper ? 'Solid 100% Annealed Copper Cat6 verified safe.' : 'WARNING: Copper Clad Aluminium (CCA) causes dusk reboot loops when camera IR turns on. Replace with solid copper.'
    };
  };

  /**
   * 8. Starlink vs 5G Rural Total Cost of Ownership (TCO)
   */
  CctvEngineeringMath.calculateStarlinkVs5gTco = function (options) {
    var starlinkHardware = Number(options.starlinkHardware) || 399;
    var starlinkMonthly = Number(options.starlinkMonthly) || 75;
    var starlinkInstall = Number(options.starlinkInstall) || 199;

    var fiveGHardware = Number(options.fiveGHardware) || 99;
    var fiveGMonthly = Number(options.fiveGMonthly) || 35;
    var fiveGInstall = Number(options.fiveGInstall) || 120;

    var calcYear = function (years) {
      var months = years * 12;
      return {
        starlink: starlinkHardware + starlinkInstall + (starlinkMonthly * months),
        fiveG: fiveGHardware + fiveGInstall + (fiveGMonthly * months)
      };
    };

    return {
      year1: calcYear(1),
      year2: calcYear(2),
      year3: calcYear(3),
      breakEvenSummary: '5G has lower upfront cost but Starlink provides guaranteed 150-300Mbps unthrottled satellite coverage where 4G/5G mast capacity drops during peak rural evening congestion.'
    };
  };

  /**
   * 9. Garden Office 60GHz / 5GHz Wi-Fi Bridge Calculator
   */
  CctvEngineeringMath.calculateGardenOfficeBridge = function (options) {
    var distanceM = Number(options.distanceM) || 75;
    var freqGhz = Number(options.freqGhz) || 5; // 5GHz or 60GHz
    var antennaHeightM = Number(options.antennaHeightM) || 3.5;
    var maxObstacleHeightM = Number(options.maxObstacleHeightM) || 2.0;

    var distanceKm = distanceM / 1000;
    // 1st Fresnel Zone Radius: r = 8.656 * sqrt(d_km / f_ghz)
    var fresnelRadiusM = 8.656 * Math.sqrt(distanceKm / freqGhz);
    var sixtyPercentFresnelM = fresnelRadiusM * 0.6;
    var pathMidpointHeightM = antennaHeightM;
    var obstacleClearanceM = pathMidpointHeightM - maxObstacleHeightM;

    return {
      fresnelRadiusM: Math.round(fresnelRadiusM * 100) / 100,
      requiredClearanceM: Math.round(sixtyPercentFresnelM * 100) / 100,
      actualClearanceM: Math.round(obstacleClearanceM * 100) / 100,
      isLineOfSightClear: obstacleClearanceM >= sixtyPercentFresnelM,
      recommendedTechnology: distanceM > 100 || obstacleClearanceM < sixtyPercentFresnelM ? 'Pre-terminated Steel Wire Armoured (SWA) Fibre Optic Cable' : (freqGhz >= 60 ? '60GHz Multi-Gigabit Wireless PtP Bridge (Sub-1ms Latency)' : '5GHz Outdoor MIMO Beam Bridge')
    };
  };

  /**
   * 10. Smart Video Doorbell Transformer & Chime Calculator
   */
  CctvEngineeringMath.calculateDoorbellTransformer = function (options) {
    var doorbellType = options.doorbellType || 'Ring Pro 2'; // Ring Pro 2, Nest, Reolink PoE
    var wireLengthM = Number(options.wireLengthM) || 12;
    var existingVoltage = Number(options.existingVoltage) || 8; // Old UK bell transformers are 8V-12V 5VA

    var requiredMinVa = 30;
    var requiredMinVolts = 16;
    var isUpgradedTransformer = existingVoltage >= requiredMinVolts;

    return {
      doorbellModel: doorbellType,
      currentVoltage: existingVoltage + 'V AC',
      isExistingTransformerCompatible: isUpgradedTransformer,
      recommendedTransformer: '24V AC 30VA DIN-Rail Transformer (Hager/BG Electrical)',
      recommendedWedgeAngle: '15-degree or 30-degree masonry corner wedge bracket to eliminate brick reveal infrared bounce',
      poeOptionAvailable: doorbellType.indexOf('PoE') !== -1 || doorbellType.indexOf('Reolink') !== -1
    };
  };

  return CctvEngineeringMath;
}));
