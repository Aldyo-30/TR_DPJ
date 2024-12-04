const hamBurger = document.querySelector(".toggle-btn");

// Toggle sidebar expansion
hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

// Add interface form submission handler (for IP addresses)
document.getElementById('addIpForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent form submission from refreshing the page

    const ipAddress = document.getElementById('ipAddress').value;
    const interfaceName = document.getElementById('interfaceSelect').value;
    

  // Data logging for debugging
    console.log("Form data:", { ipAddress, interfaceName });

    fetch('/add/ip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "address": ipAddress,
            "interface": interfaceName
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response data:", data);
      alert(data.message || data.error); // Notify user
      if (data.message) location.reload(); // Reload to refresh the IP list
    })
  .catch(err => console.error("Fetch error:", err)); // Error handling
});

// Edit IP handler
document.querySelectorAll('.edit-ip-btn').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id');

        // Fetch existing IP details to pre-fill the prompts
        fetch(`/ip/${id}`)
            .then(res => res.json())
            .then(data => {
                const currentAddress = data["address"]; // Assuming "address" is the current IP
                const currentInterface = data["interface"]; // Assuming "interface" is the current interface

                // Create prompts for new IP address and interface selection
                const newIPAddress = prompt("Pilih alamat IP baru:\nContoh: 192.168.1.1", currentAddress);
                const newInterface = prompt("Pilih interface baru (current: " + currentInterface + "):", currentInterface);

                if (newIPAddress && newInterface) {
                    fetch(`/update/ip/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ address: newIPAddress, interface: newInterface })
                    })
                    .then(res => res.json())
                    .then(data => {
                        alert(data.message || data.error); 
                        if (data.message) location.reload(); 
                    })
                    .catch(err => {
                        console.error("Error updating IP:", err);
                        alert("Failed to update the IP address.");
                    });
                }
            })
            .catch(err => {
                console.error("Error fetching IP details:", err);
                alert("Failed to fetch IP details.");
            });
    });
});

// Delete IP handler
document.querySelectorAll('.delete-ip-btn').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id');

        if (confirm("Are you sure you want to delete this IP address?")) {
        fetch(`/delete/ip/${id}`, { method: 'DELETE' })
            location.reload();
        }
    });
});

// Fetch IP details handler
document.querySelectorAll('.detail-ip-btn').forEach(button => {
    button.addEventListener('click', function () {
        const ipId = this.getAttribute('data-id');
        console.log("Fetching details for IP ID:", ipId);

        fetch(`/ip/${ipId}`)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then(data => {
                console.log("IP details:", data);

                const detailsList = document.getElementById('ipDetailsList');
              detailsList.innerHTML = ''; // Clear previous details

                for (const [key, value] of Object.entries(data)) {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    listItem.textContent = `${key}: ${value}`;
                    detailsList.appendChild(listItem);
                }

              // Show modal
                const modal = new bootstrap.Modal(document.getElementById('ipDetailModal'));
                modal.show();
            })
            .catch(err => {
                console.error("Error fetching IP details:", err);
                alert("Failed to fetch IP details. Please check your setup.");
        });
    });
});
