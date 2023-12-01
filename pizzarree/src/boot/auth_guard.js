import { boot } from "quasar/wrappers";
import { useAuthStore } from "src/stores/auth";

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
let authGuard;
export default boot(async ({ router }) => {
  router.afterEach((to, from) => {
    const toDepth = [...new Set(to.path.split("/"))].length;
    const fromDepth = [...new Set(from.path.split("/"))].length;
    to.meta.transitionName =
      toDepth < fromDepth ? "animated slideInRight" : "animated slideInLeft";
  });
  authGuard = (router) => {
    const authStore = useAuthStore();
    router.beforeEach((to, from, next) => {
      let route_match = to.matched.find((rt) => rt.name === to.name);
      let requiresAuth = route_match?.meta?.requiresAuth === true;
      let requiresNotAuth = route_match?.meta?.requiresAuth === false;
      let isAuthenticated = authStore.isAuthenticated;

      if (route_match) {
        if (requiresAuth && isAuthenticated) {
          next();
        } else if (requiresAuth && !isAuthenticated) {
          next({
            name: "login",
            query: { redirect: to.fullPath },
          });
        } else if (requiresNotAuth && isAuthenticated) {
          next({
            name: "dashboard",
          });
        } else {
          next();
        }
      } else {
        next();
      }
    });
  };
  authGuard(router); // abstract it for test
});

export { authGuard };
