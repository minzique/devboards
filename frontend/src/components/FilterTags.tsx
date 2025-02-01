interface FilterTag {
  id: string;
  label: string;
  type: "workType" | "timePosted";
}

interface FilterTagsProps {
  selectedFilters: string[];
  onFilterChange: (filterId: string) => void;
}

const FILTER_OPTIONS: FilterTag[] = [
  { id: "remote", label: "Remote", type: "workType" },
  { id: "hybrid", label: "Hybrid", type: "workType" },
  { id: "office", label: "Office", type: "workType" },
  { id: "24h", label: "24 Hours", type: "timePosted" },
  { id: "3d", label: "3 Days", type: "timePosted" },
  { id: "30d", label: "30 Days", type: "timePosted" },
];

export const FilterTags = ({ selectedFilters, onFilterChange }: FilterTagsProps) => {
  return (
    <div className="flex flex-wrap gap-2 my-4">
      {FILTER_OPTIONS.map((filter) => (
        <button
          key={filter.id}
          onClick={() => onFilterChange(filter.id)}
          className={`px-4 py-1.5 rounded-full text-sm transition-colors ${
            selectedFilters.includes(filter.id)
              ? "bg-primary text-primary-foreground"
              : "bg-muted text-muted-foreground hover:bg-muted/80"
          }`}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
};