import { useState } from "react";
import { Link } from "react-router-dom";
import Sidebar from "@/components/Sidebar";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import {
  AlertTriangle,
  Building2,
  MapPin,
  User,
  Phone,
  Calendar,
  CheckCircle2,
  XCircle,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { useReports, Report } from "@/hooks/useReports";

const severityColors = {
  LOW: "bg-green-100 text-green-800",
  MEDIUM: "bg-yellow-100 text-yellow-800",
  HIGH: "bg-red-100 text-red-800",
};

export default function ReportsList() {
  const { data, isLoading } = useReports();
  const [filter, setFilter] = useState<"all" | "resolved" | "unresolved">(
    "all"
  );

  const filteredReports = data?.results.filter((report) => {
    if (filter === "all") return true;
    return filter === "resolved" ? report.is_resolved : !report.is_resolved;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="pl-64">
        <main className="container mx-auto px-6 py-8">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3">
              <AlertTriangle className="h-8 w-8 text-red-500" />
              <h1 className="text-3xl font-bold">Environmental Reports</h1>
            </div>
            <div className="flex gap-2">
              <Button
                variant={filter === "all" ? "default" : "outline"}
                onClick={() => setFilter("all")}
              >
                All Reports
              </Button>
              <Button
                variant={filter === "unresolved" ? "default" : "outline"}
                onClick={() => setFilter("unresolved")}
              >
                Unresolved
              </Button>
              <Button
                variant={filter === "resolved" ? "default" : "outline"}
                onClick={() => setFilter("resolved")}
              >
                Resolved
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {isLoading
              ? Array.from({ length: 6 }).map((_, i) => (
                  <Card key={i} className="p-6">
                    <div className="space-y-4">
                      <Skeleton className="h-4 w-24" />
                      <Skeleton className="h-4 w-full" />
                      <Skeleton className="h-4 w-2/3" />
                    </div>
                  </Card>
                ))
              : filteredReports?.map((report) => (
                  <Link
                    key={report.id}
                    to={`/reports/${report.id}`}
                    className="block"
                  >
                    <Card className="p-6 hover:shadow-md transition-shadow">
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <Badge
                              className={`${
                                severityColors[report.severity]
                              } font-medium`}
                            >
                              {report.severity}
                            </Badge>
                            <Badge
                              variant="outline"
                              className={
                                report.is_resolved
                                  ? "text-green-600 border-green-200"
                                  : "text-red-600 border-red-200"
                              }
                            >
                              {report.is_resolved ? (
                                <CheckCircle2 className="h-3 w-3 mr-1" />
                              ) : (
                                <XCircle className="h-3 w-3 mr-1" />
                              )}
                              {report.is_resolved ? "Resolved" : "Unresolved"}
                            </Badge>
                          </div>
                          <span className="text-sm text-gray-500">
                            {formatDistanceToNow(new Date(report.created_at), {
                              addSuffix: true,
                            })}
                          </span>
                        </div>

                        <div>
                          <h3 className="font-semibold text-lg mb-1">
                            {report.description}
                          </h3>
                          <p className="text-sm text-gray-600 line-clamp-2">
                            {report.environmental_impact}
                          </p>
                        </div>

                        <div className="space-y-2 text-sm text-gray-500">
                          <div className="flex items-center gap-2">
                            <Building2 className="h-4 w-4" />
                            <span>{report.organisation.name}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <MapPin className="h-4 w-4" />
                            <span>{report.location}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <User className="h-4 w-4" />
                            <span>{report.reported_by_name}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Phone className="h-4 w-4" />
                            <span>{report.reported_by_number}</span>
                          </div>
                        </div>

                        <div className="pt-4 border-t">
                          <Button variant="outline" className="w-full">
                            View Details
                          </Button>
                        </div>
                      </div>
                    </Card>
                  </Link>
                ))}
          </div>
        </main>
      </div>
    </div>
  );
}
