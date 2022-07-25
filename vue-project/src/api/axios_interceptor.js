import axios from 'axios';

const Axios = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 1000,
});

Axios.interceptors.response.use(
  response => {
    return response;
  },
  async error => {
    const config = error.response.config;
    const status = error.response.status;

    if (status === 401) {
      if (error.response.data.msg === 'Token has expired') {
        const originalRequest = config;
        const refresh_token = localStorage.getItem('refresh_token');
        await axios
          .post(
            '/user/refresh',
            {},
            { headers: { authorization: `Bearer ${refresh_token}` } },
          )
          .then(async res => {
            const new_token = res.data;

            await localStorage.setItem('access_token', new_token);

            axios.defaults.headers.common.Authorization = `Bearer ${new_token}`;
            originalRequest.headers.Authorization = `Bearer ${new_token}`;

            return axios(originalRequest);
          });
      }
    }
    return Promise.reject(error);
  },
);

export default Axios;
