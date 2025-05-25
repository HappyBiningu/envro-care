import Sidebar from "@/components/Sidebar";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle } from "lucide-react";
import { useFilteredTasks } from "@/hooks/useFilteredTasks";
import { Skeleton } from "@/components/ui/skeleton";

export default function CompletedTasks() {
  const { data, isLoading } = useFilteredTasks("COMPLETED");

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="pl-64">
        <main className="container mx-auto px-6 py-8">
          <div className="flex items-center gap-3 mb-8">
            <CheckCircle className="h-8 w-8 text-green-500" />
            <h1 className="text-3xl font-bold">Completed Tasks</h1>
          </div>

          <div className="grid gap-4">
            {isLoading
              ? // Loading skeleton
                Array.from({ length: 3 }).map((_, i) => (
                  <Card key={i} className="hover:shadow-md transition-shadow">
                    <CardHeader className="flex flex-row items-start justify-between">
                      <div>
                        <Skeleton className="h-6 w-3/4 mb-2" />
                        <Skeleton className="h-4 w-full" />
                      </div>
                      <Skeleton className="h-5 w-20" />
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-1/2" />
                        <Skeleton className="h-4 w-1/3" />
                        <Skeleton className="h-4 w-3/4" />
                      </div>
                    </CardContent>
                  </Card>
                ))
              : data?.results.map((task) => (
                  <Card
                    key={task.id}
                    className="hover:shadow-md transition-shadow"
                  >
                    <CardHeader className="flex flex-row items-start justify-between">
                      <div>
                        <CardTitle>{task.report_ref}</CardTitle>
                        <p className="text-sm text-gray-500 mt-1">
                          {task.description}
                        </p>
                      </div>
                      <Badge
                        variant="secondary"
                        className="bg-green-100 text-green-800"
                      >
                        Completed
                      </Badge>
                    </CardHeader>
                    <CardContent>
                      <div className="text-sm text-gray-600 space-y-2">
                        <p>Organisation: {task.organisation.name}</p>
                        <p>
                          Completed:{" "}
                          {new Date(task.updated_at).toLocaleDateString()}
                        </p>
                        <p className="font-medium">Status: {task.status}</p>
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
