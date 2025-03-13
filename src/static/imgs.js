document.addEventListener("DOMContentLoaded", () => {
    const deleteForms = document.getElementsByClassName("deleteForms");
    const accDeleteButton = document.getElementById("footer--del-acc__button");

    if(accDeleteButton) {
        accDeleteButton.addEventListener('click', function () {
            if(confirm("Are you sure you want to delete your account?")) {
                fetch('/api/user', {
                    method: 'DELETE'
                })
                    .then(response => {
                        if (response.ok) {
                            window.location.href = '/login';
                        } else {
                            console.error('Request failed:', response.status);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                window.location.href = '/login';
            }
        });
    }

    if(deleteForms) {
        for (const form of deleteForms) {
            form.addEventListener("submit", async (event) => {
                event.preventDefault();

                const actionUrl = form.getAttribute("action");

                const response = await fetch(actionUrl, {
                    method: "DELETE",
                });

                if (response.ok) {
                    window.location.href = "/imgs";
                } else {
                    document.getElementById(actionUrl).textContent = response.error
                }
            });
        }
    }
});
