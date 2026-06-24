const fs = require('fs');
const path = require('path');

const src = __dirname + '/..';
const dst = src + '/www';

// Clean and recreate www
if (fs.existsSync(dst)) {
  fs.rmSync(dst, { recursive: true, force: true });
}
fs.mkdirSync(dst, { recursive: true });

// Files to copy to www/
const files = [
  'card.html',
  'manifest.json',
  'sw.js',
  'back-yushi.png',
  'back-weimin.png',
  'icon-192.png',
  'icon-512.png'
];

files.forEach(function(f) {
  var from = src + '/' + f;
  var to = dst + '/' + f;
  if (fs.existsSync(from)) {
    fs.copyFileSync(from, to);
    console.log('Copied: ' + f);
  } else {
    console.log('Missing: ' + f);
  }
});

// Create index.html as redirect to card.html
var indexHtml = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta http-equiv="refresh" content="0;url=card.html">\n</head>\n<body></body>\n</html>\n';
fs.writeFileSync(dst + '/index.html', indexHtml);
console.log('Created: index.html (redirect)');

console.log('www/ prepared successfully.');
