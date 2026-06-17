const CONFIG = window.DASHBOARD_CONFIG || {};
const DATA_SOURCE = CONFIG.DATA_SOURCE || "local";
const LOCAL_READINGS_URL = CONFIG.LOCAL_READINGS_URL || "../data/firebase-readings.json";
const FIRESTORE_READINGS_URL = CONFIG.FIRESTORE_READINGS_URL || "";
const REFRESH_MS = 5000;
const FINAL_READING_NUMBER = 29;
let visibleReadingCount = 0;
let refreshTimer;

const fields = {
  syncStatus: document.querySelector("#syncStatus"),
  lastUpdated: document.querySelector("#lastUpdated"),
  bedId: document.querySelector("#bedId"),
  healthTitle: document.querySelector("#healthTitle"),
  healthText: document.querySelector("#healthText"),
  healthScore: document.querySelector("#healthScore"),
  temperatureValue: document.querySelector("#temperatureValue"),
  humidityValue: document.querySelector("#humidityValue"),
  moistureValue: document.querySelector("#moistureValue"),
  phValue: document.querySelector("#phValue"),
  temperatureTrend: document.querySelector("#temperatureTrend"),
  humidityTrend: document.querySelector("#humidityTrend"),
  moistureTrend: document.querySelector("#moistureTrend"),
  phTrend: document.querySelector("#phTrend"),
  temperatureMeter: document.querySelector("#temperatureMeter"),
  humidityMeter: document.querySelector("#humidityMeter"),
  moistureMeter: document.querySelector("#moistureMeter"),
  phMeter: document.querySelector("#phMeter"),
  sampleCount: document.querySelector("#sampleCount"),
  trendChart: document.querySelector("#trendChart"),
  avgMoisture: document.querySelector("#avgMoisture"),
  temperatureRange: document.querySelector("#temperatureRange"),
  humidityRange: document.querySelector("#humidityRange"),
  lowestMoisture: document.querySelector("#lowestMoisture"),
  deviceName: document.querySelector("#deviceName"),
  sensorType: document.querySelector("#sensorType"),
  mqttStatus: document.querySelector("#mqttStatus"),
  firebaseStatus: document.querySelector("#firebaseStatus"),
  latestTimestamp: document.querySelector("#latestTimestamp"),
  tableUpdated: document.querySelector("#tableUpdated"),
  readingsTable: document.querySelector("#readingsTable"),
};

function formatNumber(value, digits = 1) {
  return Number(value).toFixed(digits).replace(/\.0$/, "");
}

function average(items, key) {
  return items.reduce((total, item) => total + Number(item[key] || 0), 0) / items.length;
}

function minMax(items, key) {
  const values = items.map((item) => Number(item[key] || 0));
  return [Math.min(...values), Math.max(...values)];
}

function trendLabel(current, previous, suffix = "") {
  if (!previous) return "new";
  const delta = current - previous;
  if (Math.abs(delta) < 0.05) return "steady";
  return `${delta > 0 ? "+" : ""}${formatNumber(delta, 1)}${suffix}`;
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function readingNumber(reading) {
  const match = String(reading.id || "").match(/(\d+)$/);
  return match ? Number(match[1]) : 0;
}

function readingTime(reading) {
  const value = reading.timestamp || reading.createTime || reading.updateTime;
  const time = value ? new Date(value).getTime() : NaN;
  return Number.isNaN(time) ? 0 : time;
}

function sortReadings(first, second) {
  const firstTime = readingTime(first);
  const secondTime = readingTime(second);

  if (firstTime && secondTime && firstTime !== secondTime) {
    return firstTime - secondTime;
  }

  return readingNumber(first) - readingNumber(second);
}

function formatTimestamp(value) {
  if (!value) return "--";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "--";

  return date.toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function normalizeReadings(data) {
  if (Array.isArray(data.documents)) {
    return data.documents
      .map(normalizeFirestoreDocument)
      .filter(Boolean)
      .sort(sortReadings);
  }

  const source = Array.isArray(data.readings)
    ? data.readings
    : data.readings && typeof data.readings === "object"
      ? Object.values(data.readings)
      : [];

  return source
    .filter(Boolean)
    .sort(sortReadings);
}

function unwrapFirestoreValue(value) {
  if (!value || typeof value !== "object") return value;
  if ("stringValue" in value) return value.stringValue;
  if ("integerValue" in value) return Number(value.integerValue);
  if ("doubleValue" in value) return Number(value.doubleValue);
  if ("booleanValue" in value) return Boolean(value.booleanValue);
  if ("timestampValue" in value) return value.timestampValue;
  if ("nullValue" in value) return null;
  return value;
}

function normalizeFirestoreDocument(document) {
  const fields = document.fields || {};
  const reading = {};

  Object.keys(fields).forEach((key) => {
    reading[key] = unwrapFirestoreValue(fields[key]);
  });

  if (!reading.id && document.name) {
    reading.id = document.name.split("/").pop();
  }

  reading.createTime = document.createTime;
  reading.updateTime = document.updateTime;

  return reading;
}

function readingsForCurrentTick(readings) {
  visibleReadingCount = visibleReadingCount >= readings.length ? readings.length : visibleReadingCount + 1;
  return readings.slice(0, visibleReadingCount);
}

function hasReachedFinalReading(readings) {
  const latest = readings.at(-1);
  return latest ? readingNumber(latest) >= FINAL_READING_NUMBER : false;
}

function stopFetchingReadings() {
  if (!refreshTimer) return;
  clearInterval(refreshTimer);
  refreshTimer = null;
}

function buildPath(values, width, height, min, max) {
  const range = max - min || 1;
  return values
    .map((value, index) => {
      const x = values.length === 1 ? width / 2 : (index / (values.length - 1)) * width;
      const y = height - ((value - min) / range) * height;
      return `${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(" ");
}

function renderChart(readings) {
  const width = 900;
  const height = 300;
  const padding = 28;
  const chartWidth = width - padding * 2;
  const chartHeight = height - padding * 2;
  const recent = readings.slice(-18);
  const metrics = [
    { key: "ambient_temp_c", color: "#c46c3d", min: 18, max: 32 },
    { key: "humidity_percent", color: "#2d83a3", min: 35, max: 85 },
    { key: "moisture_percent", color: "#2f7d4b", min: 0, max: 100 },
    { key: "ph", color: "#e7ad42", min: 0, max: 14 },
  ];

  const paths = metrics
    .map((metric) => {
      const values = recent.map((reading) => Number(reading[metric.key] || 0));
      const path = buildPath(values, chartWidth, chartHeight, metric.min, metric.max);
      return `<path d="${path}" transform="translate(${padding} ${padding})" fill="none" stroke="${metric.color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />`;
    })
    .join("");

  const points = recent
    .map((reading, index) => {
      const x = recent.length === 1 ? chartWidth / 2 : (index / (recent.length - 1)) * chartWidth;
      const y = chartHeight - ((Number(reading.moisture_percent || 0) - 0) / 100) * chartHeight;
      return `<circle cx="${(x + padding).toFixed(2)}" cy="${(y + padding).toFixed(2)}" r="4" fill="#2f7d4b" />`;
    })
    .join("");

  fields.trendChart.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true">
      <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="#cfd8cf" stroke-width="1" />
      ${paths}
      ${points}
    </svg>
  `;
}

function healthFromLatest(latest) {
  const moisture = Number(latest.moisture_percent || 0);
  const temp = Number(latest.ambient_temp_c || 0);
  const humidity = Number(latest.humidity_percent || 0);
  const ph = Number(latest.ph || 0);
  let score = 100;

  score -= Math.abs(moisture - 65) * 0.55;
  score -= Math.abs(temp - 23) * 2.2;
  score -= Math.abs(humidity - 62) * 0.45;
  score -= Math.max(0, Math.abs(ph - 7) - 1) * 5;

  const normalized = Math.round(clamp(score, 0, 100));
  if (normalized >= 78) {
    return {
      score: normalized,
      title: "Bed conditions are stable",
      text: "Temperature, humidity, and moisture are holding close to the observed healthy range.",
    };
  }
  if (normalized >= 55) {
    return {
      score: normalized,
      title: "Bed needs light attention",
      text: "One or more readings has drifted from the preferred vermiculture range.",
    };
  }
  return {
    score: normalized,
    title: "Bed needs intervention",
    text: "The latest reading suggests the bed should be checked before conditions stress the worms.",
  };
}

function renderDashboard(readings) {
  const latest = readings.at(-1);
  const previous = readings.at(-2);
  const health = healthFromLatest(latest);
  const [tempMin, tempMax] = minMax(readings, "ambient_temp_c");
  const [humidityMin, humidityMax] = minMax(readings, "humidity_percent");
  const [moistureMin] = minMax(readings, "moisture_percent");

  fields.bedId.textContent = latest.bed_id || "Vermiculture bed";
  fields.healthTitle.textContent = health.title;
  fields.healthText.textContent = health.text;
  fields.healthScore.textContent = health.score;

  fields.temperatureValue.textContent = `${formatNumber(latest.ambient_temp_c)} C`;
  fields.humidityValue.textContent = `${formatNumber(latest.humidity_percent)}%`;
  fields.moistureValue.textContent = `${formatNumber(latest.moisture_percent)}%`;
  fields.phValue.textContent = formatNumber(latest.ph);

  fields.temperatureTrend.textContent = trendLabel(latest.ambient_temp_c, previous?.ambient_temp_c, "C");
  fields.humidityTrend.textContent = trendLabel(latest.humidity_percent, previous?.humidity_percent, "%");
  fields.moistureTrend.textContent = trendLabel(latest.moisture_percent, previous?.moisture_percent, "%");
  fields.phTrend.textContent = trendLabel(latest.ph, previous?.ph, "");

  fields.temperatureMeter.style.width = `${clamp((latest.ambient_temp_c / 40) * 100, 0, 100)}%`;
  fields.humidityMeter.style.width = `${clamp(latest.humidity_percent, 0, 100)}%`;
  fields.moistureMeter.style.width = `${clamp(latest.moisture_percent, 0, 100)}%`;
  fields.phMeter.style.width = `${clamp((latest.ph / 14) * 100, 0, 100)}%`;

  fields.sampleCount.textContent = `${readings.length} readings`;
  fields.avgMoisture.textContent = `${formatNumber(average(readings, "moisture_percent"))}%`;
  fields.temperatureRange.textContent = `${formatNumber(tempMin)}-${formatNumber(tempMax)} C`;
  fields.humidityRange.textContent = `${formatNumber(humidityMin)}-${formatNumber(humidityMax)}%`;
  fields.lowestMoisture.textContent = `${formatNumber(moistureMin)}%`;
  fields.deviceName.textContent = latest.device || "--";
  fields.sensorType.textContent = latest.dht_sensor_type || "--";
  fields.mqttStatus.textContent = latest.mqtt_status || "--";
  fields.firebaseStatus.textContent = latest.firebase_status || "--";
  fields.latestTimestamp.textContent = formatTimestamp(latest.timestamp);
  fields.tableUpdated.textContent = `Showing newest ${Math.min(readings.length, 8)} of ${readings.length}`;

  fields.readingsTable.innerHTML = readings
    .slice(-8)
    .reverse()
    .map(
      (reading) => `
        <tr>
          <td>${reading.id}</td>
          <td class="timestamp-cell">${formatTimestamp(reading.timestamp)}</td>
          <td>${formatNumber(reading.ambient_temp_c)} C</td>
          <td>${formatNumber(reading.humidity_percent)}%</td>
          <td>${formatNumber(reading.moisture_percent)}%</td>
          <td>${formatNumber(reading.ph)}</td>
          <td><span class="status-pill">${reading.status || "NORMAL"}</span></td>
        </tr>
      `
    )
    .join("");

  renderChart(readings);
}

async function fetchReadings() {
  try {
    const dataUrl = DATA_SOURCE === "firestore" ? FIRESTORE_READINGS_URL : LOCAL_READINGS_URL;
    if (!dataUrl) throw new Error("No dashboard data URL configured");

    const separator = dataUrl.includes("?") ? "&" : "?";
    const response = await fetch(`${dataUrl}${separator}t=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const readings = normalizeReadings(data);
    if (!readings.length) throw new Error("No readings found");
    const visibleReadings = readingsForCurrentTick(readings);

    renderDashboard(visibleReadings);
    fields.syncStatus.textContent = "Live data connected";
    fields.lastUpdated.textContent = `Updated ${new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    })} - reading ${visibleReadings.length} of ${readings.length}`;
    document.querySelector(".sync-panel").classList.remove("error");

    if (hasReachedFinalReading(visibleReadings)) {
      stopFetchingReadings();
      fields.syncStatus.textContent = "Reading sequence complete";
      fields.lastUpdated.textContent = `Stopped at reading ${FINAL_READING_NUMBER}`;
    }
  } catch (error) {
    fields.syncStatus.textContent = "Data source unavailable";
    fields.lastUpdated.textContent = "Run from a local web server so fetch can read JSON";
    document.querySelector(".sync-panel").classList.add("error");
    console.error(error);
  }
}

fetchReadings();
refreshTimer = setInterval(fetchReadings, REFRESH_MS);
