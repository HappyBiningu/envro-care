import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import TaskManagement from "./pages/tasks/TaskManagement";
import PendingTasks from "./pages/tasks/PendingTasks";
import InProgressTasks from "./pages/tasks/InProgressTasks";
import CompletedTasks from "./pages/tasks/CompletedTasks";
import TaskComments from "./pages/tasks/TaskComments";
import Reports from "./pages/reports/Reports";
import ReportDetails from "./pages/reports/ReportDetails";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/tasks" element={<TaskManagement />} />
          <Route path="/dashboard/pending" element={<PendingTasks />} />
          <Route path="/dashboard/in-progress" element={<InProgressTasks />} />
          <Route path="/dashboard/completed" element={<CompletedTasks />} />
          <Route path="/dashboard/comments" element={<TaskComments />} />
          <Route path="/dashboard/reports" element={<Reports />} />
          <Route path="/dashboard/reports/:id" element={<ReportDetails />} />
          <Route path="/dashboard/profile" element={<Profile />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
