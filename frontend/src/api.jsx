import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:5000/api' });

export const uploadAndProcess = async (formData) => {
  const response = await API.post('/process', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data;
};
