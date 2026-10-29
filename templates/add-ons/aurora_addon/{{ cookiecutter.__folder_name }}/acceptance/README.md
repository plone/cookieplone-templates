# Playwright acceptance tests

End-to-end acceptance tests driven by [Playwright](https://playwright.dev/),
running against a Plone **acceptance** backend (with `RobotRemote` enabled, so
the backend can be reset between tests) and a running Aurora frontend.

They live in `tests/` and are configured through
`../playwright.config.ts`.

## Layout

- `tests/reset-fixture.ts` — `setup`/`teardown` helpers that call `RobotRemote`
  to reset the backend ZODB to the `VOLTO_ROBOT_TESTING` baseline.
- `tests/test.ts` — the extended `test`/`expect`. Provides an auto `resetBackend`
  fixture that tears down and sets up the backend around every test.
- `tests/login.ts` — `login(page)`, authenticates via `@login` and sets the
  `auth_token` cookie (equivalent to Cypress' `cy.autologin`).
- `tests/content.ts` — `createContent(...)`, creates content through the REST
  API (equivalent to `cy.createContent`).
- `tests/accessibility.ts` — `expectNoAccessibilityViolations(page, ...)`, an
  axe-core based accessibility assertion.
- `tests/*.test.ts` — the tests themselves.

## Configuration

The helpers read the following environment variables (with sensible defaults for
the acceptance backend):

- `BACKEND_HOST` (default `127.0.0.1`)
- `SITE_ID` (default `plone`)
- `API_PATH` (default `http://${BACKEND_HOST}:55001/${SITE_ID}`)
- `FRONTEND_URL` (default `http://localhost:3000`)

## Running locally

From the repository root, start the acceptance containers and run the suite:

```bash
make ci-acceptance-test
```

To iterate interactively (with the Playwright UI) against already-running
servers, start the acceptance backend and frontend, then:

```bash
make acceptance-test
```

The first time, install the browsers used by Playwright:

```bash
make -C frontend install-acceptance
```
