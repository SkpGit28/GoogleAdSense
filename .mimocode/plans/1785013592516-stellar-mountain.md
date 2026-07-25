# E-E-A-T Upgrade Plan for HotelGlobe (20 Articles)

## Overview
Upgrade all 20 static HTML hotel articles to demonstrate Google's E-E-A-T standards with author cards, methodology blocks, first-person content, pros/cons, JSON-LD schema, Open Graph tags, and trust badges.

---

## 1. Author Personas

| Author | Title | Photo (Unsplash) | Articles |
|--------|-------|-------------------|----------|
| **Mr. Lee** | Founder & Lead Travel Editor | `photo-1507003211169-0a1dd7228f2d` | 6: NYC, Dubai, Singapore, Unique Hotels, Tokyo, Switzerland |
| **Elena Rostova** | Independent Hotel Critic & Luxury Travel Writer | `photo-1494790108377-be9c29b29330` | 6: Paris, Thailand, Rome, Europe Historic, Santorini, London |
| **James Whitfield** | Budget Travel Expert & Hotel Value Analyst | `photo-1472099645785-5658abf4ff4e` | 4: Caribbean, Orlando, Las Vegas, Mexico |
| **Sofia Mendez** | Adventure & Eco-Travel Correspondent | `photo-1438761681033-6461ffad8d80` | 4: Sydney, Maldives, Costa Rica, Bali |

---

## 2. Files to Modify (24 total)

| File | Change |
|------|--------|
| `css/style.css` | Append ~220 lines of new E-E-A-T component styles |
| `js/main.js` | Add ~10 lines: `toggleMethodology()` function |
| 20 article HTML files in `articles/` | Full rewrite: head, author card, methodology, content, schema |
| `sitemap.xml` | Update `<lastmod>` dates for all 20 articles |
| `about.html` | Add "Our Team" section with 4 author bios |

---

## 3. Implementation Phases

### Phase 1: CSS Foundation (`css/style.css`)
Add to `:root`:
```css
--author-bg: #f8f9fa; --badge-verified: #0d6efd; --badge-factcheck: #198754;
--pros-color: #198754; --cons-color: #dc3545; --methodology-bg: #f0f4ff;
```

New selectors: `.author-card`, `.author-card__photo`, `.author-card__info`, `.author-card__name`, `.author-card__title`, `.author-card__bio`, `.author-card__meta`, `.badge--verified`, `.badge--factcheck`, `.methodology-box`, `.methodology-box__header`, `.methodology-box__content`, `.hotel-review-card`, `.pros-cons`, `.pros-cons__section`, `.article-image`, `.article-meta-bar`

Responsive overrides at `max-width: 768px`: stack author card, stack pros/cons grid.

### Phase 2: JavaScript (`js/main.js`)
```js
function toggleMethodology(header) {
  var content = header.nextElementSibling;
  var toggle = header.querySelector('.methodology-box__toggle');
  content.classList.toggle('open');
  toggle.classList.toggle('open');
}
```

### Phase 3: Template Article (Paris)
Transform `best-hotels-paris.html` as the reference template:
1. Add `<link rel="canonical">`, Open Graph, Twitter Card meta tags in `<head>`
2. Add JSON-LD Article schema in `<head>`
3. Replace `.article-header .meta` with `.article-meta-bar` (Published, Last Updated, Fact-Checked badge)
4. Insert author card block after ad-top
5. Insert expandable methodology box
6. Rewrite all paragraphs in first-person voice with specific details
7. Wrap each hotel in `.hotel-review-card` with image, highlight box, pros/cons grid
8. Add Unsplash `<figure>` + `<figcaption>` images per hotel
9. Verify rendering in browser

### Phase 4: Batch Process Remaining 19 Articles
Apply same transformation pattern to each file. Process in batches of 4-5 by author assignment.

### Phase 5: Site-Wide Updates
- Update `sitemap.xml` `<lastmod>` dates to `2026-07-26`
- Add "Our Team" section to `about.html` with all 4 author bios

---

## 4. HTML Template Structure (per article)

```html
<head>
  <!-- canonical, OG, Twitter Card, JSON-LD Article schema -->
</head>
<body>
  <header> [UNCHANGED] </header>

  <div class="article-header">
    <h1>[Title]</h1>
    <div class="article-meta-bar">
      <span>Published: [Date]</span>
      <span>Last Updated: July 2026</span>
      <span class="badge badge--factcheck">Fact-Checked by [Editor]</span>
    </div>
  </div>

  <div class="content-layout">
    <div class="article-content">
      <div class="ad-slot ad-top"> [UNCHANGED] </div>

      <!-- AUTHOR CARD -->
      <div class="author-card">
        <img src="[Unsplash headshot]" alt="[Name]" class="author-card__photo">
        <div class="author-card__info">
          <div class="author-card__name">[Name]</div>
          <div class="author-card__title">[Title]</div>
          <div class="author-card__bio">[Bio]</div>
          <div class="author-card__meta">
            <span>Published: [Date]</span>
            <span>Last Updated: July 2026</span>
            <span class="badge badge--verified">Verified Stay</span>
          </div>
        </div>
      </div>

      <!-- METHODOLOGY BOX (expandable) -->
      <div class="methodology-box">
        <div class="methodology-box__header" onclick="toggleMethodology(this)">
          <h4>How We Review Hotels</h4>
          <span class="methodology-box__toggle">▼</span>
        </div>
        <div class="methodology-box__content">
          <!-- Evaluation criteria + affiliate disclosure -->
        </div>
      </div>

      <!-- FIRST-PERSON INTRO -->
      <p>During my stay in [month year], I...</p>

      <!-- HOTEL REVIEW CARD (repeated per hotel) -->
      <div class="hotel-review-card">
        <div class="hotel-review-card__header">
          <h3>1. [Hotel Name]</h3>
          <span class="badge badge--verified">Verified Stay</span>
        </div>
        <div class="hotel-review-card__body">
          <figure class="article-image">
            <img src="[Unsplash]" alt="[Alt]" loading="lazy">
            <figcaption>[First-person caption]</figcaption>
          </figure>
          <p>[First-person review with specifics]</p>
          <div class="highlight-box"> [Key Details list] </div>
          <div class="pros-cons">
            <div class="pros-cons__section pros--section">
              <h5>What I Liked</h5>
              <ul class="pros-cons__list"> [3-4 items] </ul>
            </div>
            <div class="pros-cons__section cons--section">
              <h5>What Could Be Better</h5>
              <ul class="pros-cons__list"> [2-3 items] </ul>
            </div>
          </div>
        </div>
      </div>

      <div class="ad-slot ad-in-content"> [UNCHANGED] </div>
      <!-- More hotel cards... -->

      <h2>Practical Tips</h2> <ul> [First-person tips] </ul>
      <h2>Final Thoughts</h2> <p> [First-person conclusion] </p>

      <div class="ad-slot ad-bottom"> [UNCHANGED] </div>
    </div>
    <aside class="sidebar"> [UNCHANGED] </aside>
  </div>

  <footer class="footer"> [UNCHANGED] </footer>
  <script src="../js/main.js"></script>
</body>
```

---

## 5. JSON-LD Schema (per article)

**Article schema** with `@type: "Article"`, author `Person` pointing to about.html, publisher `Organization` for HotelGlobe, `datePublished`, `dateModified`, `image`, `keywords`.

**Per-hotel schema** (3-5 per article) with `@type: "Hotel"`, `name`, `image`, `address`, `aggregateRating`, `review` with author and `reviewRating`.

---

## 6. Content Transformation Rules

- Convert ALL text from third-person to first-person ("I tested...", "During my stay...")
- Add specific details: room numbers, elevator wait times, breakfast rush hours, soundproofing quality, plug socket counts, water pressure
- Add neighborhood context: nearby coffee shops, metro lines, walkable distances
- Every hotel gets: Unsplash image with caption, highlight box with key details, pros/cons grid
- No generic promotional language — honest, balanced criticism required

---

## 7. Verification Checklist

After implementation:
- [ ] All 20 articles have author card with photo, name, title, bio, dates
- [ ] All 20 articles have methodology box that toggles open/close
- [ ] All 20 articles have pros/cons grids for every hotel listed
- [ ] All 20 articles have JSON-LD Article + Hotel/Review schema
- [ ] All 20 articles have Open Graph and Twitter Card meta tags
- [ ] All 20 articles have canonical URL tags
- [ ] All 20 articles have Unsplash images with captions
- [ ] Zero third-person encyclopedic text remains
- [ ] Footer links (Privacy, Terms, Disclaimer, About, Contact) accessible on all pages
- [ ] `sitemap.xml` dates updated
- [ ] `about.html` has "Our Team" section
- [ ] Mobile responsive at 375px width (author card stacks, pros/cons stack)
