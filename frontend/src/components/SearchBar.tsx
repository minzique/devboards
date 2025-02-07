import { Search } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

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
    <form onSubmit={handleSubmit} className="w-full max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row gap-2 md:gap-4 p-2 pb-0 bg-white rounded-lg shadow-sm border-card-border">
        <div className="w-full">
          <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-1">
            Position, title, keywords
          </label>
          <Input
            type="text"
            id="query"
            name="query"
            placeholder="Enter search terms (e.g., Java, React, Nodejs)"
            className="w-full"
          />
        </div>
        <div className="w-full">
          <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-1">
            Location
          </label>
          <Input
            type="text"
            id="location"
            name="location"
            placeholder="Location (e.g., San Francisco, CA)"
            className="w-full"
          />
        </div>
        <div className="w-full md:w-auto">
          <div className="h-[1.125rem] mb-1 md:block hidden"></div>
          <Button type="submit" variant="secondary" size="lg" className="w-full md:w-auto h-[42px]">
            Search
          </Button>
        </div>
      </div>
    </form>
  );
};