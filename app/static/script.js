const BASE_URL = "http://127.0.0.1:8000"; // Update to your FastAPI server URL

// Register a new user
async function registerUser() {
	const email = document.getElementById("reg-email").value;
	const password = document.getElementById("reg-password").value;
	const resultElement = document.getElementById("register-result");

	const response = await fetch(`${BASE_URL}/auth/register`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ email, password }),
	});

	const data = await response.json();
	resultElement.textContent = data.message || "Registration error.";
}

// Login user
async function loginUser() {
	const email = document.getElementById("login-email").value;
	const password = document.getElementById("login-password").value;
	const resultElement = document.getElementById("login-result");

	const response = await fetch(`${BASE_URL}/auth/login`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ email, password }),
	});

	const data = await response.json();
	if (response.ok) {
		resultElement.textContent = "Login successful!";
		localStorage.setItem("auth_token", data.access_token); // Store JWT
	} else {
		resultElement.textContent = data.detail || "Login failed.";
	}
}

// Get job recommendations
async function getJobRecommendation() {
	const query = document.getElementById("job-query").value;
	const resultElement = document.getElementById("recommendation-result");

	const response = await fetch(
		`${BASE_URL}/generate-recommendation?query=${encodeURIComponent(query)}`,
		{
			headers: {
				Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
			},
		}
	);
	const data = await response.json();
	resultElement.textContent =
		data.recommendation || "Error fetching recommendation.";
}

// Estimate salary
async function estimateSalary() {
	const title = document.getElementById("job-title").value;
	const experience = document.getElementById("years-experience").value;
	const resultElement = document.getElementById("salary-result");

	const response = await fetch(
		`${BASE_URL}/estimate-salary?job_title=${encodeURIComponent(
			title
		)}&years_experience=${experience}`,
		{
			headers: {
				Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
			},
		}
	);
	const data = await response.json();
	resultElement.textContent =
		data.estimated_salary || "Error estimating salary.";
}

// Upload PDF
async function uploadPDF() {
	const fileInput = document.getElementById("pdf-file");
	const formData = new FormData();
	formData.append("file", fileInput.files[0]);

	const response = await fetch(`${BASE_URL}/upload-pdf`, {
		method: "POST",
		headers: { Authorization: `Bearer ${localStorage.getItem("auth_token")}` },
		body: formData,
	});
	const data = await response.json();
	document.getElementById("pdf-result").textContent =
		data.message || "Error uploading PDF.";
}

// Chat functionality
async function createNewChat() {
	const response = await fetch(`${BASE_URL}/chat`, {
		method: "POST",
		headers: { Authorization: `Bearer ${localStorage.getItem("auth_token")}` },
	});
	const data = await response.json();
	localStorage.setItem("chat_id", data.chat_id);
}

async function sendMessage() {
	const chatId = localStorage.getItem("chat_id");
	const message = document.getElementById("chat-input").value;
	const chatHistory = document.getElementById("chat-history");

	const response = await fetch(`${BASE_URL}/chat/${chatId}/message`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
		},
		body: JSON.stringify({ content: message }),
	});
	const data = await response.json();
	chatHistory.innerHTML += `<p>User: ${message}</p><p>Bot: ${
		data.llm_response || "Error in chat response."
	}</p>`;
}
