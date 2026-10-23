export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // 1. Attempt to fetch the static asset first
    let response = await env.ASSETS.fetch(request);
    
    // 2. If not found (404) and the path is /blog/*
    if (response.status === 404 && url.pathname.startsWith('/blog/')) {
      const slug = url.pathname.replace(/^\/blog\//, '').replace(/\.html$/, '').replace(/\/$/, '');
      if (slug && slug !== 'blog' && slug !== 'index') {
        // Fetch article.html and serve it with HTTP 200 directly
        const articleUrl = new URL('/article.html', request.url);
        articleUrl.searchParams.set('slug', slug);
        const articleRes = await env.ASSETS.fetch(new Request(articleUrl.toString(), request));
        if (articleRes.status === 200) {
          return new Response(articleRes.body, {
            status: 200,
            headers: articleRes.headers
          });
        }
      }
    }
    
    return response;
  }
};