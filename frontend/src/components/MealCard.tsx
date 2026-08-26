import { format, parseISO } from "date-fns";
import { Check, Loader2, X } from "lucide-react";
import type { Meal } from "../types/mess";

interface Props {
  meal: Meal;
  busy: boolean;
  onRegister: (mealId: string) => void;
  onCancel: (registrationId: string) => void;
}

const MEAL_LABEL: Record<Meal["meal_type"], string> = {
  breakfast: "Breakfast",
  lunch: "Lunch",
  snacks: "Snacks",
  dinner: "Dinner",
};

function DietDot({ isVeg }: { isVeg: boolean }) {
  return (
    <span
      className={`inline-flex h-3 w-3 shrink-0 items-center justify-center border ${
        isVeg ? "border-veg" : "border-nonveg"
      }`}
      title={isVeg ? "Vegetarian" : "Non-vegetarian"}
      aria-hidden
    >
      <span className={`h-1.5 w-1.5 rounded-full ${isVeg ? "bg-veg" : "bg-nonveg"}`} />
    </span>
  );
}

export function MealCard({ meal, busy, onRegister, onCancel }: Props) {
  const isRegistered = meal.registration !== null;
  const cutoff = parseISO(meal.cutoff_at);

  return (
    <div className="flex overflow-hidden rounded-xl border border-ink-100 bg-card shadow-ticket">
      {/* Info side */}
      <div className="flex-1 p-4">
        <div className="flex items-baseline justify-between">
          <h3 className="font-display text-base font-semibold text-ink-900">
            {MEAL_LABEL[meal.meal_type]}
          </h3>
          <span className="font-mono text-[11px] text-ink-400">{meal.mess_name}</span>
        </div>

        <ul className="mt-2.5 space-y-1.5">
          {meal.dishes.map((dish) => (
            <li key={dish.id} className="flex items-center gap-2 text-sm text-ink-600">
              <DietDot isVeg={dish.is_veg} />
              {dish.name}
            </li>
          ))}
        </ul>

        <p className="mt-3 font-mono text-[11px] text-ink-400">
          {meal.is_open
            ? `Closes ${format(cutoff, "h:mm a, d MMM")}`
            : `Closed at ${format(cutoff, "h:mm a, d MMM")}`}
        </p>
      </div>

      {/* Stub side — perforated tear-line, like a physical mess coupon */}
      <div className="ticket-perforation flex w-28 shrink-0 flex-col items-center justify-center gap-2 bg-ink-50 px-3 py-4 text-center">
        {isRegistered ? (
          <>
            <span className="animate-stamp flex items-center gap-1 rounded-full border-2 border-veg px-2 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-wider text-veg">
              <Check size={12} strokeWidth={3} />
              Booked
            </span>
            <button
              disabled={!meal.is_open || busy}
              onClick={() => meal.registration && onCancel(meal.registration.id)}
              className="flex items-center gap-1 font-mono text-[11px] font-medium text-ink-400 underline decoration-dotted underline-offset-2 hover:text-nonveg disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:text-ink-400"
            >
              {busy ? <Loader2 size={11} className="animate-spin" /> : <X size={11} />}
              Cancel
            </button>
          </>
        ) : (
          <button
            disabled={!meal.is_open || busy}
            onClick={() => onRegister(meal.id)}
            className="w-full rounded-lg bg-mustard px-2 py-2 font-mono text-[11px] font-semibold uppercase tracking-wider text-ink-900 transition-colors hover:bg-mustard-600 disabled:cursor-not-allowed disabled:bg-ink-100 disabled:text-ink-400"
          >
            {busy ? (
              <Loader2 size={13} className="mx-auto animate-spin" />
            ) : meal.is_open ? (
              "Register"
            ) : (
              "Closed"
            )}
          </button>
        )}
      </div>
    </div>
  );
}
