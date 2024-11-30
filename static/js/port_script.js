const hamBurger = document.querySelector(".toggle-btn");

// Toggle sidebar expansion
hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

// Add interface form submission handler (for ports)
document.getElementById('addInterfaceForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent form submission from refreshing the page

    const interfaceName = document.getElementById('interfaceSelect').value;
    const bridgeName = document.getElementById('bridgeSelect').value;

  // Data logging for debugging
    console.log("Form data:", { interfaceName, bridgeName });

    fetch('/add/port', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "interface": interfaceName,
            "bridge": bridgeName
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Response data:", data);
      alert(data.message || data.error); // Notify user
      if (data.message) location.reload(); // Reload to refresh the port list
    })
  .catch(err => console.error("Fetch error:", err)); // Error handling
});

// Edit port handler
document.querySelectorAll('.edit-port-btn').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id');

        // Fetch existing port details to pre-fill the prompts
        fetch(`/port/${id}`)
            .then(res => res.json())
            .then(data => {
                const currentName = data["interface"]; // Assuming "interface" is the current name
                const currentBridge = data["bridge"]; // Assuming "bridge" is the current bridge

                // Create dropdown for new name and bridge selection
                const newName = prompt("Pilih nama baru untuk port (ether1-8):\n1. ether1\n2. ether2\n3. ether3\n4. ether4\n5. ether5\n6. ether6\n7. ether7\n8. ether8", currentName);
                const newBridge = prompt("Pilih bridge baru (current: " + currentBridge + "):\n1. Bridge1\n2. Bridge2\n3. Bridge3", currentBridge);

                if (newName && newBridge) {
                    fetch(`/update/port/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ interface: newName, bridge: newBridge })
                    })
                    .then(res => res.json())
                    .then(data => {
                        alert(data.message || data.error); // Notify user
                        if (data.message) location.reload(); // Reload to reflect updated data
                    })
                    .catch(err => {
                        console.error("Error updating port:", err);
                        alert("Failed to update the port.");
                    });
                }
            })
            .catch(err => {
                console.error("Error fetching port details:", err);
                alert("Failed to fetch port details.");
            });
    });
});

// Delete port handler
document.querySelectorAll('.delete-port-btn').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id');

        if (confirm("Are you sure you want to delete this bridge?")) {
        fetch(`/delete/port/${id}`, { method: 'DELETE' })
            location.reload();
        }
    });
});

// Fetch port details handler
document.querySelectorAll('.detail-port-btn').forEach(button => {
    button.addEventListener('click', function () {
        const portId = this.getAttribute('data-id');
        console.log("Fetching details for port ID:", portId);

        fetch(`/port/${portId}`)
            .then(res => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then(data => {
                console.log("Port details:", data);

                const detailsList = document.getElementById('portDetailsList');
              detailsList.innerHTML = ''; // Clear previous details

                for (const [key, value] of Object.entries(data)) {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    listItem.textContent = `${key}: ${value}`;
                    detailsList.appendChild(listItem);
                }

              // Show modal
                const modal = new bootstrap.Modal(document.getElementById('portDetailModal'));
                modal.show();
            })
            .catch(err => {
                console.error("Error fetching port details:", err);
                alert("Failed to fetch port details. Please check your setup.");
        });
    });
});
