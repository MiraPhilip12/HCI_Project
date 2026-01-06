const API_BASE = "http://127.0.0.1:5000";
const socket = io(API_BASE);

const ageSelect = document.getElementById("ageGroupSelect");
const subjectSelect = document.getElementById("subjectSelect");
const logContainer = document.getElementById("logContainer");

function log(msg) {
  const time = new Date().toLocaleTimeString();
  const div = document.createElement("div");
  div.className = "log-entry";
  div.innerHTML = `<div class="log-time">[${time}]</div><div class="log-message">${msg}</div>`;
  logContainer.appendChild(div);
}

socket.on("connect", () => log("Connected to server"));

fetch(`${API_BASE}/api/age_groups`)
  .then(r => r.json())
  .then(data => {
    ageSelect.innerHTML = "";
    data.forEach(v => {
      const o = document.createElement("option");
      o.value = v;          // NUMBER
      o.textContent = v;    // DISPLAY NUMBER
      ageSelect.appendChild(o);
    });
    log("Age groups loaded");
  });

fetch(`${API_BASE}/api/subjects`)
  .then(r => r.json())
  .then(data => {
    subjectSelect.innerHTML = "";
    data.forEach(v => {
      const o = document.createElement("option");
      o.value = v;          // NUMBER
      o.textContent = v;
      subjectSelect.appendChild(o);
    });
    log("Subjects loaded");
  });

window.startSession = function () {
  const age = parseInt(ageSelect.value);
  const subject = parseInt(subjectSelect.value);

  if (Number.isNaN(age) || Number.isNaN(subject)) {
    log("Invalid age or subject — session NOT started");
    return;
  }

  log(`Starting session → Age=${age}, Subject=${subject}`);

  socket.emit("teacher_start_session", { age, subject });
};
