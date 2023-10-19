import { redirect } from "atomic-router";
import { router, routes } from "models/router";

// If page is not found, we will be redirected to the tzb page
redirect({
  clock: router.routeNotFound,
  route: routes.tzb,
});
