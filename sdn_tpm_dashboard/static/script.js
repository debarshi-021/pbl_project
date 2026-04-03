const deviceBody = document.getElementById("device-body");
const globalStatus = document.getElementById("global-status");
const spinner = document.getElementById("spinner");

function updateGlobalStatus(devices) {
  let statusClass = "waiting";
  let statusText = "WAITING FOR DEVICES...";

  if (devices.length > 0) {
    const hasAuthenticated = devices.some(d => d.status === "AUTHENTICATED");
    if (hasAuthenticated) {
      statusClass = "authenticated";
      statusText = "TRUSTED DEVICE CONNECTED";
    } else {
      statusClass = "rejected";
      statusText = "UNTRUSTED DEVICES DETECTED";
    }
  }

  globalStatus.className = `status ${statusClass} pulse`;
  globalStatus.querySelector(".label").textContent = statusText;
}

function renderRows(devices) {
  if (!devices.length) {
    deviceBody.innerHTML = `
      <tr class="empty-row">
        <td colspan="5">No devices detected yet.</td>
      </tr>
    `;
    return;
  }

  const rows = devices
    .map(device => {
      const statusClass = device.status === "AUTHENTICATED" ? "authenticated" : "rejected";
      return `
        <tr>
          <td>${device.id}</td>
          <td>${device.path}</td>
          <td><span class="chip ${statusClass}">${device.status}</span></td>
          <td>${device.reason}</td>
          <td>${device.time}</td>
        </tr>
      `;
    })
    .join("");

  deviceBody.innerHTML = rows;
}

async function fetchData() {
  spinner.classList.remove("hidden");
  try {
    const response = await fetch("/scan", { cache: "no-store" });
    const data = await response.json();
    renderRows(data);
    updateGlobalStatus(data);
  } catch (error) {
    console.error("Failed to fetch scan results:", error);
  } finally {
    spinner.classList.add("hidden");
  }
}

fetchData();
setInterval(fetchData, 2000);
