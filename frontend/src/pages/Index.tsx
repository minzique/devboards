import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { SearchBar } from "@/components/SearchBar";
import { FilterTags } from "@/components/FilterTags";
import { JobCard } from "@/components/JobCard";
import { jobsApi } from "@/services/api";
import type { Job } from "@/types/job";

const Index = () => {
  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchLocation, setSearchLocation] = useState("");

  const {
    data: jobs = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["jobs", searchQuery, searchLocation],
    queryFn: () => jobsApi.getJobs(searchQuery, searchLocation),
    staleTime: 1000 * 60 * 5, // Consider data fresh for 5 minutes
  });

  const handleSearch = (query: string, location: string) => {
    setSearchQuery(query);
    setSearchLocation(location);
  };

  const handleFilterChange = (filterId: string) => {
    setSelectedFilters((prev) =>
      prev.includes(filterId)
        ? prev.filter((id) => id !== filterId)
        : [...prev, filterId]
    );
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-card-border">
        <div className="container py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-secondary">DevBoards</h1>
          <button className="px-4 py-2 text-primary-foreground hover:text-primary transition-colors">
            My Jobs
          </button>
        </div>
      </header>

      <main className="container py-8 space-y-6">
        <SearchBar onSearch={handleSearch} />

        <div className="max-w-7xl mx-auto">
          <FilterTags
            selectedFilters={selectedFilters}
            onFilterChange={handleFilterChange}
          />

          {isLoading && <div>Loading jobs...</div>}
          {error && <div>Error loading jobs</div>}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
            {jobs.map((job) => (
              <JobCard key={job.job_hash} {...job} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
