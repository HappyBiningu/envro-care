import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { useComments, Comment } from "@/hooks/useComments";
import { useReadComments } from "@/hooks/useReadComments";
import { Skeleton } from "@/components/ui/skeleton";
import {
  MessageSquare,
  Send,
  User,
  Phone,
  Calendar,
  Check,
  Reply,
  X,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";

export default function TaskComments() {
  const { data, isLoading, addComment, addReply } = useComments();
  const { markAsRead, isRead } = useReadComments();
  const [newComment, setNewComment] = useState({
    description: "",
    commented_by_name: "",
    commented_by_number: "",
    ref: null,
  });
  const [replyingTo, setReplyingTo] = useState<string | null>(null);
  const [replyForm, setReplyForm] = useState({
    description: "",
    commented_by_name: "",
    commented_by_number: "",
    ref: null,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.description.trim()) return;

    addComment.mutate(newComment);
    setNewComment({
      description: "",
      commented_by_name: "",
      commented_by_number: "",
      ref: null,
    });
  };

  const handleReply = (e: React.FormEvent, parentId: string) => {
    e.preventDefault();
    if (!replyForm.description.trim()) return;

    addReply.mutate({
      parentId,
      reply: {
        ...replyForm,
        commented_by_name: newComment.commented_by_name,
        commented_by_number: newComment.commented_by_number,
      },
    });
    setReplyForm({
      description: "",
      commented_by_name: "",
      commented_by_number: "",
      ref: null,
    });
    setReplyingTo(null);
  };

  const CommentCard = ({
    comment,
    isReply = false,
  }: {
    comment: Comment;
    isReply?: boolean;
  }) => (
    <Card
      key={comment.id}
      className={`p-6 transition-colors ${
        !isRead(comment.id) ? "bg-blue-50" : ""
      } ${isReply ? "ml-8 border-l-4 border-l-blue-200" : ""}`}
    >
      <div className="flex items-start gap-4">
        <div className="h-12 w-12 rounded-full bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center shadow-sm">
          <User className="h-6 w-6 text-blue-600" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div className="flex items-center gap-3">
              <h3 className="font-semibold text-gray-900 truncate">
                {comment.commented_by_name}
              </h3>
              <div className="flex items-center gap-2 text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                <Phone className="h-3.5 w-3.5" />
                <span className="truncate">{comment.commented_by_number}</span>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <Calendar className="h-3.5 w-3.5" />
              <span>
                {formatDistanceToNow(new Date(comment.created_at), {
                  addSuffix: true,
                })}
              </span>
            </div>
          </div>
          <div className="mt-3">
            <p className="text-gray-700 whitespace-pre-wrap">
              {comment.description}
            </p>
          </div>
          <div className="mt-4 flex items-center gap-2">
            {!isRead(comment.id) && (
              <Button
                variant="outline"
                size="sm"
                className="text-blue-600 hover:text-blue-700 hover:bg-blue-50 border-blue-200"
                onClick={() => markAsRead(comment.id)}
              >
                <Check className="h-4 w-4 mr-2" />
                Mark as Read
              </Button>
            )}
            <Button
              variant="outline"
              size="sm"
              className="text-gray-600 hover:text-gray-700 hover:bg-gray-50 border-gray-200"
              onClick={() =>
                setReplyingTo(replyingTo === comment.id ? null : comment.id)
              }
            >
              {replyingTo === comment.id ? (
                <X className="h-4 w-4 mr-2" />
              ) : (
                <Reply className="h-4 w-4 mr-2" />
              )}
              {replyingTo === comment.id ? "Cancel" : "Reply"}
            </Button>
          </div>
        </div>
      </div>

      {replyingTo === comment.id && (
        <form
          onSubmit={(e) => handleReply(e, comment.id)}
          className="mt-6 space-y-4 bg-gray-50 p-4 rounded-lg border border-gray-100"
        >
          <div className="space-y-2">
            <label
              htmlFor={`reply-text-${comment.id}`}
              className="text-sm font-medium text-gray-700"
            >
              Reply
            </label>
            <Textarea
              id={`reply-text-${comment.id}`}
              value={replyForm.description}
              onChange={(e) =>
                setReplyForm({
                  ...replyForm,
                  description: e.target.value,
                })
              }
              placeholder="Write your reply here..."
              className="min-h-[100px] bg-white"
              required
            />
          </div>
          <Button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700"
            disabled={addReply.isPending}
          >
            {addReply.isPending ? (
              "Adding Reply..."
            ) : (
              <>
                <Send className="h-4 w-4 mr-2" />
                Post Reply
              </>
            )}
          </Button>
        </form>
      )}

      {comment.replies?.map((reply: Comment) => (
        <CommentCard key={reply.id} comment={reply} isReply />
      ))}
    </Card>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="pl-64">
        <main className="container mx-auto px-6 py-8">
          <div className="flex items-center gap-3 mb-8">
            <MessageSquare className="h-8 w-8 text-blue-500" />
            <h1 className="text-3xl font-bold">Task Comments</h1>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Comments List */}
            <div className="lg:col-span-2 space-y-6">
              {isLoading
                ? // Loading skeleton
                  Array.from({ length: 3 }).map((_, i) => (
                    <Card key={i} className="p-6">
                      <div className="flex items-start gap-4">
                        <Skeleton className="h-10 w-10 rounded-full" />
                        <div className="flex-1 space-y-3">
                          <div className="flex items-center gap-2">
                            <Skeleton className="h-4 w-24" />
                          </div>
                          <Skeleton className="h-4 w-full" />
                          <Skeleton className="h-4 w-2/3" />
                        </div>
                      </div>
                    </Card>
                  ))
                : data?.results.map((comment) => (
                    <CommentCard key={comment.id} comment={comment} />
                  ))}
            </div>

            {/* Add Comment Form */}
            <div className="lg:col-span-1">
              <Card className="p-6">
                <h2 className="text-xl font-semibold mb-4">Add a Comment</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <label
                      htmlFor="name"
                      className="text-sm font-medium text-gray-700"
                    >
                      Your Name
                    </label>
                    <Input
                      id="name"
                      value={newComment.commented_by_name}
                      onChange={(e) =>
                        setNewComment({
                          ...newComment,
                          commented_by_name: e.target.value,
                        })
                      }
                      placeholder="Enter your name"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <label
                      htmlFor="phone"
                      className="text-sm font-medium text-gray-700"
                    >
                      Phone Number
                    </label>
                    <Input
                      id="phone"
                      value={newComment.commented_by_number}
                      onChange={(e) =>
                        setNewComment({
                          ...newComment,
                          commented_by_number: e.target.value,
                        })
                      }
                      placeholder="Enter your phone number"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <label
                      htmlFor="comment"
                      className="text-sm font-medium text-gray-700"
                    >
                      Comment
                    </label>
                    <Textarea
                      id="comment"
                      value={newComment.description}
                      onChange={(e) =>
                        setNewComment({
                          ...newComment,
                          description: e.target.value,
                        })
                      }
                      placeholder="Write your comment here..."
                      className="min-h-[100px]"
                      required
                    />
                  </div>
                  <Button
                    type="submit"
                    className="w-full"
                    disabled={addComment.isPending}
                  >
                    {addComment.isPending ? (
                      "Adding Comment..."
                    ) : (
                      <>
                        <Send className="h-4 w-4 mr-2" />
                        Post Comment
                      </>
                    )}
                  </Button>
                </form>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
