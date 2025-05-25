import { Link, useLocation, useNavigate } from "react-router-dom";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  ListChecks,
  Clock,
  CheckCircle,
  KanbanSquare,
  MessageCircle,
  AlertTriangle,
  LogOut,
} from "lucide-react";

const menuItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    title: "Task Management",
    icon: KanbanSquare,
    path: "/dashboard/tasks",
  },
  {
    title: "Pending Tasks",
    icon: ListChecks,
    path: "/dashboard/pending",
  },
  {
    title: "In Progress",
    icon: Clock,
    path: "/dashboard/in-progress",
  },
  {
    title: "Completed",
    icon: CheckCircle,
    path: "/dashboard/completed",
  },
  {
    title: "Comments",
    icon: MessageCircle,
    path: "/dashboard/comments",
  },
  {
    title: "Reports",
    icon: AlertTriangle,
    path: "/dashboard/reports",
  },
];

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    // Add your logout logic here
    navigate("/login");
  };

  return (
    <div className="h-screen w-64 bg-white border-r border-gray-200 fixed left-0 top-0 p-4 flex flex-col">
      <div className="flex items-center gap-2 px-2 mb-8 mt-2">
        <span className="text-xl font-bold text-primary">envro-care</span>
      </div>
      <nav className="space-y-1 flex-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-gray-600 hover:bg-gray-100"
              )}
            >
              <Icon className="h-5 w-5" />
              {item.title}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto pt-4 border-t">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium text-red-600 hover:bg-red-50 w-full transition-colors"
        >
          <LogOut className="h-5 w-5" />
          Logout
        </button>
      </div>
    </div>
  );
}
