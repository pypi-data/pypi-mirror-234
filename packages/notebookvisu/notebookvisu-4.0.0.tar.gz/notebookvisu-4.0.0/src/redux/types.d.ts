// definition file for the page content structures and other interfaces

interface NotebookLayer {
  pageName: 'Notebook';
}

interface CellLayer {
  pageName: 'Cell';
  content: {
    cellId: string;
  };
}

// discriminated union type, TypeScript will infer the correct type from pageName value. Will show an error if provided with an unknown pageName.
export type SideDashboardLayer = NotebookLayer | CellLayer;

export interface SideDashboardState {
  navigationState: SideDashboardLayer[];
}

// for ThemeReducer
export interface ThemeState {
  isThemeLight: boolean;
}

// for ToCReducer
export type LocationData = {
  location_count: { [key: string]: number };
  total_count: number;
} | null;

export interface ToCState {
  displayDashboard: boolean;
  hasNotebookId: boolean;
  locationData: LocationData;
}

export interface NotebookCell {
  id: string;
  cellType: string;
}

export interface CommonDashboardState {
  notebookCells: NotebookCell[] | null;
  timeWindow: string;
  refreshBoolean: boolean;
}
