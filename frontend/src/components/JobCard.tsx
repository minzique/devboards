import { Job } from "@/types/job";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDistanceToNow } from "date-fns";
import { useAppliedJobs } from "@/hooks/useAppliedJobs";

export const JobCard = ({
  job_hash,
  title,
  company,
  location,
  salary_min,
  salary_max,
  date_posted,
  apply_url,
  job_type,
  is_remote,
  logo
}: Job) => {
  const { appliedJobs, toggleApplied } = useAppliedJobs();
  const isApplied = appliedJobs.has(job_hash);
  const formattedDate = formatDistanceToNow(new Date(date_posted), { addSuffix: true });
  const salary = salary_min && salary_max ? `$${salary_min}K - $${salary_max}K` : null;

  return (
    <div className="bg-white rounded-lg p-6 border border-gray-200 hover:border-gray-500 transition-all flex flex-col h-full">
      <div className="flex flex-col flex-grow">
        <div className="flex justify-between items-start">
          <span className="text-sm text-blue-600">{formattedDate}</span>
          {is_remote && (
            <Badge variant="secondary" className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200">
              Remote
            </Badge>
          )}
        </div>

        <div className="space-y-2">
          <h3 className="font-semibold text-lg text-gray-900">{title}</h3>
          
          <div className="flex items-center gap-2">
            {logo ? (
              <img src={logo} alt={company} className="w-5 h-5 rounded" />
            ) : (
              <div className="w-5 h-5 bg-gray-100 rounded flex items-center justify-center">
                <span className="text-xs font-medium">{company[0]}</span>
              </div>
            )}
            <span className="text-sm text-gray-600">{company}</span>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>📍 {location}</span>
          </div>
          {salary && (
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span>💰 {salary}</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>⏰ {job_type}</span>
          </div>
        </div>
      </div>

      <div className="flex gap-2 pt-4 mt-auto">
        <Button
          variant="secondary"
          className="w-full"
          onClick={() => window.open(apply_url, '_blank')}
        >
          Details
        </Button>
        <Button
          variant={isApplied ? "default" : "outline"}
          className={`w-full ${isApplied ? 'bg-yellow-400 hover:bg-yellow-500' : 'hover:bg-yellow-500 hover:text-white'}`}
          onClick={() => toggleApplied(job_hash)}
        >
          {isApplied ? 'Applied ✓' : 'Mark Applied'}
        </Button>
      </div>
    </div>
  );
};