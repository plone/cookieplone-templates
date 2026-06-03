
# Change log

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 20260320.1 (2026-03-20)


### Breaking changes:

- Use Python native namespaces @gforcada [#321](https://github.com/plone/cookieplone-templates/issues/321)


### New features:

- Add Cookieplone template `documentation_starter` scaffold. @ujsquared, @stevepiercy [#7](https://github.com/plone/cookieplone-templates/issues/7)
- Seven Frontend add-on for Plone template. @sneridagh [#128](https://github.com/plone/cookieplone-templates/issues/128)
- Add a template for Classic UI projects. @pbauer [#146](https://github.com/plone/cookieplone-templates/issues/146)
- Move all templates to be under /templates. @ericof [#176](https://github.com/plone/cookieplone-templates/issues/176)
- Add `it` to the list of available languages for a project @ericof [#183](https://github.com/plone/cookieplone-templates/issues/183)
- Add `se` to the list of available languages for a project @ericof [#184](https://github.com/plone/cookieplone-templates/issues/184)
- Support having 'hidden' templates in `cookiecutter.json` @ericof [#193](https://github.com/plone/cookieplone-templates/issues/193)
- Enhance `documentation_starter` template and add usage docs to root README. @stevepiercy [#201](https://github.com/plone/cookieplone-templates/issues/201)
- Add Read the Docs pull request preview GitHub workflow. @stevepiercy [#203](https://github.com/plone/cookieplone-templates/issues/203)
- Add documentation test workflow that builds checks for broken links, builds HTML documentation, and checks American English spelling, grammar, and syntax, and style guide. @stevepiercy [#204](https://github.com/plone/cookieplone-templates/issues/204)
- Improve grammar and wording. @pbauer [#241](https://github.com/plone/cookieplone-templates/issues/241)
- Add browser-module with jbot- and static-setup for classic addons and projects. @pbauer [#249](https://github.com/plone/cookieplone-templates/issues/249)
- Rename controlpanel folder to be controlpanels @erral [#261](https://github.com/plone/cookieplone-templates/issues/261)
- Reference zest.releaser to the file where the Python version is determined. Add make target "release". @erral @ksuess [#262](https://github.com/plone/cookieplone-templates/issues/262)
- Frontend: Support creation of scoped packages. @ericof [#270](https://github.com/plone/cookieplone-templates/issues/270)
- Frontend: Template now starts with Typescript and a config folder. @ericof [#271](https://github.com/plone/cookieplone-templates/issues/271)
- Update .vscode recommended extensions and settings for projects. @ericof [#273](https://github.com/plone/cookieplone-templates/issues/273)
- Hide the upgrades package from site-creation and quickinstaller @erral [#285](https://github.com/plone/cookieplone-templates/issues/285)
- Better TS support for the add-on setup deps and Cypress tests. @sneridagh [#302](https://github.com/plone/cookieplone-templates/issues/302)
- Babel preset in `.npmrc` compat for 19. @sneridagh [#309](https://github.com/plone/cookieplone-templates/issues/309)
- Implement five new sub-templates to generate GitHub CI configuration:
   - `ci_gh_backend_addon`
   - `ci_gh_frontend_addon`
   - `ci_gh_monorepo_addon`
   - `ci_gh_project`
   - `ci_gh_classic_project`

   These sub-templates are now used by the other templates to add the GitHub CI features to their codebase. @ericof [#333](https://github.com/plone/cookieplone-templates/issues/333)
- Implement VSCode configuration template. @ericof [#335](https://github.com/plone/cookieplone-templates/issues/335)
- Implement monorepo add-on template. @ericof [#338](https://github.com/plone/cookieplone-templates/issues/338)
- Use pnpm 9.15.9 in Volto 18. @wesleybl [#344](https://github.com/plone/cookieplone-templates/issues/344)
- Project: Manage backend installation with uv. @ericof
   - Modify Makefiles to use repoplone to obtain information about versions and image [#350](https://github.com/plone/cookieplone-templates/issues/350)
- Added filterBlobs option in mrs-developer clone by default. @sneridagh
- Added full support for Volto 19 (prerelease). @sneridagh
- Added support ?react icons in Seven add-on. @sneridagh
- Adds a new hidden template DevOps Ansible to be used by other templates. @ericof
- Catalog support for Volto 19 projects. @sneridagh
- Implement a sub-template (`agents_instructions`) to configure instructions for LLMs.
   - This initFollowing the [recomended approach for VSCode and GitHub Co-Pilot](https://code.visualstudio.com/docs/copilot/customization/custom-instructions). @ericof
- Update the version of cookiecutter-zope-instance @erral
- Volto 19 has adopted `razzle-scss-plugin` in core. @sneridagh


### Bug fixes:

- Removed `-dev` from the backend acceptance make command. @boss6825 [#121](https://github.com/plone/cookieplone-templates/issues/121)
- Fix Eslint in IDEs. @wesleybl [#161](https://github.com/plone/cookieplone-templates/issues/161)
- Avoid duplication of the documentation scaffold into `backend/docs` directory. @ujsquared, @davisagli [#202](https://github.com/plone/cookieplone-templates/issues/202)
- Use the proper Read the Docs project slug for find and replace. Unfortunately, I know of no way to check for an available RTD project slug at project generation time. @stevepiercy [#204](https://github.com/plone/cookieplone-templates/issues/204)
- Add `horse-with-no-namespace` to `backend_addon` test dependencies. @ericof [#208](https://github.com/plone/cookieplone-templates/issues/208)
- Do not remove the data when running `make clean` @erral [#214](https://github.com/plone/cookieplone-templates/issues/214)
- Change Makefile dependencies to install addons after first run @erral [#216](https://github.com/plone/cookieplone-templates/issues/216)
- Pay attention to `use_prerelease_versions` when picking a Volto version. @davisagli [#217](https://github.com/plone/cookieplone-templates/issues/217)
- Fix report_keys_usage script @ericof [#219](https://github.com/plone/cookieplone-templates/issues/219)
- Standardize usage of the repository URLs in templates. @ericof [#221](https://github.com/plone/cookieplone-templates/issues/221)
- Fix backend_addon GHA workflow. @ericof [#229](https://github.com/plone/cookieplone-templates/issues/229)
- Fixes Sonar analysis in front end package. @wesleybl [#245](https://github.com/plone/cookieplone-templates/issues/245)
- Fix plonecli compatibility @erral [#248](https://github.com/plone/cookieplone-templates/issues/248)
- In the backend add-on template, do not set a default theme @erral [#251](https://github.com/plone/cookieplone-templates/issues/251)
- Specify the Python version when creating a virtualenv in the backend Makefile. @davisagli [#254](https://github.com/plone/cookieplone-templates/issues/254)
- Avoid locking issue when creating stack site while using filestorage. @davisagli [#257](https://github.com/plone/cookieplone-templates/issues/257)
- Fix running backend tests in CI. @davisagli [#264](https://github.com/plone/cookieplone-templates/issues/264)
- Frontend: Add plonePrePublish settings to .release-it.json. @ericof [#274](https://github.com/plone/cookieplone-templates/issues/274)
- Docs: Add a build target to the Makefile. @ericof [#276](https://github.com/plone/cookieplone-templates/issues/276)
- Revert having a default scope for monorepo frontend packages. @ericof [#283](https://github.com/plone/cookieplone-templates/issues/283)
- Fix the language code for Swedish. @davisagli [#288](https://github.com/plone/cookieplone-templates/issues/288)
- Fix `make help` command in devops Makefile. @davisagli [#305](https://github.com/plone/cookieplone-templates/issues/305)
- Add `.mxdev_cache` to .gitignore in backend addons. @wesleybl [#307](https://github.com/plone/cookieplone-templates/issues/307)
- Replace the usage of from Products.CMFPlone.interfaces import INonInstallable by from plone.base.interfaces.installable import INonInstallable in the backend add-on template. @ericof [#327](https://github.com/plone/cookieplone-templates/issues/327)
- Fix repository.toml frontend.package.path setting for scoped packages. @ericof [#331](https://github.com/plone/cookieplone-templates/issues/331)
- GHA: Fix backend tests "Failed to create virtual environment". @ericof [#342](https://github.com/plone/cookieplone-templates/issues/342)
- Added the missing Webpack resolver for relative shadowing. @sneridagh
- Be explicit about the Python version when running uv venv locally in backend. @wesleybl
- Fix plonecli compatibility removing usage of mrbob.ini file @erral
- Fix varnish CI. @mauritsvanrees
- Fixed Dockerfile build command because pnpm complains about ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY. @sneridagh
- Fixed missing `SPHINXBUILD` env var from docs Makefile for RTD build. @sneridagh
- Fixed preset name in frontend scaffold to support the new razzle fork. @sneridagh
- Fixes for projects using Volto 19. @ericof
- In the frontend image, use the same pnpm-lock.yaml that was used during development. @davisagli
- Make sure commands in the backend Makefile always use the Python virtualenv it created. @davisagli
- Recursively find packages in workspace. @TimoBroeskamp
- Rename last razzle import in Storybook config. @sneridagh


### Internal:

- Project template: Test variations of `initialize_documentation` option. @ericof [#204](https://github.com/plone/cookieplone-templates/issues/204)
- Fix broken link to creating a change log entry. @acsr [#211](https://github.com/plone/cookieplone-templates/issues/211)
- Move `templates/add-ons/documentation-starter` to `templates/docs/starter`. @ericof [#227](https://github.com/plone/cookieplone-templates/issues/227)
- format boilerplate so make format has less to complain about @pbauer [#242](https://github.com/plone/cookieplone-templates/issues/242)
- Updates cache keys of the `frontend-functional` job to invalidate the cache if `package.json` or `mrs.developer.json` are changed. @wesleybl [#294](https://github.com/plone/cookieplone-templates/issues/294)
- Add support for prerelease Volto versions in codebase generation. @wesleybl [#299](https://github.com/plone/cookieplone-templates/issues/299)
- Update dependencies. @wesleybl [#303](https://github.com/plone/cookieplone-templates/issues/303)
- Backend Add On: Do not render the `news/.changelog_template.jinja` file @ericof
- Implement version and change log support. @ericof
- Prepare the first release of `cookieplone-templates`. @ericof
      - Adds `repoplone` as a Python dependency
      - Adds `make changelog` and `make release` to `Makefile`
      - Update README.md
- Refactor GHA workflows @ericof
- Remove unused namespace definition from permissions.zcml @ericof
- Require cookieplone 0.9.4 or above @ericof
- Trigger GitHub Actions workflow for external pull requests. @davisagli
- Use uv to manage project and project dependencies. @ericof


### Documentation:

- Clean up and align all the `README.md`s, and use uv's proper brand name. @stevepiercy [#189](https://github.com/plone/cookieplone-templates/issues/189)
- Add `readme-link-check.yml` for all the `README.md`s. @stevepiercy
  Fix broken links. @stevepiercy
  License badge was rendering as "Invalid" due to no absolute URL. @stevepiercy
  Replace CI badge, as individual workflows can't be checked with the new CI structure. @stevepiercy
  Minor grammar and formatting fixes. @stevepiercy [#210](https://github.com/plone/cookieplone-templates/issues/210)
- Add command for running a remote branch. @stevepiercy, @erral [#222](https://github.com/plone/cookieplone-templates/issues/222)
- Fixes GitHub actions CI badges on the README.md file for a monorepo Project. @ericof
