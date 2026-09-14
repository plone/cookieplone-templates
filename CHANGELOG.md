
# Change log

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 20260914.1 (2026-09-14)


### New features:

- Migrated the `projects/monorepo` template to the cookieplone v2 schema (`cookieplone.json`), declaring validators inline, sourcing version pins from the repository-level `cookieplone-config.json`, and converting boolean choice fields (`use_prerelease_versions`, `devops_cache`, `devops_ansible`, `devops_gha_deploy`, `initialize_documentation`) to native `boolean` properties. @ericof [#359](https://github.com/plone/cookieplone-templates/issues/359)
- Migrated `add-ons/monorepo` and `sub/addon_settings` templates to cookieplone v2 schema. @ericof [#362](https://github.com/plone/cookieplone-templates/issues/362)
- Migrated CI templates (`gh_backend_addon`, `gh_frontend_addon`, `gh_monorepo_addon`, `gh_project`, `gh_classic_project`) to the cookieplone v2 schema. @ericof [#364](https://github.com/plone/cookieplone-templates/issues/364)
- Migrated `agents/instructions` and `ide/vscode` templates to the cookieplone v2 schema. @ericof [#365](https://github.com/plone/cookieplone-templates/issues/365)
- Migrated `sub/cache`, `sub/frontend_project`, `sub/project_settings`, and `sub/classic_project_settings` templates to the cookieplone v2 schema. @ericof [#366](https://github.com/plone/cookieplone-templates/issues/366)
- Migrated `devops/ansible` template to the cookieplone v2 schema. @ericof [#367](https://github.com/plone/cookieplone-templates/issues/367)
- Migrated `docs/starter` template to the cookieplone v2 schema. @ericof [#368](https://github.com/plone/cookieplone-templates/issues/368)
- Migrated `add-ons/backend`, `add-ons/frontend`, and `add-ons/seven_addon` templates to the cookieplone v2 schema. @ericof [#369](https://github.com/plone/cookieplone-templates/issues/369)
- Migrated `projects/classic` template to the cookieplone v2 schema. @ericof [#370](https://github.com/plone/cookieplone-templates/issues/370)
- Use both the README and the CHANGELOG for the rendered version of the README for pypi @erral [#387](https://github.com/plone/cookieplone-templates/issues/387)
- Bumped cookieplone to 2.0.0b3 and adopted the built-in post-generation summary screen, configurable via `config.summary` in `cookieplone-config.json`. @ericof [#411](https://github.com/plone/cookieplone-templates/issues/411)
- Upgrade `config.versions.devops_db_version` to 18, and fix volume mappings @ericof [#418](https://github.com/plone/cookieplone-templates/issues/418)
- Upgrade `config.versions.gha_version_cache` to v6, `config.versions.gha_version_checkout` to v7,  `config.versions.gha_version_node` to 24, `config.versions.gha_version_pages_deploy` to v4.8.0, `config.versions.gha_version_setup_node` to v6.4.0,`config.versions.gha_version_upload_artifact` to v7.0.1  @ericof [#418](https://github.com/plone/cookieplone-templates/issues/418)
- Upgrade `config.versions.devops_varnish_version` to 8.0. @ericof [#418](https://github.com/plone/cookieplone-templates/issues/418)
- Upgrade `config.versions.devops_traefik_version` to v3.7 and fix label annotations in stack files. @ericof [#418](https://github.com/plone/cookieplone-templates/issues/418)
- Upgrade `config.versions.backend_python` to 3.14 @ericof [#418](https://github.com/plone/cookieplone-templates/issues/418)
- Refine descriptions in user dialog. @ksuess [#425](https://github.com/plone/cookieplone-templates/issues/425)
- Remove README sections that belong to cookieplone. @ksuess [#426](https://github.com/plone/cookieplone-templates/issues/426)
- Recommend the `ms-python.vscode-python-envs` VSCode extension and set a default for `python-envs.workspaceSearchPaths` pointing at the backend virtual environment. @ericof [#428](https://github.com/plone/cookieplone-templates/issues/428)
- Ship the towncrier changelog template inside each generated codebase, unify the towncrier settings and news fragment types across backend, frontend and project codebases, and simplify the Changelog GitHub Actions workflows, which no longer install the frontend toolchain just to check for news fragments. @ericof [#429](https://github.com/plone/cookieplone-templates/issues/429)
- Compute a `storybook-deploy` flag in the CI `config` workflow (deploy only for public repositories) and pass it through to the storybook job, instead of always deploying. @ericof [#430](https://github.com/plone/cookieplone-templates/issues/430)
- Add a Playwright acceptance test setup to the Aurora frontend add-on template (``acceptance/`` harness with a backend reset fixture, login/content/accessibility helpers and homepage/content tests, plus ``Makefile`` targets and ``package.json`` scripts), and wire it into the ``aurora_cmfplone`` project with an ``acceptance.yml`` GitHub Actions workflow and root ``Makefile`` targets. 
- Add an ``aurora_cmfplone`` project template combining an Aurora frontend with a Python CMFPlone backend, monorepo tooling, GitHub Actions, and functional integration coverage. 
- Added GitHub Actions for generated Volto projects using Nick as backend, including backend, frontend, and changelog checks. @sneridagh 
- Added `min_version` configuration to `cookieplone-config.json`. @ericof 
- Added `renderer` configuration to `cookieplone-config.json`. @ericof 
- Added a Plone Aurora project template using Nick as backend, with dedicated GitHub Actions, generation tests, and an Aurora/Nick functional test. @sneridagh 
- Added a user-facing Aurora version parameter, resolved from the latest @plone/aurora release on npm, and used it to pin Aurora in mrs.developer.json. 
- Flexible docker image name generation depending on the container registry. 
- In the project template, ask the "Support headless Plone?" question earlier and skip Volto-specific questions (version and addon name) if Classic UI is selected. 
- Restructured the `volto_nick` project as a monorepo with the Nick server in `backend`, a Volto 19 workspace in `frontend`, and root-level project and repoplone configuration. @sneridagh 
- Unify monorepo and classic templates into a single source of truth, using the `feature_headless` flag to toggle between architectures. 


### Bug fixes:

- Fixed `make format` and `make lint` on the `next` branch so they no longer fail with `Failed to spawn: ruff` on a freshly synced project environment. The top-level `Makefile` now invokes Ruff via `uvx ruff` instead of `uv run ruff`, avoiding the need for Ruff to be declared as a project dependency. @ericof [#374](https://github.com/plone/cookieplone-templates/issues/374)
- Fixed `Dockerfile.acceptance` in project @sneridagh [#416](https://github.com/plone/cookieplone-templates/issues/416)
- Removed the trailing registry separator from `__container_image_prefix`, fixing the duplicated dash it produced in container image names consumed by the plone/meta GitHub Actions. The separator is now applied only where needed (Makefiles, stack files, and docs). @ericof [#421](https://github.com/plone/cookieplone-templates/issues/421)
- Fixed the storybook job in the reusable `frontend.yml` workflows to read `node-version` from `inputs` instead of a non-existent `config` job output. @ericof [#431](https://github.com/plone/cookieplone-templates/issues/431)
- Generate `dependabot.yml` under `.github`, where GitHub reads it from, instead of the root of the codebase, where it was ignored. The file now ships with every template under `templates/ci`, so every codebase with a CI configuration gets a working Dependabot configuration. @ericof [#436](https://github.com/plone/cookieplone-templates/issues/436)
- Fix the Aurora acceptance CI job timing out on a uv cache lock: disable setup-uv's shared cache so the long-lived `uv run robot-server` process no longer contends on `setup-uv-cache/.lock`. @sneridagh 
- Fix the Aurora frontend image build: set `CI=true` in the runtime corepack step so a `node_modules` reconcile cannot abort on a modules-purge confirmation prompt (no TTY), and give `ARG AURORA_VERSION` a default to silence the `InvalidDefaultArgInFrom` buildkit warning. @sneridagh 
- Fixed per-template `Makefile`s to invoke Ruff via `uvx ruff` instead of `uv run ruff`, so that recursive `make format_templates` calls no longer fail on a freshly synced environment when Ruff is not declared as a project dependency. @ericof 
- Fixed the name of the nick database parameters in generated `config.ts`. @sneridagh 


### Internal:

- Installed cookieplone from main branch, replacing pytest-cookies dependency. @ericof [#357](https://github.com/plone/cookieplone-templates/issues/357)
- Use cookieplone 2.0.0a2 as default dependency. @ericof [#383](https://github.com/plone/cookieplone-templates/issues/383)
- Updated GitHub Actions pins in `.github/workflows/` and `.github/actions/` to use current releases: `actions/checkout@v6`, `actions/cache@v5.0.5`, `actions/setup-node@v6.3.0`, `astral-sh/setup-uv@v8.0.0`, `JarvusInnovations/background-action@v1.0.7`. Switched the `setup_python` composite action to rely on `setup-uv`'s built-in caching (`enable-cache: true` + `cache-suffix`) instead of a manual `actions/cache` block. Derived the `test-template` job matrix in `main.yml` dynamically from `cookieplone-config.json` via `.scripts/list_templates.py`. @ericof [#385](https://github.com/plone/cookieplone-templates/issues/385)
- Replaced the remaining `pipx` usages with `uvx` across templates (release-it hooks, changelog workflows, and docs), so generated projects rely consistently on `uv`. @ericof [#423](https://github.com/plone/cookieplone-templates/issues/423)
- Added a Dependabot configuration to this repository, so the GitHub Actions used by its own workflows and composite actions are kept up to date. @ericof [#437](https://github.com/plone/cookieplone-templates/issues/437)
- Added `.scripts/list_templates.py`, a helper that reads `cookieplone-config.json` and emits the list of templates either as bare paths (for `make` consumption) or as a JSON matrix (for GitHub Actions). Replaced the hardcoded `TOP_LEVEL_TEMPLATES` / `SUB_TEMPLATES` variables in the top-level `Makefile` with a single `TEMPLATES` list derived from the new script, so `make format_templates` no longer drifts from the canonical template list. @ericof 
- Declared catalog-managed i18next as a peer dependency in generated Aurora add-ons to keep react-i18next instances unified. @sneridagh 
- Ensured every template ships a `hooks/pre_prompt.py` with a `MIN_COOKIEPLONE = "2.0.0a2"` version gate. Earlier Cookieplone releases (< 2.0.0a2) do not honor the `config.min_version` field in `cookieplone-config.json`, so templates would have silently run with an incompatible CLI. Bumped the `MIN_COOKIEPLONE` constant from `1.9.9` to `2.0.0a2` on the four pre-existing hooks, and added minimal version-check hooks to the twelve templates that lacked one. @ericof 
- Refactored all `post_gen_project.py` hooks to use the new `cookieplone.utils.post_gen` (`run_post_gen_actions`, `remove_files_by_key`, `move_files`, `run_make_format`, `initialize_git_repository`) and `cookieplone.utils.subtemplates.run_subtemplates` utilities introduced in cookieplone 2.0.0a2. Removed custom `run_actions` loops and `globals()`-based subtemplate dispatch. Propagated `global_versions=versions` to all subtemplate generation calls. @ericof 
- Renamed the `seven_addon` template to `aurora_addon`. Kept the original `seven_addon` for backwards compatibility. @sner 
- Updated functional CI jobs to `JarvusInnovations/background-action@v2` for the Node.js 24 action runtime. @sneridagh 
- Updated the Aurora add-on and Aurora with Nick templates to use pnpm 11.20.0 reproducibly through Corepack. @sneridagh 
- Upgrade cookieplone to version 2.0.0b2. @ericof 
- Use one shared Nick backend subtemplate for the Volto and Aurora Nick project templates. @sneridagh 


### Tests

- Added a functional CI job that generates and installs `volto_nick`, initializes and runs Nick with Volto, and verifies their integration through Playwright. @sneridagh 
- Added a test suite for the `volto_nick` project template, covering generation, variable substitution, generated file layout, and JSON-schema validation. @ericof 

## 20260810.1 (2026-08-10)


### Bug fixes:

- Use 'uvx towncrier' instead of 'pipx run towncrier' for release-it. @frapell [#404](https://github.com/plone/cookieplone-templates/issues/404)
- Adds extra [uv] to mxdev. @wesleybl [#407](https://github.com/plone/cookieplone-templates/issues/407)
- Fix CI workflow argument source for node-version. @ksuess [#413](https://github.com/plone/cookieplone-templates/issues/413)
- Purged deprecated and redundant use of rtd-pr-preview.yml workflow in templates. @stevepiercy [#419](https://github.com/plone/cookieplone-templates/issues/419)


### Internal:

- Remove `full-icu` of onlyBuiltDependencies @wesleybl [#406](https://github.com/plone/cookieplone-templates/issues/406)
- Use Lychee for linkchecker. @stevepiercy 

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
