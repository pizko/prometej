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

  const requestModal = document.getElementById("requestModal");
  if (requestModal && window.bootstrap) {
    requestModal.addEventListener("show.bs.modal", (event) => {
      const trigger = event.relatedTarget;
      if (!trigger) return;

      const service = trigger.getAttribute("data-service") || "услуге";

      const titleNode = requestModal.querySelector("[data-request-title]");
      const sourceNode = requestModal.querySelector("[data-request-source]");
      const captchaImage = requestModal.querySelector(".captcha-image");

      if (titleNode) {
        titleNode.textContent = `${service} — заявка`;
      }

      if (sourceNode) {
        sourceNode.value = `Модальное окно: ${service}`;
      }

      if (captchaImage) {
        const baseUrl = captchaImage.getAttribute("data-base-src") || captchaImage.getAttribute("src") || "captcha.php";
        captchaImage.setAttribute("data-base-src", baseUrl);
        captchaImage.src = `${baseUrl}${baseUrl.includes("?") ? "&" : "?"}t=${Date.now()}`;
      }
    });
  }

  const galleryRoot = document.getElementById("gallery-grid");
  if (galleryRoot && window.bootstrap) {
    const lightboxElement = document.getElementById("galleryLightbox");
    const lightboxImage = document.getElementById("galleryLightboxImage");
    const lightboxCaption = document.getElementById("galleryLightboxCaption");
    const prevButton = document.querySelector("[data-gallery-prev]");
    const nextButton = document.querySelector("[data-gallery-next]");
    const lightbox = new bootstrap.Modal(lightboxElement);
    let currentIndex = 0;
    let images = [];

    const openLightbox = (index) => {
      currentIndex = index;
      const item = images[currentIndex];
      if (!item) return;
      lightboxImage.src = item.src;
      lightboxImage.alt = item.caption;
      lightboxCaption.textContent = item.caption;
      lightbox.show();
    };

    const renderGallery = (items) => {
      images = items;
      galleryRoot.innerHTML = "";

      if (!images.length) {
        galleryRoot.innerHTML = '<div class="gallery-empty">Фотографии пока не добавлены.</div>';
        return;
      }

      images.forEach((item, index) => {
        const card = document.createElement("article");
        card.className = "gallery-card";
        card.innerHTML = `
          <img class="media-cover" src="${item.src}" alt="${item.caption}">
          <div class="caption">${item.caption}</div>
        `;
        card.addEventListener("click", () => openLightbox(index));
        galleryRoot.appendChild(card);
      });
    };

    const move = (direction) => {
      if (!images.length) return;
      currentIndex = (currentIndex + direction + images.length) % images.length;
      const item = images[currentIndex];
      lightboxImage.src = item.src;
      lightboxImage.alt = item.caption;
      lightboxCaption.textContent = item.caption;
    };

    prevButton?.addEventListener("click", () => move(-1));
    nextButton?.addEventListener("click", () => move(1));

    document.addEventListener("keydown", (event) => {
      if (!lightboxElement.classList.contains("show")) return;
      if (event.key === "ArrowLeft") move(-1);
      if (event.key === "ArrowRight") move(1);
    });

    const normalizeCaption = (fileName) =>
      fileName
        .replace(/\.[^.]+$/, "")
        .replace(/[-_]+/g, " ")
        .replace(/\s+/g, " ")
        .trim();

    Promise.all([
      fetch("photo/photos.json")
        .then((response) => (response.ok ? response.json() : []))
        .catch(() => []),
      fetch("https://api.github.com/repos/pizko/prometej/contents/photo")
        .then((response) => (response.ok ? response.json() : []))
        .catch(() => []),
    ])
      .then(([manifestItems, githubItems]) => {
        const manifestMap = new Map();
        const ordered = [];

        manifestItems.forEach((item) => {
          if (!item || typeof item.src !== "string" || !/\.(png|jpe?g|webp|gif)$/i.test(item.src)) {
            return;
          }
          manifestMap.set(item.src, item);
          ordered.push({
            src: item.src,
            caption: item.caption || normalizeCaption(item.src.split("/").pop() || item.src),
          });
        });

        githubItems
          .filter((item) => item.type === "file" && /\.(png|jpe?g|webp|gif)$/i.test(item.name))
          .sort((a, b) => a.name.localeCompare(b.name, "ru", { numeric: true }))
          .forEach((item) => {
            const src = `photo/${item.name}`;
            if (manifestMap.has(src)) {
              return;
            }
            ordered.push({
              src,
              caption: normalizeCaption(item.name),
            });
          });

        renderGallery(ordered);
      })
      .catch(() => {
        galleryRoot.innerHTML = '<div class="gallery-empty">Не удалось загрузить список фотографий.</div>';
      });
  }
});
