import { INotebookTracker } from '@jupyterlab/notebook';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { ISignal, Signal } from '@lumino/signaling';
import TocDashboardPanel from '../tocDashboardPanel';
import { IOptionsManager, ICollapseChangedArgs } from '../../utils/interfaces';
import { IRenderMime } from '@jupyterlab/rendermime';

interface IOptions {
  numbering: boolean;

  numberingH1: boolean;

  syncCollapseState: boolean;

  sanitizer: IRenderMime.ISanitizer;

  translator?: ITranslator;
}

class OptionsManager extends IOptionsManager {
  constructor(
    widget: TocDashboardPanel,
    notebook: INotebookTracker,
    options: IOptions
  ) {
    super();
    this._numbering = options.numbering;
    this._numberingH1 = options.numberingH1;
    this._syncCollapseState = options.syncCollapseState;
    this._widget = widget;
    this._notebook = notebook;
    this.sanitizer = options.sanitizer;
    this.translator = options.translator || nullTranslator;
    this._collapseChanged = new Signal<this, ICollapseChangedArgs>(this);
  }

  readonly sanitizer: IRenderMime.ISanitizer;

  set notebookMetadata(value: [string, any]) {
    if (this._notebook.currentWidget !== null) {
      if (this._notebook.currentWidget.model) {
        this._notebook.currentWidget.model.setMetadata(value[0], value[1]);
      }
    }
  }

  set numbering(value: boolean) {
    this._numbering = value;
    this._widget.update();
    this.notebookMetadata = ['dashboard-toc-autonumbering', this._numbering];
  }

  get numbering() {
    return this._numbering;
  }

  set numberingH1(value: boolean) {
    if (this._numberingH1 !== value) {
      this._numberingH1 = value;
      this._widget.update();
    }
  }

  get numberingH1() {
    return this._numberingH1;
  }

  set syncCollapseState(value: boolean) {
    if (this._syncCollapseState !== value) {
      this._syncCollapseState = value;
      this._widget.update();
    }
  }

  get syncCollapseState() {
    return this._syncCollapseState;
  }

  set showCode(value: boolean) {
    this._showCode = value;
    this.notebookMetadata = ['dashboard-toc-showcode', this._showCode];
    this._widget.update();
  }

  get showCode() {
    return this._showCode;
  }

  set showMarkdown(value: boolean) {
    this._showMarkdown = value;
    this.notebookMetadata = [
      'dashboard-toc-showmarkdowntxt',
      this._showMarkdown
    ];
    this._widget.update();
  }

  get showMarkdown() {
    return this._showMarkdown;
  }

  get collapseChanged(): ISignal<this, ICollapseChangedArgs> {
    return this._collapseChanged;
  }

  set preRenderedToolbar(value: any) {
    this._preRenderedToolbar = value;
  }

  get preRenderedToolbar() {
    return this._preRenderedToolbar;
  }

  updateWidget() {
    this._widget.update();
  }

  updateAndCollapse(args: ICollapseChangedArgs) {
    this._collapseChanged.emit(args);
    this._widget.update();
  }

  initializeOptions(
    numbering: boolean,
    numberingH1: boolean,
    syncCollapseState: boolean,
    showCode: boolean,
    showMarkdown: boolean
  ) {
    this._numbering = numbering;
    this._numberingH1 = numberingH1;
    this._syncCollapseState = syncCollapseState;
    this._showCode = showCode;
    this._showMarkdown = showMarkdown;
    this._widget.update();
  }

  private _preRenderedToolbar: any = null;
  private _numbering: boolean;
  private _numberingH1: boolean;
  private _syncCollapseState: boolean;
  private _showCode = false;
  private _showMarkdown = false;
  private _notebook: INotebookTracker;
  private _widget: TocDashboardPanel;
  private _collapseChanged: Signal<this, ICollapseChangedArgs>;
  translator: ITranslator;
}

export { OptionsManager };
