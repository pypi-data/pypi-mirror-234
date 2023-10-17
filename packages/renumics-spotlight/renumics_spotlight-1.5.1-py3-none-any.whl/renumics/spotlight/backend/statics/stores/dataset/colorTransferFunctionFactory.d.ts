import { DataType } from '../../datatypes';
import { TransferFunction } from '../../hooks/useColorTransferFunction';
import { ColumnData, DataColumn, DataStatistics, TableData } from '../../types';
import { Dataset } from './dataset';
export declare const makeApplicableColorTransferFunctions: (type: DataType, data: ColumnData, stats?: DataStatistics) => TransferFunction[];
type ColumnsTransferFunctions = Record<string, {
    full: TransferFunction[];
    filtered: TransferFunction[];
}>;
export declare const makeColumnsColorTransferFunctions: (columns: DataColumn[], data: TableData, stats: Dataset['columnStats'], filteredMask: boolean[]) => ColumnsTransferFunctions;
export {};
