import { INotebookModel } from '@jupyterlab/notebook';
import { ICellModel } from '@jupyterlab/cells';

export const getMetadataComp = (
  model: INotebookModel | ICellModel | null | undefined,
  key: string,
  jupyterVersion: number
): any => {
  if (jupyterVersion === 4) {
    return (model as any)?.getMetadata(key);
  } else {
    return (model?.metadata as any)?.get(key);
  }
};

export const setMetadataComp = (
  model: INotebookModel | ICellModel | null | undefined,
  key: string,
  value: any,
  jupyterVersion: number
): void => {
  if (jupyterVersion === 4) {
    (model as any)?.setMetadata(key, value);
  } else {
    (model?.metadata as any)?.set(key, value);
  }
};

export const getCellIdsComp = (
  cells: any,
  jupyterVersion: number
): string[] => {
  if (jupyterVersion === 4) {
    return Array.from(cells).map((item: any) => item.id);
  } else {
    return Array.from(
      { length: cells.length },
      (_, index) => cells.get(index).id
    );
  }
};
