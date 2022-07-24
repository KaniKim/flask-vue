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
    const {
      config,
      response: { status },
    } = error;
    if (status === 419) {
      if (error.response.data.code === 'expired') {
        const originalRequest = config;
        const refresh_token = localStorage.getItem('refresh_token');
        // token refresh 요청
        const { data } = await axios.post(
          'http://localhost:5000/refresh_token',
          {},
          { headers: { authorization: `Bearer ${refresh_token}` } },
        );

        const new_token = {
          access_token: data.access_token,
          refresh_token: data.refresh_token,
        };

        await localStorage.setItem('access_token', new_token.access_token);
        await localStorage.setItem('refresh_token', new_token.refresh_token);

        axios.defaults.headers.common.Authorization = `Bearer ${new_token.access_token}`;
        originalRequest.headers.Authorization = `Bearer ${new_token.access_token}`;

        return axios(originalRequest);
      }
    }
    return Promise.reject(error);
  },
);

export default Axios;
