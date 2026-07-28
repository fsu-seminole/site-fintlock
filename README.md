# Fintlock marketing website

Production website for Fintlock, deployed to `https://fintlock.com` through GitHub Pages.
The site uses plain HTML, CSS, and JavaScript with no build step.

## Current approved site

The owner approved the current homepage on July 28, 2026.

- `index.html` is the canonical production homepage.
- `homepage.css` contains the approved homepage-specific styling.
- `styles.css` and `app.js` provide the shared site system.
- `work.html` features Plants in Pocket and Fintley.
- `contact.html` provides one direct email path without presenting a non-submitting web form.
- `services.html` and `privacy.html` provide the remaining supporting pages.
- `assets/` contains the approved brand and product artwork.

The approved homepage originated as `GPT Design/index-test.html` in the private local design
workspace. It was productionized before release. No file with `test` in its name is part of
the public site.

See `HANDOFF.md` for the release record and maintenance notes.

## Deployment

GitHub Pages publishes the `main` branch to `fintlock.com`. A change merged into `main`
can update the live site.

- Preserve `CNAME`, `robots.txt`, and `sitemap.xml`.
- Test changes on a branch before merging.
- Confirm the Pages deployment succeeds after a merge.
- Spot-check the live homepage and navigation after deployment.

## Content constraints

- Use official Fintlock assets only.
- Do not add fabricated statistics, testimonials, clients, or results.
- Do not use em dashes, emojis, or buzzword filler in site copy.
- Keep claims specific and supportable.
