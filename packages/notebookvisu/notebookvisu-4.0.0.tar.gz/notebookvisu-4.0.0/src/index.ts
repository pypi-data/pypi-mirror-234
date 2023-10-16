import { JupyterFrontEndPlugin } from '@jupyterlab/application';

//importing bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';

import themePlugin from './plugins/theme';
import uploadNotebookPlugin from './plugins/uploadNotebook';
import tocDashboardPlugin from './plugins/tocDashboard';
import sideDashboardPlugin from './plugins/sideDashboard';

const plugins: JupyterFrontEndPlugin<any>[] = [
  themePlugin,
  uploadNotebookPlugin,
  sideDashboardPlugin,
  tocDashboardPlugin
];
export default plugins;
