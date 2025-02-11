import axios from "axios";
import { Job } from "../types/job";

const API_URL = import.meta.env.VITE_API_URL || `https://api.${window.location.host}`;

export const jobsApi = {
  getJobs: async (query?: string, location?: string) => {
    const params = new URLSearchParams();
    if (query) params.append("query", query);
    if (location) params.append("location", location);

    const response = await axios.get<Job[]>(`${API_URL}/jobs`, { params });
    return response.data;
  },
};
