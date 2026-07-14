const fs = require('fs');
const path = require('path');

function getHomeHeader(indexPath) {
    const content = fs.readFileSync(indexPath, 'utf8');
    const pattern = /<div class="top-bar">[\s\S]*?<\/header>/;
    const match = content.match(pattern);
    if (match) {
        return match[0];
    } else {
        throw new Error("Could not find top-bar and header in index.html");
    }
}

function adjustLinksForSubdirectories(headerHtml) {
    headerHtml = headerHtml.replace(/href="index\.html"/g, 'href="../index.html"');
    headerHtml = headerHtml.replace(/href="about\.html"/g, 'href="../about.html"');
    headerHtml = headerHtml.replace(/href="before-after\.html"/g, 'href="../before-after.html"');
    headerHtml = headerHtml.replace(/href="reviews\.html"/g, 'href="../reviews.html"');
    
    headerHtml = headerHtml.replace(/href="services\//g, 'href="../services/');
    headerHtml = headerHtml.replace(/href="locations\//g, 'href="../locations/');
    headerHtml = headerHtml.replace(/href="resources\//g, 'href="../resources/');
    
    headerHtml = headerHtml.replace(/src="Images\//g, 'src="../Images/');
    headerHtml = headerHtml.replace(/src="images\//g, 'src="../images/');
    return headerHtml;
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
    const indexPath = path.join(directory, 'index.html');
    const homeHeader = getHomeHeader(indexPath);
    const subHeader = adjustLinksForSubdirectories(homeHeader);
    
    const headerPattern = /(<!-- Top Bar -->|<div class="top-bar">)[\s\S]*?<\/header>/;
    const altPattern = /<header[^>]*>[\s\S]*?<\/header>/;

    let count = 0;
    walk(directory, (filepath) => {
        if (path.extname(filepath) === '.html' && path.basename(filepath) !== 'index.html') {
            const relPath = path.relative(directory, filepath);
            const depth = (relPath.match(/[\\/]/g) || []).length;
            
            let content = fs.readFileSync(filepath, 'utf8');
            let match = content.match(headerPattern);
            if (!match) {
                match = content.match(altPattern);
            }
            
            if (match) {
                const headerToUse = depth === 0 ? homeHeader : subHeader;
                const newContent = content.slice(0, match.index) + headerToUse + content.slice(match.index + match[0].length);
                fs.writeFileSync(filepath, newContent, 'utf8');
                console.log(`Updated header in: ${relPath}`);
                count++;
            } else {
                console.log(`Could not find header in: ${relPath}`);
            }
        }
    });
    console.log(`Total files updated: ${count}`);
}

processFiles('.');
