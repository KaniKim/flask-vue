import Axios from '@/api/axios_interceptor';

function getComment(column_id) {
  return Axios.get(`/column/${column_id}/comment`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
}

function postComment(data) {
  return Axios.post(
    `/column/${data.column_id}/comment`,
    { content: data.content },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    },
  );
}

function postNextComment(data) {
  return Axios.post(
    `/comment/${data.comment_id}/next`,
    { content: data.content },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    },
  );
}

export { getComment, postComment, postNextComment };
