import { useState, useEffect } from 'react';

const STORAGE_KEY = 'applied_jobs';

export const useAppliedJobs = () => {
  const [appliedJobs, setAppliedJobs] = useState<Set<string>>(new Set());

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      setAppliedJobs(new Set(JSON.parse(stored)));
    }
  }, []);

  const toggleApplied = (jobHash: string) => {
    setAppliedJobs(prev => {
      const newSet = new Set(prev);
      if (newSet.has(jobHash)) {
        newSet.delete(jobHash);
      } else {
        newSet.add(jobHash);
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...newSet]));
      return newSet;
    });
  };

  return { appliedJobs, toggleApplied };
};
