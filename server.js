import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;
const HOST = '0.0.0.0';

app.use(express.json({ limit: '1mb' }));

// --- SYSTEM PROMPT & KNOWLEDGE BASE ---
const SYSTEM_PROMPT = `You are the official AI Assistant for DiginixIT (https://diginixit.com), a premier technology, design, legal, and financial consultancy.
Your goal is to answer visitor questions accurately, warmly, professionally, and concisely in English or Urdu (depending on how the user addresses you).

KEY FACTS ABOUT DIGINIXIT:
1. Executive Leadership:
   - Dr. Nadeem Nazir: Chief Executive & Founding Strategic Advisor at DiginixIT. Renowned for strategic technology architecture, enterprise digital transformation, corporate governance, cross-border technology compliance, and scaling high-performance engineering teams. He consults international enterprises and fast-growing startups on digital transformation, regulatory compliance, and scalable product architecture.
   - Gohar Rehman: Lead Systems Architect & Core Technical Maintainer (Email: goharrehmanfsd260@gmail.com).

2. Company Pillars & Services:
   - 01 Web Engineering: Custom SaaS, serverless web apps, real-time databases (PostgreSQL/Supabase), Three.js 3D spatial experiences, APIs, edge caching.
   - 02 UX/UI Design: Bespoke design systems, typography-first layouts, atomic design tokens, micro-animations, minimal luxury dark/light aesthetics.
   - 03 Technical SEO & Growth: Core Web Vitals optimization (<2.5s LCP), JSON-LD schemas, crawl budget tuning, organic search dominance.
   - 04 Law & Tech Compliance: Technology law, GDPR/CCPA data privacy compliance, IP protection, software copyrights, bespoke SaaS contracts.
   - 05 Corporate Finance: Financial modeling, SaaS startup valuations, fundraising strategy, capital allocation, and cash flow management.

3. Process Methodology:
   - Discover -> Build -> Launch -> Protect -> Scale

4. Insights & Blog:
   - "The Future of Web Development in 2026" (Alex Rivers)
   - "Mastering Design Systems" (Sophia Chen)
   - "Optimizing Core Web Vitals for $10k Sites" (Marcus Vance)

5. Contact & Studio Locations:
   - Corporate Address: Main Boulevard, Lahore, Punjab, Pakistan
   - Global Studio: Faisalabad, Punjab, Pakistan
   - Phone / WhatsApp: +92 300 7960300
   - Email: contact@diginix.com (or goharrehmanfsd260@gmail.com)
   - Hours: Monday - Friday, 09:00 to 18:00 PKT
   - Status: Currently accepting new projects (Avg response time: 2 hours)
   - Socials: LinkedIn (https://www.linkedin.com/company/diginixit/), Twitter/X (@diginixit), Instagram (@diginixit), GitHub (@diginixit)

BEHAVIOR:
- When asked about Dr. Nadeem Nazir, highlight his leadership, credentials, strategic governance, advisory role, and contact availability via DiginixIT.
- When asked about booking, services, or quotes, provide direct contact details (+92 300 7960300 or contact@diginix.com).
- Keep replies informative, clear, and structured with bullet points where helpful.
- Support both English and Urdu fluently.`;

function getLocalKnowledgeReply(query) {
    const q = (query || '').toLowerCase();

    if (q.includes('nadeem') || q.includes('nazir') || q.includes('doctor') || q.includes('ceo') || q.includes('founder') || q.includes('advisor')) {
        return `**Dr. Nadeem Nazir** is the **Chief Executive & Founding Strategic Advisor** at DiginixIT.\n\n` +
            `**About Dr. Nadeem Nazir:**\n` +
            `Dr. Nadeem Nazir leads DiginixIT's strategic direction, high-stakes client advisory, technology governance, and venture acceleration. With extensive academic and industrial pedigree in computer engineering and business systems, Dr. Nadeem Nazir oversees the firm's multidisciplinary practice spanning custom web software, technology law, and corporate finance. He consults international enterprises and fast-growing startups on digital transformation, regulatory compliance, and scalable product architecture.\n\n` +
            `**Core Expertise & Advisory Domains:**\n` +
            `• Enterprise Software Architecture & Scalability\n` +
            `• Corporate Governance & Cross-Border Tech Law\n` +
            `• Venture Strategy, Capital Allocation & Valuations\n` +
            `• High-Impact Engineering Leadership & Mentorship\n\n` +
            `**Contact & Appointments:**\n` +
            `To schedule a strategic technology or corporate advisory session with Dr. Nadeem Nazir, please contact DiginixIT:\n` +
            `• Voice/WhatsApp: [+92 300 7960300](tel:+923007960300)\n` +
            `• Direct Inquiries: [contact@diginix.com](mailto:contact@diginix.com)\n` +
            `• LinkedIn: [DiginixIT LinkedIn](https://www.linkedin.com/company/diginixit/)`;
    }

    if (q.includes('web') || q.includes('engineering') || q.includes('software') || q.includes('saas') || q.includes('develop') || q.includes('stack')) {
        return `**Web Engineering (01 — Engineering)**\n\n` +
            `Bespoke SaaS development, high-performance web applications, serverless architectures, and real-time database integrations.\n\n` +
            `**Key Capabilities:**\n` +
            `• Custom full-stack web applications (Modern JS/TS, React, Node.js, Express, Edge)\n` +
            `• Platform & SaaS Engineering (Portals, Client dashboards, Multi-tenant architectures)\n` +
            `• Real-time database integration (Supabase, PostgreSQL, local caching)\n` +
            `• Microservices, REST & GraphQL APIs, secure webhook automation\n` +
            `• Spatial editorial layouts with Three.js WebGL rendering & GSAP micro-animations\n\n` +
            `Contact our engineering studio at **+92 300 7960300** or **contact@diginix.com**.`;
    }

    if (q.includes('design') || q.includes('ui') || q.includes('ux') || q.includes('figma') || q.includes('interface')) {
        return `**UI/UX Design Systems (02 — Design)**\n\n` +
            `Bespoke design systems, user experience architecture, and high-fidelity interface design.\n\n` +
            `**Key Capabilities:**\n` +
            `• Atomic Design Systems and shared CSS/HSL token libraries\n` +
            `• Cardless, typographic layouts with strict spatial hierarchy\n` +
            `• Interactive micro-interactions, cursor physics, and magnetic button behaviors\n` +
            `• Responsive layouts tailored across ultra-wide desktop to mobile\n` +
            `• Dark-mode-first aesthetic and minimal luxury styling`;
    }

    if (q.includes('seo') || q.includes('vitals') || q.includes('speed') || q.includes('google') || q.includes('rank') || q.includes('audit')) {
        return `**Technical SEO & Growth (03 — Growth)**\n\n` +
            `Core Web Vitals optimization, semantic structured data schemas, crawl budget tuning, and organic traffic acceleration.\n\n` +
            `**Key Capabilities:**\n` +
            `• Sub-2.5s LCP, zero layout shifts (CLS), and optimal FID/INP Core Web Vitals\n` +
            `• JSON-LD Schema.org rich results (Organization, LocalBusiness, FAQPage, BreadcrumbList)\n` +
            `• Topic cluster architecture & semantic content optimization\n` +
            `• Local SEO for regional market authority & global search discovery\n` +
            `• Conversion rate optimization (CRO) with frictionless user flows`;
    }

    if (q.includes('law') || q.includes('legal') || q.includes('compliance') || q.includes('gdpr') || q.includes('ccpa') || q.includes('contract') || q.includes('ip')) {
        return `**Law & Tech Compliance (04 — Protection)**\n\n` +
            `Technology law consultancy, GDPR/CCPA data privacy compliance audits, IP protection, and contract drafting.\n\n` +
            `**Key Capabilities:**\n` +
            `• Data privacy auditing (GDPR, CCPA, local data security statutes)\n` +
            `• Intellectual property (IP) assignment, patent filings, and proprietary software protection\n` +
            `• Bespoke SaaS Master Service Agreements (MSA), SLAs, and Terms of Service\n` +
            `• Vendor liability audits and cyber regulatory risk management`;
    }

    if (q.includes('finance') || q.includes('valuation') || q.includes('fundrais') || q.includes('cash flow') || q.includes('budget') || q.includes('investor')) {
        return `**Corporate Finance & Valuation (05 — Scale)**\n\n` +
            `Financial forecasting models, company valuations, fundraising strategies, and cash flow structuring for tech ventures.\n\n` +
            `**Key Capabilities:**\n` +
            `• DCF & multiple-based valuation models for SaaS and tech startups\n` +
            `• Investor-ready pro-forma financial decks and cap table modeling\n` +
            `• Cash flow optimization, unit economics (CAC, LTV, Churn) analysis\n` +
            `• Growth budget forecasting and capital allocation frameworks`;
    }

    if (q.includes('contact') || q.includes('email') || q.includes('phone') || q.includes('number') || q.includes('address') || q.includes('location') || q.includes('office') || q.includes('hire') || q.includes('quote')) {
        return `**Get in Touch with DiginixIT:**\n\n` +
            `• **Voice / WhatsApp**: [+92 300 7960300](tel:+923007960300)\n` +
            `• **Email**: [contact@diginix.com](mailto:contact@diginix.com)\n` +
            `• **Corporate Address**: Main Boulevard, Lahore, 54000, Punjab, Pakistan\n` +
            `• **Global Studio**: Global Engineering Studio, Faisalabad, Punjab, Pakistan\n` +
            `• **Working Hours**: Monday to Friday: 09:00 AM – 06:00 PM (PKT)\n` +
            `• **Status**: Currently accepting new projects (Average response: 2 hours)\n\n` +
            `Follow us on [LinkedIn](https://www.linkedin.com/company/diginixit/) or [Twitter/X](https://twitter.com/diginixit).`;
    }

    return `**DiginixIT | Build, Protect & Scale Your Business**\n\n` +
        `We are a premier multidisciplinary technology agency specializing in:\n` +
        `1. **Web Engineering**: High-performance SaaS & web infrastructure\n` +
        `2. **UI/UX Design**: Tokenized, typography-first design systems\n` +
        `3. **Technical SEO**: Core Web Vitals (<2.5s) & rich schema\n` +
        `4. **Tech Law & Compliance**: GDPR/CCPA & IP protection\n` +
        `5. **Corporate Finance**: Tech valuations & strategic modeling\n\n` +
        `Executive Leadership: **Dr. Nadeem Nazir**\n` +
        `Direct Inquiries: [+92 300 7960300](tel:+923007960300) | [contact@diginix.com](mailto:contact@diginix.com)`;
}

// --- SECURE SERVER-SIDE CHAT ENDPOINT ---
app.post('/api/chat', async (req, res) => {
    try {
        const { message, history } = req.body || {};
        if (!message || typeof message !== 'string') {
            return res.status(400).json({ error: 'Message is required' });
        }

        const apiKey = process.env.GROK_API_KEY || process.env.XAI_API_KEY;
        const model = process.env.GROK_MODEL || 'grok-beta';

        // If no secret key is set on the server yet, respond with verified local knowledge
        if (!apiKey) {
            const reply = getLocalKnowledgeReply(message);
            return res.json({
                reply: reply,
                source: 'local_knowledge',
                note: 'Grok API key not set in server environment variables. Operating in verified Diginix knowledge mode.'
            });
        }

        // Prepare messages payload for xAI Grok API
        const messages = [
            { role: 'system', content: SYSTEM_PROMPT }
        ];

        if (Array.isArray(history)) {
            const recent = history.slice(-8);
            recent.forEach(m => {
                if (m && (m.role === 'user' || m.role === 'assistant') && m.content) {
                    messages.push({ role: m.role, content: String(m.content) });
                }
            });
        }

        messages.push({ role: 'user', content: message });

        const xaiResponse = await fetch('https://api.x.ai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey.trim()}`
            },
            body: JSON.stringify({
                model: model,
                messages: messages,
                temperature: 0.6,
                max_tokens: 800,
                stream: false
            })
        });

        if (!xaiResponse.ok) {
            const errData = await xaiResponse.json().catch(() => ({}));
            console.error('xAI Grok API error:', errData);
            const fallbackReply = getLocalKnowledgeReply(message);
            return res.json({
                reply: fallbackReply,
                source: 'fallback_knowledge',
                error_detail: errData.error?.message || xaiResponse.statusText
            });
        }

        const data = await xaiResponse.json();
        const botReply = data.choices?.[0]?.message?.content || getLocalKnowledgeReply(message);

        return res.json({
            reply: botReply,
            source: 'grok_api',
            model: model
        });

    } catch (err) {
        console.error('Server /api/chat error:', err);
        const fallback = getLocalKnowledgeReply(req.body?.message || '');
        return res.json({
            reply: fallback,
            source: 'error_fallback'
        });
    }
});

// Serve static assets with html extension resolution
app.use(express.static(__dirname, {
    extensions: ['html', 'htm'],
    index: 'index.html'
}));

// Route fallback for 404 errors
app.use((req, res) => {
    res.status(404).sendFile(path.join(__dirname, '404.html'));
});

app.listen(PORT, HOST, () => {
    console.log(`DiginixIT server listening on http://${HOST}:${PORT}`);
    if (process.env.GROK_API_KEY || process.env.XAI_API_KEY) {
        console.log(`Grok AI configured in environment variables (${process.env.GROK_MODEL || 'grok-beta'})`);
    } else {
        console.log(`Note: GROK_API_KEY not found in environment variables. Set GROK_API_KEY in .env to enable live xAI completions.`);
    }
});
