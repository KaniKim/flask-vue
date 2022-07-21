import axios from 'axios';

function registerUser(userData) {
  return axios.post('http://localhost:5000/user/sign-up', userData);
}

function loginUser(userData) {
  return axios.post('http://localhost:5000/user/login', userData);
}

function checkUser() {
  return axios.get('http://localhost:5000/user/me', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    },
  });
}

export { registerUser, loginUser, checkUser };
