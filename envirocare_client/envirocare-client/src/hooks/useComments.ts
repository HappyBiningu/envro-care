import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { config } from "@/config";
import { useToast } from "@/components/ui/use-toast";

export type Comment = {
  id: string;
  ref: string | null;
  description: string;
  commented_by_name: string;
  commented_by_number: string;
  created_at: string;
  updated_at: string;
  replies?: Comment[];
};

type CommentsResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Comment[];
};

export function useComments() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  const query = useQuery({
    queryKey: ["comments"],
    queryFn: async () => {
      const response = await axios.get<CommentsResponse>(
        `${config.api.baseUrl}comments`
      );
      return response.data;
    },
  });

  const addComment = useMutation({
    mutationFn: async (
      comment: Omit<Comment, "id" | "created_at" | "updated_at">
    ) => {
      const response = await axios.post<Comment>(
        `${config.api.baseUrl}comments`,
        comment
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["comments"] });
      toast({
        title: "Comment Added",
        description: "Your comment has been added successfully.",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to add comment. Please try again.",
        variant: "destructive",
      });
      console.error("Error adding comment:", error);
    },
  });

  const addReply = useMutation({
    mutationFn: async ({
      parentId,
      reply,
    }: {
      parentId: string;
      reply: Omit<Comment, "id" | "created_at" | "updated_at">;
    }) => {
      const response = await axios.post<Comment>(
        `${config.api.baseUrl}comments/${parentId}/replies`,
        reply
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["comments"] });
      toast({
        title: "Reply Added",
        description: "Your reply has been added successfully.",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to add reply. Please try again.",
        variant: "destructive",
      });
      console.error("Error adding reply:", error);
    },
  });

  return {
    ...query,
    addComment,
    addReply,
  };
}
