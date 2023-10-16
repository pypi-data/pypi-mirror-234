import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import {
  INotebookModel,
  NotebookPanel,
  NotebookActions,
  Notebook
} from '@jupyterlab/notebook';
import { JSONExt, JSONObject } from '@lumino/coreutils';
import { IDisposable } from '@lumino/disposable';
import { Signal } from '@lumino/signaling';
import { Cell, CodeCell, MarkdownCell } from '@jupyterlab/cells';
import { processCellOutput } from '../utils/utils';
import { PLUGIN_ID } from '../utils/constants';
import { postCodeExec, postMarkdownExec } from '../api';
import { StringId } from '../utils/types';
import { Selectors } from '../utils/constants';
import { isNotebookValid } from '../utils/utils';
import { getMetadataComp } from '../utils/compatibility';

export class ExecutionExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  constructor(settingRegistry: ISettingRegistry, jupyterVersion: number) {
    this._settingRegistry = settingRegistry;
    this._jupyterVersion = jupyterVersion;
  }

  createNew(panel: NotebookPanel) {
    return new ExecutionDisposable(
      panel,
      this._settingRegistry,
      this._jupyterVersion
    );
  }

  private _settingRegistry: ISettingRegistry;
  private _jupyterVersion: number;
}

class ExecutionDisposable implements IDisposable {
  constructor(
    panel: NotebookPanel,
    settingRegistry: ISettingRegistry,
    jupyterVersion: number
  ) {
    this._panel = panel;
    this._settingRegistry = settingRegistry;
    this._jupyterVersion = jupyterVersion;

    settingRegistry.load(`${PLUGIN_ID}:settings`).then(
      (settings: ISettingRegistry.ISettings) => {
        this._updateSettings(settings);
        settings.changed.connect(this._updateSettings.bind(this));

        // if the plugin is enabled, force recording of timing
        // we only do this once (not on every settings update) in case the user turns it off
        if (settings.get('ExecutionExtension').composite) {
          this._settingRegistry
            .load('@jupyterlab/notebook-extension:tracker')
            .then(
              (nbSettings: ISettingRegistry.ISettings) =>
                nbSettings.set('recordTiming', true),
              (err: Error) => {
                console.error(
                  `${PLUGIN_ID}: Could not force metadata recording: ${err}`
                );
              }
            );
        }
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

        // connect to cell execution
        NotebookActions.executed.connect(this._onCellExecuted, this);

        panel.disposed.connect(() =>
          NotebookActions.executed.disconnect(this._onCellExecuted, this)
        );
      }
    });
  }

  private _updateSettings(settings: ISettingRegistry.ISettings) {
    this._isExecutionSettingEnabled = settings.get('ExecutionExtension')
      .composite as boolean;
  }

  private _onCellExecuted(
    sender: any,
    args: { notebook: Notebook; cell: Cell }
  ) {
    if (this._isExecutionSettingEnabled) {
      const { notebook, cell } = args;

      // only track the executions of the current panel instance
      if (notebook !== this._panel.content) {
        return;
      }
      if (cell instanceof CodeCell) {
        const executionMetadata = getMetadataComp(
          cell.model,
          'execution',
          this._jupyterVersion
        ) as JSONObject;
        if (executionMetadata && JSONExt.isObject(executionMetadata)) {
          const startTimeStr = (executionMetadata[
            'shell.execute_reply.started'
          ] || executionMetadata['iopub.execute_input']) as string | null;
          const endTimeStr = executionMetadata['shell.execute_reply'] as
            | string
            | null;
          const executionAborted =
            endTimeStr && !executionMetadata['iopub.execute_input'];

          if (!executionAborted) {
            if (endTimeStr && startTimeStr) {
              const outputs = cell.model.outputs.toJSON();
              const notebookModel = this._panel.model;
              const { status, cell_output_length } = processCellOutput(outputs);
              const orig_cell_id: string | undefined = getMetadataComp(
                notebookModel,
                Selectors.cellMapping,
                this._jupyterVersion
              )?.find(([key]: [key: string]) => key === cell.model.id)?.[1];

              if (orig_cell_id) {
                postCodeExec({
                  notebook_id: this._notebookId,
                  instance_id: this._instanceId,
                  language_mimetype:
                    getMetadataComp(
                      notebookModel,
                      'language_info',
                      this._jupyterVersion
                    )['mimetype'] || 'text/plain',
                  cell_id: cell.model.id,
                  orig_cell_id: orig_cell_id,
                  t_start: startTimeStr,
                  t_finish: endTimeStr,
                  status: status,
                  cell_input: cell.model.sharedModel.getSource(),
                  cell_output_model: outputs,
                  cell_output_length: cell_output_length
                });
              }
            }
          }
        }
      } else if (cell instanceof MarkdownCell) {
        const orig_cell_id: string | undefined = getMetadataComp(
          this._panel.model,
          Selectors.cellMapping,
          this._jupyterVersion
        )?.find(([key]: [key: string]) => key === cell.model.id)?.[1];

        if (orig_cell_id) {
          postMarkdownExec({
            notebook_id: this._notebookId,
            instance_id: this._instanceId,
            cell_id: cell.model.id,
            orig_cell_id: orig_cell_id,
            time: new Date().toISOString(),
            cell_content: cell.model.sharedModel.getSource()
          });
        }
      }
    }
  }

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

    Signal.clearData(this);
  }

  private _panel: NotebookPanel;
  private _settingRegistry: ISettingRegistry;
  private _jupyterVersion: number;
  private _isDisposed = false;
  private _notebookId: StringId = undefined;
  private _instanceId: StringId = undefined;
  private _isExecutionSettingEnabled = false;
}
