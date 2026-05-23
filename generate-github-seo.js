const fs = require('fs');
const path = require('path');

const outputDir = 'C:\\Users\\Gary\\github-cctv-seo';

const urls = fs.readFileSync('C:\\Users\\Gary\\published-urls.txt', 'utf8')
    .split('\n')
    .map(line => {
        const parts = line.split(' - ');
        return parts.length === 2 ? { title: parts[0].trim(), url: parts[1].trim() } : null;
    })
    .filter(Boolean);

// Unique URLs only
const uniqueUrls = Array.from(new Map(urls.map(item => [item.url, item])).values());

const css = `
body { font-family: 'Inter', sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; }
h1, h2, h3 { color: #0056b3; }
.hub-article { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; }
a { color: #0056b3; text-decoration: none; font-weight: bold; }
a:hover { text-decoration: underline; }
.cta { display: block; width: max-content; margin: 20px 0; padding: 10px 20px; background: #28a745; color: white; border-radius: 5px; }
`;

fs.writeFileSync(path.join(outputDir, 'style.css'), css);

const pages = [
    {
        filename: 'index.html',
        title: 'Top 10 CCTV Installers in the UK 2026',
        h1: 'The Ultimate Guide to CCTV Security in 2026',
        content: `
            <p>Welcome to the ultimate hub for understanding modern CCTV systems in the UK. With rising crime rates and falling hardware costs, there has never been a better time to invest in a robust security system.</p>
            <h2>Why Upgrade in 2026?</h2>
            <p>Modern systems offer AI-powered human detection, full-color night vision, and seamless smartphone integration. But before you install, you must understand the <a href="${uniqueUrls[Math.floor(Math.random()*uniqueUrls.length)].url}">legal requirements for home CCTV</a>.</p>
            <h2>Wired vs Wireless</h2>
            <p>One of the biggest debates is <a href="${uniqueUrls[Math.floor(Math.random()*uniqueUrls.length)].url}">wired vs wireless CCTV</a>. For the unpredictable UK weather, hardwired PoE systems always win out on reliability.</p>
        `
    },
    {
        filename: 'cctv-planning-permission.html',
        title: 'CCTV Planning Permission: What You Need to Know',
        h1: 'Do You Need Planning Permission for CCTV?',
        content: `
            <p>A common question among homeowners is whether they need local council approval to put up cameras. Generally, the answer is no, provided you follow the rules.</p>
            <p>However, if you live in a listed building or a conservation area, the rules are drastically different. For a comprehensive breakdown, check out this guide on <a href="${uniqueUrls[Math.floor(Math.random()*uniqueUrls.length)].url}">CCTV planning permission in the UK</a>.</p>
        `
    },
    {
        filename: 'night-vision-technology.html',
        title: 'ColorVu Night Vision: The New Standard',
        h1: 'How Night Vision Technology is Changing',
        content: `
            <p>Gone are the days of grainy, black-and-white infrared footage. In 2026, technologies like Hikvision's ColorVu are making full-color night vision the standard.</p>
            <p>If you want to understand how these f/1.0 aperture lenses work, read this deep dive into <a href="${uniqueUrls[Math.floor(Math.random()*uniqueUrls.length)].url}">Night Vision CCTV technology</a>.</p>
        `
    }
];

pages.forEach(page => {
    const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${page.title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hub-article">
        <h1>${page.h1}</h1>
        ${page.content}
        <br>
        <h3>Related Resources</h3>
        <ul>
            ${uniqueUrls.slice(0, 5).map(u => `<li><a href="${u.url}">${u.title}</a></li>`).join('\n')}
        </ul>
    </div>
</body>
</html>
    `;
    fs.writeFileSync(path.join(outputDir, page.filename), html.trim());
});

console.log("Successfully generated GitHub SEO pages with backlinks.");
