document.addEventListener("DOMContentLoaded", () => {
  const yearNodes = document.querySelectorAll("[data-current-year], [data-year]");
  yearNodes.forEach((node) => {
    node.textContent = String(new Date().getFullYear());
  });

  const refreshButtons = document.querySelectorAll("[data-captcha-refresh]");
  refreshButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetId = button.getAttribute("data-captcha-target");
      if (!targetId) return;
      const image = document.getElementById(targetId);
      if (!image) return;
      const baseUrl = image.getAttribute("data-base-src") || image.getAttribute("src") || "captcha.php";
      image.setAttribute("data-base-src", baseUrl);
      image.src = `${baseUrl}${baseUrl.includes("?") ? "&" : "?"}t=${Date.now()}`;
    });
  });
});
