import { describe, expect, test, beforeAll } from "@jest/globals";
import {
  installQuasarPlugin,
  qLayoutInjections,
} from "@quasar/quasar-app-extension-testing-unit-jest";
import { useAuthStore } from "src/stores/auth";
import { setupUtils, router, i18n, realStore } from "app/test/utils"
import { mount, flushPromises } from "@vue/test-utils";

import RouterViewSuspense from "src/components/partials/RouterViewSuspense";
import authGuard from "src/boot/auth_guard";
import { api } from "src/boot/axios";
import LoginPage from "pages/user/LoginPage.vue";

installQuasarPlugin();
setupUtils();

// const LoginComponent = defineComponent({
//   components: { LoginPageStepper, UserLayout },
//   template: "<Suspense><UserLayout><LoginPageStepper/></UserLayout></Suspense>",
//   setup: () => LoginPageStepper.setup(),
// });
// we would have done it like
// wrapper = await mountRouteSuspense(App) // but not wrapper.vm props to test

describe("App", () => {
  let wrapper;
  let authStore;
  let push = jest.spyOn(router, "push");
  let api_post = jest.spyOn(api, "post");
  let username = "test";
  beforeAll(async () => {
    wrapper = mount(LoginPage, {
      global: {
        plugins: [router, i18n, realStore],
        provide: qLayoutInjections(),
        stubs: {
          AppSvgIcon: true,
          SvgIcon: true,
          RouterViewSuspense: RouterViewSuspense,
          DarkButton: true,
          LanguageSwitcher: true,
        },
        // renderStubDefaultSlot: false,
      },
      // shallow: false,
    });
    authGuard({ router });
    authStore = useAuthStore();
    push({ name: "Login" });
    await flushPromises();
  });

  test("allows unauthenticated user access to login page", async () => {
    expect(router.currentRoute.value.name).toEqual("Login");
    expect(authStore.isAuthenticated).toEqual(false);
    expect(authStore.potentialUsername).toBeNull;
    expect(wrapper.vm.step).toEqual(1);
  });
  test("redirects unauthenticated user to login if requiresAuth:true ", async () => {
    expect(authStore.isAuthenticated).toEqual(false);
    push({ name: "Dashboard" });
    await flushPromises();
    expect(router.currentRoute.value.name).toEqual("Login"); // not dashboard
  });

  test("throw validation error with empty username", async () => {
    let form = await wrapper.findComponent("form");
    await wrapper.findComponent("button[type=submit]").trigger("submit");
    expect(
      await wrapper.findComponent("button[type=submit]").componentVM.label
    ).toEqual("Next");

    await flushPromises();
    expect(form.emitted("submit")).not.toBeUndefined();
    expect(form.emitted("validationError")).not.toBeUndefined();
    expect(form.emitted("validationError")[0][0].hasError).toEqual(true);
  });

  test("throw validation error with incorrect username", async () => {
    api_post.mockRejectedValue(
      new Error(["Unable to log in with provided credentials."])
    );
    let form = await wrapper.findComponent("form");
    await wrapper.find("input[name=username]").setValue(username);
    await wrapper.findComponent("button[type=submit]").trigger("submit"); // or await form.trigger("submit.prevent");
    await flushPromises();
    expect(wrapper.vm.validateStepForm.errors.errors).not.toEqual({});
    expect(wrapper.vm.step).toEqual(1);
  });

  test("allows user with correct username to proceed to step 2", async () => {
    // let form = await wrapper.findComponent("form");
    expect(authStore.isAuthenticated).toEqual(false);
    api_post.mockResolvedValue({
      status: 207,
      data: { checks: "true", username: username },
    });
    await wrapper.find("input[name=username]").setValue(username);
    await wrapper.findComponent("button[type=submit]").trigger("submit");
    await flushPromises();
    expect(wrapper.vm.step).toEqual(2);
    expect(authStore.potentialUsername).toEqual(username);
  });
  // part of previous test
  test("directs login to step 2 if potentialUser exists", async () => {
    push({ name: "Login" });
    await flushPromises();

    expect(wrapper.vm.step).toEqual(2);
    expect(authStore.isAuthenticated).toEqual(false);
    expect(await wrapper.find(".q-select__focus-target").element.value).toEqual(
      username
    );
    api_post.mockResolvedValue({
      status: 200,
      data: {
        avatar: "",
        email_verified: true,
        is_active: true,
        new_device: false,
        phone_verified: false,
        token: "blablabla",
        user_id: 1,
        username: "risha",
        profile: { email_verified: true, phone_verified: true },
        tenants: [],
      },
    });
    await wrapper.find("input[type=password]").setValue(username); // any sudo password
    await wrapper.findComponent("form").trigger("submit.prevent");
    await flushPromises();
    expect(authStore.isAuthenticated).toBe(true);
    expect(router.currentRoute.value.name).toEqual("Dashboard");
  });
  // test("allows user to login with new credentials");
});
