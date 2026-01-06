const socket = io("http://127.0.0.1:5000");

// UI elements
const studentIdEl = document.getElementById("studentId");
const statusBadge = document.getElementById("statusBadge");
const questionText = document.getElementById("questionText");
const questionNumber = document.getElementById("questionNumber");
const currentAnswerEl = document.getElementById("currentAnswer");
const feedbackEl = document.getElementById("feedback");

// State
let currentAnswer = "";
let correctAnswer = null;
let testActive = false;

// Socket connection
socket.on("connect", () => {
  studentIdEl.textContent = "Student connected";
  statusBadge.textContent = "Connected";
  statusBadge.className = "status-badge status-connected";
});

// Test started
socket.on("test_started", (data) => {
  testActive = true;
  currentAnswer = "";
  correctAnswer = String(data.first_question.correct_answer);

  questionText.textContent = data.first_question.question;
  questionNumber.textContent = `Question 1 / ${data.questions.length}`;
  currentAnswerEl.textContent = "";

  statusBadge.textContent = "Test Active";
  statusBadge.className = "status-badge status-active";
});

// Raw TUIO marker input
socket.on("tuio_marker", (data) => {
  if (!testActive) return;

  const id = data.marker_id;
  console.log("Marker detected:", id);

  // 0–9 → digits
  if (id >= 0 && id <= 9) {
    currentAnswer += id.toString();
    updateAnswerUI();
  }

  // 51 → clear
  if (id === 51) {
    currentAnswer = "";
    updateAnswerUI();
  }

  // 50 → confirm
  if (id === 50) {
    confirmAnswer();
  }
});

// Update UI
function updateAnswerUI() {
  currentAnswerEl.textContent = currentAnswer;
}

// Confirm logic
function confirmAnswer() {
  if (currentAnswer.length === 0) return;

  const isCorrect = currentAnswer === correctAnswer;

  feedbackEl.textContent = isCorrect
    ? "Correct ✔"
    : `Incorrect ✘ (Correct: ${correctAnswer})`;

  feedbackEl.className =
    "feedback show " + (isCorrect ? "correct" : "incorrect");

  console.log("Answer confirmed:", currentAnswer, isCorrect);

  testActive = false; // stop further input
}

const canvas = document.getElementById("markerCanvas");
const ctx = canvas.getContext("2d");

socket.on("tuio_marker", (data) => {
  const { marker_id, x, y, angle } = data;

const socket = io();
socket.on("tuio_marker", data => {
    console.log("Marker:", data.marker_id, data.x, data.y);

    // Example: map marker 50 to option A
    if (data.marker_id === 50) {
        document.getElementById("optionA").classList.add("active");
    }
});

  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Convert normalized coords to pixels
  const px = x * canvas.width;
  const py = y * canvas.height;

  // Draw marker
  ctx.beginPath();
  ctx.arc(px, py, 20, 0, Math.PI * 2);
  ctx.fillStyle = "rgba(0, 120, 255, 0.6)";
  ctx.fill();
  ctx.stroke();

  // Draw ID
  ctx.fillStyle = "black";
  ctx.font = "14px Arial";
  ctx.fillText(`ID: ${marker_id}`, px - 15, py - 25);
});
