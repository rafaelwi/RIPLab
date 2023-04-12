import { useState, useMemo } from "react";


export default function useUndoableState(init: string) {
  const [states, setStates] = useState<string[]>([init]); // Used to store history of all states
  const [index, setIndex] = useState<number>(0); // Index of current state within `states`
  const state = useMemo(() => states[index], [states, index]); // Current state

  const setState = (value: string) => {
    // If state has not changed, return to avoid triggering a re-render
    if (state === value) {
      return;
    }
    const copy = states.slice(0, index + 1); // This removes all future (redo) states after current index
    copy.push(value);
    setStates(copy);
    setIndex(copy.length - 1);
  };

  // Clear all state history
  const resetState = (init: string) => {
    setIndex(0);
    setStates([init]);
  };

  // Allows you to go back (undo) N steps
  const goBack = (steps: number = 1) => {
    setIndex(Math.max(0, Number(index) - (Number(steps) || 1)));
  };

  // Allows you to go forward (redo) N steps
  const goForward = (steps: number = 1) => {
    setIndex(Math.min(states.length - 1, Number(index) + (Number(steps) || 1)));
  };

  return {
    state,
    setState,
    resetState,
    index,
    lastIndex: states.length - 1,
    goBack,
    goForward,
  };
}