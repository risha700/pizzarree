import { describe, expect, test, afterEach, beforeEach } from "@jest/globals";
import { installQuasarPlugin } from "@quasar/quasar-app-extension-testing-unit-jest";
import { flushPromises } from "@vue/test-utils";
import App from "src/App";
import { useAuthStore } from "src/stores/auth";
import {mountRouteSuspense, router, setupUtils } from "app/test/utils";

installQuasarPlugin();
setupUtils();

describe("App User", () => {
  let wrapper;
  let authStore;
  let push = jest.spyOn(router, "push");

  beforeEach(async () => {
    wrapper = await mountRouteSuspense(App);
    authStore = useAuthStore({});
  });

  afterEach(async () => {
    authStore?.$reset();
    // router.options.history.destroy(); // this doesnt reset router you need to create new instance
    // await router.isReady();
  });

  test("renders public home page", async () => {
    let page = wrapper.find(".q-page-container");
    expect(page.html()).not.toBe("");
    expect(router.currentRoute.value.name).toEqual("Home");
  });

  // test("renders public about page", async () => {
  //   push({ name: "about" });
  //   await flushPromises();
  //   expect(router.currentRoute.value.name).toEqual("About");
  // });

  test("redirects unauthenticated dashboard to login", async () => {
    expect(authStore.isAuthenticated).toEqual(false);
    push({ name: "Dashboard" });
    await flushPromises();
    expect(push).toHaveBeenCalledWith({ name: "Dashboard" });
    expect(router.currentRoute.value.redirectedFrom.name).toEqual("Dashboard");
    expect(router.currentRoute.value.name).toEqual("Login");
    // console.log(wrapper.vm);
  });

  test("redirecs authenticated to dashboard when requireAuth=false", async () => {
    expect(authStore.isAuthenticated).toEqual(false);
    authStore.authUser = { token: "test@test.test" }; //sudo authenticate
    expect(authStore.isAuthenticated).toEqual(true);
    push({ name: "Register" });
    await flushPromises();
    // expect(push).toHaveBeenCalledTimes(3);
    expect(router.currentRoute.value.name).toEqual("Dashboard");
  });

  test("accepts authenticated to any route", async () => {
    authStore.authUser = { token: "test@test.test" }; //sudo authenticate
    expect(authStore.isAuthenticated).toEqual(true);
    // push({ name: "about" });
    // await flushPromises();
    // expect(push).toHaveBeenCalledWith({ name: "about" });
    // expect(router.currentRoute.value.name).toEqual("about");
    push({ name: "Dashboard" });
    await flushPromises();
    expect(push).toHaveBeenCalledWith({ name: "Dashboard" });
    expect(router.currentRoute.value.name).toEqual("Dashboard");
  });
});
