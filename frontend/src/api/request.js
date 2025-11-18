import axios from "axios";

const request = axios.create({
  baseURL: "/", // 使用 Vite 代理
  timeout: 10000,
});

request.interceptors.response.use(
  (res) => res.data,
  (err) => Promise.reject(err)
);

export default request;
