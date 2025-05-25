import Sidebar from "@/components/Sidebar";
import TopNav from "@/components/TopNav";
import Stats from "@/components/Stats";
import { Card } from "@/components/ui/card";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const tasksByMonth = [
  { month: "Jan", completed: 45, pending: 20, inProgress: 15 },
  { month: "Feb", completed: 38, pending: 25, inProgress: 18 },
  { month: "Mar", completed: 52, pending: 15, inProgress: 12 },
  { month: "Apr", completed: 40, pending: 22, inProgress: 20 },
];

const taskDistribution = [
  { name: "Water Issues", value: 35 },
  { name: "Air Quality", value: 25 },
  { name: "Waste Management", value: 20 },
  { name: "Noise Pollution", value: 15 },
  { name: "Others", value: 5 },
];

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8"];

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="pl-64">
        <TopNav />
        <main className="container mx-auto px-6 py-8">
          <div className="space-y-8">
            <div>
              <h1 className="text-3xl font-bold">Dashboard</h1>
              <p className="text-gray-600 mt-2">
                Overview of environmental tasks and metrics
              </p>
            </div>

            <Stats />

            <div className="grid md:grid-cols-2 gap-6">
              <Card className="p-6">
                <h3 className="text-lg font-semibold mb-4">Tasks Overview</h3>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={tasksByMonth}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Bar
                        dataKey="completed"
                        fill="#22c55e"
                        name="Completed"
                      />
                      <Bar dataKey="pending" fill="#eab308" name="Pending" />
                      <Bar
                        dataKey="inProgress"
                        fill="#3b82f6"
                        name="In Progress"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </Card>

              <Card className="p-6">
                <h3 className="text-lg font-semibold mb-4">
                  Task Distribution
                </h3>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={taskDistribution}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) =>
                          `${name} ${(percent * 100).toFixed(0)}%`
                        }
                      >
                        {taskDistribution.map((entry, index) => (
                          <Cell
                            key={`cell-${index}`}
                            fill={COLORS[index % COLORS.length]}
                          />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
