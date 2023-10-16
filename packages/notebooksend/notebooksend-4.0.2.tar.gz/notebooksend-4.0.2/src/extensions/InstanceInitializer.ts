import { Signal } from '@lumino/signaling';
import { v4 as uuidv4 } from 'uuid';
import { IDisposable } from '@lumino/disposable';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { NotebookPanel, INotebookModel } from '@jupyterlab/notebook';
import { Selectors } from '../utils/constants';
import { getMetadataComp, setMetadataComp } from '../utils/compatibility';

export class InstanceInitializer
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  constructor(jupyterVersion: number) {
    this._jupyterVersion = jupyterVersion;
  }

  createNew(panel: NotebookPanel) {
    return new InstanceInitializerDisposable(panel, this._jupyterVersion);
  }

  private _jupyterVersion: number;
}

class InstanceInitializerDisposable implements IDisposable {
  constructor(panel: NotebookPanel, jupyterVersion: number) {
    panel.context.ready.then(() => {
      const notebookModel = panel.context.model;

      if (
        getMetadataComp(notebookModel, Selectors.notebookId, jupyterVersion)
      ) {
        // if no instance_id yet, assign a random one
        if (
          !getMetadataComp(notebookModel, Selectors.instanceId, jupyterVersion)
        ) {
          setMetadataComp(
            notebookModel,
            Selectors.instanceId,
            uuidv4(),
            jupyterVersion
          );
        }
      }
    });
  }

  get isDisposed(): boolean {
    return this._isDisposed;
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    this._isDisposed = true;
    Signal.clearData(this);
  }

  private _isDisposed = false;
}
