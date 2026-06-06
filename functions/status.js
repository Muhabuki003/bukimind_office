/**
 * BUKIMIND Status Proxy
 * Fetches status.json from GitHub and returns with no-cache headers.
 * This avoids GitHub's 5-minute CDN cache on raw.githubusercontent.com.
 */
export async function onRequest(context) {
  const url = 'https://raw.githubusercontent.com/Muhabuki003/bukimind-status/main/status.json';

  const response = await fetch(url);
  const body = await response.text();

  return new Response(body, {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0',
      'Pragma': 'no-cache',
      'Expires': '0',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
