function validateLogin(email, password) {
  if (email.trim() === "" || password === "") {
    return "Email and password are required.";
  }
  if (!email.includes("@")) {
    return "Email must contain @.";
  }
  if (password.length < 8) {
    return "Password must be at least 8 characters.";
  }
  return null;
}

const form = document.getElementById("login-form");
const message = document.getElementById("message");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const error = validateLogin(email, password);

  if (error) {
    message.textContent = error;
    return;
  }

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.trim(), password }),
    });
    const body = await response.json();
    message.textContent = body.message || "Login failed.";
  } catch (_err) {
    message.textContent = "Could not reach the server.";
  }
});
