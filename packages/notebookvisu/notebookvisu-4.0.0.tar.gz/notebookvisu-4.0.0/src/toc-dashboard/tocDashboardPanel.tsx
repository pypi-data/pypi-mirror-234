import { Message } from '@lumino/messaging';
import { ActivityMonitor, PathExt } from '@jupyterlab/coreutils';
import { ReactWidget } from '@jupyterlab/apputils';
import * as React from 'react';
import {
  ITranslator,
  TranslationBundle,
  nullTranslator
} from '@jupyterlab/translation';
import { NotebookPanel } from '@jupyterlab/notebook';
import { TOC_DASHBOARD_RENDER_TIMEOUT } from '../utils/constants';
import TocDashboardTree from './tocDashboardTree';
import { ICurrentPanel } from '../utils/interfaces';
import { Provider } from 'react-redux';
import NoNotebookPlaceholder from './NoNotebookPlaceholder';
import { ToolbarComponent } from './generator/toolbar_generator';
import Loader from '../side-dashboard/components/placeholder/Loader';
import { CommandRegistry } from '@lumino/commands';
import { areListsEqual } from '../utils/utils';
import { AppDispatch, store } from '../redux/store';
import { setFetchedLocationData } from '../redux/reducers/ToCDashboardReducer';
const dispatch = store.dispatch as AppDispatch;

class TocDashboardPanel extends ReactWidget {
  constructor(translator: ITranslator | null, commands: CommandRegistry) {
    super();
    this._trans = (translator || nullTranslator).load('jupyterlab');
    this._current = null;
    this._monitor = null;
    this._toolbar = null;
    this._commands = commands;
    this._notebookCells = null;
  }

  get current(): ICurrentPanel | null {
    return this._current;
  }

  set current(value: ICurrentPanel | null) {
    // if they are the same as previously, do nothing
    if (
      value &&
      this._current &&
      this._current.panel === value.panel &&
      this._current.notebookGenerator === value.notebookGenerator
    ) {
      return;
    }

    if (this._current) {
      this._current.panel.disposed.disconnect(this._onPanelDisposed, this);
    }

    this._current = value;

    if (this._current) {
      this._current.panel.disposed.connect(this._onPanelDisposed, this);
    }

    if (this._current) {
      if (this._current.notebookGenerator.toolbarGenerator) {
        this._toolbar = this._current.notebookGenerator.toolbarGenerator();
      } else {
        this._toolbar = null;
      }
    }
    // dispose an old activity monitor if one existed...
    if (this._monitor) {
      this._monitor.dispose();
      this._monitor = null;
    }
    // if we are wiping the ToC dashboard, update and return...
    if (!this._current) {
      this.update();
      return;
    }

    const context = this._current.panel.context;

    // Throttle the rendering rate of the table of contents:
    this._monitor = new ActivityMonitor({
      signal: context.model.contentChanged,
      timeout: TOC_DASHBOARD_RENDER_TIMEOUT
    });

    this._monitor.activityStopped.connect(this.update, this);

    this.update();
  }

  private _onPanelDisposed(_panel: NotebookPanel) {
    // when the panel is disposed, dispose from the toc panel (calling the _current setter)
    this.current = null;
  }

  protected onAfterShow(msg: Message): void {
    this.update();
  }

  protected onUpdateRequest(msg: Message): void {
    this._updateCellList();
    // this calls render() through the parent class
    super.onUpdateRequest(msg);
  }

  protected _updateCellList(): void {
    const cells = this._current?.panel.model?.cells;
    if (cells) {
      const cellList = Array.from(cells).map(c => c.id);

      if (!areListsEqual(cellList, this._notebookCells)) {
        this._notebookCells = cellList;
        dispatch(setFetchedLocationData(null));
        return;
      }
    } else {
      this._notebookCells = null;
    }
  }

  render(): JSX.Element {
    return (
      <>
        {this._current ? (
          <>
            {this._current.panel.sessionContext.isReady ? (
              <Provider store={store}>
                <div className="dashboard-TableOfContents">
                  <div className="dashboard-stack-panel-header">
                    {PathExt.basename(this._current.panel.context.localPath)}
                  </div>
                  {this._toolbar && <this._toolbar />}
                  <TocDashboardTree
                    headings={this._current.notebookGenerator.generate(
                      this._current.panel
                    )}
                    itemRenderer={this._current.notebookGenerator.itemRenderer}
                    // notebookGenerator={this._current.notebookGenerator}
                    notebookPanel={this._current.panel}
                    commands={this._commands}
                    notebookCells={this._notebookCells}
                  />
                </div>
              </Provider>
            ) : (
              <Loader />
            )}
          </>
        ) : (
          <NoNotebookPlaceholder title={this._trans.__('Dashboard ToC')} />
        )}
      </>
    );
  }

  private _trans: TranslationBundle;
  private _current: ICurrentPanel | null;
  private _toolbar: ToolbarComponent | null;
  private _monitor: ActivityMonitor<any, any> | null;
  private _commands: CommandRegistry;
  private _notebookCells: string[] | null | undefined;
}

export default TocDashboardPanel;
