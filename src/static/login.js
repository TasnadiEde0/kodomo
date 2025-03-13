document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm")
    const responseParagraph = document.getElementById("response");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        if (!username || !password) {
            responseParagraph.textContent = "Please fill in all fields.";
            return;
        }

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                window.location.href = "/index";
            } else {
                const result = await response.json();
                responseParagraph.textContent = result.error || "An error occurred.";
            }
        } catch (error) {
            responseParagraph.textContent = "Failed to send request. Please try again.";
        }
    });
});
