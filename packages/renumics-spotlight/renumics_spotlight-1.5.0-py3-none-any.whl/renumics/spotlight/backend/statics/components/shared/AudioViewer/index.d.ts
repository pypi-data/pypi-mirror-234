interface Props {
    url?: string;
    peaks?: number[];
    windows: [number, number][];
    editable: boolean;
    optional: boolean;
    showControls?: boolean;
    onEditWindow?: (window: [number, number]) => void;
    onDeleteWindow?: () => void;
    onRegionEnter?: (windowIndex: number) => void;
    onRegionLeave?: (windowIndex: number) => void;
    onRegionClick?: (windowIndex: number) => void;
}
declare const AudioViewer: ({ url, peaks, windows, editable, optional, showControls, onEditWindow, onDeleteWindow, onRegionEnter, onRegionLeave, onRegionClick, }: Props) => JSX.Element;
export default AudioViewer;
