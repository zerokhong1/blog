# blog

[![Publish site](https://github.com/zerokhong1/blog/actions/workflows/publish.yml/badge.svg)](https://github.com/zerokhong1/blog/actions/workflows/publish.yml)

Source of <https://zerokhong1.github.io/blog/>, my notes on learning SLAM with 3D Gaussian Splatting: one question per post, derived on paper and checked in code. Built with [Quarto](https://quarto.org) and published to GitHub Pages by GitHub Actions.

## Quick start

Install [Quarto](https://quarto.org/docs/get-started/). Posts with Python cells also need `pip install jupyter numpy matplotlib`.

```bash
git clone https://github.com/zerokhong1/blog.git
cd blog
quarto preview        # live preview in the browser, reloads on save
```

## Write a post

1. Start from the template:

   ```bash
   mkdir posts/YYYY-MM-DD-short-slug
   cp _templates/post.qmd posts/YYYY-MM-DD-short-slug/index.qmd
   ```

   The template shows the conventions for math, equation labels, figures and captions.
2. Fill in `title`, `description`, `date` and `categories`. Keep `draft: true` while writing and run `quarto preview`.
3. When it is ready, set `draft: false` and render that post on its own, so its code runs and the results are stored in `_freeze/`:

   ```bash
   quarto render posts/YYYY-MM-DD-short-slug/index.qmd
   ```

4. Commit the post folder **and** `_freeze/`, then push to `main`. The site updates a minute or two later.

### Before you publish

- [ ] One question, answered in this order: derivation, then code that matches a reference implementation with the numbers printed, then what is still open.
- [ ] 1,200–2,500 words and at least one figure, with a caption that says what to look at.
- [ ] Every figure, equation and code snippet taken from a course or paper is credited where it appears and listed in References. MIT OpenCourseWare material is CC BY-NC-SA, which this site's CC BY 4.0 does not cover: keep the credit and name that licence in the caption.
- [ ] Nothing unpublished: no results or ideas from ongoing work.
- [ ] The template's HTML comments are deleted. They are invisible on the page but stay in its HTML source.
- [ ] The post was rendered on its own after the last code change, and `_freeze/` is committed.

## How publishing works

- Every push to `main` runs [`.github/workflows/publish.yml`](.github/workflows/publish.yml): Quarto renders the site and the result is deployed to GitHub Pages (**Settings → Pages → Build and deployment → Source: GitHub Actions**). To publish again without a new commit, open **Actions → Publish site → Run workflow**.
- Posts use `freeze: true` (set in `posts/_metadata.yml`), so CI never runs Python; it reuses the results stored in `_freeze/`. A plain `quarto render` reuses them too, so the numbers on the site go stale unless you render the changed post on its own.
- `draft: true` only hides a post on the site. This repository is public, so anyone can read a pushed draft on GitHub. Commit a post only when it is ready to go out.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Deploy fails with "Ensure GitHub Pages has been enabled" | Set the Pages source to GitHub Actions (see above), then re-run the workflow. |
| Render fails in CI with a Jupyter or Python error | The post's results are missing from `_freeze/`. Render the post locally and commit `_freeze/`. |
| Numbers on the site don't match the code | Render the post on its own and commit `_freeze/`. |
| `git push` is rejected as non-fast-forward | The remote has commits you don't have yet, for example from another machine. Run `git pull --rebase`, then push. |

## Layout

```
_quarto.yml          site settings: title, navbar, theme, KaTeX math
index.qmd            post listing and RSS feed (index.xml)
about.qmd            About page
posts/_metadata.yml  defaults for every post: author, freeze, table of contents, licence
posts/<date-slug>/   one folder per post: index.qmd and its figures
_templates/post.qmd  post template; files and folders starting with "_" are never rendered
_freeze/             stored code results, created by the first render of a post with code
styles.css           small style tweaks
.github/workflows/   publish workflow
```

## Licence

Text: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code snippets: MIT, unless a post says otherwise. Material from other sources keeps its own licence and is credited where it appears.
