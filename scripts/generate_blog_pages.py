import os
import json
import re
from bs4 import BeautifulSoup

WORKSPACE = '/Users/user/Downloads/diginixit-saas-platform'
JSON_PATH = '/Users/user/.gemini/antigravity-ide/brain/ed438988-c45e-4023-b242-82622a9ae3ec/scratch/supabase_articles.json'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    supabase_articles = json.load(f)

# Built-in Core Web Vitals article
cwv_article = {
    "id": 100,
    "title": "Core Web Vitals as a Business Metric",
    "summary": "What founders, CTOs and digital leaders should know about website performance, mobile pass rates, conversion impacts, and engineering performance as a business discipline in 2026.",
    "author": "Dr. Nadeem Nazir",
    "date": "2026-10-20",
    "category": "SEO",
    "status": "published",
    "image": "/images/core_web_vitals_guide.webp",
    "image_caption": "Core Web Vitals as a Business Metric: Overview for founders, CTOs and digital leaders in the USA, UK and Europe."
}

# Load CWV content from js/articles-data.js
with open(os.path.join(WORKSPACE, 'js/articles-data.js'), 'r', encoding='utf-8') as f:
    js_content = f.read()

m = re.search(r'"id":\s*"2"[\s\S]*?"content":\s*"(<[\s\S]*?>)"\s*\n\s*\}', js_content)
if m:
    cwv_article['content'] = m.group(1).encode('utf-8').decode('unicode_escape')
else:
    # Read from existing blog/core-web-vitals-business-metric.html
    with open(os.path.join(WORKSPACE, 'blog/core-web-vitals-business-metric.html'), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        art_elem = soup.find('article', id='article-content')
        cwv_article['content'] = art_elem.decode_contents() if art_elem else ""

# Defined clean slugs map
SLUG_MAP = {
    22: "artificial-intelligence-in-management",
    21: "gaming-guide-tips-trends-gear",
    20: "ai-business-automation-agents",
    19: "seo-guide-ranking-in-ai-search",
    18: "cybersecurity-for-businesses-threats-protection",
    17: "ai-powered-design-ui-ux-workflows",
    15: "uae-vat-taxation-guide-rates-compliance",
    14: "uae-tax-registration-process",
    12: "uae-corporate-tax-law",
    9: "web-development-roadmap-for-beginners",
    8: "ui-ux-design-roadmap-for-beginners",
    7: "best-digital-products-to-sell",
    6: "new-taxation-law-pakistan",
    5: "punjab-protection-of-ownership-immovable-property",
    4: "inheritance-laws-pakistan-daughters-property-rights",
    3: "multi-agent-systems-enterprise-scale",
    2: "create-sell-notion-templates-using-ai",
    1: "affordable-seo-services-small-business",
    100: "core-web-vitals-business-metric"
}

CATEGORY_IMAGES = {
    "SEO": "/images/growth_illustration.webp",
    "Tech": "/images/structure_foundation_illustration.webp",
    "AI": "/images/engineering_cartoon.webp",
    "Web": "/images/web_engineering.webp",
    "Design": "/images/ui_ux_design.webp",
    "Law & Tax": "/images/law_compliance.webp",
    "Business": "/images/corporate_finance.webp"
}

all_articles = [cwv_article] + [a for a in supabase_articles if a['id'] != 1]
# Add slug to all
for a in all_articles:
    aid = a['id']
    a['slug'] = SLUG_MAP.get(aid, re.sub(r'[^a-z0-9]+', '-', a['title'].lower()).strip('-'))
    if not a.get('image'):
        cat = a.get('category', 'Tech')
        a['image'] = CATEGORY_IMAGES.get(cat, "/images/growth_illustration.webp")
    if not a.get('image_caption'):
        a['image_caption'] = f"{a['title']} — Insights by DiginixIT."

# Build pages
def build_article_html(art, other_articles):
    canonical_url = f"https://diginixit.com/blog/{art['slug']}"
    og_image = f"https://diginixit.com{art['image']}"
    initials = ''.join([part[0] for part in (art.get('author') or 'DN').split()[:2]]).upper()
    
    # Meta description (max 155 chars)
    desc = art.get('summary', '').strip()
    if len(desc) > 155:
        desc = desc[:152].rsplit(' ', 1)[0] + '...'
    if not desc:
        desc = f"Read {art['title']} on DiginixIT Insights Blog. Comprehensive analysis, guidelines, and strategic insights."
        
    # Title (max 60 chars)
    page_title = art['title']
    if len(f"{page_title} | DiginixIT") <= 60:
        meta_title = f"{page_title} | DiginixIT"
    elif len(page_title) <= 60:
        meta_title = page_title
    else:
        meta_title = page_title[:57].rsplit(' ', 1)[0] + '...'

    schema_breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://diginixit.com/" },
            { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://diginixit.com/blog" },
            { "@type": "ListItem", "position": 3, "name": art['title'], "item": canonical_url }
        ]
    }

    schema_article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": art['title'],
        "description": desc,
        "image": [og_image],
        "datePublished": art.get('date') or '2026-10-22',
        "dateModified": '2026-10-22',
        "author": [{
            "@type": "Person",
            "name": art.get('author') or 'Dr. Nadeem Nazir',
            "url": "https://diginixit.com/blog"
        }],
        "publisher": {
            "@type": "Organization",
            "name": "DiginixIT",
            "url": "https://diginixit.com/",
            "logo": {
                "@type": "ImageObject",
                "url": "https://diginixit.com/favicon.svg"
            }
        },
        "url": canonical_url,
        "mainEntityOfPage": canonical_url,
        "inLanguage": "en-US"
    }

    # Related items (pick 2 other articles)
    rel_html = ""
    for r in other_articles[:2]:
        r_url = f"/blog/{r['slug']}"
        rel_html += f"""
        <div class="p-6 rounded-xl border border-hairline bg-canvas-soft flex flex-col justify-between group hover:border-hairline-strong transition-colors">
            <div>
                <span class="text-[10px] font-mono text-primary uppercase tracking-widest">{r.get('category','Insights')}</span>
                <h4 class="font-bold text-base text-ink mt-2 group-hover:text-ink-mute transition-colors leading-snug">
                    <a href="{r_url}">{r['title']}</a>
                </h4>
                <p class="text-xs text-ink-mute mt-2 line-clamp-2 leading-relaxed">{r.get('summary','')}</p>
            </div>
            <div class="mt-4 pt-4 border-t border-hairline flex items-center justify-between text-xs font-medium">
                <span class="text-ink-mute font-mono">{r.get('date','2026')}</span>
                <a href="{r_url}" class="text-ink hover:underline">Read &rarr;</a>
            </div>
        </div>
        """

    # Demote any h1 in article body to h2 so the page has exactly 1 h1 (the main headline)
    content_body = re.sub(r'<h1(\s*[^>]*)>', r'<h2\1>', art['content'], flags=re.IGNORECASE)
    content_body = re.sub(r'</h1>', r'</h2>', content_body, flags=re.IGNORECASE)
    
    # Ensure any images in content_body have alt attribute
    soup_body = BeautifulSoup(content_body, 'html.parser')
    for img in soup_body.find_all('img'):
        if not img.get('alt'):
            img['alt'] = f"{art['title']} — illustration"
    content_body = str(soup_body)

    html = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <script>
        // Instant check for maintenance mode to prevent page flash of content
        try {{
            if (JSON.parse(localStorage.getItem('settings') || '{{}}').maintenanceMode) {{
                document.documentElement.style.display = 'none';
                window.location.replace('/maintenance');
            }}
        }} catch (e) {{ }}
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-adsense-account" content="ca-pub-3363493243397953">
    <title>{meta_title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{meta_title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{og_image}">
    <meta property="article:published_time" content="{art.get('date', '2026-10-22')}">
    <meta property="article:modified_time" content="2026-10-22">
    <meta property="article:author" content="{art.get('author', 'Dr. Nadeem Nazir')}">
    <meta property="article:section" content="{art.get('category', 'Technology')}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{meta_title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{og_image}">

    <!-- DNS Prefetch & Preconnect -->
    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
    <link rel="dns-prefetch" href="https://unpkg.com">
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <meta name="color-scheme" content="light">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- Tailwind Configuration Inline -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', 'sans-serif'],
                        serif: ['Lora', 'serif']
                    }},
                    colors: {{
                        canvas: '#ffffff',
                        'canvas-soft': '#fafafa',
                        'canvas-night': '#1c1c1c',
                        ink: '#171717',
                        'ink-mute': '#707070',
                        'ink-faint': '#b2b2b2',
                        primary: '#3ecf8e',
                        'primary-deep': '#24b47e',
                        hairline: '#dfdfdf',
                        'hairline-strong': '#c7c7c7',
                        'hairline-cool': '#ededed'
                    }},
                    letterSpacing: {{ tighter: '-0.04em', tight: '-0.02em' }}
                }}
            }}
        }};
    </script>

    <!-- Core Libraries -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js" defer></script>
    <script src="https://unpkg.com/lucide@latest" defer></script>

    <!-- Custom Stylesheet -->
    <link rel="stylesheet" href="/css/style.css">

    <!-- Structured Data: BreadcrumbList -->
    <script type="application/ld+json">
{json.dumps(schema_breadcrumb, indent=4)}
    </script>

    <!-- Structured Data: BlogPosting -->
    <script type="application/ld+json">
{json.dumps(schema_article, indent=4)}
    </script>

    <style>
        html, body {{
            overflow-x: hidden;
            max-width: 100%;
        }}
        * {{ box-sizing: border-box; }}
        img, video, iframe, table {{ max-width: 100%; }}

        #article-content {{
            font-family: 'Lora', Georgia, Cambria, serif;
            color: var(--color-ink, #171717);
            font-size: 1.125rem;
            line-height: 1.8;
            letter-spacing: -0.003em;
            word-break: break-word;
            overflow-wrap: break-word;
        }}
        @media (min-width: 640px) {{
            #article-content {{ font-size: 1.25rem; }}
        }}
        #article-content p {{
            font-family: 'Lora', Georgia, Cambria, serif !important;
            font-size: 1.125rem;
            line-height: 1.8;
            font-weight: 400;
            color: #171717;
            margin-bottom: 2rem;
        }}
        @media (min-width: 640px) {{
            #article-content p {{ font-size: 1.25rem; }}
        }}
        #article-content > p:first-of-type,
        #article-content p.lead {{
            font-size: 1.2rem;
            line-height: 1.75;
            color: #242424;
        }}
        @media (min-width: 640px) {{
            #article-content > p:first-of-type,
            #article-content p.lead {{ font-size: 1.35rem; }}
        }}
        #article-content h1,
        #article-content h2,
        #article-content h3,
        #article-content h4,
        #article-content h5,
        #article-content h6 {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            color: var(--color-ink, #171717);
            font-weight: 700 !important;
            line-height: 1.3;
            margin-top: 3rem;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
            word-break: break-word;
        }}
        #article-content h1 {{ font-size: clamp(1.75rem, 4vw, 2.35rem); }}
        #article-content h2 {{ font-size: clamp(1.4rem, 3.5vw, 1.85rem); }}
        #article-content h3 {{ font-size: clamp(1.2rem, 3vw, 1.5rem); }}

        #article-content ul,
        #article-content ol {{
            font-family: 'Lora', Georgia, serif !important;
            font-size: 1.125rem;
            line-height: 1.75;
            margin-bottom: 1.75rem;
        }}
        @media (min-width: 640px) {{
            #article-content ul,
            #article-content ol {{ font-size: 1.25rem; }}
        }}
        #article-content li {{
            font-family: 'Lora', Georgia, serif !important;
            margin-bottom: 0.5rem;
        }}
        #article-content a {{
            color: var(--color-ink);
            text-decoration: underline;
            font-weight: 500;
            transition: opacity 0.2s ease;
            word-break: break-word;
        }}
        #article-content a:hover {{ opacity: 0.8; }}

        #article-content ul {{
            list-style-type: disc !important;
            padding-left: 1.75rem !important;
            margin-bottom: 1.25rem !important;
        }}
        #article-content ol {{
            list-style-type: decimal !important;
            padding-left: 1.75rem !important;
            margin-bottom: 1.25rem !important;
        }}
        #article-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}
        #article-content th,
        #article-content td {{
            padding: 0.75rem 1rem;
            border: 1px solid var(--color-hairline, #dfdfdf);
        }}
        #article-content th {{
            background: var(--color-canvas-soft, #fafafa);
            font-family: 'Inter', sans-serif !important;
            font-weight: 600;
            font-size: 0.875rem;
        }}
        #article-content blockquote {{
            margin: 2rem 0;
            padding: 1.25rem 1.5rem;
            background: var(--color-canvas-soft, #fafafa);
            border-left: 3px solid var(--color-primary, #3ecf8e);
            border-radius: 0 0.5rem 0.5rem 0;
            font-style: italic;
        }}
        #article-content blockquote strong {{
            font-style: normal;
        }}
    </style>
</head>

<body class="bg-canvas text-ink">
    <div class="noise"></div>

    <!-- Reading Progress Pinned to Top -->
    <div id="read-progress" class="fixed top-0 left-0 h-1 bg-primary z-[60] transition-all duration-75" style="width: 0%;"></div>

    <!-- Universal Navigation -->
    <header id="navbar" class="fixed w-full top-0 z-50 transition-all duration-300 py-4 px-6 md:px-12 bg-canvas/90 backdrop-blur-md border-b border-hairline">
        <div class="max-w-[1280px] mx-auto flex justify-between items-center">
            <a href="/" class="flex items-center gap-2 group cursor-pointer" aria-label="DiginixIT Home">
                <span class="font-bold text-xl tracking-tighter text-ink group-hover:text-primary transition-colors">DIGINIXIT</span>
            </a>

            <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-ink-mute" aria-label="Main Navigation">
                <a href="/" class="hover:text-ink transition-colors">Home</a>
                <div class="relative group" id="services-nav-group">
                    <a href="/services" class="hover:text-ink transition-colors flex items-center gap-1 py-2">
                        <span>Our Services</span>
                        <svg class="w-3.5 h-3.5 opacity-60 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </a>
                    <div class="services-dropdown" id="services-dropdown">
                        <a href="/web-engineering" class="service-dropdown-item">
                            <span class="service-dropdown-dot"></span>
                            <div>
                                <div class="service-dropdown-title">Web Engineering</div>
                                <div class="service-dropdown-desc">High-performance web apps, SaaS &amp; APIs</div>
                            </div>
                        </a>
                        <a href="/ui-ux-design" class="service-dropdown-item">
                            <span class="service-dropdown-dot"></span>
                            <div>
                                <div class="service-dropdown-title">UI/UX Design</div>
                                <div class="service-dropdown-desc">Design systems, Figma &amp; product UX</div>
                            </div>
                        </a>
                        <a href="/technical-seo" class="service-dropdown-item">
                            <span class="service-dropdown-dot"></span>
                            <div>
                                <div class="service-dropdown-title">Technical SEO</div>
                                <div class="service-dropdown-desc">Core Web Vitals &amp; crawl architecture</div>
                            </div>
                        </a>
                        <a href="/social-media-marketing" class="service-dropdown-item">
                            <span class="service-dropdown-dot"></span>
                            <div>
                                <div class="service-dropdown-title">Social Media Marketing</div>
                                <div class="service-dropdown-desc">Multi-channel growth &amp; content systems</div>
                            </div>
                        </a>
                        <a href="/law-compliance" class="service-dropdown-item">
                            <span class="service-dropdown-dot"></span>
                            <div>
                                <div class="service-dropdown-title">Law &amp; Compliance</div>
                                <div class="service-dropdown-desc">Tech contracts, GDPR, IP &amp; data privacy</div>
                            </div>
                        </a>
                        <a href="/corporate-finance" class="service-dropdown-item">
                            <span class="service-dropdown-dot"></span>
                            <div>
                                <div class="service-dropdown-title">Corporate Finance</div>
                                <div class="service-dropdown-desc">Valuation, cap table &amp; financial models</div>
                            </div>
                        </a>
                    </div>
                </div>
                <a href="/blog" class="text-ink font-semibold transition-colors">Blog</a>
                <a href="/contact" class="hover:text-ink transition-colors">Contact</a>
            </nav>

            <div class="flex items-center gap-4">
                <a href="/auth" class="text-xs uppercase tracking-wider font-semibold text-ink px-4 py-2 border border-hairline rounded hover:bg-canvas-soft transition-colors">Portal</a>
                <button id="mobile-menu-btn" class="md:hidden p-2 text-ink hover:text-primary transition-colors" aria-label="Toggle Navigation Menu">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                </button>
            </div>
        </div>
    </header>

    <!-- Mobile Navigation Drawer -->
    <div id="mobile-drawer" class="fixed inset-0 z-40 bg-canvas transform translate-x-full transition-transform duration-300 md:hidden pt-20 px-6">
        <nav class="flex flex-col gap-6 text-lg font-medium text-ink">
            <a href="/" class="border-b border-hairline pb-3">Home</a>
            <a href="/services" class="border-b border-hairline pb-3">Services</a>
            <a href="/blog" class="border-b border-hairline pb-3 font-semibold text-primary">Blog</a>
            <a href="/contact" class="border-b border-hairline pb-3">Contact</a>
            <a href="/auth" class="btn-primary mt-4 text-center">Client Portal</a>
        </nav>
    </div>

    <!-- Main Article Content Container -->
    <main class="pt-32 pb-24 max-w-[820px] mx-auto px-6">
        <!-- Breadcrumb Navigation -->
        <nav class="flex items-center gap-2 text-xs text-ink-mute mb-8 uppercase tracking-widest font-mono" aria-label="Breadcrumb">
            <a href="/" class="hover:text-ink transition-colors">Home</a>
            <span>/</span>
            <a href="/blog" class="hover:text-ink transition-colors">Blog</a>
            <span>/</span>
            <span class="text-ink font-semibold">{art.get('category','Insights')}</span>
        </nav>

        <!-- Article Header -->
        <header class="mb-10">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-medium bg-canvas-soft border border-hairline text-primary mb-4">
                <span>{art.get('category','Insights')}</span>
                <span>&bull;</span>
                <span>{art.get('date', '2026-10-22')}</span>
            </div>
            <h1 class="text-3xl md:text-5xl font-bold tracking-tight text-ink mb-6 leading-[1.15]" style="letter-spacing: -0.02em;">
                {art['title']}
            </h1>

            <!-- Author & Metadata Bar -->
            <div class="flex items-center justify-between py-4 border-y border-hairline text-sm text-ink-mute">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-canvas-soft border border-hairline flex items-center justify-center font-bold text-xs text-ink">
                        {initials}
                    </div>
                    <div>
                        <div class="font-semibold text-ink text-sm">{art.get('author','Dr. Nadeem Nazir')}</div>
                        <time datetime="{art.get('date','2026-10-22')}" class="text-xs text-ink-mute">{art.get('date','2026-10-22')}</time>
                    </div>
                </div>

                <!-- Share Actions -->
                <div class="flex items-center gap-2">
                    <a href="https://twitter.com/intent/tweet?text={art['title']}&url={canonical_url}" target="_blank" rel="noopener" class="p-2 text-ink-mute hover:text-ink rounded border border-hairline hover:bg-canvas-soft transition-colors" aria-label="Share on X">
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    </a>
                    <a href="https://www.linkedin.com/sharing/share-offsite/?url={canonical_url}" target="_blank" rel="noopener" class="p-2 text-ink-mute hover:text-ink rounded border border-hairline hover:bg-canvas-soft transition-colors" aria-label="Share on LinkedIn">
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
                    </a>
                </div>
            </div>
        </header>

        <!-- Hero Image -->
        <figure class="my-8 rounded-xl overflow-hidden border border-hairline bg-canvas-soft">
            <img src="{art['image']}" alt="{art['title']}" width="1200" height="630" class="w-full h-auto object-cover max-h-[580px]" fetchpriority="high">
            <figcaption class="text-xs text-ink-mute py-2.5 px-4 text-center border-t border-hairline bg-canvas">{art['image_caption']}</figcaption>
        </figure>

        <!-- Article Body Content -->
        <article id="article-content" class="space-y-6">
{content_body}
        </article>

        <!-- Author Bio Section -->
        <section class="my-16 p-6 rounded-xl border border-hairline bg-canvas-soft flex flex-col sm:flex-row items-center sm:items-start gap-4">
            <div class="w-14 h-14 rounded-full bg-canvas border border-hairline flex items-center justify-center font-bold text-base text-ink shrink-0">
                {initials}
            </div>
            <div>
                <h3 class="text-base font-bold text-ink mb-1">{art.get('author','Dr. Nadeem Nazir')}</h3>
                <p class="text-xs text-ink-mute leading-relaxed mb-3">
                    Senior Technical SEO Strategist &amp; Principal Systems Architect at DiginixIT. Specializing in search engine entity architectures, sub-second Core Web Vitals optimization, and enterprise digital scalability frameworks.
                </p>
                <div class="flex items-center gap-3 text-xs font-mono text-primary">
                    <a href="/technical-seo" class="hover:underline">Technical SEO Services &rarr;</a>
                    <a href="/blog" class="hover:underline">All Publications &rarr;</a>
                </div>
            </div>
        </section>

        <!-- Related Insights -->
        <section class="my-16 border-t border-hairline pt-12">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl font-bold tracking-tight text-ink">Recommended Reading</h3>
                <a href="/blog" class="text-xs font-mono text-primary hover:underline">All Articles &rarr;</a>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {rel_html}
            </div>
        </section>

        <!-- Newsletter / Consultation Callout -->
        <section class="my-12 p-8 rounded-2xl border border-hairline bg-canvas-soft text-center">
            <h3 class="text-xl font-bold text-ink mb-2">Build Resilient Systems With DiginixIT</h3>
            <p class="text-sm text-ink-mute max-w-md mx-auto mb-6">
                Need enterprise-grade web engineering, product design, or technical SEO architecture? Connect with our senior consultants.
            </p>
            <a href="/contact" class="btn-primary inline-block">Schedule Architecture Review</a>
        </section>
    </main>

    <!-- Footer -->
    <footer class="bg-canvas border-t border-hairline py-12 px-6 md:px-12">
        <div class="max-w-[1280px] mx-auto flex flex-col md:flex-row justify-between items-center gap-6 text-xs text-ink-mute">
            <div class="flex items-center gap-2">
                <span class="font-bold tracking-tight text-ink">DIGINIXIT</span>
                <span>&bull;</span>
                <span>&copy; 2026 DiginixIT. All rights reserved.</span>
            </div>
            <div class="flex gap-6">
                <a href="/" class="hover:text-ink transition-colors">Home</a>
                <a href="/services" class="hover:text-ink transition-colors">Services</a>
                <a href="/blog" class="hover:text-ink transition-colors">Blog</a>
                <a href="/contact" class="hover:text-ink transition-colors">Contact</a>
            </div>
        </div>
    </footer>

    <!-- Reading Progress JS -->
    <script>
        window.addEventListener('scroll', () => {{
            const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            const bar = document.getElementById('read-progress');
            if (bar) bar.style.width = scrolled + '%';
        }});
    </script>
    <script src="/js/ui-components.js" defer></script>
    <script src="/js/articles-data.js" defer></script>
    <script src="/js/common.js" defer></script>
    <script src="/js/script.js" defer></script>
</body>
</html>
"""
    return html

# Generate all pages
os.makedirs(os.path.join(WORKSPACE, 'blog'), exist_ok=True)
generated_count = 0

for i, art in enumerate(all_articles):
    others = [o for o in all_articles if o['slug'] != art['slug']]
    page_html = build_article_html(art, others)
    out_path = os.path.join(WORKSPACE, 'blog', f"{art['slug']}.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    generated_count += 1
    print(f"[{generated_count}] Generated blog/{art['slug']}.html (ID {art['id']})")

print(f"\nSuccessfully generated {generated_count} static blog pages!")
