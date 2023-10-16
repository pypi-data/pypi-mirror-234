import { Signal } from '@lumino/signaling';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IDisposable } from '@lumino/disposable';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { NotebookPanel } from '@jupyterlab/notebook';
import { postCellAlteration } from '../api';
import { PLUGIN_ID, Selectors } from '../utils/constants';
import { StringId } from '../utils/types';
import { isNotebookValid } from '../utils/utils';
import { getCellIdsComp, getMetadataComp } from '../utils/compatibility';

export class AlterationExtension implements DocumentRegistry.WidgetExtension {
  constructor(settingRegistry: ISettingRegistry, jupyterVersion: number) {
    this._settingRegistry = settingRegistry;

    this._jupyterVersion = jupyterVersion;
  }

  createNew(panel: NotebookPanel): IDisposable {
    return new AlterationDisposable(
      panel,
      this._settingRegistry,
      this._jupyterVersion
    );
  }

  private _settingRegistry: ISettingRegistry;
  private _jupyterVersion: number;
}

class AlterationDisposable implements IDisposable {
  constructor(
    panel: NotebookPanel,
    settingRegistry: ISettingRegistry,
    jupyterVersion: number
  ) {
    this._jupyterVersion = jupyterVersion;

    settingRegistry.load(`${PLUGIN_ID}:settings`).then(
      (settings: ISettingRegistry.ISettings) => {
        this._updateSettings(settings);
        settings.changed.connect(this._updateSettings.bind(this));
      },
      (err: Error) => {
        console.error(
          `${PLUGIN_ID}: Could not load settings, so did not activate: ${err}`
        );
      }
    );

    panel.context.ready.then(() => {
      if (isNotebookValid(panel, jupyterVersion)) {
        this._notebookId = getMetadataComp(
          panel.context.model,
          Selectors.notebookId,
          jupyterVersion
        );
        this._instanceId = getMetadataComp(
          panel.context.model,
          Selectors.instanceId,
          jupyterVersion
        );
        this._cellIdList = getCellIdsComp(
          panel.context.model.cells,
          jupyterVersion
        );

        // connect to notebook cell insertion/deletion/move/set
        panel.context.model.cells.changed.connect(this._onCellsAltered, this);

        // release connection
        panel.disposed.connect(this._onPanelDisposed, this);
      }
    });
  }

  private _updateSettings(settings: ISettingRegistry.ISettings) {
    this._isAlterationSettingEnabled = settings.get('AlterationExtension')
      .composite as boolean;
  }

  private _onCellsAltered = (cells: any) => {
    const newCellIdList: string[] = getCellIdsComp(cells, this._jupyterVersion);
    if (this._isAlterationSettingEnabled) {
      const addedIds: string[] = newCellIdList.filter(
        item => !this._cellIdList.includes(item)
      );
      const removedIds: string[] = this._cellIdList.filter(
        item => !newCellIdList.includes(item)
      );

      for (const added_id of addedIds) {
        postCellAlteration({
          notebook_id: this._notebookId,
          instance_id: this._instanceId,
          cell_id: added_id,
          alteration_type: 'ADD',
          time: new Date().toISOString()
        });
      }
      for (const removed_id of removedIds) {
        postCellAlteration({
          notebook_id: this._notebookId,
          instance_id: this._instanceId,
          cell_id: removed_id,
          alteration_type: 'REMOVE',
          time: new Date().toISOString()
        });
      }
    }
    this._cellIdList = newCellIdList;
  };

  private _onPanelDisposed = (panel: NotebookPanel) => {
    panel.context.model.cells.changed.disconnect(this._onCellsAltered, this);
  };

  get isDisposed(): boolean {
    return this._isDisposed;
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }

    this._isDisposed = true;
    this._notebookId = null;
    this._instanceId = null;
    this._cellIdList = [];

    Signal.clearData(this);
  }

  private _jupyterVersion: number;
  private _isDisposed = false;
  private _notebookId: StringId = undefined;
  private _instanceId: StringId = undefined;
  private _isAlterationSettingEnabled = false;
  private _cellIdList: string[] = [];
}
