import { AlertTriangle, X } from "lucide-react";

interface Props {
  message: string;
  onDismiss: () => void;
}

export function ErrorToast({ message, onDismiss }: Props) {
  return (
    <div className="fixed bottom-5 left-1/2 z-50 flex w-[calc(100%-2.5rem)] max-w-sm -translate-x-1/2 items-start gap-2.5 rounded-xl border border-nonveg/30 bg-ink-900 px-4 py-3 text-canvas shadow-ticket">
      <AlertTriangle size={16} className="mt-0.5 shrink-0 text-mustard" />
      <p className="flex-1 text-sm leading-snug">{message}</p>
      <button onClick={onDismiss} aria-label="Dismiss" className="shrink-0 text-ink-400 hover:text-canvas">
        <X size={14} />
      </button>
    </div>
  );
}
