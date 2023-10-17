import { DataColumn, Vec2 } from '../types';
type Domain = [number, number];
export interface Settings {
    sequence: {
        yAxis: {
            multiple: boolean;
            setMultiple: (multiple: boolean) => void;
            domains: {
                [key: string]: [number, number];
            };
            syncDomain: (key: string, domain: Domain) => void;
            unsyncDomain: (key: string) => void;
        };
        xAxis: {
            extents: Vec2;
            setExtents: (ext: Vec2) => void;
            isSynchronized: boolean;
            setIsSynchronized: (value: boolean) => void;
        };
        visibleColumns: Map<DataColumn, boolean>;
        setSelectableColumns: (columns: DataColumn[]) => void;
        setIsColumnVisible: (column: DataColumn, isVisible: boolean) => void;
    };
}
declare const useSettings: import("zustand").UseBoundStore<import("zustand").StoreApi<Settings>>;
export default useSettings;
