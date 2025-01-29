import { Heart } from "lucide-react";
import { useState } from "react";

interface JobCardProps {
  id: string;
  title: string;
  company: string;
  location: string;
  salary?: string;
  type: string;
  postedAt: string;
  logo?: string;
  applyUrl: string;
}

export const JobCard = ({
  id,
  title,
  company,
  location,
  salary,
  type,
  postedAt,
  logo,
  applyUrl,
}: JobCardProps) => {
  const [isSaved, setIsSaved] = useState(false);

  const toggleSave = () => {
    setIsSaved(!isSaved);
    // TODO: Implement save to local storage
  };

  return (
    <div className="bg-card p-6 rounded-lg border border-card-border hover:shadow-md transition-shadow animate-fade-in">
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-muted rounded-md flex items-center justify-center">
            {logo ? (
              <img src={logo} alt={company} className="w-8 h-8 object-contain" />
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
      
      <div className="space-y-3">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span>{location}</span>
          <span>•</span>
          <span>{type}</span>
          {salary && (
            <>
              <span>•</span>
              <span>{salary}</span>
            </>
          )}
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">{postedAt}</span>
          <a
            href={applyUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-primary text-primary-foreground px-6 py-2 rounded-md hover:bg-primary-hover transition-colors"
          >
            Apply
          </a>
        </div>
      </div>
    </div>
  );
};