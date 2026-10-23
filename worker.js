export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      
      // 1. Attempt to fetch the static asset first
      let response = await env.ASSETS.fetch(request);
      
      // 2. If not found (404) and the path is /blog/*
      if (response.status === 404 && url.pathname.startsWith('/blog/')) {
        const slug = url.pathname.replace(/^\/blog\//, '').replace(/\.html$/, '').replace(/\/$/, '');
        if (slug && slug !== 'blog' && slug !== 'index') {
          // Fetch article.html directly without query params so env.ASSETS matches the physical file
          const articleUrl = new URL('/article.html', request.url);
          const articleRes = await env.ASSETS.fetch(new Request(articleUrl.toString()));
          if (articleRes.status === 200) {
            // Clone or return response directly with 200 OK
            const newHeaders = new Headers(articleRes.headers);
            newHeaders.set('content-type', 'text/html; charset=utf-8');
            return new Response(articleRes.body, {
              status: 200,
              headers: newHeaders
            });
          }
        }
      }
      
      return response;
    } catch (err) {
      return new Response(`Worker error: ${err.message}\n${err.stack}`, {
        status: 500,
        headers: { 'content-type': 'text/plain' }
      });
    }
  }
};