document.addEventListener("DOMContentLoaded", async () => {
    const searchInput = document.querySelector(".search-input");
    const resultsContainer = document.querySelector(".results");

    // Fetch the JSON data (Replace 'data.json' with actual path)
    let data = [];
    try {
        const response = await fetch("data.json");
        data = await response.json();
    } catch (error) {
        console.error("Error loading JSON data:", error);
        return;
    }

    // Initialize Fuse.js
    const fuse = new Fuse(data, {
        keys: ["name", "source", "title", "topics"],
        threshold: 0.3
    });

    // Function to render search results
    function renderResults(results) {
        resultsContainer.innerHTML = "";
        if (results.length === 0) {
            resultsContainer.innerHTML = "<p>No results found.</p>";
            return;
        }

        results.forEach(({ item }) => {
            const resultItem = document.createElement("div");
            resultItem.classList.add("result-item");
            resultItem.innerHTML = `
                <h3>${item.name}</h3>
                <p><strong>Source:</strong> ${item.source}</p>
                <p><strong>Title:</strong><a href="${item.url}">${item.title}</a></p>
                <p><strong>Topics:</strong> ${item.topics.join(", ")}</p>
            `;
            resultsContainer.appendChild(resultItem);
        });
    }

    // Search as the user types
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim();
        if (query.length > 0) {
            const results = fuse.search(query);
            renderResults(results);
        } else {
            resultsContainer.innerHTML = "";
        }
    });
});