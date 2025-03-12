document.addEventListener("DOMContentLoaded", () => {
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
  
  // Fetch articles data from articles.json
  fetch('articles.json')
    .then(response => response.json())
    .then(articles => {
      // Initialize Fuse.js
      const fuse = new Fuse(articles, {
        keys: ["title", "author", "source.name"],
        threshold: 0.3
      });

      // Create author page URLs
      function getAuthorPageUrl(authorName) {
        if (!authorName) return null;
        return "authors/" + authorName.replace(/ /g, "_").replace(/\//g, "_").replace(/\\/g, "_").toLowerCase() + ".html";
      }

      // Function to render search results
      function renderSearchResults(results) {
        resultsContainer.innerHTML = ''; // Clear previous results

        results.forEach(result => {
          const resultItem = document.createElement('div');
          resultItem.classList.add('result-item');

          // Create and append the title element with link
          const titleElement = document.createElement('p');
          titleElement.classList.add('title');
          const titleLink = document.createElement('a');
          titleLink.href = result.item.url; // Set the href attribute
          titleLink.textContent = result.item.title;
          titleElement.appendChild(titleLink);
          resultItem.appendChild(titleElement);

          // Create and append the author element with link
          const authorElement = document.createElement('p');
          authorElement.classList.add('author');
          const authorLink = document.createElement('a');
          authorLink.href = getAuthorPageUrl(result.item.author);
          authorLink.textContent = result.item.author;
          authorElement.appendChild(authorLink);
          resultItem.appendChild(authorElement);

          // Create and append the source element with link
          const sourceElement = document.createElement('p');
          sourceElement.classList.add('source');
          sourceElement.textContent = result.item.source.name;
          resultItem.appendChild(sourceElement);

          // Append the result item to the results container
          resultsContainer.appendChild(resultItem);
        });
      }

      // Search as the user types
      searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim();
        if (query.length > 0) {
          const results = fuse.search(query);
          renderSearchResults(results);
        } else {
          resultsContainer.innerHTML = "";
        }
      });
    })
    .catch(error => console.error('Error fetching articles:', error));
});