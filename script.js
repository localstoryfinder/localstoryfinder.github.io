document.addEventListener("DOMContentLoaded", async () => {
    const searchInput = document.querySelector(".search-input");
    const resultsContainer = document.querySelector(".results");
    const menuBtn = document.querySelector(".menu-btn");
    const dropdownMenu = document.querySelector(".dropdown-menu");
    
    // RSS source name mapping
    const sourceNameMapping = {
      "calhealthreport.org": "California Health Report",
      "sf.streetsblog.org": "Streetsblog SF",
      "kpoo.com": "KPOO",
      "boldlatina.com": "Bold Latina",
      "thesunreporter.com": "San Francisco Sun Reporter", // Added missing comma here
      "Sfstandard.com": "SF Standard"
    };
    
    // Function to get formatted source name
    function getSourceName(source) {
      if (!source || !source.name) return "Unknown Source";
      return sourceNameMapping[source.name] || source.name;
    }
    
    // Toggle dropdown menu
    menuBtn.addEventListener("click", () => {
      dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block";
    });
    
    // Fetch the JSON data
    let data = [];
    try {
      const response = await fetch("articles.json");
      data = await response.json();
    } catch (error) {
      console.error("Error loading JSON data:", error);
      return;
    }
    
    // Initialize Fuse.js
    const fuse = new Fuse(data, {
      keys: ["author", "source.name", "title", "description"],
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
        
        // Format the source name
        const sourceName = getSourceName(item.source);
        
        resultItem.innerHTML = `
          <h3 class="author-name">${item.author || "Unknown Author"}</h3>
          <p class="source-name">${sourceName}</p>
          <p><a href="${item.url}" target="_blank">${item.title}</a></p>
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
