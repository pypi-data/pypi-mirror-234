import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { ITranslator } from '@jupyterlab/translation';
import { ActivityMonitor } from '@jupyterlab/coreutils';
import { Message } from '@lumino/messaging';
import { NotebookPanel } from '@jupyterlab/notebook';
import { TOC_DASHBOARD_RENDER_TIMEOUT } from '../utils/constants';
import DashboardComponent from './dashboardComponent';
import { areListsEqual } from '../utils/utils';
import { IMarkdownTranslator } from '../plugins/sideDashboard';
import { Provider } from 'react-redux';
import { AppDispatch, store } from '../redux/store';
import { setNotebookCells } from '../redux/reducers/CommonDashboardReducer';
import { NotebookCell } from '../redux/types';
const dispatch = store.dispatch as AppDispatch;

class DashboardSidePanel extends ReactWidget {
  constructor(
    markdownTranslator: IMarkdownTranslator,
    translator: ITranslator | undefined
  ) {
    super();

    this.addClass('dashboard-react-widget');

    this._panel = null;
    this._monitor = null;
    this._notebookCells = null;
    this._markdownTranslator = markdownTranslator;
  }

  get panel(): NotebookPanel | null {
    return this._panel;
  }

  set panel(value: NotebookPanel | null) {
    if (value && this._panel && this._panel === value) {
      return;
    }

    if (this._panel) {
      this._panel.disposed.disconnect(this._onPanelDisposed, this);
    }

    this._panel = value;

    if (this._panel) {
      this._panel.disposed.connect(this._onPanelDisposed, this);
    }

    // dispose an old activity monitor if one existed...
    if (this._monitor) {
      this._monitor.dispose();
      this._monitor = null;
    }
    // if we are wiping the ToC dashboard, update and return...
    if (!this._panel) {
      this.update();
      return;
    }

    const context = this._panel.context;

    // throttle the rendering rate of the table of contents:
    this._monitor = new ActivityMonitor({
      signal: context.model.contentChanged,
      timeout: TOC_DASHBOARD_RENDER_TIMEOUT
    });
    this._monitor.activityStopped.connect(this.update, this);
    this.update();
  }

  private _onPanelDisposed(_panel: NotebookPanel) {
    // when the panel is disposed, dispose from the toc panel (calling the _panel setter)
    this.panel = null;
  }

  protected onAfterShow(msg: Message): void {
    this.update();
  }

  protected onUpdateRequest(msg: Message): void {
    this._updateCellList();

    // this calls render() through the parent class
    super.onUpdateRequest(msg);
  }

  protected _updateCellList() {
    const cells = this._panel?.model?.cells;
    if (cells) {
      const cellList = Array.from(cells).map(c => c.id);

      if (!areListsEqual(cellList, this._notebookCells)) {
        this._notebookCells = cellList;
        const notebookList: NotebookCell[] = Array.from(cells).map(c => ({
          id: c.id,
          cellType: c.type
        }));
        dispatch(setNotebookCells(notebookList));
        return;
      }
    } else {
      this._notebookCells = null;
    }
  }

  render(): JSX.Element {
    return (
      <Provider store={store}>
        <DashboardComponent
          panel={this._panel}
          markdownTranslator={this._markdownTranslator}
        />
      </Provider>
    );
  }

  private _panel: NotebookPanel | null;
  private _monitor: ActivityMonitor<any, any> | null;
  private _notebookCells: string[] | null;
  private _markdownTranslator: IMarkdownTranslator;
}

export default DashboardSidePanel;
