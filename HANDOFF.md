# Fintlock production handoff

**Owner approval date:** July 28, 2026

**Production homepage:** `index.html`

**Live domain:** `https://fintlock.com`

**Deployment branch:** `main`

## Current source of truth

The repository-root `index.html` is the production version of the owner-approved homepage.
It was promoted from the private local design source `GPT Design/index-test.html`.

The production file has already been prepared for public release:

- Temporary `noindex,nofollow` metadata was removed.
- Test-only homepage and contact links were replaced with production links.
- The homepage canonical and Open Graph URLs point to `https://fintlock.com/`.
- The test stylesheet was promoted as `homepage.css`.
- No public filename or internal link contains `test`.

Future production edits should be made against the root website files on a branch. Do not
upload the private design workspace or reintroduce `index-test.html` as a public page.

## Site files

| File | Purpose |
| --- | --- |
| `index.html` | Owner-approved production homepage. |
| `homepage.css` | Homepage-specific approved styling. |
| `styles.css` | Shared site styles. |
| `app.js` | Shared navigation, motion, footer, and contact behavior. |
| `work.html` | Products and selected work. |
| `services.html` | Software and technology-integration services. |
| `contact.html` | Contact page using the visitor's email application. |
| `privacy.html` | Privacy notice. |
| `assets/` | Approved brand and product artwork. |
| `CNAME` | GitHub Pages custom-domain configuration. |
| `robots.txt` | Search crawler rules. |
| `sitemap.xml` | Production page index. |

## Release checks

- Verify the homepage at desktop and mobile sizes.
- Verify Work, Services, Contact, and Privacy navigation.
- Verify product images, wordmarks, favicon, and social-card assets.
- Confirm the production homepage does not contain `noindex,nofollow`.
- Preserve `CNAME`, `robots.txt`, and `sitemap.xml`.
- Confirm the GitHub Pages deployment succeeds and spot-check `https://fintlock.com`.
