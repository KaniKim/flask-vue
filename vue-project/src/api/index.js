import Axios from '@/api/axios_interceptor';

function registerUser(userData) {
  return Axios.post('/user/sign-up', userData);
}

function loginUser(userData) {
  return Axios.post('/user/login', userData);
}

function editUser(userData) {
  return Axios.put('/user/me', userData, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

function checkUser() {
  return Axios.get('/user/me', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

function deleteUser(userData) {
  return Axios.delete('/user/me', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
    data: {
      email: userData.email,
      password: userData.password,
    },
  });
}

export { registerUser, loginUser, checkUser, editUser, deleteUser };
