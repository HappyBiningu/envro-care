import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { config } from "@/config";
import { useToast } from "@/components/ui/use-toast";

export type Task = {
  id: string;
  organisation: {
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
  description: string;
  report_ref: string;
  severity: "LOW" | "MEDIUM" | "HIGH";
  status: "PENDING" | "IN_PROGRESS" | "COMPLETED";
  created_at: string;
  updated_at: string;
};

type TasksResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Task[];
};

export function useTasks() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  const query = useQuery({
    queryKey: ["tasks"],
    queryFn: async () => {
      const response = await axios.get<TasksResponse>(
        `${config.api.baseUrl}tasks`
      );
      return response.data;
    },
  });

  const updateStatus = useMutation({
    mutationFn: async ({
      taskId,
      status,
    }: {
      taskId: string;
      status: Task["status"];
    }) => {
      const response = await axios.patch<Task>(
        `${config.api.baseUrl}tasks/${taskId}`,
        { status }
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      toast({
        title: "Status Updated",
        description: "Task status has been updated successfully.",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to update task status. Please try again.",
        variant: "destructive",
      });
      console.error("Error updating task status:", error);
    },
  });

  return {
    ...query,
    updateStatus,
  };
}
