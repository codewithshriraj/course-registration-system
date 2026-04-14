const statusMessage = document.getElementById("status-message");

function setStatus(message, isError = false) {
    statusMessage.textContent = message;
    statusMessage.style.color = isError ? "#b42338" : "#0f6ba8";
}

async function request(url, method = "GET", payload = null) {
    const options = { method, headers: { "Content-Type": "application/json" } };
    if (payload) options.body = JSON.stringify(payload);

    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok || !data.success) {
        throw new Error(data.message || "Request failed");
    }

    return data;
}

function validateEmail(email) {
    return /^[\w.-]+@[\w.-]+\.\w+$/.test(email);
}

function formatDate(value) {
    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) {
        return value;
    }
    return parsed.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

document.getElementById("student-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        student_id: document.getElementById("student_id").value.trim(),
        full_name: document.getElementById("full_name").value.trim(),
        email: document.getElementById("email").value.trim(),
        phone_number: document.getElementById("phone_number").value.trim(),
        branch: document.getElementById("branch").value.trim(),
        semester: document.getElementById("semester").value.trim(),
    };

    if (!validateEmail(payload.email)) {
        setStatus("Please enter a valid email address", true);
        return;
    }

    try {
        const result = await request("/add_student", "POST", payload);
        setStatus(result.message);
        event.target.reset();
    } catch (error) {
        setStatus(error.message, true);
    }
});

document.getElementById("course-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        course_id: document.getElementById("course_id").value.trim(),
        course_name: document.getElementById("course_name").value.trim(),
        instructor_name: document.getElementById("instructor_name").value.trim(),
        credits: document.getElementById("credits").value.trim(),
        department: document.getElementById("department").value.trim(),
    };

    try {
        const result = await request("/add_course", "POST", payload);
        setStatus(result.message);
        event.target.reset();
        await loadCourses();
    } catch (error) {
        setStatus(error.message, true);
    }
});

async function loadCourses() {
    try {
        const result = await request("/courses");
        const tbody = document.querySelector("#courses-table tbody");
        tbody.innerHTML = "";

        if (!Array.isArray(result.data) || result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">No courses found.</td></tr>';
            setStatus("No courses available yet");
            return;
        }

        result.data.forEach((course) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${course.course_id}</td>
                <td>${course.course_name}</td>
                <td>${course.instructor_name}</td>
                <td>${course.credits}</td>
                <td>${course.department}</td>
            `;
            tbody.appendChild(row);
        });

        setStatus("Courses loaded successfully");
    } catch (error) {
        setStatus(error.message, true);
    }
}

document.getElementById("load-courses").addEventListener("click", loadCourses);

document.getElementById("register-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        student_id: document.getElementById("reg_student_id").value.trim(),
        course_id: document.getElementById("reg_course_id").value.trim(),
    };

    try {
        const result = await request("/register_course", "POST", payload);
        setStatus(result.message);
        event.target.reset();
        await loadRegistrations();
    } catch (error) {
        setStatus(error.message, true);
    }
});

document.getElementById("drop-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        student_id: document.getElementById("drop_student_id").value.trim(),
        course_id: document.getElementById("drop_course_id").value.trim(),
    };

    try {
        const result = await request("/drop_course", "POST", payload);
        setStatus(result.message);
        event.target.reset();
        await loadRegistrations();
    } catch (error) {
        setStatus(error.message, true);
    }
});

async function loadRegistrations(studentId = "") {
    try {
        const query = studentId ? `?student_id=${encodeURIComponent(studentId)}` : "";
        const result = await request(`/registrations${query}`);
        const tbody = document.querySelector("#registrations-table tbody");
        tbody.innerHTML = "";

        if (!Array.isArray(result.data) || result.data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">No registrations found for the selected criteria.</td></tr>';
            setStatus("No registrations found");
            return;
        }

        result.data.forEach((registration) => {
            const row = document.createElement("tr");
            const pillClass = registration.status === "Dropped" ? "pill pill-danger" : "pill pill-success";
            row.innerHTML = `
                <td>${registration.registration_id}</td>
                <td>${registration.student_id}</td>
                <td>${registration.full_name}</td>
                <td>${registration.course_id}</td>
                <td>${registration.course_name}</td>
                <td>${formatDate(registration.registration_date)}</td>
                <td><span class="${pillClass}">${registration.status}</span></td>
            `;
            tbody.appendChild(row);
        });

        setStatus("Registrations loaded successfully");
    } catch (error) {
        setStatus(error.message, true);
    }
}

document.getElementById("filter-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const studentId = document.getElementById("filter_student_id").value.trim();
    await loadRegistrations(studentId);
});

document.getElementById("delete-student-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const studentId = document.getElementById("delete_student_id").value.trim();

    try {
        const result = await request(`/delete_student/${encodeURIComponent(studentId)}`, "DELETE");
        setStatus(result.message);
        event.target.reset();
        await loadRegistrations();
    } catch (error) {
        setStatus(error.message, true);
    }
});

document.getElementById("delete-course-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const courseId = document.getElementById("delete_course_id").value.trim();

    try {
        const result = await request(`/delete_course/${encodeURIComponent(courseId)}`, "DELETE");
        setStatus(result.message);
        event.target.reset();
        await loadCourses();
    } catch (error) {
        setStatus(error.message, true);
    }
});

loadCourses();
loadRegistrations();
