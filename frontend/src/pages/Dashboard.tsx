import { useMemo, useState } from "react";
import { DaySelector } from "../components/DaySelector";
import { ErrorToast } from "../components/ErrorToast";
import { Header } from "../components/Header";
import { MealCard } from "../components/MealCard";
import { useMessMenu } from "../hooks/useMessMenu";

export function Dashboard() {
  const { menu, loading, error, setError, pendingMealId, register, cancel } = useMessMenu(7);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  const dates = useMemo(() => menu.map((d) => d.date), [menu]);
  const activeDate = selectedDate ?? dates[0];
  const activeDay = menu.find((d) => d.date === activeDate);

  return (
    <div className="min-h-screen">
      <Header />

      <main className="mx-auto max-w-3xl px-5 py-6">
        <div className="mb-5 flex items-baseline justify-between">
          <h1 className="font-display text-2xl font-semibold text-ink-900">This week's menu</h1>
          <span className="font-mono text-[11px] text-ink-400">7-day window</span>
        </div>

        {loading && (
          <div className="grid gap-3">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="h-28 animate-pulse rounded-xl bg-ink-100/60" />
            ))}
          </div>
        )}

        {!loading && dates.length > 0 && (
          <>
            <DaySelector dates={dates} selected={activeDate} onSelect={setSelectedDate} />

            <div className="mt-5 grid gap-3">
              {activeDay?.meals.map((meal) => (
                <MealCard
                  key={meal.id}
                  meal={meal}
                  busy={pendingMealId === meal.id}
                  onRegister={register}
                  onCancel={(registrationId) => cancel(registrationId, meal.id)}
                />
              ))}
            </div>
          </>
        )}
      </main>

      {error && <ErrorToast message={error} onDismiss={() => setError(null)} />}
    </div>
  );
}
