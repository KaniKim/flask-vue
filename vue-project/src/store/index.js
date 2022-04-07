import { createStore } from "vuex";

export default createStore({
  state: {
    user: null,
    password: null,
  },
  getters: {
    user: (state) => {
      return state.user;
    },
    password: (state) => {
      return state.password;
    },
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setPassword(state, password) {
      state.password = password;
    },
  },
  actions: {},
  modules: {},
});
