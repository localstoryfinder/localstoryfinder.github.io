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
    "thesunreporter.com": "San Francisco Sun Reporter", 
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
  
  // Create author page URLs
  function getAuthorPageUrl(authorName) {
    if (!authorName) return null;
    return "authors/" + authorName.replace(/ /g, "_").replace(/\//g, "_").replace(/\\/g, "_").toLowerCase() + ".html";
  }

  // Include author links
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
      
      // Get author link
      const authorName = item.author || "Unknown Author";
      const authorLink = authorName !== "Unknown Author" ? getAuthorPageUrl(authorName) : null;
      
      // Create author and source HTML
      const authorHTML = authorLink 
        ? `<span class="author-name"><a href="${authorLink}">${authorName}</a></span>`
        : `<span class="author-name">${authorName}</span>`;
      const sourceHTML = `<span class="source-name">${sourceName}</span>`;

      resultItem.innerHTML = `
        <p class="result-text"><a href="${item.url}" target="_blank">${item.title}</a></p>
        <p class="result-text">${authorHTML} &nbsp;&nbsp; ${sourceHTML}</p>
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