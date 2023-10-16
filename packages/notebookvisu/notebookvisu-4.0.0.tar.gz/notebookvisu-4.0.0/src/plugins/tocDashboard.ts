import {
  ILabShell,
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ITranslator } from '@jupyterlab/translation';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { analyticsIcon } from '../icons';
import { NotebookPanel, INotebookTracker } from '@jupyterlab/notebook';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import TocDashboardPanel from '../toc-dashboard/tocDashboardPanel';
import { IGenerator } from '../utils/interfaces';
import { APP_ID, CommandIDs, PluginIDs } from '../utils/constants';
import { createNotebookGenerator } from '../toc-dashboard/generator';

async function activateTOCDashboard(
  app: JupyterFrontEnd,
  labShell: ILabShell,
  restorer: ILayoutRestorer,
  rendermime: IRenderMimeRegistry,
  translator: ITranslator,
  notebookTracker: INotebookTracker,
  settingRegistry?: ISettingRegistry
) {
  console.log('JupyterLab extension tocDashboard is activated!');

  const trans = translator.load('jupyterlab');

  const tocDashboardPanel = new TocDashboardPanel(translator, app.commands);

  tocDashboardPanel.title.icon = analyticsIcon;
  tocDashboardPanel.title.caption = trans.__('Dashboard ToC');
  tocDashboardPanel.id = 'dashboard-toc-code';
  tocDashboardPanel.node.setAttribute('role', 'region');
  tocDashboardPanel.node.setAttribute(
    'aria-label',
    trans.__('Dashboard ToC section')
  );

  labShell.add(tocDashboardPanel, 'left', { rank: 400 });

  app.commands.addCommand(CommandIDs.showDashboardToCPanel, {
    label: trans.__('Dashboard ToC'),
    execute: () => {
      labShell.activateById(tocDashboardPanel.id);
    }
  });

  if (restorer) {
    restorer.add(tocDashboardPanel, `${APP_ID}:dashboard-toc-restorer`);
  }

  // attempt to load plugin settings:
  let settings: ISettingRegistry.ISettings | undefined;
  if (settingRegistry) {
    try {
      settings = await settingRegistry.load(PluginIDs.tocDashboardPlugin);
    } catch (error) {
      console.error(
        `Failed to load settings for the Dashboard ToC extension.\n\n${error}`
      );
    }
  }

  const notebookGenerator: IGenerator = createNotebookGenerator(
    notebookTracker,
    tocDashboardPanel,
    rendermime.sanitizer,
    translator,
    settings
  );

  // update the ToC when the active widget changes:
  labShell.currentChanged.connect(onConnect);

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
      if (
        tocDashboardPanel.current &&
        tocDashboardPanel.current.panel.isDisposed
      ) {
        tocDashboardPanel.current = null;
      }
      return;
    }
    const notebookPanel = widget as NotebookPanel;
    tocDashboardPanel.current = {
      panel: notebookPanel,
      notebookGenerator: notebookGenerator
    };
  }
}

const tocDashboardPlugin: JupyterFrontEndPlugin<void> = {
  id: PluginIDs.tocDashboardPlugin,
  autoStart: true,
  requires: [
    ILabShell,
    ILayoutRestorer,
    IRenderMimeRegistry,
    ITranslator,
    INotebookTracker
  ],
  optional: [ISettingRegistry],
  activate: activateTOCDashboard
};

export default tocDashboardPlugin;
