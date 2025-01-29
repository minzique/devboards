import { useState } from "react";
import { SearchBar } from "@/components/SearchBar";
import { FilterTags } from "@/components/FilterTags";
import { JobCard } from "@/components/JobCard";

// Mock data for initial development
const MOCK_JOBS = [
  {
    id: "1",
    title: "Software Engineer, Product",
    company: "Meta",
    location: "Menlo Park, CA, United States",
    type: "Full-time",
    salary: "$175 - $250K",
    postedAt: "1 minute ago",
    applyUrl: "#",
  },
  {
    id: "2",
    title: "Frontend Engineer",
    company: "Apple",
    location: "Cupertino, CA, United States",
    type: "Full-time",
    salary: "$150 - $220K",
    postedAt: "3 hours ago",
    applyUrl: "#",
  },
  {
    id: "3",
    title: "Senior Software Engineer",
    company: "Tesla",
    location: "Palo Alto, CA, United States",
    type: "Full-time",
    salary: "$180 - $260K",
    postedAt: "1 day ago",
    applyUrl: "#",
  },
];

const Index = () => {
  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);
  const [jobs, setJobs] = useState(MOCK_JOBS);

  const handleSearch = (query: string, location: string) => {
    console.log("Searching for:", { query, location });
    // TODO: Implement actual search
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
          <h1 className="text-2xl font-bold text-secondary">JobsFromSpace</h1>
          <button className="px-4 py-2 text-primary-foreground hover:text-primary transition-colors">
            My Jobs
          </button>
        </div>
      </header>

      <main className="container py-8 space-y-6">
        <SearchBar onSearch={handleSearch} />
        
        <div className="max-w-4xl mx-auto">
          <FilterTags
            selectedFilters={selectedFilters}
            onFilterChange={handleFilterChange}
          />
          
          <div className="grid gap-4 mt-6">
            {jobs.map((job) => (
              <JobCard key={job.id} {...job} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;