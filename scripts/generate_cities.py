from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "cities.json"
SERVICES_PATH = ROOT / "data" / "services.json"
CITIES_DIR = ROOT / "cities"
BASE_URL = "https://prometej01.ru"
DEFAULT_OG_IMAGE = f"{BASE_URL}/assets/images/fire.jpg"
PHONE = "+7 (929) 676-00-98"
PHONE_HREF = "+79296760098"


def load_json(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    letters = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z",
        "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
        "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
    text = "".join(letters.get(ch, ch) for ch in value.lower())
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "city"


def build_nav(active: str = "") -> str:
    items = [
        ("Главная", "/", active == "home"),
        ("О нас", "/about/", active == "about"),
        ("Услуги", "/services/", active == "services"),
        ("Контакты", "/contacts/", active == "contacts"),
        ("Галерея", "/gallery/", active == "gallery"),
        ("Продукция", "/products/", active == "products"),
        ("Цены", "/prices/", active == "prices"),
        ("Блог", "/blog/", active == "blog"),
        ("Города", "/cities/", active == "cities"),
    ]
    return "\n".join(
        f'              <li class="nav-item"><a class="nav-link{" active" if is_active else ""}" href="{href}">{label}</a></li>'
        for label, href, is_active in items
    )


def city_title(item: dict) -> str:
    return item.get("title") or f"Системы безопасности в {city_where(item)}"


def city_where(item: dict) -> str:
    return item.get("city_prepositional") or item["city"]


def city_description(item: dict) -> str:
    city = item["city"]
    region = item.get("region")
    area = f" и {region}" if region else ""
    return item.get("description") or (
        f"Прометей01: видеонаблюдение, СКУД, слаботочные сети, электромонтаж, "
        f"пожарная сигнализация, огнезащита и ПНР в {city_where(item)}{area}."
    )


def city_intro(item: dict) -> str:
    city = item["city"]
    region = item.get("region")
    where = city_where(item)
    area = f" в {where} и {region}" if region else f" в {where}"
    variants = [
        "для коммерческих объектов, производственных площадок, офисов, складов и частных домов",
        "для объектов с разной нагрузкой: от небольшого офиса до распределенной площадки",
        "для бизнеса, управляющих компаний, складов, магазинов и частных заказчиков",
        "для объектов, где важны контроль доступа, наблюдение, пожарная безопасность и понятная эксплуатация",
    ]
    phrase = variants[sum(ord(ch) for ch in city) % len(variants)]
    return item.get("hero_intro") or (
        f"Проектируем, монтируем и обслуживаем инженерные системы безопасности{area}: видеонаблюдение, СКУД, "
        f"слаботочные сети, электромонтаж, пожарную сигнализацию, огнезащиту, ПНР и исполнительную документацию {phrase}."
    )


def service_cards(services: list[dict], city: str) -> str:
    cards = []
    for service in services:
        points = "\n".join(f"                  <li>{escape(point)}</li>" for point in service.get("points", []))
        cards.append(
            f"""          <div class="col-md-6 col-xl-3">
            <article class="service-card h-100">
              <div class="card-body">
                <h3>{escape(service["name"])}</h3>
                <p>{escape(service["city_text"]).format(city=city)}</p>
                <ul class="list-check small mb-0">
{points}
                </ul>
              </div>
            </article>
          </div>"""
        )
    return "\n".join(cards)


def build_faq(item: dict) -> list[dict]:
    city = item["city"]
    region = item.get("region")
    where = city_where(item)
    area = f"{where} и {region}" if region else where
    return [
        {
            "question": f"Какие системы можно заказать в {where}?",
            "answer": "Можно заказать видеонаблюдение, СКУД, слаботочные сети, электромонтаж, пожарную сигнализацию, огнезащиту, ПНР и исполнительную документацию.",
        },
        {
            "question": "Можно ли получить предварительный расчет?",
            "answer": "Да. Для предварительного расчета достаточно описать объект, задачи, примерное количество точек и желаемые сроки. Точная смета формируется после уточнения условий монтажа.",
        },
        {
            "question": f"Работаете ли вы по объектам в регионе {area}?",
            "answer": "Да, рассматриваем объекты по городу и региону. Формат работ зависит от объема, состава оборудования, сроков и требований к документации.",
        },
        {
            "question": "Можно ли заказать только ПНР или исполнительную документацию?",
            "answer": "Да, можно обратиться не только за монтажом, но и за пуско-наладочными работами, проверкой системы, оформлением исполнительной документации и лабораторными услугами.",
        },
    ]


def faq_cards(faq: list[dict]) -> str:
    return "\n".join(
        f"""          <div class="col-md-6"><article class="service-card h-100"><div class="card-body"><h3>{escape(item["question"])}</h3><p>{escape(item["answer"])}</p></div></article></div>"""
        for item in faq
    )


def step_cards() -> str:
    steps = [
        ("Аудит задачи", "Уточняем тип объекта, зоны риска, требования к доступу, видеонаблюдению, пожарной безопасности и документации."),
        ("Подбор решения", "Подбираем оборудование, кабельные трассы, способ монтажа и состав работ под реальные условия объекта."),
        ("Монтаж и ПНР", "Выполняем прокладку линий, установку оборудования, подключение, программирование и проверку сценариев работы."),
        ("Передача результата", "Передаем систему в рабочем состоянии, объясняем базовую эксплуатацию и согласуем дальнейшее обслуживание."),
    ]
    return "\n".join(
        f"""          <div class="col-md-6 col-xl-3"><article class="service-card h-100"><div class="card-body"><h3>{escape(title)}</h3><p>{escape(text)}</p></div></article></div>"""
        for title, text in steps
    )


def schema_json(item: dict, services: list[dict], canonical_url: str) -> str:
    city = item["city"]
    city_in = city_where(item)
    faq = build_faq(item)
    payload = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfessionalService",
                "@id": f"{BASE_URL}/#organization",
                "name": "Прометей01",
                "url": f"{BASE_URL}/",
                "telephone": PHONE,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Москва",
                    "streetAddress": "Ангарская улица, д.6",
                    "addressCountry": "RU",
                },
                "areaServed": [
                    {"@type": "Country", "name": "Россия"},
                    {"@type": "City", "name": "Москва"},
                    {"@type": "AdministrativeArea", "name": "Московская область"},
                ],
            },
            {
                "@type": "WebPage",
                "@id": f"{canonical_url}#webpage",
                "url": canonical_url,
                "name": city_title(item),
                "description": city_description(item),
                "inLanguage": "ru-RU",
                "about": {"@id": f"{BASE_URL}/#organization"},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumbs",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Города", "item": f"{BASE_URL}/cities/"},
                    {"@type": "ListItem", "position": 3, "name": city_in, "item": canonical_url},
                ],
            },
            {
                "@type": "ItemList",
                "@id": f"{canonical_url}#services",
                "name": f"Услуги Прометей01 в {city_in}",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index + 1,
                        "item": {
                            "@type": "Service",
                            "name": f"{service['name']} в {city_in}",
                            "provider": {"@id": f"{BASE_URL}/#organization"},
                            "areaServed": [
                                {"@type": "Country", "name": "Россия"},
                                {"@type": "City", "name": city}
                            ],
                        },
                    }
                    for index, service in enumerate(services)
                ],
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": [
                    {"@type": "Question", "name": entry["question"], "acceptedAnswer": {"@type": "Answer", "text": entry["answer"]}}
                    for entry in faq
                ],
            },
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def build_city_page(item: dict, services: list[dict]) -> str:
    item = {**item}
    item.setdefault("slug", slugify(item["city"]))
    city = escape(item["city"])
    city_in = escape(city_where(item))
    title = escape(city_title(item))
    description = escape(city_description(item))
    hero_intro = escape(city_intro(item))
    canonical_url = f"{BASE_URL}/cities/{escape(item['slug'])}/"
    faq = build_faq(item)

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title if "Прометей01" in title else title + " | Прометей01"}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:site_name" content="Прометей01">
  <meta property="og:image" content="{DEFAULT_OG_IMAGE}">
  <meta property="og:image:alt" content="Прометей01 — системы безопасности в {city_in}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <script type="application/ld+json">
{schema_json(item, services, canonical_url)}
  </script>
</head>
<body>
  <header class="topbar"><nav class="navbar navbar-expand-xl navbar-dark"><div class="container"><a class="logo-link" href="/"><span class="logo-frame"><img src="/assets/images/logo.png" alt="Прометей01" onerror="this.style.display='none'; this.nextElementSibling.style.display='grid';"><span class="logo-fallback" style="display:none;">01</span></span><span class="logo-text">Прометей01<small>Системы безопасности</small></span></a><button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Открыть меню"><span class="navbar-toggler-icon"></span></button><div class="collapse navbar-collapse justify-content-end" id="mainNav"><ul class="navbar-nav align-items-xl-center gap-xl-1">
{build_nav("cities")}
  </ul></div></div></nav></header>

  <main>
    <section class="hero"><div class="container"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>→</span><a href="/cities/">Города</a><span>→</span><span aria-current="page">{city_in}</span></nav><div class="row align-items-center g-4"><div class="col-lg-7"><h1 class="hero-title">Системы безопасности <span>в {city_in}</span></h1><p class="hero-lead">{hero_intro}</p><div class="hero-actions"><a class="btn btn-accent btn-lg px-4" href="#city-contact-form">Получить расчет</a><a class="btn btn-outline-light btn-lg px-4" href="/services/">Смотреть услуги</a></div><div class="hero-features"><div class="hero-feature"><img src="/assets/images/icon-support.webp" alt=""><div><strong>Работаем по России</strong><small>Городские и региональные объекты</small></div></div><div class="hero-feature"><img src="/assets/images/icon-monitoring.webp" alt=""><div><strong>8 направлений</strong><small>От камер до документации</small></div></div><div class="hero-feature"><img src="/assets/images/icon-book.webp" alt=""><div><strong>Передача результата</strong><small>ПНР, проверка, документы</small></div></div></div></div><div class="col-lg-5"><div class="hero-visual"><div class="hero-orb"></div><div class="hero-card"><img src="/assets/images/robot.webp" alt="Прометей01 в {city_in}"></div></div></div></div></div></section>

    <section class="section-tight"><div class="container"><div class="metric-strip"><article class="metric-card"><span class="metric-value">15+</span><div>лет в сфере безопасности</div></article><article class="metric-card"><span class="metric-value">8</span><div>направлений работ</div></article><article class="metric-card"><span class="metric-value">300+</span><div>объектов в работе и на сервисе</div></article><article class="metric-card"><span class="metric-value">РФ</span><div>выезды и проекты по России</div></article></div></div></section>

    <section class="section" id="city-services"><div class="container"><div class="section-kicker">Услуги</div><h2 class="section-title">Что можно заказать в {city_in}</h2><p class="section-copy">Закрываем комплексные и отдельные задачи: монтаж, настройку, ремонт, обслуживание, пуско-наладку и подготовку документации.</p><div class="row g-4">
{service_cards(services, city_in)}
    </div></div></section>

    <section class="section"><div class="container"><div class="section-kicker">Этапы</div><h2 class="section-title">Как проходит работа</h2><div class="row g-4">
{step_cards()}
    </div></div></section>

    <section class="section"><div class="container"><div class="row g-4 align-items-start"><div class="col-lg-7"><div class="surface-card"><div class="section-kicker">Подход</div><h2 class="section-title">Не просто монтаж оборудования, а рабочая система</h2><p class="section-copy">Для объекта в {city_in} важно не только установить камеры, считыватели или кабельные трассы. Система должна быть понятной для эксплуатации, обслуживаемой, согласованной с требованиями объекта и готовой к дальнейшему расширению.</p><ul class="list-check"><li>Подбираем решение под задачи и условия объекта.</li><li>Учитываем кабельные трассы, питание, точки доступа и сценарии безопасности.</li><li>Проводим настройку, проверку и передаем результат без технического хаоса.</li></ul></div></div><div class="col-lg-5"><div class="surface-card overflow-hidden"><img class="media-cover" src="/assets/images/camera-intro.webp" alt="Системы безопасности в {city_in}"></div></div></div></div></section>

    <section class="section"><div class="container"><div class="section-kicker">FAQ</div><h2 class="section-title">Частые вопросы по работам в {city_in}</h2><div class="row g-4">
{faq_cards(faq)}
    </div></div></section>

    <section class="section"><div class="container"><div class="form-shell" id="city-contact-form"><div class="row g-4 align-items-start"><div class="col-lg-5"><div class="section-kicker text-white-50">Заявка</div><h2 class="section-title text-white">Получить расчет по объекту в {city_in}</h2><p class="contact-meta mb-2"><strong>Телефон:</strong><br><a href="tel:{PHONE_HREF}" class="text-white">{PHONE}</a></p><p class="contact-meta mb-0">Оставьте заявку, и мы уточним задачу, сроки, состав работ и формат выезда.</p></div><div class="col-lg-7"><form action="/send.php" method="post"><input type="hidden" name="form_source" value="Городская страница: {city}"><input type="text" name="website" class="d-none" tabindex="-1" autocomplete="off"><div class="row g-3"><div class="col-md-6"><input class="form-control" name="name" type="text" placeholder="Ваше имя" required></div><div class="col-md-6"><input class="form-control" name="phone" type="tel" placeholder="Телефон *" required></div><div class="col-12"><input class="form-control" name="email" type="email" placeholder="Email"></div><div class="col-12"><textarea class="form-control" name="comment" rows="4" placeholder="Кратко опишите задачу"></textarea></div><div class="col-12"><div class="captcha-box"><div class="captcha-row"><img class="captcha-image" id="city-captcha-image" src="/captcha.php" data-base-src="/captcha.php" alt="CAPTCHA"><button class="btn btn-outline-light" type="button" data-captcha-refresh data-captcha-target="city-captcha-image">Обновить код</button></div></div></div><div class="col-12"><input class="form-control" name="captcha" type="text" placeholder="Введите код с картинки" required></div><div class="col-12"><div class="form-check text-white-50"><input class="form-check-input" type="checkbox" id="consent-city" name="consent" value="yes" required><label class="form-check-label" for="consent-city">Я ознакомлен с информированным <a href="/assets/docs/soglasie.pdf" target="_blank" rel="noopener">согласием</a> и согласен на обработку данных.</label></div></div><div class="col-12 d-flex flex-wrap gap-3 align-items-center"><button class="btn btn-accent btn-lg px-4" type="submit">Получить расчет</button></div></div></form></div></div></div></div></section>
  </main>

  <footer class="footer"><div class="container d-flex flex-column flex-md-row justify-content-between gap-2"><div><strong>Прометей01</strong></div><div>© <span data-year></span> Прометей01</div></div></footer>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
  <script src="/assets/js/app.js"></script>
</body>
</html>
"""


def build_cities_index(items: list[dict]) -> str:
    cards = "\n".join(
        f"""          <div class="col-md-6 col-xl-3"><article class="service-card h-100"><div class="card-body"><h3>{escape(item["city"])}</h3><p>{escape(city_description(item))}</p><a class="btn btn-outline-dark" href="{escape(item.get("slug") or slugify(item["city"]))}/">Открыть страницу</a></div></article></div>"""
        for item in items
    )

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Системы безопасности по городам России | Прометей01</title>
  <meta name="description" content="Прометей01 выполняет монтаж видеонаблюдения, СКУД, слаботочных систем, пожарной сигнализации, огнезащиты и ПНР по городам России.">
  <link rel="canonical" href="{BASE_URL}/cities/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Системы безопасности по городам России — Прометей01">
  <meta property="og:description" content="Видеонаблюдение, СКУД, слаботочные системы, пожарная безопасность, огнезащита, ПНР и исполнительная документация.">
  <meta property="og:url" content="{BASE_URL}/cities/">
  <meta property="og:site_name" content="Прометей01">
  <meta property="og:image" content="{DEFAULT_OG_IMAGE}">
  <meta property="og:image:alt" content="Городские страницы Прометей01">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type": "ListItem", "position": 1, "name": "Главная", "item": "{BASE_URL}/"}},
          {{"@type": "ListItem", "position": 2, "name": "Города", "item": "{BASE_URL}/cities/"}}
        ]
      }},
      {{
        "@type": "CollectionPage",
        "name": "Системы безопасности по городам России",
        "url": "{BASE_URL}/cities/"
      }}
    ]
  }}
  </script>
</head>
<body>
  <header class="topbar"><nav class="navbar navbar-expand-xl navbar-dark"><div class="container"><a class="logo-link" href="/"><span class="logo-frame"><img src="/assets/images/logo.png" alt="Прометей01" onerror="this.style.display='none'; this.nextElementSibling.style.display='grid';"><span class="logo-fallback" style="display:none;">01</span></span><span class="logo-text">Прометей01<small>Системы безопасности</small></span></a><button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Открыть меню"><span class="navbar-toggler-icon"></span></button><div class="collapse navbar-collapse justify-content-end" id="mainNav"><ul class="navbar-nav align-items-xl-center gap-xl-1">
{build_nav("cities")}
  </ul></div></div></nav></header>

  <main>
    <section class="hero"><div class="container"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>→</span><span aria-current="page">Города</span></nav><div class="row align-items-center g-4"><div class="col-lg-7"><h1 class="hero-title">Системы безопасности <span>по городам России</span></h1><p class="hero-lead">Проектируем, монтируем и обслуживаем видеонаблюдение, СКУД, слаботочные сети, электромонтаж, пожарную сигнализацию, огнезащиту, ПНР и исполнительную документацию.</p><div class="hero-actions"><a class="btn btn-accent btn-lg px-4" href="#cities-grid">Смотреть города</a><a class="btn btn-outline-light btn-lg px-4" href="/services/">Услуги</a></div></div><div class="col-lg-5"><div class="hero-visual"><div class="hero-orb"></div><div class="hero-card"><img src="/assets/images/robot.webp" alt="Прометей01"></div></div></div></div></div></section>
    <section class="section-tight"><div class="container"><div class="metric-strip"><article class="metric-card"><span class="metric-value">{len(items)}</span><div>городов в разделе</div></article><article class="metric-card"><span class="metric-value">8</span><div>основных направлений</div></article><article class="metric-card"><span class="metric-value">15+</span><div>лет опыта</div></article><article class="metric-card"><span class="metric-value">РФ</span><div>работаем по России</div></article></div></div></section>
    <section class="section" id="cities-grid"><div class="container"><div class="section-kicker">География</div><h2 class="section-title">Выберите город</h2><div class="row g-4">
{cards}
    </div></div></section>
  </main>

  <footer class="footer"><div class="container d-flex flex-column flex-md-row justify-content-between gap-2"><div><strong>Прометей01</strong></div><div>© <span data-year></span> Прометей01</div></div></footer>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js"></script>
  <script src="/assets/js/app.js"></script>
</body>
</html>
"""


def main() -> None:
    items = load_json(DATA_PATH)
    services = load_json(SERVICES_PATH)
    CITIES_DIR.mkdir(parents=True, exist_ok=True)

    normalized_items = []
    for item in items:
        item = {**item}
        item.setdefault("slug", slugify(item["city"]))
        normalized_items.append(item)
        city_dir = CITIES_DIR / item["slug"]
        city_dir.mkdir(parents=True, exist_ok=True)
        (city_dir / "index.html").write_text(build_city_page(item, services), encoding="utf-8")

    (CITIES_DIR / "index.html").write_text(build_cities_index(normalized_items), encoding="utf-8")
    print(f"Сгенерировано городов: {len(normalized_items)}")


if __name__ == "__main__":
    main()
