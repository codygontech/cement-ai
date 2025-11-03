# Documentation Deployment Guide

How to deploy the JK Cement AI documentation to various hosting platforms.

---

## 🌐 Deployment Options

### Option 1: Netlify (Recommended for Static Sites) ⭐
- **Best For**: Quick deployment, custom domains, free SSL
- **Effort**: Minimal
- **Cost**: Free tier available

### Option 2: GitHub Pages
- **Best For**: GitHub integration, simple setup
- **Effort**: Minimal
- **Cost**: Free

### Option 3: Vercel
- **Best For**: Next.js sites, fast deployments
- **Effort**: Minimal
- **Cost**: Free tier available

### Option 4: ReadTheDocs
- **Best For**: Technical documentation, versioning
- **Effort**: Moderate
- **Cost**: Free for open source

### Option 5: MkDocs + Netlify/Vercel
- **Best For**: Beautiful themed documentation
- **Effort**: Moderate
- **Cost**: Free

---

## 🚀 Option 1: Deploy to Netlify (Simplest)

### Method A: Direct Markdown Deployment

**Step 1: Create `index.html`**

Create a simple index that redirects to your README:

```html
<!-- docs-wiki/index.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=/README.html">
    <title>JK Cement AI Documentation</title>
</head>
<body>
    <p>Redirecting to <a href="/README.html">documentation</a>...</p>
</body>
</html>
```

**Step 2: Create `netlify.toml`**

```toml
# docs-wiki/netlify.toml
[build]
  publish = "."
  command = "echo 'No build needed'"

[[redirects]]
  from = "/"
  to = "/README.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
```

**Step 3: Deploy to Netlify**

**Via Netlify CLI:**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd docs-wiki
netlify deploy --prod
```

**Via Netlify Web UI:**
1. Go to https://app.netlify.com/
2. Click "Add new site" → "Import an existing project"
3. Connect to your Git repository
4. Set build settings:
   - Base directory: `docs-wiki`
   - Build command: `echo 'No build needed'`
   - Publish directory: `docs-wiki`
5. Click "Deploy site"

**Result:** Your docs will be live at `https://your-site-name.netlify.app`

---

### Method B: Use a Static Site Generator (Better UX)

Convert your Markdown to a beautiful static site using **Docsify**, **MkDocs**, or **Docusaurus**.

#### Using Docsify (Easiest)

**Step 1: Create `index.html`**

```html
<!-- docs-wiki/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>JK Cement AI Documentation</title>
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="description" content="JK Cement AI Optimization System Documentation">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: 'JK Cement AI Docs',
      repo: 'https://github.com/codygontech/cement-ai',
      loadSidebar: true,
      subMaxLevel: 2,
      search: 'auto',
      search: {
        placeholder: 'Search documentation...',
        noData: 'No results found',
        depth: 3
      },
      coverpage: false,
      onlyCover: false,
      auto2top: true,
      themeColor: '#4285F4'
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify/lib/plugins/search.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-bash.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-python.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-typescript.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-json.min.js"></script>
</body>
</html>
```

**Step 2: Create `_sidebar.md`**

```markdown
<!-- docs-wiki/_sidebar.md -->
* [Home](/)
* [Documentation Index](INDEX.md)

* Getting Started
  * [Quick Start](getting-started/quick-start.md)
  * [Architecture](getting-started/architecture.md)

* Backend
  * [API Reference](backend/api-reference.md)

* Features
  * [AI Chat System](features/ai-chat.md)

* Deployment
  * [Overview](deployment/overview.md)

* Development
  * [Setup](development/setup.md)

* Reference
  * [Environment Variables](reference/environment-variables.md)
```

**Step 3: Create `.nojekyll`**

```bash
touch docs-wiki/.nojekyll
```

**Step 4: Deploy to Netlify**

```bash
cd docs-wiki
netlify deploy --prod
```

**Result:** Beautiful, searchable documentation at `https://your-site-name.netlify.app`

---

#### Using MkDocs (Most Professional)

**Step 1: Install MkDocs**

```bash
pip install mkdocs mkdocs-material
```

**Step 2: Create `mkdocs.yml`**

```yaml
# docs-wiki/mkdocs.yml
site_name: JK Cement AI Documentation
site_url: https://your-site-name.netlify.app
site_description: Complete documentation for JK Cement AI Optimization System
site_author: JK Cement Team
repo_url: https://github.com/codygontech/cement-ai
repo_name: cement-ai

theme:
  name: material
  palette:
    primary: blue
    accent: orange
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight
    - content.code.copy
  icon:
    repo: fontawesome/brands/github

nav:
  - Home: README.md
  - Index: INDEX.md
  - Getting Started:
      - Quick Start: getting-started/quick-start.md
      - Architecture: getting-started/architecture.md
  - Backend:
      - API Reference: backend/api-reference.md
  - Features:
      - AI Chat System: features/ai-chat.md
  - Deployment:
      - Overview: deployment/overview.md
  - Development:
      - Setup: development/setup.md
  - Reference:
      - Environment Variables: reference/environment-variables.md

markdown_extensions:
  - admonition
  - codehilite
  - meta
  - toc:
      permalink: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

plugins:
  - search
  - git-revision-date-localized

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/codygontech/cement-ai
```

**Step 3: Create `netlify.toml`**

```toml
# docs-wiki/netlify.toml
[build]
  publish = "site"
  command = "pip install mkdocs-material && mkdocs build"

[build.environment]
  PYTHON_VERSION = "3.11"
```

**Step 4: Create `requirements.txt`**

```txt
# docs-wiki/requirements.txt
mkdocs>=1.5.0
mkdocs-material>=9.0.0
```

**Step 5: Deploy**

Push to GitHub and connect to Netlify, or use CLI:

```bash
mkdocs build
netlify deploy --prod --dir=site
```

**Result:** Professional documentation site with Material Design theme

---

## 🎨 Option 2: GitHub Pages

### Quick Deploy

**Step 1: Create `docs` branch or use `docs/` folder**

```bash
# Option A: Use docs folder in main branch
mkdir -p docs
cp -r docs-wiki/* docs/

# Option B: Create gh-pages branch
git checkout -b gh-pages
# Keep only docs-wiki content
```

**Step 2: Enable GitHub Pages**

1. Go to repository Settings → Pages
2. Select source: `gh-pages` branch or `main` branch `/docs` folder
3. Click Save

**Step 3: Configure (if using custom domain)**

Create `CNAME` file:
```
docs.yourdomain.com
```

**Result:** Docs available at `https://username.github.io/repo-name/`

---

## ⚡ Option 3: Vercel

**Step 1: Install Vercel CLI**

```bash
npm install -g vercel
```

**Step 2: Deploy**

```bash
cd docs-wiki
vercel --prod
```

**Step 3: Configure `vercel.json` (optional)**

```json
{
  "version": 2,
  "public": true,
  "github": {
    "silent": true
  }
}
```

**Result:** Docs at `https://your-project.vercel.app`

---

## 📚 Option 4: ReadTheDocs

**Step 1: Create `.readthedocs.yaml`**

```yaml
# .readthedocs.yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

mkdocs:
  configuration: docs-wiki/mkdocs.yml

python:
  install:
    - requirements: docs-wiki/requirements.txt
```

**Step 2: Connect to ReadTheDocs**

1. Go to https://readthedocs.org/
2. Import repository
3. Build documentation

**Result:** Docs at `https://your-project.readthedocs.io`

---

## 🔧 Complete Netlify Setup (Recommended)

Here's a complete setup using Docsify for the best balance of simplicity and features:

### File Structure

```
docs-wiki/
├── index.html          # Docsify entry point
├── _sidebar.md         # Navigation sidebar
├── _navbar.md          # Top navigation (optional)
├── .nojekyll          # Disable Jekyll processing
├── netlify.toml       # Netlify configuration
├── README.md          # Homepage
├── INDEX.md           # Documentation index
├── getting-started/
├── backend/
├── features/
├── deployment/
├── development/
└── reference/
```

### Files to Create

**1. `index.html`** (Already shown above)

**2. `_navbar.md`**

```markdown
<!-- docs-wiki/_navbar.md -->
* [Home](/)
* [API Docs](backend/api-reference.md)
* [Quick Start](getting-started/quick-start.md)
* [GitHub](https://github.com/codygontech/cement-ai)
```

**3. `.nojekyll`**

```bash
touch docs-wiki/.nojekyll
```

**4. `netlify.toml`**

```toml
[build]
  publish = "."
  command = "echo 'Static site - no build needed'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Deploy

```bash
cd docs-wiki

# Deploy to Netlify
netlify deploy --prod

# Or link to Git and auto-deploy
netlify init
```

---

## 🎯 Recommended Setup

For your use case, I recommend:

### **Option 1: Docsify + Netlify** (Fastest)

**Pros:**
- ✅ No build step needed
- ✅ Beautiful UI out of the box
- ✅ Full-text search
- ✅ Live updates (no rebuild)
- ✅ Free hosting
- ✅ Custom domain support

**Setup Time:** 10 minutes

**Steps:**
1. Add `index.html` with Docsify
2. Add `_sidebar.md`
3. Add `.nojekyll`
4. Deploy with `netlify deploy`

### **Option 2: MkDocs Material + Netlify** (Most Professional)

**Pros:**
- ✅ Professional appearance
- ✅ Best navigation
- ✅ Search functionality
- ✅ Version control
- ✅ Mobile responsive

**Setup Time:** 20 minutes

**Steps:**
1. Install MkDocs Material
2. Create `mkdocs.yml`
3. Configure `netlify.toml` with build
4. Deploy

---

## 🚀 Quick Start Commands

### Deploy with Netlify (Manual)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Navigate to docs
cd docs-wiki

# Deploy
netlify deploy --prod
```

### Deploy with Netlify (Git)

```bash
# Initialize Git if not already
git init
git add .
git commit -m "Add documentation"

# Push to GitHub
git remote add origin https://github.com/yourusername/cement-docs.git
git push -u origin main

# Connect on Netlify web UI
# https://app.netlify.com/start
```

---

## 🌐 Custom Domain Setup

### On Netlify

1. Go to Site Settings → Domain Management
2. Add custom domain: `docs.yourdomain.com`
3. Follow DNS configuration instructions
4. SSL certificate auto-provisioned

### DNS Configuration (Example)

Add CNAME record:
```
docs.yourdomain.com → your-site.netlify.app
```

---

## 📊 Comparison Table

| Platform | Setup | Cost | Features | Best For |
|----------|-------|------|----------|----------|
| **Netlify** | ⭐⭐⭐⭐⭐ | Free | Auto-deploy, SSL, CDN | Most projects |
| **GitHub Pages** | ⭐⭐⭐⭐ | Free | Git integration | GitHub projects |
| **Vercel** | ⭐⭐⭐⭐⭐ | Free | Fast, auto-deploy | Next.js/React |
| **ReadTheDocs** | ⭐⭐⭐ | Free | Versioning, themes | OSS projects |
| **MkDocs** | ⭐⭐⭐ | Free | Beautiful, powerful | Technical docs |

---

## 🎨 Enhancing Your Docs

### Add Search

Docsify has built-in search. For MkDocs:

```yaml
plugins:
  - search:
      lang: en
```

### Add Analytics

Add to `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

### Add Custom CSS

Create `custom.css`:

```css
/* docs-wiki/custom.css */
:root {
  --theme-color: #4285F4;
  --code-theme-background: #f6f8fa;
}

.sidebar {
  border-right: 1px solid #eee;
}

.markdown-section code {
  font-size: 0.9em;
}
```

Link in `index.html`:
```html
<link rel="stylesheet" href="/custom.css">
```

---

## ✅ Final Checklist

Before deploying:

- [ ] Test all links work locally
- [ ] Images load correctly
- [ ] Code blocks are formatted
- [ ] Navigation is intuitive
- [ ] Mobile responsive
- [ ] Search works
- [ ] No broken links
- [ ] Custom domain configured (if needed)
- [ ] Analytics added (if needed)
- [ ] SSL certificate active

---

## 🆘 Troubleshooting

### Links Not Working

**Problem:** Relative links broken  
**Solution:** Use absolute paths from root: `/getting-started/quick-start.md`

### Images Not Loading

**Problem:** Image paths incorrect  
**Solution:** Place images in `/images/` folder, reference as `/images/pic.png`

### 404 Errors

**Problem:** Direct URL access fails  
**Solution:** Add redirect rule in `netlify.toml`:
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

---

## 📞 Need Help?

- **Netlify Docs**: https://docs.netlify.com/
- **Docsify Guide**: https://docsify.js.org/
- **MkDocs Guide**: https://www.mkdocs.org/

---

**Ready to deploy?** Let's go with Docsify + Netlify for the easiest setup! 🚀
