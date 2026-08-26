import { format, isToday, isTomorrow, parseISO } from "date-fns";

interface Props {
  dates: string[];
  selected: string;
  onSelect: (date: string) => void;
}

function label(dateStr: string) {
  const d = parseISO(dateStr);
  if (isToday(d)) return "Today";
  if (isTomorrow(d)) return "Tomorrow";
  return format(d, "EEE");
}

export function DaySelector({ dates, selected, onSelect }: Props) {
  return (
    <div className="scrollbar-none -mx-5 flex gap-2 overflow-x-auto px-5 pb-1">
      {dates.map((date) => {
        const active = date === selected;
        const d = parseISO(date);
        return (
          <button
            key={date}
            onClick={() => onSelect(date)}
            className={`flex min-w-[64px] flex-col items-center rounded-xl border px-3 py-2 transition-colors ${
              active
                ? "border-ink-900 bg-ink-900 text-canvas shadow-ticket"
                : "border-ink-100 bg-card text-ink-600 hover:border-ink-400"
            }`}
          >
            <span className="font-mono text-[10px] uppercase tracking-wider opacity-80">
              {label(date)}
            </span>
            <span className="font-display text-lg font-semibold leading-tight">
              {format(d, "d")}
            </span>
          </button>
        );
      })}
    </div>
  );
}
