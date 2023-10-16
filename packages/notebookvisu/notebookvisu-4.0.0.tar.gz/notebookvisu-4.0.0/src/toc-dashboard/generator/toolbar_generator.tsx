import { INotebookTracker } from '@jupyterlab/notebook';
import { TranslationBundle } from '@jupyterlab/translation';
import {
  codeIcon,
  markdownIcon,
  numberingIcon,
  refreshIcon
} from '@jupyterlab/ui-components';
import { hideIcon, showIcon } from '../../icons';
import * as React from 'react';
import { OptionsManager } from './options_manager';

import { store, AppDispatch } from '../../redux/store';
import {
  setDisplayHideDashboard,
  initialToCDashboardState
} from '../../redux/reducers/ToCDashboardReducer';
import { refreshDashboards } from '../../redux/reducers/CommonDashboardReducer';

const dispatch = store.dispatch as AppDispatch;

type IProperties = Record<string, never>;

interface IState {
  showCode: boolean;

  showMarkdown: boolean;

  numbering: boolean;

  showVisuDashboard: boolean;
}

export type ToolbarComponent = React.ComponentType<IProperties>;

function toolbar(
  options: OptionsManager,
  tracker: INotebookTracker
): ToolbarComponent {
  return class Toolbar extends React.Component<IProperties, IState> {
    constructor(props: IProperties) {
      super(props);
      this._trans = options.translator.load('jupyterlab');
      this.state = {
        showCode: true,
        showMarkdown: false,
        numbering: false,
        showVisuDashboard: initialToCDashboardState.displayDashboard
      };
      if (tracker.currentWidget) {
        // read saved user settings in notebook metadata:
        void tracker.currentWidget.context.ready.then(() => {
          if (tracker.currentWidget) {
            tracker.currentWidget.content.activeCellChanged.connect(() => {
              options.updateWidget();
            });
            const numbering = tracker.currentWidget.model?.metadata[
              'dashboard-toc-autonumbering'
            ] as boolean;
            const showCode = tracker.currentWidget.model?.metadata[
              'dashboard-toc-showcode'
            ] as boolean;
            const showMarkdown = tracker.currentWidget.model?.metadata[
              'dashboard-toc-showmarkdowntxt'
            ] as boolean;
            options.initializeOptions(
              numbering || options.numbering,
              options.numberingH1,
              options.syncCollapseState,
              showCode || options.showCode,
              showMarkdown || options.showMarkdown
            );
            this.setState({
              showCode: options.showCode,
              showMarkdown: options.showMarkdown,
              numbering: options.numbering
            });
          }
        });
      }
    }

    toggleCode() {
      options.showCode = !options.showCode;
      this.setState({ showCode: options.showCode });
    }

    toggleMarkdown() {
      options.showMarkdown = !options.showMarkdown;
      this.setState({ showMarkdown: options.showMarkdown });
    }

    toggleNumbering() {
      options.numbering = !options.numbering;
      this.setState({ numbering: options.numbering });
    }

    toggleShowVisuDashboard() {
      // dispatch show/hide the dashboard component action
      const showVisuDashboard = this.state.showVisuDashboard;
      dispatch(setDisplayHideDashboard(!showVisuDashboard));
      this.setState({ showVisuDashboard: !showVisuDashboard });
    }

    refreshDashboard() {
      // dispatch refresh action
      dispatch(refreshDashboards());
    }

    render() {
      const codeToggleIcon = (
        <div
          onClick={event => this.toggleCode()}
          role="text"
          aria-label={this._trans.__('Toggle Code Cells')}
          title={this._trans.__('Toggle Code Cells')}
          className={
            this.state.showCode
              ? 'dashboard-toc-toolbar-icon-selected'
              : 'dashboard-toc-toolbar-icon'
          }
        >
          <codeIcon.react />
        </div>
      );

      const markdownToggleIcon = (
        <div
          onClick={event => this.toggleMarkdown()}
          role="text"
          aria-label={this._trans.__('Toggle Markdown Text Cells')}
          title={this._trans.__('Toggle Markdown Text Cells')}
          className={
            this.state.showMarkdown
              ? 'dashboard-toc-toolbar-icon-selected'
              : 'dashboard-toc-toolbar-icon'
          }
        >
          <markdownIcon.react />
        </div>
      );

      const numberingToggleIcon = (
        <div
          onClick={event => this.toggleNumbering()}
          role="text"
          aria-label={this._trans.__('Toggle Auto-Numbering')}
          title={this._trans.__('Toggle Auto-Numbering')}
          className={
            this.state.numbering
              ? 'dashboard-toc-toolbar-icon-selected'
              : 'dashboard-toc-toolbar-icon'
          }
        >
          <numberingIcon.react />
        </div>
      );

      const showVisuDashboardToggleIcon = (
        <div
          onClick={event => this.toggleShowVisuDashboard()}
          role="text"
          aria-label={
            this.state.showVisuDashboard
              ? this._trans.__('Hide Visualization Dashboard')
              : this._trans.__('Show Visualization Dashboard')
          }
          title={
            this.state.showVisuDashboard
              ? this._trans.__('Hide Visualization Dashboard')
              : this._trans.__('Show Visualization Dashboard')
          }
          className={'dashboard-toc-toolbar-icon'}
        >
          {this.state.showVisuDashboard ? (
            <hideIcon.react />
          ) : (
            <showIcon.react />
          )}
        </div>
      );

      const refreshButtonIcon = (
        <div
          onClick={event => this.refreshDashboard()}
          role="text"
          aria-label={this._trans.__('Refresh Dashboard')}
          title={this._trans.__('Refresh Dashboard')}
          className={'dashboard-toc-toolbar-icon'}
        >
          <refreshIcon.react />
        </div>
      );

      return (
        <div>
          <div className={'dashboard-toc-toolbar'}>
            <div className="dashboard-toc-toolbar-compartment">
              {codeToggleIcon}
              {markdownToggleIcon}
              {numberingToggleIcon}
            </div>
            <div className={'dashboard-toc-toolbar-compartment'}>
              {showVisuDashboardToggleIcon}
              {refreshButtonIcon}
            </div>
          </div>
        </div>
      );
    }

    _trans: TranslationBundle;
  };
}

export { toolbar };
