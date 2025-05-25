import { useTasks, type Task } from "@/hooks/useTasks";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

export default function TaskBoard() {
  const { data, isLoading, error, updateStatus } = useTasks();

  const handleDragStart = (e: React.DragEvent, taskId: string) => {
    e.dataTransfer.setData("taskId", taskId);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent, targetStatus: string) => {
    e.preventDefault();
    const taskId = e.dataTransfer.getData("taskId");
    updateStatus.mutate({ taskId, status: targetStatus as Task["status"] });
  };

  const getTasksByStatus = (status: string) =>
    data?.results.filter((task) => task.status === status) || [];

  const renderColumn = (status: string, title: string) => (
    <div
      className="task-column"
      onDragOver={handleDragOver}
      onDrop={(e) => handleDrop(e, status)}
    >
      <h3 className="font-semibold mb-4">{title}</h3>
      <div className="space-y-4">
        {isLoading
          ? // Loading skeleton
            Array.from({ length: 3 }).map((_, i) => (
              <Card key={i} className="task-card">
                <CardHeader className="p-4 pb-2">
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-full" />
                </CardHeader>
                <CardContent className="p-4 pt-2">
                  <Skeleton className="h-5 w-20" />
                </CardContent>
              </Card>
            ))
          : getTasksByStatus(status).map((task) => (
              <Card
                key={task.id}
                className="task-card"
                draggable
                onDragStart={(e) => handleDragStart(e, task.id)}
              >
                <CardHeader className="p-4 pb-2">
                  <CardTitle className="text-lg">{task.report_ref}</CardTitle>
                  <CardDescription>{task.description}</CardDescription>
                </CardHeader>
                <CardContent className="p-4 pt-2">
                  <Badge
                    variant={
                      task.severity === "HIGH"
                        ? "destructive"
                        : task.severity === "MEDIUM"
                        ? "default"
                        : "secondary"
                    }
                  >
                    {task.severity}
                  </Badge>
                </CardContent>
              </Card>
            ))}
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {renderColumn("PENDING", "Pending")}
      {renderColumn("IN_PROGRESS", "In Progress")}
      {renderColumn("COMPLETED", "Completed")}
    </div>
  );
}
