export type NotebookEvent =
  | NotebookClickEvent
  | CellClickEvent
  | CodeExecutionEvent
  | MarkdownExecutionEvent
  | CellAlterationEvent;

export class NotebookClickEvent {
  name: 'Notebook Click' = 'Notebook Click';

  constructor(
    public click_type: 'ON' | 'OFF',
    public click_duration: number | null
  ) {}
}

export class CellClickEvent {
  name: 'Cell Click' = 'Cell Click';

  constructor(
    public cell_id: string,
    public orig_cell_id: string,
    public click_type: 'ON' | 'OFF',
    public click_duration: number | null
  ) {}
}

export class CodeExecutionEvent {
  name: 'Code Execution' = 'Code Execution';

  constructor(
    public language_mimetype: string,
    public cell_id: string,
    public orig_cell_id: string,
    public status: 'ok' | 'error',
    public cell_input: string,
    public cell_output_length: number
  ) {}
}

export class MarkdownExecutionEvent {
  name: 'Markdown Execution' = 'Markdown Execution';

  constructor(
    public cell_id: string,
    public orig_cell_id: string,
    public cell_content: string
  ) {}
}

export class CellAlterationEvent {
  name: 'Cell Alteration' = 'Cell Alteration';

  constructor(
    public cell_id: string,
    public alteration_type: 'ADD' | 'REMOVE'
  ) {}
}
