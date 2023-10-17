interface SettingsStore {
    [key: string]: unknown;
}
export declare const useStore: import("zustand").UseBoundStore<Omit<import("zustand").StoreApi<SettingsStore>, "persist"> & {
    persist: {
        setOptions: (options: Partial<import("zustand/middleware").PersistOptions<SettingsStore, unknown>>) => void;
        clearStorage: () => void;
        rehydrate: () => void | Promise<void>;
        hasHydrated: () => boolean;
        onHydrate: (fn: (state: SettingsStore) => void) => () => void;
        onFinishHydration: (fn: (state: SettingsStore) => void) => () => void;
        getOptions: () => Partial<import("zustand/middleware").PersistOptions<SettingsStore, unknown>>;
    };
}>;
type Setter<T> = (value: T | ((previous: T) => T)) => void;
declare function useSetting<T>(name: string, defaultValue: T, global?: boolean): [T, Setter<T>];
export default useSetting;
