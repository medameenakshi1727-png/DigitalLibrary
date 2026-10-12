// Live client-side catalog filter. Server-side search also works without JavaScript.
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("catalogSearch");
  const items = Array.from(document.querySelectorAll(".book-item"));
  const noResults = document.getElementById("noLiveResults");
  if (!input || items.length === 0) return;

  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();
    let visible = 0;
    items.forEach((item) => {
      const matches = item.dataset.search.includes(query);
      item.classList.toggle("d-none", !matches);
      if (matches) visible += 1;
    });
    if (noResults) noResults.classList.toggle("d-none", visible > 0);
  });
});
