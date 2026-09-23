document.addEventListener('DOMContentLoaded', () => {
    // Attach event listeners to Promote, Demote, and Delete buttons
    // These buttons send requests to update user roles or remove users

    // Promote User Button
    document.querySelectorAll('.promote-btn').forEach(button => {
        button.addEventListener('click', () => {
            const userId = button.dataset.id;
            fetch(`/promote/${userId}`, { method: 'POST' })
                .then(() => location.reload()) // Reload page to show changes
                .catch(err => console.error(err));
        });
    });

    // Demote User Button
    document.querySelectorAll('.demote-btn').forEach(button => {
        button.addEventListener('click', () => {
            const userId = button.dataset.id;
            fetch(`/demote/${userId}`, { method: 'POST' })
                .then(() => location.reload())
                .catch(err => console.error(err));
        });
    });

    // Delete User Button
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', () => {
            let userId = button.dataset.id;

            if (confirm("Are you sure you want to delete this user?")) {
                fetch(`/delete/${userId}`, { method: 'POST' })
                    .then(response => {
                        if (response.ok) {
                            location.reload(); // Refresh the page after deleting user
                        }
                    })
                    .catch(error => console.error("Error:", error));
            }
        });
    });

    // Search functionality for filtering user table
    const searchBar = document.getElementById('searchBar');
    searchBar.addEventListener('keyup', searchTable);

    // Toggle Add User Form visibility
    const addUserBtn = document.getElementById('addUserBtn');
    addUserBtn.addEventListener('click', toggleAddUserForm);

    function searchTable() {
        let input = searchBar.value.toLowerCase();
        let rows = document.querySelectorAll("#userTable tbody tr");
        rows.forEach(row => {
            let name = row.cells[1].textContent.toLowerCase();
            let role = row.cells[2].textContent.toLowerCase();
            row.style.display = (name.includes(input) || role.includes(input)) ? "" : "none";
        });
    }

    function toggleAddUserForm() {
        let form = document.getElementById("addUserForm");
        let table = document.getElementById("userTable");
        form.style.display = form.style.display === "none" ? "block" : "none";
        table.style.display = table.style.display === "none" ? "table" : "none";
    }

    // Handles UI updates for Promote, Demote, and Delete actions without reloading
    const userTable = document.getElementById('userTable');
    userTable.addEventListener('click', function(event) {
        let target = event.target;

        if (target.classList.contains('promote-btn')) {
            // Update UI instantly without requiring a page reload
            let row = target.closest('tr');
            let roleCell = row.cells[2];
            if (roleCell.textContent === 'Employee') {
                roleCell.textContent = 'Admin';
                target.textContent = 'Demote';
            } else {
                roleCell.textContent = 'Employee';
                target.textContent = 'Promote';
            }
        }
    });
});
