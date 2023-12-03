import {defineComponent,h,Suspense } from 'vue'
import {flushPromises, mount} from '@vue/test-utils'
import {createRouter, createWebHistory} from "vue-router";
import routes from "src/router/routes";
import {createI18n} from "vue-i18n";
import messages from "src/i18n";
import {createTestingPinia} from "@pinia/testing";
import {createPinia} from "pinia";
import authGuard from "src/boot/auth_guard";
import {qLayoutInjections} from "@quasar/quasar-app-extension-testing-unit-jest";
import RouterViewSuspense from "components/partials/RouterViewSuspense.vue";
import axios from "axios";

export const router = createRouter({
  history: createWebHistory(),
  routes: routes,
  mode: "abstract",
});
export const i18n = createI18n({
  legacy: false,
  locale: "en-US",
  fallbackLocale: "en-US",
  globalInjection: true,
  messages,
  // silentFallbackWarn: true,
});
export const setupUtils = () => {
  global.window.axios = axios;
  global.window.delay = jest.fn();
  global.window.scrollTo = jest.fn();
  jest.mock("axios", () => {
    return {
      create: jest.fn(() => ({
        get: jest.fn(),
        post: jest.fn(),
        patch: jest.fn(),
        delete: jest.fn(),
        interceptors: {
          request: { use: jest.fn(), eject: jest.fn() },
          response: { use: jest.fn(), eject: jest.fn() },
        },
      })),
    };
  });
};
export const mountSuspense = async (component, options) => {
  const wrapper = mount(
    defineComponent({
      render() {
        return h(Suspense, null, {
          default: () => h(component),
          fallback: () => h("div", "fallback"),
        });
      },
    }),
    options
  );

  await flushPromises();
  return wrapper;
};


export const testStore = createTestingPinia();
export const realStore = createPinia();



export const mountRouteSuspense = async (Component, options) => {
  const wrapper = mount(
    defineComponent({
      components: { Component },
      template: "<Suspense><Component/></Suspense>",
    }),
    {
      global: {
        plugins: [router, i18n, testStore],
        stubs: {
          AppSvgIcon: true,
          SvgIcon: true,
          DarkButton: true,
          LanguageSwitcher: true,
          ComingSoon: true,
          RouterViewSuspense: RouterViewSuspense,
          QEditor: true, // this make test fails maximum call exceeded
        },
        // mocks: {},
        provide: qLayoutInjections(),
      },
      ...options,
    }
  );

  authGuard({ router });

  await flushPromises();

  return wrapper;
};
