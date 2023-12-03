import { beforeEach, describe, expect, it } from "@jest/globals";
import {
  installQuasarPlugin,
  qLayoutInjections,
} from "@quasar/quasar-app-extension-testing-unit-jest";
import { mount, flushPromises } from "@vue/test-utils";
import App from "src/App";
import {testStore, router, i18n} from "app/test/utils";

installQuasarPlugin();

describe("App", () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(App, {
      global: {
        plugins: [router, i18n, testStore],
        stubs: [],
        provide: qLayoutInjections(),
        // renderStubDefaultSlot: false,
      },
      // shallow: false,
    });
  });

  it("renders", async () => {
    await router.isReady();
    await flushPromises();
    expect(wrapper.html()).not.toBe("");
  });
});
