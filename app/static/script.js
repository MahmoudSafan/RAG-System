// static/script.js
const API_URL = "http://127.0.0.1:8000"; // Your FastAPI base URL
let token = null;

// Show registration form
function showRegister() {
	document.getElementById("auth-section").innerHTML = `
    <h2>Register</h2>
    <form id="register-form">
      <input type="email" id="reg-email" placeholder="Email" required>
      <input type="password" id="reg-password" placeholder="Password" required>
      <button type="submit">Register</button>
    </form>`;

	document.getElementById("register-form").onsubmit = register;
}

// Login function
async function login(event) {
	event.preventDefault();
	const email = document.getElementById("email").value;
	const password = document.getElementById("password").value;

	const response = await fetch(`${API_URL}/auth/token`, {
		method: "POST",
		headers: { "Content-Type": "application/x-www-form-urlencoded" },
		body: new URLSearchParams({ username: email, password }),
	});
	const data = await response.json();
	if (data.access_token) {
		token = data.access_token;
		document.getElementById("auth-section").style.display = "none";
		document.getElementById("interaction-section").style.display = "block";
	} else {
		alert("Login failed");
	}
}

// Register function
async function register(event) {
	event.preventDefault();
	const email = document.getElementById("reg-email").value;
	const password = document.getElementById("reg-password").value;

	const response = await fetch(`${API_URL}/auth/register`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ email, password }),
	});
	const data = await response.json();
	if (response.ok) {
		alert("Registration successful");
		showLogin();
	} else {
		alert(data.detail || "Registration failed");
	}
}

// Get Job Recommendations
async function getRecommendations() {
	const query = document.getElementById("job-query").value;
	const response = await fetch(
		`${API_URL}/generate-recommendation?query=${query}`,
		{
			headers: { Authorization: `Bearer ${token}` },
		}
	);
	const data = await response.json();
	document.getElementById("recommendation-output").innerText =
		data.recommendation;
}

// Estimate Salary
async function estimateSalary() {
	const jobTitle = document.getElementById("job-title").value;
	const yearsExperience = document.getElementById("years-experience").value;

	const response = await fetch(
		`${API_URL}/estimate-salary?job_title=${jobTitle}&years_experience=${yearsExperience}`,
		{
			headers: { Authorization: `Bearer ${token}` },
		}
	);
	const data = await response.json();
	document.getElementById("salary-output").innerText = data.estimated_salary;
}

// Logout function
function logout() {
	token = null;
	document.getElementById("interaction-section").style.display = "none";
	document.getElementById("auth-section").style.display = "block";
}
