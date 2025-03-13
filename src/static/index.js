document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("navbar--logout-button");
    const imgUploadForm = document.getElementById("content--img-form");
    const periodUploadForm = document.getElementById("content--period-form");
    const accDeleteButton = document.getElementById("footer--del-acc__button");
    const dateSelector = document.getElementById("form--date");

    if(dateSelector) {
        dateSelector.value = new Date().toISOString().split("T")[0];
    }

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

    if(logoutButton) {
        logoutButton.addEventListener('click', function() {
            fetch('/logout', {
              method: 'POST'
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
        });
    }

    if(imgUploadForm) {
        imgUploadForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const formData = new FormData(imgUploadForm);
            try {
                const response = await fetch(imgUploadForm.action, {
                    method: imgUploadForm.method,
                    body: formData,
                });

                const result = await response.json();

                if (response.ok) {
                    window.location.href = "/index";
                } else {
                    document.getElementById("content--img-form__error").textContent = result.message || "An error occurred during upload.";
                }
            } catch (error) {
                console.error("Error during form submission:", error);
            }
        });
    }

    if(periodUploadForm) {
        periodUploadForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const formData = new FormData(periodUploadForm);
            try {
                const response = await fetch(periodUploadForm.action, {
                    method: periodUploadForm.method,
                    body: formData,
                });

                const result = await response.json();

                if (response.ok) {
                    window.location.href = "/index";
                } else {
                    document.getElementById("content--period-form__error").textContent = result.message || "An error occurred during upload.";
                }
            } catch (error) {
                console.error("Error during form submission:", error);
            }
        });
    }
});