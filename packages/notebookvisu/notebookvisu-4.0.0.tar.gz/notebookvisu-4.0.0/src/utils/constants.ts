export const BACKEND_API_URL = 'https://api.unianalytics.ch';
// export const BACKEND_API_URL = 'http://localhost:5000';

// adapt the app ids in the schema/*.json if this value is changed
export const APP_ID = 'notebookvisu';

export const STORAGE_KEY = `@jupyterlab/${APP_ID}:sidedashboard`;

export const TOC_DASHBOARD_RENDER_TIMEOUT = 1000;

export const AUTOMATIC_FETCHING_INTERVAL = 10000000;

// A plugin id has to be of the form APP_ID:<schema name without .json>
export namespace PluginIDs {
  export const sideDashboardPlugin = `${APP_ID}:sideDashboardPlugin`;

  export const tocDashboardPlugin = `${APP_ID}:tocDashboardPlugin`;

  export const themePlugin = `${APP_ID}:themePlugin`;

  export const uploadNotebookPlugin = `${APP_ID}:uploadNotebookPlugin`;
}

export namespace CommandIDs {
  export const dashboardOpenVisu = `${APP_ID}:dashboard-open-visu`;

  export const uploadNotebook = `${APP_ID}:dashboard-upload-notebook`;

  export const copyDownloadLink = `${APP_ID}:dashboard-copy-download-link`;

  export const showDashboardToCPanel = `${APP_ID}:dashboard-toc-open-panel`;
}

export const visuIconClass = 'jp-icon3';

export const notebookSelector =
  '.jp-DirListing-item[data-file-type="notebook"]';

// notebook metadata field names
const SELECTOR_ID = 'unianalytics';
export namespace Selectors {
  export const notebookId = `${SELECTOR_ID}_notebook_id`;

  export const instanceId = `${SELECTOR_ID}_instance_id`;

  export const cellMapping = `${SELECTOR_ID}_cell_mapping`;
}
