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
  is_remote: RemoteType;
  salary_min?: number;
  salary_max?: number;
  salary_currency: string;
  apply_url: string;
  date_posted: string;
  date_fetched: string;
  source: string;
}
export enum RemoteType {
  REMOTE = 0,
  HYBRID = 1,
  ONSITE = 2
}
export const getCompanyLogo = (company: string): string => {
  return `/logos/${company.toLowerCase()}.png`;
};
