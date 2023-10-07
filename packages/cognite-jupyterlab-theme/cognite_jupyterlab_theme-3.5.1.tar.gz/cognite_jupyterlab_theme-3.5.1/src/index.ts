import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the cognite_jupyterlab_theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'cognite_jupyterlab_theme:plugin',
  description: 'A JupyterLab extension adding a Cognite theme.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension cognite_jupyterlab_theme is activated!');

    manager.register({
      name: 'Cognite',
      isLight: true,
      load: () => manager.loadCSS('cognite_jupyterlab_theme/index.css'),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
