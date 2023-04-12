export interface ImageOperationProp {
    url: string;
    setImageURL: (url: string) => void;
}

export interface ImageHistoryProp {
    url: string;
    originalURL: string;
    history: string[];
    undoHistory: string[];
}

export interface DropdownProp {
    url: string;
    setImageURL: (url: string) => void;
    original: string;
    setOriginal: (url: string) => void;
    history: string[];
    modifyHistory: (action: string, url: string) => void;
    undoHistory: string[];
}

export interface ImageReaderProp {
    url: string;
}
