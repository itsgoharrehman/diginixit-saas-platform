import os, json

def build_page(art, other_art, content_html):
    canonical_url = f"https://diginixit.com/blog/{art['slug']}"
    og_image = f"https://diginixit.com{art['image']}"
    
    schema_breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://diginixit.com/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": "https://diginixit.com/blog"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": art['title'],
                "item": canonical_url
            }
        ]
    }
    
    schema_article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": art['title'],
        "description": art['meta_desc'],
        "image": [og_image],
        "datePublished": art['date'],
        "dateModified": art['date_modified'],
        "author": [{
            "@type": "Person",
            "name": art['author'],
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

    initials = ''.join([part[0] for part in art['author'].split()[:2]]).upper()

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
    <title>{art['meta_title']}</title>
    <meta name="description" content="{art['meta_desc']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{art['meta_title']}">
    <meta property="og:description" content="{art['meta_desc']}">
    <meta property="og:image" content="{og_image}">
    <meta property="article:published_time" content="{art['date']}">
    <meta property="article:modified_time" content="{art['date_modified']}">
    <meta property="article:author" content="{art['author']}">
    <meta property="article:section" content="{art['category']}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{art['meta_title']}">
    <meta name="twitter:description" content="{art['meta_desc']}">
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
            border: 1px solid var(--color-hairline, #e5e5e5);
            padding: 0.65rem 0.85rem;
            text-align: left;
        }}
        #article-content th {{
            background-color: var(--color-canvas-soft, #f9f9f9);
            font-weight: 600;
        }}
        #article-content blockquote {{
            border-left: 3px solid var(--color-primary);
            padding-left: 1.5rem;
            font-style: italic;
            color: var(--color-ink-mute);
            margin: 2rem 0;
        }}
        #article-content code {{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            background-color: var(--color-canvas-soft);
            padding: 0.2em 0.4em;
            border-radius: var(--radius-xs);
            font-size: 0.85em;
        }}
        #article-content pre {{
            padding: 1rem;
            overflow-x: auto;
            margin-bottom: 1.75rem;
            background-color: var(--color-canvas-night);
            color: var(--color-on-dark);
            border-radius: var(--radius-sm);
            max-width: 100%;
            white-space: pre-wrap;
        }}
        @media (max-width: 640px) {{
            main {{
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 5.5rem !important;
            }}
            #article-content {{ font-size: 1rem !important; }}
        }}
    </style>
</head>

<body class="bg-canvas text-ink antialiased selection:bg-neutral-200">
    <!-- Navbar -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-canvas/80 backdrop-blur-md border-b border-hairline transition-all duration-300">
        <div class="max-w-[1280px] mx-auto px-6 h-16 flex items-center justify-between">
            <a href="/" class="flex items-center gap-2 group">
                <span class="font-bold text-xl tracking-tight text-ink group-hover:opacity-80 transition-opacity">DIGINIXIT<span class="text-primary">.</span></span>
            </a>

            <!-- Desktop Nav Items -->
            <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-ink-mute" aria-label="Main Navigation">
                <a href="/" class="hover:text-ink transition-colors">Home</a>
                <div class="nav-dropdown-wrapper relative group" id="nav-services-dropdown">
                    <a href="/services" class="nav-item-link inline-flex items-center gap-1.5 py-2 hover:text-ink transition-colors" id="nav-services" aria-haspopup="true" aria-expanded="false">
                        <span>Our Services</span>
                        <svg class="w-3.5 h-3.5 nav-dropdown-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
                    </a>
                    <div class="nav-dropdown-menu">
                        <a href="/web-engineering" class="nav-dropdown-item">
                            <span class="item-title">Web Engineering</span>
                            <span class="item-desc">High-performance apps &amp; custom SaaS architecture</span>
                        </a>
                        <a href="/ui-ux-design" class="nav-dropdown-item">
                            <span class="item-title">UI/UX Product Design</span>
                            <span class="item-desc">Bespoke design systems &amp; cognitive flows</span>
                        </a>
                        <a href="/technical-seo" class="nav-dropdown-item">
                            <span class="item-title">Technical SEO</span>
                            <span class="item-desc">Core Web Vitals &amp; entity search architecture</span>
                        </a>
                        <a href="/social-media-marketing" class="nav-dropdown-item">
                            <span class="item-title">Social Media Marketing</span>
                            <span class="item-desc">Audience acquisition &amp; organic distribution loops</span>
                        </a>
                        <a href="/law-compliance" class="nav-dropdown-item">
                            <span class="item-title">Law &amp; Tech Compliance</span>
                            <span class="item-desc">GDPR audits, enterprise MSAs &amp; IP protection</span>
                        </a>
                        <a href="/corporate-finance" class="nav-dropdown-item">
                            <span class="item-title">Corporate Finance</span>
                            <span class="item-desc">Dynamic financial models, valuations &amp; runways</span>
                        </a>
                        <div class="nav-dropdown-divider"></div>
                        <a href="/services" class="nav-dropdown-footer">
                            <span>Overview: All Capabilities</span>
                            <span class="text-primary font-bold">&rarr;</span>
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
            <span class="text-ink font-semibold">{art['category']}</span>
        </nav>

        <!-- Article Header -->
        <header class="mb-10">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-mono font-medium bg-canvas-soft border border-hairline text-primary mb-4">
                <span>{art['category']}</span>
                <span>&bull;</span>
                <span>{art['read_time']}</span>
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
                        <div class="font-semibold text-ink text-sm">{art['author']}</div>
                        <time datetime="{art['date']}" class="text-xs text-ink-mute">{art['date']}</time>
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
            <img src="{art['image']}" alt="{art['image_alt']}" width="1200" height="630" class="w-full h-auto object-cover max-h-[580px]" fetchpriority="high">
            <figcaption class="text-xs text-ink-mute py-2.5 px-4 text-center border-t border-hairline bg-canvas">{art['caption']}</figcaption>
        </figure>

        <!-- Article Body Content -->
        <article id="article-content" class="space-y-6">
{content_html}
        </article>

        <!-- Author Bio Section -->
        <section class="my-16 p-6 rounded-xl border border-hairline bg-canvas-soft flex flex-col sm:flex-row items-center sm:items-start gap-4">
            <div class="w-14 h-14 rounded-full bg-canvas border border-hairline flex items-center justify-center font-bold text-base text-ink shrink-0">
                {initials}
            </div>
            <div>
                <h3 class="text-base font-bold text-ink mb-1">{art['author']}</h3>
                <p class="text-xs text-ink-mute leading-relaxed mb-3">
                    Senior Technical SEO Strategist &amp; Principal Systems Architect at DiginixIT. Specializing in search engine entity architectures, sub-second Core Web Vitals optimization, and enterprise digital scalability frameworks.
                </p>
                <div class="flex items-center gap-3 text-xs font-mono text-primary">
                    <a href="/technical-seo" class="hover:underline">Technical SEO Services &rarr;</a>
                    <a href="/blog" class="hover:underline">All Publications &rarr;</a>
                </div>
            </div>
        </section>

        <!-- Related Insights & Pillar Navigation -->
        <section class="border-t border-hairline pt-12" aria-label="Related Insights">
            <h2 class="text-2xl font-bold tracking-tight text-ink mb-6" style="letter-spacing: -0.02em;">Related Insights &amp; Capabilities</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Companion Article Card -->
                <div class="p-5 border border-hairline rounded-xl hover:border-hairline-strong transition-all bg-canvas group">
                    <span class="text-[10px] font-mono uppercase tracking-wider text-primary font-semibold block mb-2">{other_art['category']} &bull; Research Paper</span>
                    <h3 class="text-base font-bold text-ink mb-2 group-hover:text-primary transition-colors">
                        <a href="/blog/{other_art['slug']}">{other_art['title']}</a>
                    </h3>
                    <p class="text-xs text-ink-mute line-clamp-3 mb-4 leading-relaxed">{other_art['meta_desc']}</p>
                    <a href="/blog/{other_art['slug']}" class="text-xs font-semibold text-ink inline-flex items-center gap-1 group-hover:text-primary">
                        <span>Read Full Insight</span> &rarr;
                    </a>
                </div>

                <!-- Pillar Service Card -->
                <div class="p-5 border border-hairline rounded-xl hover:border-hairline-strong transition-all bg-canvas group">
                    <span class="text-[10px] font-mono uppercase tracking-wider text-primary font-semibold block mb-2">Core Service Capability</span>
                    <h3 class="text-base font-bold text-ink mb-2 group-hover:text-primary transition-colors">
                        <a href="/technical-seo">Technical SEO &amp; Search Architecture</a>
                    </h3>
                    <p class="text-xs text-ink-mute line-clamp-3 mb-4 leading-relaxed">Infrastructure-level search engine optimization: sub-second Core Web Vitals, nested Schema.org entity graphs, and topical authority architecture.</p>
                    <a href="/technical-seo" class="text-xs font-semibold text-ink inline-flex items-center gap-1 group-hover:text-primary">
                        <span>Explore Capabilities</span> &rarr;
                    </a>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer-light border-t border-hairline bg-canvas-soft py-12">
        <div class="max-w-[1280px] mx-auto px-6 flex flex-col md:flex-row justify-between items-center text-sm gap-y-4 md:gap-y-0 text-ink-mute">
            <div class="font-bold text-ink" style="letter-spacing: -0.04em;">DIGINIXIT<span class="text-primary">.</span></div>
            <div class="flex flex-wrap justify-center gap-x-6 gap-y-2 text-xs">
                <a href="/" class="hover:text-ink">Home</a>
                <a href="/services" class="hover:text-ink">Services</a>
                <a href="/blog" class="hover:text-ink">Blog</a>
                <a href="/contact" class="hover:text-ink">Contact</a>
                <a href="/technical-seo" class="hover:text-ink">Technical SEO</a>
                <a href="/web-engineering" class="hover:text-ink">Web Engineering</a>
            </div>
            <div class="text-xs">&copy; 2026 DiginixIT. All rights reserved.</div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="/js/ui-primitives.js" defer></script>
    <script src="/js/ui-components.js" defer></script>
    <script src="/js/articles-data.js" defer></script>
    <script src="/js/common.js" defer></script>
    <script src="/js/script.js" defer></script>
</body>
</html>
"""
    return html

# Load articles from articles-data.js
with open('js/articles-data.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Execute JS in Python or extract JSON
import re
match = re.search(r'window\.builtInArticles\s*=\s*(\[[\s\S]*?\]);\s*$', code)
if match:
    articles = json.loads(match.group(1))
    art1 = next(a for a in articles if a['id'] == '1')
    art2 = next(a for a in articles if a['id'] == '2')

    art1_meta = {
        'slug': art1['slug'],
        'title': art1['title'],
        'meta_title': f"{art1['title']} | DiginixIT Insights",
        'meta_desc': "Learn how small businesses can drive compounding organic traffic and attract qualified local customers on a budget using targeted SEO and local map packs.",
        'author': art1['author'],
        'date': art1['date'],
        'date_modified': '2026-10-22',
        'read_time': '7 min read',
        'category': art1['category'],
        'image': '/' + art1['image'].lstrip('/'),
        'image_alt': 'Affordable SEO strategies, keyword research, and organic traffic growth diagnostics for small businesses',
        'caption': art1.get('image_caption', 'Affordable SEO strategies and local visibility framework for small business owners.')
    }

    art2_meta = {
        'slug': art2['slug'],
        'title': art2['title'],
        'meta_title': f"{art2['title']} (2026 Guide) | DiginixIT",
        'meta_desc': "What founders, CTOs and digital leaders should know about Core Web Vitals, mobile pass rates, conversion impacts, and engineering performance as a metric.",
        'author': art2['author'],
        'date': art2['date'],
        'date_modified': '2026-10-22',
        'read_time': '12 min read',
        'category': art2['category'],
        'image': '/' + art2['image'].lstrip('/'),
        'image_alt': 'Core Web Vitals as a Business Metric: Overview for founders, CTOs and digital leaders in the USA, UK and Europe',
        'caption': art2.get('image_caption', 'Core Web Vitals as a Business Metric: Overview for founders, CTOs and digital leaders in the USA, UK and Europe.')
    }

    # Generate page 1
    page1_html = build_page(art1_meta, art2_meta, art1['content'])
    with open('blog/affordable-seo-services-small-business.html', 'w', encoding='utf-8') as f:
        f.write(page1_html)
    print("Created blog/affordable-seo-services-small-business.html successfully.")

    # Generate page 2
    page2_html = build_page(art2_meta, art1_meta, art2['content'])
    with open('blog/core-web-vitals-business-metric.html', 'w', encoding='utf-8') as f:
        f.write(page2_html)
    print("Created blog/core-web-vitals-business-metric.html successfully.")
else:
    print("Error: Could not parse builtInArticles from js/articles-data.js")
