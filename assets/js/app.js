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
      const price = trigger.getAttribute("data-price") || "";
      const targetHref = trigger.getAttribute("data-lead-href") || "contacts.html";

      const titleNode = requestModal.querySelector("[data-request-title]");
      const textNode = requestModal.querySelector("[data-request-text]");
      const buttonNode = requestModal.querySelector("[data-request-link]");

      if (titleNode) {
        titleNode.textContent = service;
      }

      if (textNode) {
        textNode.textContent = price
          ? `Ориентир по стоимости: ${price}. Оставьте заявку, и мы уточним задачу и подготовим предложение.`
          : "Оставьте заявку, и мы уточним задачу и подготовим предложение.";
      }

      if (buttonNode) {
        buttonNode.setAttribute("href", targetHref);
      }
    });
  }

  const galleryRoot = document.getElementById("gallery-grid");
  if (galleryRoot && window.bootstrap) {
    const fallbackGallery = [
      "photo/gallery-1.jpg",
      "photo/gallery-2.jpg",
      "photo/gallery-3.jpg",
      "photo/gallery-4.jpg",
      "photo/gallery-5.jpg",
      "photo/gallery-6.jpg",
      "photo/gallery-7.jpg",
      "photo/gallery-8.jpg",
      "photo/gallery-9.jpg",
      "photo/gallery-10.jpg",
      "photo/gallery-11.jpg",
      "photo/gallery-12.jpg",
      "photo/gallery-13.jpg",
      "photo/gallery-14.jpg",
    ];

    const captions = [
      "Монтаж и примеры объектов",
      "Видеонаблюдение и доступ",
      "Реальные рабочие кейсы",
      "Установка оборудования",
      "Домофония и входные группы",
      "Сервис и сопровождение",
      "Пожарная безопасность и монтаж",
      "Настройка камер и точек обзора",
      "СКУД и инженерная часть",
      "Рабочие выезды на объекты",
      "Интеграция оборудования",
      "Примеры завершенных работ",
      "Сложные узлы и установка",
      "Финальный вид на объекте",
    ];

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

    fetch("https://api.github.com/repos/pizko/prometej/contents/photo")
      .then((response) => {
        if (!response.ok) {
          throw new Error("GitHub API unavailable");
        }
        return response.json();
      })
      .then((items) => {
        const remoteImages = items
          .filter((item) => item.type === "file" && /\.(png|jpe?g|webp|gif)$/i.test(item.name))
          .sort((a, b) => a.name.localeCompare(b.name, "ru", { numeric: true }))
          .map((item, index) => ({
            src: `photo/${item.name}`,
            caption: captions[index] || `Фото ${index + 1}`,
          }));

        renderGallery(remoteImages);
      })
      .catch(() => {
        renderGallery(
          fallbackGallery.map((src, index) => ({
            src,
            caption: captions[index] || `Фото ${index + 1}`,
          }))
        );
      });
  }
});
