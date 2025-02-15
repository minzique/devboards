import { Job, RemoteType } from "@/types/job";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDistanceToNow } from "date-fns";
import { useAppliedJobs } from "@/contexts/AppliedJobsContext"; // Update import path

const getRemoteTypeLabel = (type: number): string => {
  switch (Number(type)) {  // I didn't know TS was so strict about this
    case RemoteType.REMOTE:  // 0
      return "Remote";
    case RemoteType.HYBRID:  // 1
      return "Hybrid";
    case RemoteType.ONSITE:  // 2
      return "On-site";
    default:
      console.log("Unknown remote type:", type);
      return "Unknown";
  }
};

export const JobCard = ({ job_hash, ...props }: Job) => {
  const { appliedJobs, toggleApplied, debug } = useAppliedJobs();
  const isApplied = appliedJobs.has(job_hash);
  const formattedDate = formatDistanceToNow(new Date(props.date_posted), {
    addSuffix: true,
  });
  const salary =
    props.salary_min && props.salary_max ? `$${props.salary_min}K - $${props.salary_max}K` : null;

  let logo = null;
  if (props.company_logo)
    logo = `/logos/${props.company.toLowerCase()}.png`;
  
  
  return (
    <div className="bg-white rounded-lg p-6 border border-gray-200 hover:border-gray-500 transition-all flex flex-col h-full">
      {/* Top content */}
      <div>
        <div className="flex justify-between items-start mb-4">
          
          <Badge variant="secondary" className="bg-blue-100 text-blue-800 hover:bg-blue-200">
            {formattedDate}
          </Badge>
          {/* <span className="text-sm text-blue-600">{formattedDate}</span> */}

          {props.is_remote && (
            <Badge
              variant="secondary"
              className="bg-yellow-100 text-yellow-800 hover:bg-yellow-200"
            >
              {getRemoteTypeLabel(props.is_remote)}
            </Badge>
          )}
        </div>

        <h3 className="font-semibold text-lg text-gray-900 mb-4">{props.title}</h3>
        {/* <div className="flex items-center border-b ">  </div> */}
      </div>

      {/* Bottom content */}
      <div className="mt-auto">
        <div className="space-y-2 py-4 border-b border-gray-100">
          <div className="flex items-center gap-2 mb-2 border-gray-100">
            {logo ? (
              <a href={props.company_website} target="_blank" rel="noreferrer">
                <img 
                  src={logo} 
                  alt={props.company} 
                  className="h-[27px] w-auto max-w-[75px] max-h-[27px] object-contain rounded" 
                />
              </a>
            ) : (
              <div className="w-5 h-5 bg-gray-100 rounded flex items-center justify-center">
                <span className="text-xs font-medium">{props.company[0]}</span>
              </div>
            )}
            {/* <span className="text-sm text-gray-800">
              {logo ? "- " : ""}
              {props.company}
            </span> */}
          </div>

          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>📍 {props.location}</span>
          </div>
          {salary && (
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span>💰 {salary}</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>⏰ {props.job_type}</span>
          </div>
        </div>

        <div className="flex gap-2 pt-4">
          <Button
            variant="secondary"
            className="w-full"
            onClick={() => window.open(props.apply_url, "_blank")}
          >
            Details
          </Button>
          <Button
            variant={isApplied ? "default" : "outline"}
            className={`w-full ${
              isApplied
                ? "bg-yellow-400 hover:bg-yellow-500"
                : "hover:bg-yellow-500 hover:text-white"
            }`}
            onClick={() => {
              toggleApplied(job_hash);
              // Debug current state after toggle
              setTimeout(debug, 0);
            }}
          >
            {isApplied ? "Applied ✓" : "Mark Applied"}
          </Button>
        </div>
      </div>
    </div>
  );
};