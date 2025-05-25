
import { Button } from "@/components/ui/button";
import { useNavigate, useLocation } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();
  const isHome = location.pathname === "/";

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-effect">
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <a href="/" className="text-2xl font-bold text-primary">
              envro-care
            </a>
          </div>
          <div className="flex items-center space-x-4">
            {isHome ? (
              <Button
                onClick={() => navigate("/login")}
                variant="default"
                className="bg-primary hover:bg-primary/90"
              >
                Portal Login
              </Button>
            ) : (
              <Button
                onClick={() => navigate("/")}
                variant="ghost"
                className="hover:bg-primary/10"
              >
                Back to Home
              </Button>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}
