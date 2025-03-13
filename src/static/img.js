window.onload = async () => {
    const logoutButton = document.getElementById('navbar--logout-button');
    const accDeleteButton = document.getElementById("footer--del-acc__button");
    const deleteButton = document.getElementById('content-delete-button');

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
        logoutButton.addEventListener('click', function () {
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

    if(deleteButton) {
        deleteButton.addEventListener('click', function () {
            fetch('/api/images/' + deleteButton.getAttribute("img_id"), {
                method: 'DELETE'
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/index';
                } else {
                    console.error('Request failed:', response.status);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
}