const hamBurger = document.querySelector(".toggle-btn");

// Toggle sidebar expansion
hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

// Add pool form submission handler (for IP pools)
document.getElementById('addIpPoolForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent form submission from refreshing the page

    const poolName = document.getElementById('poolName').value;
    const ipPool = document.getElementById('ipPool').value;
    

  // Data logging for debugging
    console.log("Form data:", { poolName, ipPool });

    fetch('/add/pool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "name": poolName,
            "ranges": ipPool
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response data:", data);
      alert(data.message || data.error); // Notify user
      if (data.message) location.reload(); // Reload to refresh the IP pool list
    })
  .catch(err => console.error("Fetch error:", err)); // Error handling
});

// Edit IP pool handler
document.querySelectorAll('.edit-ip-pool-btn').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id');

        // Fetch existing IP pool details to pre-fill the prompts
        fetch(`/pool/${id}`)
            .then(res => res.json())
            .then(data => {
                const currentName = data["name"]; // Assuming "name" is the current pool name
                const currentranges = data["ranges"]; // Assuming "ranges" is the current pool ranges

                // Create prompts for new pool name and ranges selection
                const newPoolName = prompt("Pilih nama pool baru:", currentName);
                const newipPool = prompt("Pilih alamat pool baru (current: " + currentranges + "):", currentranges);

                if (newPoolName && newipPool) {
                    fetch(`/update/pool/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name: newPoolName, ranges: newipPool })
                    })
                    .then(res => res.json())
                    .then(data => {
                        alert(data.message || data.error); 
                        if (data.message) location.reload(); 
                    })
                    .catch(err => {
                        console.error("Error updating IP pool:", err);
                        alert("Failed to update the IP pool.");
                    });
                }
            })
            .catch(err => {
                console.error("Error fetching IP pool details:", err);
                alert("Failed to fetch IP pool details.");
            });
    });
});

// Delete IP pool handler
document.querySelectorAll('.delete-ip-pool-btn').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id');

        if (confirm("Are you sure you want to delete this IP pool?")) {
        fetch(`/delete/pool/${id}`, { method: 'DELETE' })
            location.reload();
        }
    });
});

// Fetch IP pool details handler
document.querySelectorAll('.detail-ip-pool-btn').forEach(button => {
    button.addEventListener('click', function () {
        const poolId = this.getAttribute('data-id');
        console.log("Fetching details for IP pool ID:", poolId);

        fetch(`/pool/${poolId}`)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then(data => {
                console.log("IP pool details:", data);

                const detailsList = document.getElementById('ipPoolDetailsList');
              detailsList.innerHTML = ''; // Clear previous details

                for (const [key, value] of Object.entries(data)) {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    listItem.textContent = `${key}: ${value}`;
                    detailsList.appendChild(listItem);
                }

              // Show modal
                const modal = new bootstrap.Modal(document.getElementById('ipPoolDetailModal'));
                modal.show();
            })
            .catch(err => {
                console.error("Error fetching IP pool details:", err);
                alert("Failed to fetch IP pool details. Please check your setup.");
        });
    });
});
