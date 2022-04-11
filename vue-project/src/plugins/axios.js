import axios from "axios";
import Cookies from "js-cookie";
import { refreshToken } from "@/plugins/login";

axios.defaults.baseURL = "http://localhost:8000";

axios.interceptors.request.use(
  async function (config) {
    config.headers.token = Cookies.get("token");
    config.headers.refresh_token = Cookies.get("refresh_token");

    return config;
  },
  (err) => {
    return Promise.reject(err);
  }
);

axios.interceptors.response.use(
  (res) => {
    return res;
  },
  async (err) => {
    const errAPI = err.config;

    if (err.response.data.status === 400 && errAPI.retry === undefined) {
      errAPI.retry = true;
      await refreshToken();
      return axios(errAPI);
    }
    return Promise.reject(err);
  }
);
