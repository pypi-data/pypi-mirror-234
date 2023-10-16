import { IOutput } from '@jupyterlab/nbformat';

export type StringId = string | null | undefined;

export interface IExecBatchObject {
  cell_id: string;
  orig_cell_id: StringId;
  t_start: string;
  t_finish: string;
  status: string;
  cell_input: string;
  cell_output_model: IOutput[];
  cell_output_length: number;
}

export interface ICellExecObject extends IExecBatchObject {
  notebook_id: StringId;
  instance_id: StringId;
  language_mimetype: string;
}

export interface IMarkdownExecObject {
  notebook_id: StringId;
  instance_id: StringId;
  cell_id: string;
  orig_cell_id: StringId;
  time: string;
  cell_content: string;
}

export interface INotebookClick {
  notebook_id: StringId;
  instance_id: StringId;
  click_type: string; // ON or OFF
  time: string;
  click_duration: number | null;
}

export interface ICellClick {
  notebook_id: StringId;
  instance_id: StringId;
  cell_id: string;
  orig_cell_id: StringId;
  click_type: string; // ON or OFF
  time: string;
  click_duration: number | null;
}

export interface ICellAlteration {
  notebook_id: StringId;
  instance_id: StringId;
  cell_id: string;
  alteration_type: string; // ADD or REMOVE
  time: string;
}
