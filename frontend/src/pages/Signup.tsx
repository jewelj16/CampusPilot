import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authApi } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { UserPlus, Loader2 } from "lucide-react";

export function Signup() {
  const [name, setName] = useState("");
  const [rollNo, setRollNo] = useState("");
  const [hostel, setHostel] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await authApi.signup({ name, roll_no: rollNo, hostel, password });
      login(data.access_token);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-ink-50 p-4">
      <div className="w-full max-w-md overflow-hidden rounded-xl bg-white shadow-xl shadow-ink-200/20 ring-1 ring-ink-100">
        <div className="bg-ink-900 p-8 text-white">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-mustard text-ink-900">
              <UserPlus size={24} strokeWidth={2.5} />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">CampusPilot</h1>
              <p className="font-mono text-sm text-ink-300">New Registration</p>
            </div>
          </div>
        </div>
        
        <div className="ticket-perforation-top p-8">
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            {error && (
              <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600 ring-1 ring-inset ring-red-600/20">
                {error}
              </div>
            )}
            
            <div className="flex flex-col gap-1.5">
              <label className="font-mono text-[11px] font-semibold uppercase tracking-wider text-ink-400">
                Full Name
              </label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="rounded-lg border-0 bg-ink-50 px-4 py-3 text-ink-900 ring-1 ring-inset ring-ink-200 transition-shadow focus:bg-white focus:ring-2 focus:ring-inset focus:ring-mustard sm:text-sm"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="font-mono text-[11px] font-semibold uppercase tracking-wider text-ink-400">
                Roll Number
              </label>
              <input
                type="text"
                required
                value={rollNo}
                onChange={(e) => setRollNo(e.target.value)}
                className="rounded-lg border-0 bg-ink-50 px-4 py-3 text-ink-900 ring-1 ring-inset ring-ink-200 transition-shadow focus:bg-white focus:ring-2 focus:ring-inset focus:ring-mustard sm:text-sm"
              />
            </div>
            
            <div className="flex flex-col gap-1.5">
              <label className="font-mono text-[11px] font-semibold uppercase tracking-wider text-ink-400">
                Hostel
              </label>
              <input
                type="text"
                required
                value={hostel}
                onChange={(e) => setHostel(e.target.value)}
                placeholder="e.g. Hostel A"
                className="rounded-lg border-0 bg-ink-50 px-4 py-3 text-ink-900 ring-1 ring-inset ring-ink-200 transition-shadow focus:bg-white focus:ring-2 focus:ring-inset focus:ring-mustard sm:text-sm"
              />
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="font-mono text-[11px] font-semibold uppercase tracking-wider text-ink-400">
                Password
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="rounded-lg border-0 bg-ink-50 px-4 py-3 text-ink-900 ring-1 ring-inset ring-ink-200 transition-shadow focus:bg-white focus:ring-2 focus:ring-inset focus:ring-mustard sm:text-sm"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-2 flex w-full items-center justify-center gap-2 rounded-lg bg-mustard px-4 py-3 font-mono text-sm font-semibold uppercase tracking-wider text-ink-900 transition-colors hover:bg-mustard-600 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {loading ? <Loader2 size={18} className="animate-spin" /> : "Sign Up"}
            </button>
          </form>

          <div className="mt-6 text-center font-mono text-xs text-ink-400">
            Already have an account?{" "}
            <Link to="/login" className="font-medium text-ink-900 underline underline-offset-2 hover:text-mustard-700">
              Log in instead
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
