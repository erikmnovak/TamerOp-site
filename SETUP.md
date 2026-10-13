# Moving publication to TamerOp-site

The website and library are independent repositories. Their local directories
remain adjacent for convenience; `TAMEROP_SOURCE` selects any other library
checkout explicitly. The website build records both repositories and verifies
which TamerOp checkout Julia loads.

## Before assigning the domain

1. Publish the prepared website sources to `erikmnovak/TamerOp-site` and the
   corresponding removal of website sources from `erikmnovak/TamerOp.jl`.
   Keep the library's mathematical fixtures and visualization contract under
   `test/`. Its package tests must work without the website directory.
2. In the new repository, open **Settings → Pages** and select **GitHub Actions**
   as the build source. The repository already supplies the workflow; GitHub
   does not need to generate another one.
3. Let the Documentation workflow build and deploy. Check its temporary
   `https://erikmnovak.github.io/TamerOp-site/` address, including a nested page,
   an image, search and a notebook download. Keep the existing domain attached
   to the old site until this succeeds.

## Assign tamerop.com

In the old repository's **Settings → Pages**, remove its custom domain.
Immediately open **Settings → Pages** in `TamerOp-site`, set **Custom domain**
to `tamerop.com`, and save. Keep the domain with the same GitHub account.
Because the account and GitHub Pages hosting service are unchanged, the
existing DNS records normally remain appropriate; check GitHub's DNS result
before changing records at the domain registrar.

Enable **Enforce HTTPS** when GitHub makes the option available. Verify the
homepage, a nested article and a downloadable notebook through
`https://tamerop.com/`, then check the revision record at
`https://tamerop.com/downloads/publication.json`. Certificate provisioning and
domain activation may take time. See GitHub's
[custom domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

The old library Documentation workflow is removed by this migration. Keep its
last deployment available until the new site is verified; removing source
files alone does not require first deleting the old Pages site.

## Later changes

Website pushes build in this repository. A scheduled check looks for a new
library `main` twice an hour and builds when the published revision differs.
For an immediate update after a library push, run the Documentation workflow
manually. This arrangement uses each repository's ordinary workflow token and
does not require a persistent token shared between projects.

Installing TamerOp uses the library repository. Website sources, assets,
build tools and notebooks are absent from future registered library source
trees after the removal is published. Existing registered releases retain
their original contents.
