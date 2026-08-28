import { UtensilsCrossed, LogOut } from "lucide-react";
import { useEffect, useState } from "react";
import { authApi } from "../api/client";
import { useAuth } from "../context/AuthContext";

export function Header() {
  const [user, setUser] = useState<any>(null);
  const { logout } = useAuth();

  useEffect(() => {
    authApi.me().then(setUser).catch(() => logout());
  }, [logout]);

  return (
    <header className="border-b border-ink-100 bg-card relative">
      <div className="mx-auto flex max-w-3xl items-center justify-between px-5 py-4">
        <div className="flex items-center gap-2.5">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-ink-900 text-mustard">
            <UtensilsCrossed size={18} strokeWidth={2.25} />
          </span>
          <div className="leading-tight">
            <p className="font-display text-lg font-semibold tracking-tight text-ink-900">
              CampusPilot
            </p>
            <p className="font-mono text-[11px] uppercase tracking-wider text-ink-400">
              Mess Registration
            </p>
          </div>
        </div>
        <div className="flex items-center gap-4 text-right">
          {user ? (
            <div>
              <p className="text-sm font-medium text-ink-900">{user.name}</p>
              <p className="font-mono text-[11px] text-ink-400">{user.roll_no} &middot; {user.hostel}</p>
            </div>
          ) : (
            <div className="h-8 w-24 animate-pulse rounded bg-ink-100"></div>
          )}
          <button
            onClick={logout}
            className="rounded-lg p-2 text-ink-400 transition-colors hover:bg-red-50 hover:text-red-600"
            title="Log out"
          >
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </header>
  );
}
