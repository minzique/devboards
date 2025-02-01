import { Search } from "lucide-react";

interface SearchBarProps {
  onSearch: (query: string, location: string) => void;
}

export const SearchBar = ({ onSearch }: SearchBarProps) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const query = (form.elements.namedItem("query") as HTMLInputElement).value;
    const location = (form.elements.namedItem("location") as HTMLInputElement).value;
    onSearch(query, location);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-4xl mx-auto">
      <div className="flex gap-4 p-4 bg-white rounded-lg shadow-sm border border-card-border">
        <div className="flex-1">
          <input
            type="text"
            name="query"
            placeholder="Position, title, keywords"
            className="w-full px-4 py-2 rounded-md border border-card-border focus:outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>
        <div className="flex-1">
          <input
            type="text"
            name="location"
            placeholder="Location"
            className="w-full px-4 py-2 rounded-md border border-card-border focus:outline-none focus:ring-2 focus:ring-primary/20"
          />
        </div>
        <button
          type="submit"
          className="px-6 py-2 bg-secondary text-white rounded-md hover:bg-secondary/90 transition-colors flex items-center gap-2"
        >
          <Search size={20} />
          <span>Search</span>
        </button>
      </div>
    </form>
  );
};