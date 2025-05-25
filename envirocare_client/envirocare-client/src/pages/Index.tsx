
import { Button } from "@/components/ui/button";
import Header from "@/components/Header";
import { ArrowRight, CheckCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Index() {
  const navigate = useNavigate();
  
  const features = [
    "Real-time complaint tracking",
    "Efficient task management",
    "Progress monitoring",
    "Instant notifications",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-secondary/50 to-white">
      <Header />
      
      <main className="pt-24">
        {/* Hero Section */}
        <section className="container mx-auto px-6 py-12 md:py-24">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 leading-tight">
              Environmental Care
              <span className="text-primary block mt-2">Made Simple</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Streamline environmental issue reporting and management with our comprehensive platform designed for organizations like ZIMWA and EMA.
            </p>
            <div className="flex justify-center gap-4">
              <Button
                onClick={() => navigate("/login")}
                className="bg-primary hover:bg-primary/90 text-white px-8 py-6 text-lg group"
              >
                Access Portal
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-6 py-24 bg-white/50 backdrop-blur-sm rounded-3xl my-12">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">
              Everything you need to manage environmental concerns
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="flex items-start space-x-4 p-6 rounded-xl card-hover glass-effect"
                >
                  <CheckCircle className="h-6 w-6 text-primary flex-shrink-0" />
                  <div>
                    <h3 className="font-semibold text-xl mb-2">{feature}</h3>
                    <p className="text-gray-600">
                      Streamline your environmental management processes with our intuitive platform.
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
