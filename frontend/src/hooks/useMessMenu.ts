import { useCallback, useEffect, useState } from "react";
import { messApi } from "../api/client";
import type { DayMenu } from "../types/mess";

export function useMessMenu(days = 7) {
  const [menu, setMenu] = useState<DayMenu[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pendingMealId, setPendingMealId] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await messApi.getMenu(days);
      setMenu(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't load the menu.");
    } finally {
      setLoading(false);
    }
  }, [days]);

  useEffect(() => {
    load();
  }, [load]);

  const register = useCallback(
    async (mealId: string) => {
      setPendingMealId(mealId);
      try {
        await messApi.register(mealId);
        await load();
      } catch (err) {
        setError(err instanceof Error ? err.message : "Couldn't complete the registration.");
      } finally {
        setPendingMealId(null);
      }
    },
    [load]
  );

  const cancel = useCallback(
    async (registrationId: string, mealId: string) => {
      setPendingMealId(mealId);
      try {
        await messApi.cancel(registrationId);
        await load();
      } catch (err) {
        setError(err instanceof Error ? err.message : "Couldn't cancel the registration.");
      } finally {
        setPendingMealId(null);
      }
    },
    [load]
  );

  return { menu, loading, error, setError, pendingMealId, register, cancel };
}
