import { store } from "quasar/wrappers";
import { createPinia } from "pinia";
import { createPersistedState } from "pinia-plugin-persistedstate";
import SecureLS from "secure-ls";
const ls = new SecureLS({
  encodingType: "aes",
  isCompression: false,
  encryptionSecret: "sqhcngU9Ll++96qnbdAOuTrG60ncO24iSrewzm/xHqk=",
});

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default store((/* { ssrContext } */) => {
  const pinia = createPinia();

  pinia.use(
    createPersistedState({
      storage: {
        getItem: (key) => ls.get(key),
        setItem: (key, value) => ls.set(key, value),
        removeItem: (key) => ls.remove(key),
      },
    })
  );
  return pinia;
});
