import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import Header from "@/components/Header";
import { config } from "@/config";
import axios from "axios";
export default function Login() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);

  //   const onSubmit = async (data: FormValues) => {
  //     setLoading(true);
  //     const credentials = {
  //         email: data.email,
  //         password: data.password,
  //     };
  //     const authUrl = `${import.meta.env.VITE_BACKEND_URL}/login/`;

  //     try {
  //         const response = await axios.post(authUrl, credentials, {
  //             headers: {
  //                 'Content-Type': 'application/json',
  //             },
  //         });

  //         if (response.status === 200) {
  //             let user_url = `${import.meta.env.VITE_BACKEND_URL}/get-user-data`;
  //             const user_response = await axios.get(user_url);
  //             dispatch(authSlice.actions.loginSuccess(user_response.data));

  //             toast({
  //                 title: 'Login successful',
  //                 description: 'Welcome back to the dashboard!',
  //             });

  //             navigate('/dashboard', { replace: true });
  //         }
  //     } catch (error) {
  //         if (axios.isAxiosError(error)) {
  //             const errorMessage = error.response?.status === 400 ? error.response.data.error : 'Something went wrong. Please try again.';

  //             toast({
  //                 title: 'Login failed',
  //                 description: errorMessage,
  //                 variant: 'destructive',
  //             });
  //         }
  //     } finally {
  //         setLoading(false);
  //     }
  // };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const email = (e.target as HTMLFormElement).email.value;
    const password = (e.target as HTMLFormElement).password.value;
    try {
      const response = await axios.post(`${config.api.baseUrl}token/`, {
        username:email,
        password,
      });
      if (response.status === 200) {
        navigate("/dashboard");
        toast({
          title: "Welcome back!",
          description: "You have successfully logged in.",
        });
      } else {
        toast({
          title: "Login failed",
          description: "Invalid email or password.",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.log(error);
      toast({
        title: "Login failed",
        description: error.response.data.error,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-secondary/50 to-white">
      <Header />

      <div className="container mx-auto px-6 py-24">
        <div className="max-w-md mx-auto glass-effect rounded-2xl p-8">
          <h2 className="text-3xl font-bold text-center mb-8">Portal Login</h2>
          <form onSubmit={handleLogin} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">
                Email
              </label>
              <Input
                id="email"
                type="email"
                placeholder="organization@example.com"
                required
                className="w-full"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                required
                className="w-full"
              />
            </div>
            <Button
              type="submit"
              className="w-full bg-primary hover:bg-primary/90"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
