import {
  ILabShell,
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { analyticsIcon } from '../icons';
import {
  APP_ID,
  visuIconClass,
  CommandIDs,
  PluginIDs
} from '../utils/constants';
import { CellButton } from '../widget-extensions/CellButton';
import { NotebookButton } from '../widget-extensions/NotebookButton';
import { store, AppDispatch } from '../redux/store';
import {
  navigateToNotebook,
  navigateToCell
} from '../redux/reducers/SideDashboardReducer';
import DashboardSidePanel from '../side-dashboard/dashboardSidePanel';
import { NotebookPanel } from '@jupyterlab/notebook';
import { IMarkdownParser, IRenderMime } from '@jupyterlab/rendermime';
import { Sanitizer } from '@jupyterlab/apputils';

export interface IMarkdownTranslator {
  markdownParser: IMarkdownParser;
  sanitizer: IRenderMime.ISanitizer;
}

const dispatch = store.dispatch as AppDispatch;

function activateDashboard(
  app: JupyterFrontEnd,
  restorer: ILayoutRestorer,
  labShell: ILabShell,
  markdownParser: IMarkdownParser,
  translator?: ITranslator | null
) {
  console.log('JupyterLab extension sideDashboard is activated!');

  const trans = (translator ?? nullTranslator).load('jupyterlab');

  // create the dashboard widget:
  const markdownTranslator: IMarkdownTranslator = {
    markdownParser: markdownParser,
    sanitizer: new Sanitizer()
  };
  const dashboardPanel = new DashboardSidePanel(
    markdownTranslator,
    translator ?? undefined
  );
  dashboardPanel.title.icon = analyticsIcon;
  dashboardPanel.title.caption = trans.__('Side Dashboard');
  dashboardPanel.id = 'side-dashboard';
  dashboardPanel.node.setAttribute('role', 'region');
  dashboardPanel.node.setAttribute(
    'aria-label',
    trans.__('Side dashboard section')
  );

  // add the dashboard panel to the right area:
  app.shell.add(dashboardPanel, 'right', {
    rank: 1000,
    type: 'Side dashboard'
  });

  app.commands.addCommand(CommandIDs.dashboardOpenVisu, {
    // isPalette is true when representing the command in the palette, if not provided, args[isPalette] is undefined => False
    label: 'Visualization',
    // caption = hovering caption
    caption: 'Open Notebook Dashboard',
    icon: analyticsIcon,
    iconClass: visuIconClass,
    execute: args => {
      if (args['from'] === 'Notebook') {
        dispatch(navigateToNotebook());
      } else if (args['from'] === 'Cell') {
        dispatch(
          navigateToCell({
            cellId: args['cell_id'] as string
          })
        );
      }
      // else, keep the current navigationState

      // open the dashboard
      if (!dashboardPanel.isVisible) {
        app.shell.activateById(dashboardPanel.id);
      }
    }
  });

  // add cell button
  app.docRegistry.addWidgetExtension('Notebook', new CellButton(app.commands));

  // add notebook toolbar button
  app.docRegistry.addWidgetExtension(
    'Notebook',
    new NotebookButton(app.commands)
  );

  if (restorer) {
    restorer.add(dashboardPanel, `${APP_ID}:dashboard-restorer`);
  }

  // update the panel when the active widget changes
  if (labShell) {
    labShell.currentChanged.connect(onConnect);
  }

  // connect to current widget
  void app.restored.then(() => {
    onConnect();
  });

  function onConnect() {
    const widget = app.shell.currentWidget;
    if (!widget) {
      return;
    }
    // only proceed if the new widget is a notebook panel

    if (!(widget instanceof NotebookPanel)) {
      // if the previously used widget is still available, stick with it.
      // otherwise, set the current ToC panel to null.
      if (dashboardPanel.panel && dashboardPanel.panel.isDisposed) {
        dashboardPanel.panel = null;
      }
      return;
    }
    const notebookPanel = widget as NotebookPanel;
    dashboardPanel.panel = notebookPanel;
  }
}

const sideDashboardPlugin: JupyterFrontEndPlugin<void> = {
  id: PluginIDs.sideDashboardPlugin,
  description: 'Visualization dashboard integrated into the side panel',
  autoStart: true,
  requires: [ILayoutRestorer, ILabShell, IMarkdownParser],
  optional: [ITranslator],
  activate: activateDashboard
};

export default sideDashboardPlugin;
