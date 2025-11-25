import axios from "axios";
const apiBase = "http://127.0.0.1:5000/function";

export function generateCase(formData) {
  return axios.post(`${apiBase}/generate`, formData, { headers: {"Content-Type":"multipart/form-data"} });
}

export function getCaseList() {
  return axios.get(`${apiBase}/cases`);
}

export function deleteCase(timestamp) {
  return axios.delete(`${apiBase}/delete/${timestamp}`);
}

export function getCaseDetail(timestamp) {
  return axios.get(`${apiBase}/case_detail/${timestamp}`);
}

export function downloadCase(timestamp) {
  return axios.get(`${apiBase}/download/${timestamp}`, { responseType:"blob" });
}
