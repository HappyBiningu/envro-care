import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { config } from "@/config";

export type Organisation = {
  id: string;
  name: string;
  description: string;
  phone: string;
  email: string;
  address: string;
  created_at: string;
  updated_at: string;
  approved: boolean;
};

export type Report = {
  id: string;
  organisation: Organisation;
  ref: string;
  description: string;
  location: string;
  notes: string | null;
  affected_area: string;
  environmental_impact: string;
  severity: "LOW" | "MEDIUM" | "HIGH";
  is_resolved: boolean;
  reported_by_name: string;
  reported_by_number: string;
  resolved_date: string | null;
  created_at: string;
  updated_at: string;
};

type ReportsResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Report[];
};

export function useReports() {
  return useQuery({
    queryKey: ["complaints"],
    queryFn: async () => {
      const response = await axios.get<ReportsResponse>(
        `${config.api.baseUrl}complaints`
      );
      return response.data;
    },
  });
}

export function useReport(id: string) {
  return useQuery({
    queryKey: ["complaints", id],
    queryFn: async () => {
      const response = await axios.get<Report>(
        `${config.api.baseUrl}complaints/${id}`
      );
      return response.data;
    },
    enabled: !!id,
  });
}
