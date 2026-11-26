# Wiki publishing

The root wiki/ directory is the single source for the GitHub Wiki and GitHub Pages documentation. These files are outside the Copier-rendered template.

## GitHub Wiki

Enable Wikis in repository settings and create the first Home page in the Wiki interface. Run the Publish wiki workflow. It calls the shared [wiki-publish.yml](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/wiki-publish.yml).

The workflow tries the job token by default. If it cannot write to the wiki, configure an authorized WIKI_TOKEN Actions secret. Never commit tokens.

Matching published pages are updated from source. Unrelated wiki pages are preserved. Removing a source Markdown file does not delete its published counterpart.

## Documentation website

Set Settings → Pages → Build and deployment → Source to GitHub Actions. Run the Documentation website workflow. It calls the shared [wiki-pages.yml](https://github.com/RuchirChawdhry/ci-workflows/blob/main/.github/workflows/wiki-pages.yml).

The shared workflow builds an Astro Starlight site, generates Markdown mirrors and machine-readable indexes, checks links and deploys to Pages on non-PR runs.

Expected website: [copier-kotlin-android](https://ruchirchawdhry.github.io/copier-kotlin-android/). The URL becomes usable after successful deployment.

## Editing

Use a single H1 at the start of each Markdown page. Use hyphenated ASCII filenames and relative wiki links. Update _Sidebar.md when adding pages; _Site.json enables the feature-card landing page. Edit the source files rather than published copies.

See the central [Wiki publishing guide](https://github.com/RuchirChawdhry/ci-workflows/blob/main/docs/wiki-publish.md) and [Wiki Pages guide](https://github.com/RuchirChawdhry/ci-workflows/blob/main/docs/wiki-pages.md).
