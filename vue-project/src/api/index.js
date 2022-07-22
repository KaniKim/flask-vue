import axios from 'axios';

function registerUser(userData) {
  return axios.post('http://localhost:5000/user/sign-up', userData);
}

function loginUser(userData) {
  return axios.post('http://localhost:5000/user/login', userData);
}

function editUser(userData) {
  return axios.put('http://localhost:5000/user/me', userData, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    },
  });
}

function checkUser() {
  return axios.get('http://localhost:5000/user/me', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    },
  });
}

function deleteUser(userData) {
  return axios.delete('http://localhost:5000/user/me', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    },
    data: {
      email: userData.email,
      password: userData.password,
    },
  });
}

export { registerUser, loginUser, checkUser, editUser, deleteUser };
