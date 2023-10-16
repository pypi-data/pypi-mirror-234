import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  LabShell
} from '@jupyterlab/application';
import { FocusExtension } from './extensions/FocusExtension';
import { ExecutionExtension } from './extensions/ExecutionExtension';
import { AlterationExtension } from './extensions/AlterationExtension';
import { InstanceInitializer } from './extensions/InstanceInitializer';
import { CellMappingExtension } from './extensions/CellMappingExtension';
import { PLUGIN_ID } from './utils/constants';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { compareVersions } from './utils/utils';

const activate = (
  app: JupyterFrontEnd,
  settingRegistry: ISettingRegistry
): void => {
  console.log(`JupyterLab extension ${PLUGIN_ID} is activated!`);

  const targetVersion = '3.1.0';
  const appNumbers = app.version.match(/[0-9]+/g);

  if (appNumbers && compareVersions(app.version, targetVersion) >= 0) {
    settingRegistry.load(`${PLUGIN_ID}:settings`).catch((err: Error) => {
      console.error(`${PLUGIN_ID}: Could not load settings, error: ${err}`);
    });

    const jupyterVersion = parseInt(appNumbers[0]);

    // // adds an instance_id to the notebook
    app.docRegistry.addWidgetExtension(
      'Notebook',
      new InstanceInitializer(jupyterVersion)
    );

    // // updates the notebook metadata to track the current-to-original notebook cell id mapping
    app.docRegistry.addWidgetExtension(
      'Notebook',
      new CellMappingExtension(jupyterVersion)
    );

    const labShell = app.shell as LabShell;
    // notebook widget extension with notebook ON/OFF + cell ON/OFF messaging
    app.docRegistry.addWidgetExtension(
      'Notebook',
      new FocusExtension(labShell, settingRegistry, jupyterVersion)
    );

    // notebook widget extension with cell insertion/deletion messaging
    app.docRegistry.addWidgetExtension(
      'Notebook',
      new AlterationExtension(settingRegistry, jupyterVersion)
    );

    // notebook widget extension with code and markdown cell execution messaging
    app.docRegistry.addWidgetExtension(
      'Notebook',
      new ExecutionExtension(settingRegistry, jupyterVersion)
    );
  } else {
    console.log(`Use a more recent version of JupyterLab (>=${targetVersion})`);
  }
};

const plugin: JupyterFrontEndPlugin<void> = {
  id: `${PLUGIN_ID}:plugin`,
  autoStart: true,
  requires: [ISettingRegistry],
  activate: activate
};

export default plugin;
