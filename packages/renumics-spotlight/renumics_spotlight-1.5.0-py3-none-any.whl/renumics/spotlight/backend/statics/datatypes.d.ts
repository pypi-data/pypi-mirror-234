export declare const datakinds: readonly ["int", "float", "bool", "str", "array", "datetime", "Mesh", "Sequence1D", "Embedding", "Image", "Audio", "Video", "Category", "Window", "Unknown"];
export type DataKind = typeof datakinds[number];
export interface BaseDataType<K extends DataKind, L extends boolean = false, B extends boolean = false> {
    kind: K;
    binary: B;
    lazy: L;
    optional: boolean;
}
export type UnknownDataType = BaseDataType<'Unknown'>;
export type IntegerDataType = BaseDataType<'int'>;
export type FloatDataType = BaseDataType<'float'>;
export type BooleanDataType = BaseDataType<'bool'>;
export type DateTimeDataType = BaseDataType<'datetime'>;
export type ArrayDataType = BaseDataType<'array', true>;
export type WindowDataType = BaseDataType<'Window'>;
export type StringDataType = BaseDataType<'str', true>;
export type EmbeddingDataType = BaseDataType<'Embedding', true>;
export type SequenceDataType = BaseDataType<'Sequence1D', true, true>;
export type MeshDataType = BaseDataType<'Mesh', true, true>;
export type ImageDataType = BaseDataType<'Image', true, true>;
export type AudioDataType = BaseDataType<'Audio', true, true>;
export type VideoDataType = BaseDataType<'Video', true, true>;
export interface CategoricalDataType extends BaseDataType<'Category'> {
    kind: 'Category';
    categories: Record<string, number>;
    invertedCategories: Record<number, string>;
}
export type DataType = UnknownDataType | IntegerDataType | FloatDataType | BooleanDataType | StringDataType | ArrayDataType | DateTimeDataType | MeshDataType | SequenceDataType | EmbeddingDataType | ImageDataType | AudioDataType | VideoDataType | WindowDataType | CategoricalDataType;
export declare const isInteger: (type: DataType) => type is IntegerDataType;
export declare const isFloat: (type: DataType) => type is FloatDataType;
export declare const isBoolean: (type: DataType) => type is BooleanDataType;
export declare const isString: (type: DataType) => type is StringDataType;
export declare const isArray: (type: DataType) => type is ArrayDataType;
export declare const isDateTime: (type: DataType) => type is DateTimeDataType;
export declare const isMesh: (type: DataType) => type is MeshDataType;
export declare const isSequence: (type: DataType) => type is SequenceDataType;
export declare const isEmbedding: (type: DataType) => type is EmbeddingDataType;
export declare const isImage: (type: DataType) => type is ImageDataType;
export declare const isAudio: (type: DataType) => type is AudioDataType;
export declare const isVideo: (type: DataType) => type is VideoDataType;
export declare const isWindow: (type: DataType) => type is WindowDataType;
export declare const isCategorical: (type: DataType) => type is CategoricalDataType;
export declare const isUnknown: (type: DataType) => type is UnknownDataType;
export type NumericalDataType = IntegerDataType | FloatDataType;
export declare const isNumerical: (type: DataType) => type is NumericalDataType;
export type ScalarDataType = NumericalDataType | StringDataType | BooleanDataType;
export declare const isScalar: (type: DataType) => type is ScalarDataType;
export declare function getNullValue(kind: DataKind): number | boolean | string | null;
export declare const unknownDataType: UnknownDataType;
