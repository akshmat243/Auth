import axios from '../api/axios';

export const login = async (username, password) => {
  const response = await axios.post('login/', { username, password });
  localStorage.setItem('access', response.data.access);
  localStorage.setItem('refresh', response.data.refresh);
};

export const signup = async (username, email, password, password2) => {
  const response = await axios.post('signup/', { username, email, password, password2 });
  return response.data;
};

export const logout = async () => {
  const refresh = localStorage.getItem('refresh');
  if (refresh) {
    await axios.post('logout/', { refresh });
  }
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
};
