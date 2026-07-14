const fs = require('fs');
const path = require('path');

const indexContent = fs.readFileSync('index.html', 'utf8');
const footerMatch = indexContent.match(/<footer class="main-footer">[\s\S]*?<\/footer>/);

if (!footerMatch) {
    console.error("Could not find footer in index.html");
    process.exit(1);
}

const baseFooter = footerMatch[0];

function adjustFooterForDepth(footerHtml, depth) {
    if (depth === 0) {
        return footerHtml;
    }
    
    const prefix = '../'.repeat(depth);
    
    let adjusted = footerHtml.replace(/href="([^"]+)"/g, (match, url) => {
        if (url.startsWith('http') || url.startsWith('tel:') || url.startsWith('mailto:') || url.startsWith('#') || url.startsWith('/')) {
            return `href="${url}"`;
        }
        return `href="${prefix}${url}"`;
    });

    adjusted = adjusted.replace(/src="([^"]+)"/g, (match, url) => {
        if (url.startsWith('http') || url.startsWith('tel:') || url.startsWith('mailto:') || url.startsWith('#') || url.startsWith('/')) {
            return `src="${url}"`;
        }
        return `src="${prefix}${url}"`;
    });
    
    return adjusted;
}

function walk(dir, callback) {
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        const filepath = path.join(dir, file);
        const stat = fs.statSync(filepath);
        if (stat && stat.isDirectory()) {
            if (file !== '.git' && file !== 'node_modules') {
                walk(filepath, callback);
            }
        } else {
            callback(filepath);
        }
    });
}

function processFiles(directory) {
    walk(directory, (filepath) => {
        if (filepath.endsWith('.html') && path.basename(filepath) !== 'index.html') {
            const relPath = path.relative(directory, filepath);
            const depth = (relPath.match(/[\\/]/g) || []).length;
            
            let content = fs.readFileSync(filepath, 'utf8');
            const newFooter = adjustFooterForDepth(baseFooter, depth);
            const newContent = content.replace(/<footer[^>]*>[\s\S]*?<\/footer>/, newFooter);
            
            if (content !== newContent) {
                fs.writeFileSync(filepath, newContent, 'utf8');
                console.log(`Updated footer in: ${relPath}`);
            }
        }
    });
}

processFiles('.');
