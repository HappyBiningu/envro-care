import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { config } from "@/config";
import { type Task } from "./useTasks";

type TasksResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Task[];
};

export function useFilteredTasks(status: Task["status"]) {
  return useQuery({
    queryKey: ["tasks", status],
    queryFn: async () => {
      const response = await axios.get<TasksResponse>(
        `${config.api.baseUrl}tasks`,
        {
          params: {
            status,
          },
        }
      );
      return response.data;
    },
  });
}
