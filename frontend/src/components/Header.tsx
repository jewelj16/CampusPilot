import { UtensilsCrossed } from "lucide-react";

export function Header() {
  return (
    <header className="border-b border-ink-100 bg-card">
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
        <div className="text-right">
          <p className="text-sm font-medium text-ink-900">Aditi Rao</p>
          <p className="font-mono text-[11px] text-ink-400">CS21B045 &middot; Hostel A</p>
        </div>
      </div>
    </header>
  );
}
