import axios from "axios";
import { boot } from "quasar/wrappers";
import { useAuthStore } from "src/stores/auth";

const api = axios.create({}); // will override it in App.vue

function readCookie(name) {
  let nameEQ = name + "=";
  let ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

export default boot(({ app }) => {
  let authStore = useAuthStore();

  api.interceptors.request.use((config) => {
    let auth_token = authStore.authUser.token || authStore.getTempToken || null;
    if (auth_token) {
      config.headers.Authorization = `Token ${auth_token}`;
    }

    let csrf_token =
      document.head.querySelector('meta[name="csrf-token"]') ||
      readCookie("csrftoken");
    if (csrf_token) {
      // config.headers.CSRFToken = csrf_token.content || csrf_token;
      config.headers["X-CSRFToken"] = csrf_token.content || csrf_token;
    }
    config.headers.common = {
      "X-Requested-With": "XMLHttpRequest",
      "Accept": "application/json",
      "Content-Type": "application/json",
      // "Authorization":"Token fbece30bb8de632cd7d8d4a78f68207a22453ba6",
      // Content-Language
      // Accept-Language
      "Access-Control-Allow-Origin": "*",
    };
    config.timeout = 60 * 1 * 1000 // 1 minute
    return config;
  });

  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
});
export { api };
