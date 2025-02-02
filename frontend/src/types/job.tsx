export interface Job {
  job_hash: string;
  title: string;
  description: string;
  company: string;
  company_id?: number;
  company_logo?: string;
  company_website?: string;
  location: string;
  job_type: "full-time" | "part-time" | "contract" | "internship";
  is_remote: "remote" | "hybrid" | "in-office";
  salary_min?: number;
  salary_max?: number;
  salary_currency: string;
  apply_url: string;
  date_posted: string;
  date_fetched: string;
  source: string;
  logo?: string;
}
