import { Job } from "@/types/job";
import { Heart } from "lucide-react";
import { describe } from "node:test";
import { useState } from "react";



export const JobCard = ({
  job_hash,
  title,
  company,
  location,
  salary_min,
  salary_max,
  date_posted,
  description,
  apply_url,
  source,
  job_type,
  logo
}: Job) => {
  const [isSaved, setIsSaved] = useState(false);

  const toggleSave = () => {
    setIsSaved(!isSaved);
    // TODO: Implement save to local storage
  };

  return (
    <div className="bg-card h-full p-6 rounded-lg border border-card-border hover:shadow-md transition-shadow animate-fade-in flex flex-col justify-between">
      <div className="space-y-4">
        <div className="flex justify-between items-start">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-muted rounded-md flex items-center justify-center">
              {logo ? (
                <img
                  src={logo}
                  alt={company}
                  className="w-8 h-8 object-contain"
                />
              ) : (
                <span className="text-lg font-semibold">{company[0]}</span>
              )}
            </div>
            <div>
              <h3 className="font-semibold text-lg text-secondary">{title}</h3>
              <p className="text-muted-foreground">{company}</p>
            </div>
          </div>
          <button
            onClick={toggleSave}
            className="text-muted-foreground hover:text-primary transition-colors"
          >
            <Heart className={isSaved ? "fill-primary" : ""} />
          </button>
        </div>

        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span>{location}</span>
          <span>•</span>
          <span>{job_type}</span>
          {(salary_max && salary_min) && (
            <>
              <span>•</span>
              <span>{salary_min} - {salary_max}</span>
            </>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between mt-4">
        <span className="text-sm text-muted-foreground">{date_posted}</span>
        <a
          href={apply_url}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-primary text-primary-foreground px-6 py-2 rounded-md hover:bg-primary-hover transition-colors"
        >
          Apply
        </a>
      </div>
    </div>
  );
};