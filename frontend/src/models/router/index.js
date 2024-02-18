import { createHistoryRouter, createRoute } from "atomic-router";
import { createBrowserHistory } from "history";

export const routes = {
  tzb: createRoute(),
  reminders: createRoute(),
  os: createRoute(),
};

export const router = createHistoryRouter({
  routes: [
<<<<<<< HEAD
    { path: "/", route: routes.tzb },
    { path: "/tzb", route: routes.tzb },
=======
    { path: "/", route: routes.tzbtemplate },
    { path: "/tzbtemplate", route: routes.tzbtemplate },
>>>>>>> templates
    { path: "/reminders", route: routes.reminders },
    { path: "/os", route: routes.os },
  ],
});

router.setHistory(createBrowserHistory());
