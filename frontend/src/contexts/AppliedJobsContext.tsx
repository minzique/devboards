import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';

const STORAGE_KEY = 'applied_jobs';

interface AppliedJobsContextType {
  appliedJobs: Set<string>;
  toggleApplied: (jobHash: string) => void;
  debug: () => void;
}

const AppliedJobsContext = createContext<AppliedJobsContextType | null>(null);

export function AppliedJobsProvider({ children }: { children: ReactNode }) {
  const [appliedJobs, setAppliedJobs] = useState<Set<string>>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      console.log('Initial stored value:', stored);
      const parsed = stored ? JSON.parse(stored) : [];
      console.log('Parsed stored value:', parsed);
      const set = new Set(parsed);
      console.log('Initial Set:', Array.from(set));
      return set;
    } catch (e) {
      console.error('Error reading stored jobs:', e);
      return new Set();
    }
  });

  useEffect(() => {
    console.log('Saving to localStorage:', Array.from(appliedJobs));
    localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(appliedJobs)));
  }, [appliedJobs]);

  const toggleApplied = useCallback((jobHash: string) => {
    console.log('Toggle called with hash:', jobHash);
    console.log('Current state before toggle:', Array.from(appliedJobs));
    
    setAppliedJobs(prev => {
      const newSet = new Set(prev);
      const hasJob = newSet.has(jobHash);
      console.log('Has job already:', hasJob);
      
      if (hasJob) {
        newSet.delete(jobHash);
        console.log('Job removed');
      } else {
        newSet.add(jobHash);
        console.log('Job added');
      }
      
      console.log('New state:', Array.from(newSet));
      return newSet;
    });
  }, []);

  const debug = useCallback(() => {
    console.log('Current applied jobs:', Array.from(appliedJobs));
    console.log('localStorage value:', localStorage.getItem(STORAGE_KEY));
  }, [appliedJobs]);

  const value = {
    appliedJobs,
    toggleApplied,
    debug
  };

  return (
    <AppliedJobsContext.Provider value={value}>
      {children}
    </AppliedJobsContext.Provider>
  );
}

export function useAppliedJobs() {
  const context = useContext(AppliedJobsContext);
  if (!context) {
    throw new Error('useAppliedJobs must be used within an AppliedJobsProvider');
  }
  return context;
}
