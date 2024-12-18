// Function to fetch JSON data and display in the corresponding tab
function loadData(jsonFile, containerId) {
    fetch(jsonFile)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById(containerId);
            container.innerHTML = ""; // Clear previous content
            data.forEach(item => {
                const card = document.createElement('div');
                card.className = 'col-md-4';
                card.innerHTML = `
                    <div class="card">
                        <div class="card-header">${item.Title || item.title}</div>
                        <div class="card-body">
                            <p><strong>Price:</strong> ${item.Price || item.price}</p>
                            <p><strong>Location:</strong> ${item.Location || item.location}</p>
                            <p><strong>Rating:</strong> ${item.Rating || 'N/A'}</p>
                            <p><strong>Reviews:</strong> ${item['Reviews Count'] || 'N/A'}</p>
                        </div>
                    </div>`;
                container.appendChild(card);
            });
        })
        .catch(error => console.error('Error loading data:', error));
}

// Load data into tabs
document.addEventListener("DOMContentLoaded", () => {
    loadData('/used-cars', 'usedCarsContainer');
    loadData('/new-cars', 'newCarsContainer');
    loadData('/bikes', 'bikesContainer');
});
