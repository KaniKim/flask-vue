import axios from 'axios';

function writeColumn(columnData) {
  return axios.post('http://localhost:5000/column/', columnData, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    },
  });
}

function myColumn() {
  return axios.get('http://localhost:5000/column/me', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    },
  });
}

function allColumn() {
  return axios.get('http://localhost:5000/board/all', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    },
  });
}

function specificBoard(specific) {
  return axios.get(`http://localhost:5000/board/${specific}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    },
  });
}

function specificColumn(specific) {
  return axios.get(
    `http://localhost:5000/board/${specific.name}/column/${specific.column.id}`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('jwt')}`,
      },
    },
  );
}

export { writeColumn, myColumn, allColumn, specificColumn, specificBoard };
