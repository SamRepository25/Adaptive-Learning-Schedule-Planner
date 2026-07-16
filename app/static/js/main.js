const API_BASE = "/api";

// --- DOM references ---
const form = document.getElementById("subject-form");
const formError = document.getElementById("form-error");

const timetableList = document.getElementById("timetable-list");
const timetableEmpty = document.getElementById("timetable-empty");

const examsList = document.getElementById("exams-list");
const examsEmpty = document.getElementById("exams-empty");

const subjectCards = document.getElementById("subject-cards");
const subjectsEmpty = document.getElementById("subjects-empty");

const weeklyGrid = document.getElementById("weekly-grid");
const weeklyEmpty = document.getElementById("weekly-empty");

const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");

const dailyMinutesInput = document.getElementById("daily-minutes");

// --- Helpers ---

function getDailyMinutes() {
    const val = parseInt(dailyMinutesInput.value, 10);
    return (Number.isFinite(val) && val >= 30 && val <= 600) ? val : 120;
}

function urgencyLevel(score) {
    if (score >= 1) return "high";
    if (score >= 0.3) return "medium";
    return "low";
}

function formatDate(isoString) {
    const d = new Date(isoString);
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function showFormError(message) {
    formError.textContent = message;
    formError.hidden = false;
}

function clearFormError() {
    formError.hidden = true;
    formError.textContent = "";
}

// --- Rendering ---

function renderTimetable(timetable) {
    timetableList.innerHTML = "";

    if (timetable.length === 0) {
        timetableEmpty.hidden = false;
        progressText.textContent = "0 / 0 sessions";
        progressFill.style.width = "0%";
        return;
    }
    timetableEmpty.hidden = true;

    let completedCount = 0;
    timetable.forEach((session) => {
        if (session.completed) completedCount++;
        const li = document.createElement("li");
        li.className = "session-row" + (session.completed ? " completed" : "");
        li.innerHTML = `
            <input type="checkbox" class="session-checkbox" data-id="${session.id}" ${session.completed ? "checked" : ""}>
            <span class="session-time">${session.start_time} – ${session.end_time}</span>
            <div class="row-main"><div class="row-title">${escapeHtml(session.name)}</div></div>
        `;
        timetableList.appendChild(li);
    });

    timetableList.querySelectorAll(".session-checkbox").forEach((cb) => {
        cb.addEventListener("change", () => toggleCompletion(cb.dataset.id));
    });

    const pct = Math.round((completedCount / timetable.length) * 100);
    progressFill.style.width = `${pct}%`;
    progressText.textContent = `${completedCount} / ${timetable.length} sessions`;
}

function renderExams(exams) {
    examsList.innerHTML = "";

    if (exams.length === 0) {
        examsEmpty.hidden = false;
        return;
    }
    examsEmpty.hidden = true;

    exams.forEach((exam) => {
        const li = document.createElement("li");
        li.className = "exam-row";
        li.innerHTML = `<span>${escapeHtml(exam.name)}</span><span class="exam-days">${exam.days_left} day(s) left</span>`;
        examsList.appendChild(li);
    });
}

function renderSubjectCards(schedule) {
    subjectCards.innerHTML = "";

    if (schedule.length === 0) {
        subjectsEmpty.hidden = false;
        return;
    }
    subjectsEmpty.hidden = true;

    const difficultyLabel = { 1: "Easy", 3: "Medium", 5: "Hard" };

    schedule.forEach((item) => {
        const div = document.createElement("div");
        div.className = "subject-card";
        div.dataset.level = urgencyLevel(item.urgency_score);
        div.innerHTML = `
            <h3>${escapeHtml(item.name)}</h3>
            <div class="card-row"><span>Difficulty</span><span>${difficultyLabel[item.difficulty]}</span></div>
            <div class="card-row"><span>Exam Date</span><span>${formatDate(item.exam_date)}</span></div>
            <div class="card-row"><span>Days Left</span><span>${item.days_left}</span></div>
            <div class="card-row"><span>Urgency</span><span>${item.urgency_score}</span></div>
            <div class="card-row"><span>Allocated</span><span>${item.allocated_minutes}m</span></div>
            <button class="delete-btn" data-id="${item.id}">Delete</button>
        `;
        subjectCards.appendChild(div);
    });

    subjectCards.querySelectorAll(".delete-btn").forEach((btn) => {
        btn.addEventListener("click", () => deleteSubject(btn.dataset.id));
    });
}

function renderWeeklyPlan(plan) {
    weeklyGrid.innerHTML = "";

    const days = Object.keys(plan);
    if (days.length === 0 || days.every((d) => plan[d].length === 0)) {
        weeklyEmpty.hidden = false;
        return;
    }
    weeklyEmpty.hidden = true;

    days.forEach((day) => {
        const div = document.createElement("div");
        div.className = "weekly-day";
        const items = plan[day].map((name) => `<li>${escapeHtml(name)}</li>`).join("");
        div.innerHTML = `<h4>${day}</h4><ul>${items || "<li>—</li>"}</ul>`;
        weeklyGrid.appendChild(div);
    });
}

function renderDashboard(stats) {
    document.getElementById("stat-total-subjects").textContent = stats.total_subjects;
    document.getElementById("stat-total-minutes").textContent = `${stats.total_daily_minutes}m`;
    document.getElementById("stat-upcoming-exams").textContent = stats.upcoming_exams;
    document.getElementById("stat-sessions-today").textContent = stats.sessions_today;
}

// --- API calls ---

async function loadDashboard() {
    try {
        const res = await fetch(`${API_BASE}/dashboard?daily_minutes=${getDailyMinutes()}`);
        if (!res.ok) throw new Error("Failed to load dashboard");
        renderDashboard(await res.json());
    } catch (err) {
        // Dashboard failures are non-critical; leave placeholders in place.
    }
}

async function loadTimetable() {
    try {
        const res = await fetch(`${API_BASE}/timetable?daily_minutes=${getDailyMinutes()}`);
        if (!res.ok) throw new Error("Failed to load timetable");
        const data = await res.json();
        renderTimetable(data.timetable || []);
    } catch (err) {
        timetableList.innerHTML = "";
        timetableEmpty.hidden = false;
        timetableEmpty.textContent = "Could not load timetable. Check your connection.";
    }
}

async function loadExams() {
    try {
        const res = await fetch(`${API_BASE}/exams/upcoming`);
        if (!res.ok) throw new Error("Failed to load exams");
        const data = await res.json();
        renderExams(data.exams || []);
    } catch (err) {
        examsList.innerHTML = "";
        examsEmpty.hidden = false;
        examsEmpty.textContent = "Could not load exams. Check your connection.";
    }
}

async function loadSubjectCards() {
    try {
        const res = await fetch(`${API_BASE}/schedule?daily_minutes=${getDailyMinutes()}`);
        if (!res.ok) throw new Error("Failed to load subjects");
        const data = await res.json();
        renderSubjectCards(data.schedule || []);
    } catch (err) {
        subjectCards.innerHTML = "";
        subjectsEmpty.hidden = false;
        subjectsEmpty.textContent = "Could not load subjects. Check your connection.";
    }
}

async function loadWeeklyPlan() {
    try {
        const res = await fetch(`${API_BASE}/weekly-plan`);
        if (!res.ok) throw new Error("Failed to load weekly plan");
        const data = await res.json();
        renderWeeklyPlan(data.weekly_plan || {});
    } catch (err) {
        weeklyGrid.innerHTML = "";
        weeklyEmpty.hidden = false;
        weeklyEmpty.textContent = "Could not load weekly plan. Check your connection.";
    }
}

async function refreshAll() {
    await Promise.all([
        loadDashboard(),
        loadTimetable(),
        loadExams(),
        loadSubjectCards(),
        loadWeeklyPlan()
    ]);
}

async function toggleCompletion(subjectId) {
    try {
        const res = await fetch(`${API_BASE}/sessions/${subjectId}/complete`, { method: "POST" });
        if (!res.ok) throw new Error("Failed to update session");
        await Promise.all([loadTimetable(), loadDashboard()]);
    } catch (err) {
        alert("Network error — could not update session. Check your connection.");
    }
}

async function deleteSubject(id) {
    try {
        const res = await fetch(`${API_BASE}/subjects/${id}`, { method: "DELETE" });
        const data = await res.json();
        if (!res.ok) {
            alert(data.error || "Failed to delete subject");
            return;
        }
        await refreshAll();
    } catch (err) {
        alert("Network error — could not delete subject. Check your connection.");
    }
}

async function addSubject(payload) {
    let res;
    try {
        res = await fetch(`${API_BASE}/subjects`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
    } catch (networkErr) {
        throw new Error("Network error — check your connection and try again.");
    }

    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.error || "Failed to add subject");
    }
    return data;
}

// --- Event listeners ---

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearFormError();

    const payload = {
        name: document.getElementById("name").value.trim(),
        exam_date: document.getElementById("exam_date").value,
        difficulty: parseInt(document.getElementById("difficulty").value, 10)
    };

    try {
        await addSubject(payload);
        form.reset();
        document.getElementById("difficulty").value = "3";
        await refreshAll();
    } catch (err) {
        showFormError(err.message);
    }
});

dailyMinutesInput.addEventListener("change", () => {
    loadTimetable();
    loadDashboard();
    loadSubjectCards();
});

// --- Init ---

document.addEventListener("DOMContentLoaded", refreshAll);
