// The root route of the app. Plone Aurora provides it: the client-safe part
// from `@plone/aurora/app/root`, and the middleware and the loader from
// `@plone/aurora/app/root.server`, which React Router keeps out of the client.
export { handle, Layout, ErrorBoundary } from '@plone/aurora/app/root';
export { middleware, loader } from '@plone/aurora/app/root.server';
