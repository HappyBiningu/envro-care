import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { config } from "@/config";

export type TaskStatistics = {
  tasks_pending: number;
  tasks_in_progress: number;
  tasks_completed: number;
  total_tasks: number;
};

export function useTaskStatistics() {
  return useQuery({
    queryKey: ["task-statistics"],
    queryFn: async () => {
      const response = await axios.get<TaskStatistics>(
        `${config.api.baseUrl}tasks/statistics/`
      );
      return response.data;
    },
  });
}
