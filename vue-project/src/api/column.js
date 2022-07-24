import Axios from '@/api/axios_interceptor';

function writeColumn(columnData) {
  return Axios.post('/column/', columnData, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

function myColumn() {
  return Axios.get('/column/me', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

function allColumn() {
  return Axios.get('/board/all', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

function specificBoard(specific) {
  return Axios.get(`/board/${specific}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

function specificColumn(specific) {
  return Axios.get(`/board/${specific.name}/column/${specific.column_id}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

function clickLike(id) {
  return Axios.post(`/column/${id}/like`, null, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

export {
  writeColumn,
  myColumn,
  allColumn,
  specificColumn,
  specificBoard,
  clickLike,
};
