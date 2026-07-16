const API_BASE = "/api";

const form = document.getElementById("subject-form");
const formError = document.getElementById("form-error");
const subjectsList = document.getElementById("subjects-list");
const subjectsEmpty = document.getElementById("subjects-empty");
const scheduleList = document.getElementById("schedule-list");
const scheduleEmpty = document.getElementById("schedule-empty");

// --- Helpers ---

function urgencyLevel(score) {
    if (score >= 1) return "high";
    if (score >= 0.3) return "medium";
    return "low";
}

function formatDate(isoString) {
    const d = new Date(isoString);
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
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

function renderSubjects(subjects) {
    subjectsList.innerHTML = "";

    if (subjects.length === 0) {
        subjectsEmpty.hidden = false;
        return;
    }
    subjectsEmpty.hidden = true;

    const difficultyLabel = { 1: "Easy", 3: "Medium", 5: "Hard" };

    subjects.forEach((subject) => {
        const li = document.createElement("li");
        li.className = "list-row";
        li.innerHTML = `
            <div class="row-main">
                <div class="row-title">${escapeHtml(subject.name)}</div>
                <div class="row-meta">Exam: ${formatDate(subject.exam_date)} · ${difficultyLabel[subject.difficulty]}</div>
            </div>
            <button class="delete-btn" data-id="${subject.id}" aria-label="Delete ${escapeHtml(subject.name)}">✕</button>
        `;
        subjectsList.appendChild(li);
    });

    // Attach delete handlers
    subjectsList.querySelectorAll(".delete-btn").forEach((btn) => {
        btn.addEventListener("click", () => deleteSubject(btn.dataset.id));
    });
}

function renderSchedule(schedule) {
    scheduleList.innerHTML = "";

    if (schedule.length === 0) {
        scheduleEmpty.hidden = false;
        return;
    }
    scheduleEmpty.hidden = true;

    schedule.forEach((item) => {
        const li = document.createElement("li");
        li.className = "list-row";
        li.innerHTML = `
            <span class="urgency-dot" data-level="${urgencyLevel(item.urgency_score)}"></span>
            <div class="row-main">
                <div class="row-title">${escapeHtml(item.name)}</div>
                <div class="row-meta">${item.days_left} day(s) left</div>
            </div>
            <div class="row-minutes">${item.allocated_minutes}m</div>
        `;
        scheduleList.appendChild(li);
    });
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

// --- API calls ---

async function loadSubjects() {
    const res = await fetch(`${API_BASE}/subjects`);
    const data = await res.json();
    renderSubjects(data);
}

async function loadSchedule() {
    const res = await fetch(`${API_BASE}/schedule`);
    const data = await res.json();
    renderSchedule(data.schedule || []);
}

async function refreshAll() {
    await Promise.all([loadSubjects(), loadSchedule()]);
}

async function deleteSubject(id) {
    const res = await fetch(`${API_BASE}/subjects/${id}`, { method: "DELETE" });
    if (!res.ok) {
        const data = await res.json();
        alert(data.error || "Failed to delete subject");
        return;
    }
    await refreshAll();
}

async function addSubject(payload) {
    const res = await fetch(`${API_BASE}/subjects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.error || "Failed to add subject");
    }
    return data;
}

// --- Form submit ---

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
        document.getElementById("difficulty").value = "3"; // reset to default
        await refreshAll();
    } catch (err) {
        showFormError(err.message);
    }
});

// --- Init ---

document.addEventListener("DOMContentLoaded", refreshAll);

async function loadSubjects() {
    try {
        const res = await fetch(`${API_BASE}/subjects`);
        if (!res.ok) throw new Error("Failed to load subjects");
        const data = await res.json();
        renderSubjects(data);
    } catch (err) {
        subjectsList.innerHTML = "";
        subjectsEmpty.hidden = false;
        subjectsEmpty.textContent = "Could not load subjects. Check your connection.";
    }
}

async function loadSchedule() {
    try {
        const res = await fetch(`${API_BASE}/schedule`);
        if (!res.ok) throw new Error("Failed to load schedule");
        const data = await res.json();
        renderSchedule(data.schedule || []);
    } catch (err) {
        scheduleList.innerHTML = "";
        scheduleEmpty.hidden = false;
        scheduleEmpty.textContent = "Could not load schedule. Check your connection.";
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