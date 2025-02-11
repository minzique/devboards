import { Job, isWithinTimeframe, matchesRemoteFilter } from "@/types/job";
import { JobCard } from "./JobCard";
import { FilterTags } from "./FilterTags";
import { useState, useMemo } from "react";

interface JobListProps {
  jobs: Job[];
}

export const JobList = ({ jobs }: JobListProps) => {
  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredJobs = useMemo(() => {
    return jobs.filter(job => {
      // Apply remote type filters
      const remoteFilter = selectedFilters.find(f => ["remote", "hybrid", "office"].includes(f));
      if (remoteFilter && !matchesRemoteFilter(job, remoteFilter)) {
        return false;
      }

      // Apply time filters
      const timeFilter = selectedFilters.find(f => ["24h", "3d", "30d"].includes(f));
      if (timeFilter && !isWithinTimeframe(job.date_posted, timeFilter)) {
        return false;
      }

      // Apply search filter
      if (searchQuery) {
        const searchLower = searchQuery.toLowerCase();
        return (
          job.title.toLowerCase().includes(searchLower) ||
          job.company.toLowerCase().includes(searchLower) ||
          job.description.toLowerCase().includes(searchLower)
        );
      }

      return true;
    });
  }, [jobs, selectedFilters, searchQuery]);

  const handleFilterChange = (filterId: string) => {
    setSelectedFilters(prev => {
      if (prev.includes(filterId)) {
        return prev.filter(f => f !== filterId);
      }
      return [...prev, filterId];
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4">
      <FilterTags 
        selectedFilters={selectedFilters} 
        onFilterChange={handleFilterChange}
        onSearch={setSearchQuery}
        searchQuery={searchQuery}
      />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredJobs.map(job => (
          <JobCard key={job.job_hash} {...job} />
        ))}
      </div>
    </div>
  );
};
