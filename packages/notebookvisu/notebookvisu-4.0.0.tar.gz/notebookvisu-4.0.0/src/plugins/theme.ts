import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { PluginIDs } from '../utils/constants';
import { store, AppDispatch } from '../redux/store';
import { changeTheme } from '../redux/reducers/ThemeReducer';

const dispatch = store.dispatch as AppDispatch;

const themePlugin: JupyterFrontEndPlugin<void> = {
  id: PluginIDs.themePlugin,
  autoStart: true,
  optional: [IThemeManager],
  activate: (app: JupyterFrontEnd, theme: IThemeManager) => {
    // connect to theme changes and dispatch to store if theme is light or not
    theme.themeChanged.connect((_theme, changedArgs) => {
      dispatch(changeTheme(_theme.isLight(changedArgs.newValue)));
    });
  }
};

export default themePlugin;
