import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertTriangle, CheckCircle, Clock } from "lucide-react";
import { useTaskStatistics } from "@/hooks/useTaskStatistics";
import { Skeleton } from "@/components/ui/skeleton";

export default function Stats() {
  const { data: stats, isLoading } = useTaskStatistics();

  const statCards = [
    {
      title: "Pending Tasks",
      value: stats?.tasks_pending ?? "0",
      icon: AlertTriangle,
      color: "text-yellow-500",
    },
    {
      title: "In Progress",
      value: stats?.tasks_in_progress ?? "0",
      icon: Clock,
      color: "text-blue-500",
    },
    {
      title: "Completed",
      value: stats?.tasks_completed ?? "0",
      icon: CheckCircle,
      color: "text-green-500",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {statCards.map((stat, index) => {
        const Icon = stat.icon;
        return (
          <Card key={index} className="card-hover">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <Icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <Skeleton className="h-8 w-16" />
              ) : (
                <div className="text-2xl font-bold">{stat.value}</div>
              )}
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
