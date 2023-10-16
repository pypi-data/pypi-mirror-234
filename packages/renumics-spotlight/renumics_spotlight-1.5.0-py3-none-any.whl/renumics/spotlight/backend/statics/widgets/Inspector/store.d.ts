import { ReactNode } from 'react';
import { StoreApi } from 'zustand';
import { ViewConfig } from './types';
export interface State {
    views: ViewConfig[];
    addView: (view: ViewConfig) => void;
    removeView: (view: ViewConfig) => void;
    moveView: (source: number, target: number) => void;
}
export declare const StoreContext: import("react").Context<StoreApi<State> | null>;
interface ProviderProps {
    children?: ReactNode;
}
declare const StoreProvider: ({ children }: ProviderProps) => JSX.Element;
declare function useStore<T>(selector: (state: State) => T): T;
export { useStore, StoreProvider };
