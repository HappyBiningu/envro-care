import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import TopNav from "@/components/TopNav";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useTasks } from "@/hooks/useTasks";
import { Task } from "@/hooks/useTasks";
import {
  DragDropContext,
  Droppable,
  Draggable,
  DropResult,
} from "@hello-pangea/dnd";
import { useToast } from "@/components/ui/use-toast";
import TaskUpdateModal from "@/components/TaskUpdateModal";

const columns = [
  {
    id: "PENDING",
    title: "Pending",
    color: "bg-yellow-100 text-yellow-800",
  },
  {
    id: "IN_PROGRESS",
    title: "In Progress",
    color: "bg-blue-100 text-blue-800",
  },
  {
    id: "COMPLETED",
    title: "Completed",
    color: "bg-green-100 text-green-800",
  },
];

export default function TaskManagement() {
  const { data, isLoading, updateStatus } = useTasks();
  const { toast } = useToast();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [newStatus, setNewStatus] = useState<Task["status"]>("PENDING");
  const [isUpdating, setIsUpdating] = useState(false);

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const taskId = result.draggableId;
    const newStatus = result.destination.droppableId as Task["status"];
    const task = data?.results.find((t) => t.id === taskId);

    if (task && task.status !== newStatus) {
      setSelectedTask(task);
      setNewStatus(newStatus);
      setIsModalOpen(true);
    }
  };

  const handleStatusUpdate = async (notes: string) => {
    if (!selectedTask) return;

    setIsUpdating(true);
    try {
      await updateStatus.mutateAsync({
        taskId: selectedTask.id,
        status: newStatus,
      });

      toast({
        title: "Success",
        description: "Task status updated successfully",
      });
      setIsModalOpen(false);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update task status",
        variant: "destructive",
      });
    } finally {
      setIsUpdating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <div className="pl-64">
          <TopNav />
          <main className="container mx-auto px-6 py-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {columns.map((column) => (
                <Card key={column.id}>
                  <CardHeader>
                    <CardTitle className="text-lg">{column.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {[1, 2, 3].map((i) => (
                        <div
                          key={i}
                          className="h-24 bg-gray-100 rounded-lg animate-pulse"
                        />
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </main>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="pl-64">
        <TopNav />
        <main className="container mx-auto px-6 py-8">
          <DragDropContext onDragEnd={handleDragEnd}>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {columns.map((column) => (
                <Card key={column.id}>
                  <CardHeader>
                    <CardTitle className="text-lg">{column.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Droppable droppableId={column.id}>
                      {(provided) => (
                        <div
                          {...provided.droppableProps}
                          ref={provided.innerRef}
                          className="space-y-4"
                        >
                          {data?.results
                            .filter((task) => task.status === column.id)
                            .map((task, index) => (
                              <Draggable
                                key={task.id}
                                draggableId={task.id}
                                index={index}
                              >
                                {(provided) => (
                                  <div
                                    ref={provided.innerRef}
                                    {...provided.draggableProps}
                                    {...provided.dragHandleProps}
                                    className="bg-white p-4 rounded-lg shadow-sm border border-gray-200"
                                  >
                                    <div className="flex items-center justify-between mb-2">
                                      <Badge
                                        className={`${column.color} font-medium`}
                                      >
                                        {task.severity}
                                      </Badge>
                                      <span className="text-sm text-gray-500">
                                        {new Date(
                                          task.created_at
                                        ).toLocaleDateString()}
                                      </span>
                                    </div>
                                    <h3 className="font-medium mb-2">
                                      {task.description}
                                    </h3>
                                    <p className="text-sm text-gray-600 line-clamp-2">
                                      {task.report_ref}
                                    </p>
                                  </div>
                                )}
                              </Draggable>
                            ))}
                          {provided.placeholder}
                        </div>
                      )}
                    </Droppable>
                  </CardContent>
                </Card>
              ))}
            </div>
          </DragDropContext>

          <TaskUpdateModal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            onSubmit={handleStatusUpdate}
            isLoading={isUpdating}
            taskTitle={selectedTask?.description || ""}
            newStatus={newStatus}
          />
        </main>
      </div>
    </div>
  );
}
