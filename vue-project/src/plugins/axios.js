import axios from "axios";
import Cookies from "js-cookie";
import { refreshToken } from "@/plugins/login";

const AxiosInst = axios.create();

AxiosInst.interceptors.request.use(
  async function (config) {
    config.headers.authorization = Cookies.get("access_token");

    return config;
  },
  (err) => {
    return Promise.reject(err);
  }
);

AxiosInst.interceptors.response.use(
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

export default AxiosInst;
