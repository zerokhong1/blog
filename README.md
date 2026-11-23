# zerokhong1.github.io

Source of my blog: SLAM, Gaussian splatting and 4D reconstruction, derived on paper and checked in code. Built with [Quarto](https://quarto.org) and published to GitHub Pages by GitHub Actions.

## One-time setup

1. Create an empty public repository named `zerokhong1.github.io` on GitHub.
2. Push this folder:

   ```bash
   git init -b main
   git add .
   git commit -m "Blog skeleton"
   git remote add origin https://github.com/zerokhong1/zerokhong1.github.io.git
   git push -u origin main
   ```

3. On GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. The workflow in `.github/workflows/publish.yml` runs on every push to `main`. The site appears at <https://zerokhong1.github.io>. If the first run failed at the deploy step because Pages was not enabled yet, open **Actions → Publish site → Run workflow**.

## Write a post

Install [Quarto](https://quarto.org/docs/get-started/) once. Posts with Python cells also need `pip install jupyter numpy matplotlib` on your machine.

1. Copy `_templates/post.qmd` to `posts/YYYY-MM-DD-short-slug/index.qmd`.
2. Preview while writing:

   ```bash
   quarto preview
   ```

3. When it is ready, set `draft: false` and render that post on its own:

   ```bash
   quarto render posts/YYYY-MM-DD-short-slug/index.qmd
   ```

   Rendering a single file always runs its code and saves the results in `_freeze/`. A plain `quarto render` does not: posts use `freeze: true`, so it reuses old results and the numbers on the site can go stale. Do this again after every change to a post's code.
4. Commit `posts/…` **and** `_freeze/`, then push. CI never runs your code; it reuses `_freeze/`.

`draft: true` only blanks the page on the site. This repository is public, so anyone can still read a pushed draft's source. Commit a post only when it is ready to publish, and keep anything that touches unpublished work out of git until it is cleared.

## Layout

```
_quarto.yml          site settings (title, navbar, theme, KaTeX math)
index.qmd            post listing and RSS feed
about.qmd            about page
posts/_metadata.yml  defaults for every post (author, freeze, licence)
posts/<date-slug>/   one folder per post
_templates/post.qmd  post template (never rendered)
styles.css           small style tweaks
```

## Licence

Text: CC BY 4.0. Code snippets: MIT, unless a post says otherwise.
