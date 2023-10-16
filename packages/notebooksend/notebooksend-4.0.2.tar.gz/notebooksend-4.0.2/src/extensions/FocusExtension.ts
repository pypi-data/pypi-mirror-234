import { Signal } from '@lumino/signaling';
import { IDisposable } from '@lumino/disposable';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { Cell, ICellModel } from '@jupyterlab/cells';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { postNotebookClick, postCellClick } from '../api';
import { LabShell } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { PLUGIN_ID, Selectors } from '../utils/constants';
import { StringId } from '../utils/types';
import { isNotebookValid } from '../utils/utils';
import { getMetadataComp } from '../utils/compatibility';

type ClickType = 'OFF' | 'ON';

export class FocusExtension implements DocumentRegistry.WidgetExtension {
  constructor(
    labShell: LabShell,
    settingRegistry: ISettingRegistry,
    jupyterVersion: number
  ) {
    this._labShell = labShell;
    this._settingRegistry = settingRegistry;
    this._jupyterVersion = jupyterVersion;
  }

  createNew(panel: NotebookPanel): IDisposable {
    return new FocusDisposable(
      panel,
      this._labShell,
      this._settingRegistry,
      this._jupyterVersion
    );
  }

  private _labShell: LabShell;
  private _settingRegistry: ISettingRegistry;
  private _jupyterVersion: number;
}

class FocusDisposable implements IDisposable {
  constructor(
    panel: NotebookPanel,
    labShell: LabShell,
    settingRegistry: ISettingRegistry,
    jupyterVersion: number
  ) {
    this._panel = panel;
    this._jupyterVersion = jupyterVersion;

    this._settingPromise = settingRegistry.load(`${PLUGIN_ID}:settings`);
    this._settingPromise.then(
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

        // call it a first time after the panel is ready to send missed start-up signals
        this._onCellChanged(panel.content, panel.content.activeCell);
        this._onNotebookChanged(labShell);

        // connect to active cell changes
        panel.content.activeCellChanged.connect(this._onCellChanged, this);

        // connect to panel changes
        labShell.currentChanged.connect(this._onNotebookChanged, this);

        // panel.content is disposed before panel itself, so release the associated connection before
        panel.content.disposed.connect(this._onContentDisposed, this);
      }
    });
  }

  private _updateSettings(settings: ISettingRegistry.ISettings) {
    this._isFocusSettingEnabled = settings.get('FocusExtension')
      .composite as boolean;
  }

  private _onContentDisposed = (content: Notebook) => {
    content.activeCellChanged.disconnect(this._onCellChanged, this);
    // directly release the content.disposed connection
    content.disposed.disconnect(this._onContentDisposed, this);
  };

  private _onCellChanged = (
    content: Notebook,
    activeCell: Cell<ICellModel> | null
  ) => {
    this._sendCellClick('OFF');

    // change both the id of the last active cell and the corresponding orig cell id
    this._setActiveCellAndOrigCellId(activeCell);

    if (this._focusON) {
      this._sendCellClick('ON');
    }
  };

  private _setActiveCellAndOrigCellId = (
    activeCell: Cell<ICellModel> | null
  ) => {
    this._lastActiveCellId = activeCell?.model.sharedModel.getId();
    if (this._lastActiveCellId) {
      this._lastOrigCellId = getMetadataComp(
        this._panel?.model,
        Selectors.cellMapping,
        this._jupyterVersion
      )?.find(([key]: [key: string]) => key === this._lastActiveCellId)?.[1];
    } else {
      this._lastOrigCellId = null;
    }
  };

  private _onNotebookChanged = (_labShell: LabShell) => {
    if (_labShell.currentWidget === this._panel) {
      this._isActive = true;
      // send ON message only if it's still active by the time the panel is ready (and if it's not already focused on)
      // the setting loading promise might resolve after the focus on the notebook, so still need to wait for it
      this._settingPromise.then((settings: ISettingRegistry.ISettings) => {
        if (!this.isDisposed) {
          if (this._isActive && !this._focusON) {
            this._sendNotebookClick('ON');
            this._sendCellClick('ON');
            this._focusON = true;
          }
        }
      });
    } else {
      // check if there was focus on that notebook
      if (this._focusON) {
        this._sendNotebookClick('OFF');
        this._sendCellClick('OFF');
      }
      this._focusON = false;
      this._isActive = false;
    }
  };

  private _sendCellClick = (clickType: ClickType) => {
    if (this._lastActiveCellId && this._isFocusSettingEnabled) {
      let cellDurationSec: number | null = null;
      if (clickType === 'ON') {
        this._cellStart = new Date();
        cellDurationSec = null;
      } else {
        const cellEnd = new Date();
        cellDurationSec =
          (cellEnd.getTime() - this._cellStart.getTime()) / 1000;
      }

      if (this._lastOrigCellId) {
        postCellClick({
          notebook_id: this._notebookId,
          instance_id: this._instanceId,
          cell_id: this._lastActiveCellId,
          orig_cell_id: this._lastOrigCellId,
          click_type: clickType,
          time: new Date().toISOString(),
          click_duration: cellDurationSec
        });
      }
    }
  };

  private _sendNotebookClick = (clickType: ClickType) => {
    if (this._isFocusSettingEnabled) {
      let notebookDurationSec: number | null = null;
      if (clickType === 'ON') {
        this._notebookStart = new Date();
        notebookDurationSec = null;
      } else {
        const notebookEnd = new Date();
        notebookDurationSec =
          (notebookEnd.getTime() - this._notebookStart.getTime()) / 1000;
      }

      postNotebookClick({
        notebook_id: this._notebookId,
        instance_id: this._instanceId,
        click_type: clickType,
        time: new Date().toISOString(),
        click_duration: notebookDurationSec
      });
    }
  };

  get isDisposed(): boolean {
    return this._isDisposed;
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }

    if (this._focusON) {
      this._sendNotebookClick('OFF');
      this._sendCellClick('OFF');
    }

    this._focusON = false;
    this._isActive = false;
    this._isDisposed = true;
    this._panel = null;
    this._notebookId = null;
    this._instanceId = null;
    this._lastActiveCellId = null;

    Signal.clearData(this);
  }

  private _jupyterVersion: number;
  private _focusON = false;
  private _isActive = false;
  private _isDisposed = false;
  private _panel: NotebookPanel | null;
  private _isFocusSettingEnabled = false;
  private _settingPromise: Promise<ISettingRegistry.ISettings>;
  private _notebookId: StringId = undefined;
  private _instanceId: StringId = undefined;
  private _lastActiveCellId: string | null | undefined = null;
  private _lastOrigCellId: string | null | undefined = null;

  private _notebookStart: Date = new Date();
  private _cellStart: Date = new Date();
}
