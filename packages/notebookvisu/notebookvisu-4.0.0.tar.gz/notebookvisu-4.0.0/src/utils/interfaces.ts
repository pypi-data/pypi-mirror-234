import { IWidgetTracker } from '@jupyterlab/apputils';
import { ISignal } from '@lumino/signaling';
import { INotebookHeading } from './headings';
import { NotebookPanel } from '@jupyterlab/notebook';

export abstract class IOptionsManager {}

export interface ICollapseChangedArgs {
  collapsedState: boolean;

  heading: INotebookHeading;
}

export type ItemRenderer = (
  item: INotebookHeading,
  headings: INotebookHeading[]
) => JSX.Element | null;

export interface IGenerator {
  tracker: IWidgetTracker<NotebookPanel>;

  options?: IOptionsManager;

  collapseChanged?: ISignal<IOptionsManager, ICollapseChangedArgs>;

  itemRenderer: ItemRenderer;

  toolbarGenerator?: () => any;

  generate(panel: NotebookPanel, options?: IOptionsManager): INotebookHeading[];
}

export interface ICurrentPanel {
  panel: NotebookPanel;

  notebookGenerator: IGenerator;
}
