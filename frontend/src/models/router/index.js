import { createHistoryRouter, createRoute } from "atomic-router";
import { createBrowserHistory } from "history";

export const routes = {
  tzb: createRoute(),
  reminders: createRoute(),
  os: createRoute(),
};

export const router = createHistoryRouter({
  routes: [
    { path: "/tzb", route: routes.tzb },
    { path: "/reminders", route: routes.reminders },
    { path: "/os", route: routes.os },
  ],
});

router.setHistory(createBrowserHistory());
