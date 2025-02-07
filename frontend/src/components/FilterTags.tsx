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

const CheckIcon = () => (
  <svg className="w-3 h-3 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
  </svg>
);

export const FilterTags = ({ selectedFilters, onFilterChange }: FilterTagsProps) => {
  const handleTimeFilter = (filterId: string) => {
    // Remove any existing time filter
    const currentTimeFilter = selectedFilters.find(f => 
      FILTER_OPTIONS.find(opt => opt.id === f)?.type === 'timePosted'
    );
    
    if (currentTimeFilter) {
      onFilterChange(currentTimeFilter); // Remove old filter
    }
    onFilterChange(filterId); // Add new filter
  };

  const baseButtonClass = "rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-zinc-400 bg-zinc-100 text-zinc-900 hover:bg-zinc-200 border border-zinc-200 px-4 py-2 text-base w-full";
  const baseFilterClass = "flex items-center gap-2 cursor-pointer px-4 py-2 rounded-md";

  return (
    <div className="flex gap-4 lg:gap-6 justify-center lg:items-center pb-6">
      <div className="lg:hidden">
        <button className={baseButtonClass}>Filter</button>
      </div>

      <div className="hidden lg:block">
        <div className="flex flex-col gap-1 flex-1 w-full">
          <input
            type="text"
            placeholder="Filter e.g., skill, company"
            className="rounded-lg border border-zinc-200 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-zinc-400 h-10 px-3 py-2 text-base min-w-60 w-full bg-lime-50"
          />
        </div>
      </div>

      <div className="hidden lg:block">
        <div className="flex gap-2">
          {FILTER_OPTIONS.filter(f => f.type === "workType").map(filter => (
            <label
              key={filter.id}
              className={`${baseFilterClass} ${
                selectedFilters.includes(filter.id)
                  ? "border-zinc-600 border-2 bg-amber-300"
                  : "border border-zinc-300 bg-amber-300"
              }`}
            >
              <div className="relative">
                {selectedFilters.includes(filter.id) && <CheckIcon />}
                <input
                  type="checkbox"
                  className="absolute w-0 h-0 opacity-0"
                  checked={selectedFilters.includes(filter.id)}
                  onChange={() => onFilterChange(filter.id)}
                />
              </div>
              <span className="text-sm capitalize select-none">{filter.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="hidden lg:block">
        <div className="flex gap-2">
          <div className="flex gap-2 flex-wrap justify-center">
            {FILTER_OPTIONS.filter(f => f.type === "timePosted").map(filter => (
              <label
                key={filter.id}
                className={`${baseFilterClass} ${
                  selectedFilters.includes(filter.id)
                    ? "border-zinc-600 border-2 bg-blue-100"
                    : "border border-zinc-300 bg-blue-100"
                }`}
              >
                <div className="relative w-4 h-4">
                  <div className="absolute w-4 h-4 rounded-full border-2 border-zinc-600">
                    {selectedFilters.includes(filter.id) && (
                      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-zinc-600" />
                    )}
                  </div>
                  <input
                    type="radio"
                    name="postedAge"
                    className="absolute w-0 h-0 opacity-0"
                    checked={selectedFilters.includes(filter.id)}
                    onChange={() => handleTimeFilter(filter.id)}
                  />
                </div>
                <span className="text-sm capitalize select-none">{filter.label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};