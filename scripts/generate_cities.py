from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cities.json"
CITIES_DIR = ROOT / "cities"


def build_city_page(item: dict) -> str:
    city = escape(item["city"])
    title = escape(item["title"])
    description = escape(item["description"])
    hero_intro = escape(item["hero_intro"])
    lead = escape(item["lead"])

    service_points = "\n".join(
        f"            <li>{escape(point)}</li>" for point in item["service_points"]
    )
    faq_blocks = "\n".join(
        f"""        <article class="service-card"><div class="card-body"><h3>{escape(faq["question"])}</h3><p>{escape(faq["answer"])}</p></div></article>"""
        for faq in item["faq"]
    )

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Прометей01</title>
  <meta name="description" content="{description}">
  <link rel="icon" href="../../favicon.ico" sizes="any">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/styles.css">
</head>
<body>
  <header class="topbar">
    <nav class="navbar navbar-expand-xl navbar-dark">
      <div class="container">
        <a class="logo-link" href="../../index.html">
          <span class="logo-frame">
            <img src="../../assets/images/logo.png" alt="Прометей01" onerror="this.style.display='none'; this.nextElementSibling.style.display='grid';">
            <span class="logo-fallback" style="display:none;">01</span>
          </span>
          <span class="logo-text">
            Прометей01
            <small>Системы безопасности</small>
          </span>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Открыть меню">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="mainNav">
          <ul class="navbar-nav align-items-xl-center gap-xl-1">
              <li class="nav-item"><a class="nav-link" href="../../index.html">Главная</a></li>
              <li class="nav-item"><a class="nav-link" href="../../about.html">О нас</a></li>
              <li class="nav-item"><a class="nav-link" href="../../services.html">Услуги</a></li>
              <li class="nav-item"><a class="nav-link" href="../../contacts.html">Контакты</a></li>
              <li class="nav-item"><a class="nav-link" href="../../gallery.html">Галерея</a></li>
              <li class="nav-item"><a class="nav-link" href="../../products.html">Продукция</a></li>
              <li class="nav-item"><a class="nav-link" href="../../prices.html">Цены</a></li>
              <li class="nav-item"><a class="nav-link" href="../../blog.html">Блог</a></li>
              <li class="nav-item"><a class="nav-link active" href="../index.html">Города</a></li>
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <section class="page-hero">
      <div class="container">
        <h1 class="section-title text-white">{title}</h1>
        <p>{hero_intro}</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="row g-4 align-items-start">
          <div class="col-lg-7">
            <div class="surface-card">
              <div class="section-kicker">Как мы работаем</div>
              <h2 class="section-title">Решения по безопасности для города {city}</h2>
              <p class="section-copy">{lead}</p>
              <ul class="list-check">
{service_points}
              </ul>
            </div>
          </div>
          <div class="col-lg-5">
            <div class="surface-card overflow-hidden">
              <img class="media-cover" src="../../assets/images/camera-intro.webp" alt="Системы безопасности в {city}">
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-kicker">FAQ</div>
        <h2 class="section-title">Частые вопросы по {city}</h2>
        <div class="row g-4">
          <div class="col-md-6">
{faq_blocks}
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="form-shell">
          <div class="row g-4 align-items-start">
            <div class="col-lg-5">
              <div class="section-kicker text-white-50">Заявка</div>
              <h2 class="section-title text-white">Получить расчет по объекту в {city}</h2>
              <p class="contact-meta mb-2"><strong>Телефон:</strong><br><a href="tel:+79296760098" class="text-white">+7 (929) 676-00-98</a></p>
              <p class="contact-meta mb-0">Оставьте заявку, и мы уточним задачу, сроки и состав работ.</p>
            </div>
            <div class="col-lg-7">
              <form action="../../send.php" method="post">
                <input type="hidden" name="form_source" value="Городская страница: {city}">
                <input type="text" name="website" class="d-none" tabindex="-1" autocomplete="off">
                <div class="row g-3">
                  <div class="col-md-6"><input class="form-control" name="name" type="text" placeholder="Ваше имя" required></div>
                  <div class="col-md-6"><input class="form-control" name="phone" type="tel" placeholder="Телефон *" required></div>
                  <div class="col-12"><input class="form-control" name="email" type="email" placeholder="Email"></div>
                  <div class="col-12"><textarea class="form-control" name="comment" rows="4" placeholder="Кратко опишите задачу"></textarea></div>
                  <div class="col-12">
                    <div class="captcha-box">
                      <div class="captcha-row">
                        <img class="captcha-image" id="city-captcha-image" src="../../captcha.php" data-base-src="../../captcha.php" alt="CAPTCHA">
                        <button class="btn btn-outline-light" type="button" data-captcha-refresh data-captcha-target="city-captcha-image">Обновить код</button>
                      </div>
                    </div>
                  </div>
                  <div class="col-12"><input class="form-control" name="captcha" type="text" placeholder="Введите код с картинки" required></div>
                  <div class="col-12">
                    <div class="form-check text-white-50">
                      <input class="form-check-input" type="checkbox" id="consent-city" name="consent" value="yes" required>
                      <label class="form-check-label" for="consent-city">Я ознакомлен с информированным <a href="../../index.html">согласием</a> и согласен на обработку данных.</label>
                    </div>
                  </div>
                  <div class="col-12 d-flex flex-wrap gap-3 align-items-center">
                    <button class="btn btn-accent btn-lg px-4" type="submit">Получить расчет</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container d-flex flex-column flex-md-row justify-content-between gap-2">
      <div><strong>Прометей01</strong></div>
      <div>© <span data-year></span> Прометей01</div>
    </div>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
  <script src="../../assets/js/app.js"></script>
</body>
</html>
"""


def build_cities_index(items: list[dict]) -> str:
    cards = "\n".join(
        f"""      <div class="col-md-6 col-xl-4"><article class="service-card"><div class="card-body"><h3>{escape(item["city"])}</h3><p>{escape(item["description"])}</p><a class="btn btn-outline-dark" href="{escape(item["slug"])}/">Открыть страницу</a></div></article></div>"""
        for item in items
    )

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Города — Прометей01</title>
  <meta name="description" content="Городские страницы Прометей01 для локального поиска и услуг по безопасности.">
  <link rel="icon" href="../favicon.ico" sizes="any">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/styles.css">
</head>
<body>
  <header class="topbar">
    <nav class="navbar navbar-expand-xl navbar-dark">
      <div class="container">
        <a class="logo-link" href="../index.html">
          <span class="logo-frame">
            <img src="../assets/images/logo.png" alt="Прометей01" onerror="this.style.display='none'; this.nextElementSibling.style.display='grid';">
            <span class="logo-fallback" style="display:none;">01</span>
          </span>
          <span class="logo-text">
            Прометей01
            <small>Системы безопасности</small>
          </span>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Открыть меню">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="mainNav">
          <ul class="navbar-nav align-items-xl-center gap-xl-1">
              <li class="nav-item"><a class="nav-link" href="../index.html">Главная</a></li>
              <li class="nav-item"><a class="nav-link" href="../about.html">О нас</a></li>
              <li class="nav-item"><a class="nav-link" href="../services.html">Услуги</a></li>
              <li class="nav-item"><a class="nav-link" href="../contacts.html">Контакты</a></li>
              <li class="nav-item"><a class="nav-link" href="../gallery.html">Галерея</a></li>
              <li class="nav-item"><a class="nav-link" href="../products.html">Продукция</a></li>
              <li class="nav-item"><a class="nav-link" href="../prices.html">Цены</a></li>
              <li class="nav-item"><a class="nav-link" href="../blog.html">Блог</a></li>
              <li class="nav-item"><a class="nav-link active" href="index.html">Города</a></li>
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <section class="page-hero">
      <div class="container">
        <h1 class="section-title text-white">Города</h1>
        <p>Основа под локальные страницы для поискового трафика. Здесь будут собираться отдельные страницы по городам и направлениям работ.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="row g-4">
{cards}
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container d-flex flex-column flex-md-row justify-content-between gap-2">
      <div><strong>Прометей01</strong></div>
      <div>© <span data-year></span> Прометей01</div>
    </div>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
  <script src="../assets/js/app.js"></script>
</body>
</html>
"""


def main() -> None:
    items = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    CITIES_DIR.mkdir(parents=True, exist_ok=True)

    for item in items:
        city_dir = CITIES_DIR / item["slug"]
        city_dir.mkdir(parents=True, exist_ok=True)
        (city_dir / "index.html").write_text(build_city_page(item), encoding="utf-8")

    (CITIES_DIR / "index.html").write_text(build_cities_index(items), encoding="utf-8")
    print(f"Сгенерировано городов: {len(items)}")


if __name__ == "__main__":
    main()
