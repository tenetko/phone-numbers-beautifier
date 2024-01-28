import { createHistoryRouter, createRoute } from "atomic-router";
import { createBrowserHistory } from "history";

export const routes = {
  tzb: createRoute(),
  tzbtemplate: createRoute(),
  reminders: createRoute(),
  os: createRoute(),
};

export const router = createHistoryRouter({
  routes: [
    { path: "/", route: routes.tzb },
    { path: "/tzb", route: routes.tzb },
    { path: "/tzbtemplate", route: routes.tzbtemplate },
    { path: "/reminders", route: routes.reminders },
    { path: "/os", route: routes.os },
  ],
});

router.setHistory(createBrowserHistory());
