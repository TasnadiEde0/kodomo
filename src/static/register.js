document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");
    const responseParagraph = document.getElementById("response");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const password2 = document.getElementById("password2").value;
        const first_name = document.getElementById("first_name").value;
        const last_name = document.getElementById("last_name").value;
        const birth_date = document.getElementById("birth_date").value;
        const address = document.getElementById("address").value;
        const post_code = document.getElementById("post_code").value;
        const email = document.getElementById("email").value;

        if (!username || !password || !password2) {
            responseParagraph.textContent = "Username and password are required.";
            return;
        }

        if (password !== password2) {
            responseParagraph.textContent = "Passwords do not match.";
            return;
        }

        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username,
                    password,
                    first_name,
                    last_name,
                    birth_date,
                    address,
                    post_code,
                    email,
                }),
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
