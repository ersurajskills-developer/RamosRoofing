const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;

const redirects = {
  '/about': '/about.html',
  '/before-after': '/before-after.html',
  '/reviews': '/reviews.html'
};

const server = http.createServer((req, res) => {
  // Parse URL path (ignoring query strings)
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  let urlPath = parsedUrl.pathname;

  // 1. Check direct netlify redirects
  if (redirects[urlPath]) {
    urlPath = redirects[urlPath];
  }

  // 2. Resolve final filesystem path
  let filePath = path.join(__dirname, urlPath);

  // If path ends with / or has no extension, and we can find a matching file
  fs.stat(filePath, (err, stats) => {
    if (!err && stats.isDirectory()) {
      // Check for index.html in directory
      const indexFilePath = path.join(filePath, 'index.html');
      serveFile(indexFilePath, res);
    } else {
      // Check if file exists as-is
      fs.access(filePath, fs.constants.F_OK, (errAsIs) => {
        if (!errAsIs) {
          serveFile(filePath, res);
        } else {
          // Check pretty URL: append .html and see if it exists
          const htmlFilePath = filePath + '.html';
          fs.access(htmlFilePath, fs.constants.F_OK, (errHtml) => {
            if (!errHtml) {
              serveFile(htmlFilePath, res);
            } else {
              // Not found, serve 404
              serve404(res);
            }
          });
        }
      });
    }
  });
});

function serveFile(filePath, res) {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.webp': 'image/webp',
    '.mp4': 'video/mp4',
    '.webm': 'video/webm',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.pdf': 'application/pdf'
  };

  const contentType = mimeTypes[ext] || 'application/octet-stream';

  fs.readFile(filePath, (error, content) => {
    if (error) {
      res.writeHead(500);
      res.end(`Server Error: ${error.code}`);
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
}

function serve404(res) {
  const default404Path = path.join(__dirname, '404.html');
  fs.access(default404Path, fs.constants.F_OK, (err) => {
    if (!err) {
      fs.readFile(default404Path, (error, content) => {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end(content, 'utf-8');
      });
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
    }
  });
}

server.listen(PORT, () => {
  console.log(`Serving local site at: http://localhost:${PORT}`);
});
