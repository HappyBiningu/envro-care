import { useParams } from "react-router-dom";
import Sidebar from "@/components/Sidebar";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  AlertTriangle,
  Building2,
  MapPin,
  User,
  Phone,
  Calendar,
  CheckCircle2,
  XCircle,
  Mail,
  Globe,
  ArrowLeft,
} from "lucide-react";
import { formatDistanceToNow, format } from "date-fns";
import { useReport } from "@/hooks/useReports";

const severityColors = {
  LOW: "bg-green-100 text-green-800",
  MEDIUM: "bg-yellow-100 text-yellow-800",
  HIGH: "bg-red-100 text-red-800",
};

export default function ReportDetails() {
  const { id } = useParams<{ id: string }>();
  const { data: report, isLoading } = useReport(id || "");

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <div className="pl-64">
          <main className="container mx-auto px-6 py-8">
            <div className="space-y-6">
              <Skeleton className="h-8 w-64" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-2/3" />
            </div>
          </main>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <div className="pl-64">
          <main className="container mx-auto px-6 py-8">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900">
                Report not found
              </h1>
              <p className="mt-2 text-gray-600">
                The report you're looking for doesn't exist or has been removed.
              </p>
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
        <main className="container mx-auto px-6 py-8">
          <div className="mb-8">
            <Button
              variant="ghost"
              className="mb-4"
              onClick={() => window.history.back()}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Reports
            </Button>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertTriangle className="h-8 w-8 text-red-500" />
                <h1 className="text-3xl font-bold">Report Details</h1>
              </div>
              <div className="flex items-center gap-2">
                <Badge
                  className={`${severityColors[report.severity]} font-medium`}
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
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-6">
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-6">
                    <div>
                      <h2 className="text-xl font-semibold mb-2">
                        {report.description}
                      </h2>
                      <p className="text-gray-600 whitespace-pre-wrap">
                        {report.environmental_impact}
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <h3 className="font-medium text-gray-900">Location</h3>
                        <div className="flex items-center gap-2 text-gray-600">
                          <MapPin className="h-4 w-4" />
                          <span>{report.location}</span>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <h3 className="font-medium text-gray-900">
                          Affected Area
                        </h3>
                        <p className="text-gray-600">{report.affected_area}</p>
                      </div>
                    </div>

                    {report.notes && (
                      <div className="space-y-2">
                        <h3 className="font-medium text-gray-900">Notes</h3>
                        <p className="text-gray-600">{report.notes}</p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold mb-4">
                    Reporter Details
                  </h3>
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 text-gray-600">
                      <User className="h-4 w-4" />
                      <span>{report.reported_by_name}</span>
                    </div>
                    <div className="flex items-center gap-2 text-gray-600">
                      <Phone className="h-4 w-4" />
                      <span>{report.reported_by_number}</span>
                    </div>
                    <div className="flex items-center gap-2 text-gray-600">
                      <Calendar className="h-4 w-4" />
                      <span>
                        Reported{" "}
                        {formatDistanceToNow(new Date(report.created_at), {
                          addSuffix: true,
                        })}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              <Card>
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold mb-4">
                    Organisation Details
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-900">
                        {report.organisation.name}
                      </h4>
                      <p className="text-sm text-gray-600">
                        {report.organisation.description}
                      </p>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-gray-600">
                        <Phone className="h-4 w-4" />
                        <span>{report.organisation.phone}</span>
                      </div>
                      <div className="flex items-center gap-2 text-gray-600">
                        <Mail className="h-4 w-4" />
                        <span>{report.organisation.email}</span>
                      </div>
                      <div className="flex items-center gap-2 text-gray-600">
                        <Globe className="h-4 w-4" />
                        <span className="whitespace-pre-line">
                          {report.organisation.address}
                        </span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold mb-4">Report Details</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Reference Number</span>
                      <span className="font-medium">{report.ref}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Created</span>
                      <span className="font-medium">
                        {format(new Date(report.created_at), "PPP")}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Last Updated</span>
                      <span className="font-medium">
                        {format(new Date(report.updated_at), "PPP")}
                      </span>
                    </div>
                    {report.resolved_date && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Resolved Date</span>
                        <span className="font-medium">
                          {format(new Date(report.resolved_date), "PPP")}
                        </span>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
