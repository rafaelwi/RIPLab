export interface ImageOperationProp {
    url: string;
    setImageURL: (url: string) => void;
}

export interface ImageHistoryProp {
    url: string;
    originalURL: string;
    history: string[];
}

export interface DropdownProp {
    url: string;
    setImageURL: (url: string) => void;
    original: string;
    setOriginal: (url: string) => void;
    modifyHistory: (action: string, url: string) => void;
}

export interface ImageReaderProp {
    url: string;
}
