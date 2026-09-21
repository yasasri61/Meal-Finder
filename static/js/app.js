document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("img").forEach(img => {
    img.addEventListener("error", () => {
      img.style.display = "none";
      const fallback = document.createElement("div");
      fallback.className = "image-fallback";
      fallback.textContent = "🍽️";
      img.parentElement.appendChild(fallback);
    }, { once: true });
  });
});
