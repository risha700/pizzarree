import { defineStore } from "pinia";
import { api } from "src/boot/axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    authUser: {
      preference: {},
    },
    tempToken: {
      value: null,
      expiry: null,
      expired: true,
    },
    potentialUsername: null,
    potentialUsers: [],
  }),
  persist: {
    beforeRestore: (ctx) => {
      // console.log(`about to restore '${ctx.store.$id}'`);
    },
  },
  getters: {
    isAuthenticated: (state) => {
      if (state.authUser && state.authUser.token) {
        return true;
      }
      return false;
    },
    getTempToken: (state) => {
      return state.tempToken.value;
    },
    isTempTokenExpired: (state) => {
      return state.tempToken.expired;
    },
    getUserPreference: (state) => {
      return state.authUser.preference;
    },
  },
  actions: {
    async logIn(form, url) {
      await form
        .post(url)
        .then((data) => {
          this.authUser = data;
        })
        .catch((e) => e);
    },
    async getProfileData(url) {
      let data = await api.get(url);
      Object.keys({ data }).map((key) => {
        switch (typeof data[key]) {
          case "object":
            key === "tenants"
              ? (this.authUser[key] = data[key])
              : Object.keys(data[key]).map((sub_key) => {
                  this.authUser[sub_key] = data[key][sub_key];
                });
            break;
          case "string":
            this.authUser[key] = data[key];
            break;
        }
      });
      // set theme and language here
    },
    async logOut() {
      this.authUser = { preference: {} };
      this.tempToken = {};
    },
    async setTempToken(token) {
      let setExpirey = (expiryTimeStamp, min) => {
        return new Date(expiryTimeStamp.getTime() + min * 60000) || false;
      };

      if (typeof token === "object") {
        this.tempToken.value = token.value;
        this.tempToken.expiry = token.expiry
          ? setExpirey(token.expiry, token.expiryMinutes || 3)
          : setExpirey(new Date(), token.expiryMinutes || 3);
      } else {
        this.tempToken.value = token;
      }
      await this.validateTempToken();
    },
    async clearTempToken() {
      this.tempToken.value = null;
      this.tempToken.expiry = null;
      this.tempToken.expired = true;
    },
    async validateTempToken() {
      let now = new Date();
      let limit_ts = new Date(this.tempToken.expiry);
      this.tempToken.expired = now.getTime() > limit_ts.getTime();
    },
    async setPotenialUser(username) {
      try {
        this.potentialUsers.push(username);
      } catch (error) {
        this.potentialUsers = [].push(username);
      }

      this.potentialUsers = [...new Set(this.potentialUsers)];
      this.potentialUsername = username;
    },
    async unsetPotentialUsers(username) {
      let idx = this.potentialUsers.indexOf(username);
      if (idx >= 0) {
        this.potentialUsers.splice(idx, 1);
        this.potentialUsername = this.potentialUsers[0] || null;
      }
    },
    async persistUserPreference(url, preference) {
      await api
        .patch(url, preference)
        .then(async ({ data }) => {
          let { language, theme } = data.preference;
          this.authUser.preference.language = language;
          this.authUser.preference.theme = theme;
        })
        .catch((e) => e);
    },
    async setUserPrefrence(pref) {
      this.authUser.preference[Object.keys(pref)[0]] = Object.values(pref)[0];
    },
  },
});
