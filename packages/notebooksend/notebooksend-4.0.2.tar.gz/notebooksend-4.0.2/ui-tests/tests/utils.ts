import { IJupyterLabPageFixture } from '@jupyterlab/galata';
import {
  NotebookEvent,
  NotebookClickEvent,
  CellClickEvent,
  CodeExecutionEvent,
  MarkdownExecutionEvent,
  CellAlterationEvent
} from './types';

const generateNotebookJSON = (
  hasNotebookId: boolean,
  notebookId: string,
  instanceId: string
) => {
  const notebookJSON = {
    cells: [
      {
        cell_type: 'markdown',
        id: 'cell_1',
        metadata: {},
        source: ['# Main Title']
      },
      {
        cell_type: 'code',
        execution_count: 1,
        id: 'cell_2',
        metadata: {
          execution: {
            'iopub.execute_input': '2023-07-10T11:05:42.086171Z',
            'iopub.status.busy': '2023-07-10T11:05:42.085142Z',
            'iopub.status.idle': '2023-07-10T11:05:42.117294Z',
            'shell.execute_reply': '2023-07-10T11:05:42.115263Z',
            'shell.execute_reply.started': '2023-07-10T11:05:42.086171Z'
          }
        },
        outputs: [],
        source: ['import time']
      },
      {
        cell_type: 'code',
        execution_count: 2,
        id: 'cell_3',
        metadata: {
          execution: {
            'iopub.execute_input': '2023-07-10T11:05:44.799398Z',
            'iopub.status.busy': '2023-07-10T11:05:44.798385Z',
            'iopub.status.idle': '2023-07-10T11:05:45.826184Z',
            'shell.execute_reply': '2023-07-10T11:05:45.824210Z',
            'shell.execute_reply.started': '2023-07-10T11:05:44.799398Z'
          }
        },
        outputs: [],
        source: ['time.sleep(1)\n', '2+3']
      },
      {
        cell_type: 'markdown',
        id: 'cell_4',
        metadata: {},
        source: ['## Function section']
      },
      {
        cell_type: 'code',
        execution_count: 3,
        id: 'cell_5',
        metadata: {
          execution: {
            'iopub.execute_input': '2023-06-02T13:34:25.149066Z',
            'iopub.status.busy': '2023-06-02T13:34:25.142635Z',
            'iopub.status.idle': '2023-06-02T13:34:25.175064Z',
            'shell.execute_reply': '2023-06-02T13:34:25.174059Z',
            'shell.execute_reply.started': '2023-06-02T13:34:25.149066Z'
          }
        },
        outputs: [
          {
            name: 'stdout',
            output_type: 'stream',
            text: ['This is a function\n']
          },
          {
            data: {
              'text/plain': ['4']
            },
            execution_count: 3,
            metadata: {},
            output_type: 'execute_result'
          }
        ],
        source: [
          'def f(a) : \n',
          '    print("This is a function")\n',
          '    return a+2\n',
          'f(2)'
        ]
      },
      {
        cell_type: 'code',
        execution_count: null,
        id: 'cell_6',
        metadata: {},
        outputs: [],
        source: []
      }
    ],
    metadata: {
      unianalytics_instance_id: instanceId,
      unianalytics_cell_mapping: [
        ['cell_1', 'cell_1'],
        ['cell_2', 'cell_2'],
        ['cell_3', 'cell_3'],
        ['cell_4', 'cell_4'],
        ['cell_5', 'cell_5'],
        ['cell_6', 'cell_6']
      ],
      kernelspec: {
        display_name: 'Python 3 (ipykernel)',
        language: 'python',
        name: 'python3'
      },
      language_info: {
        codemirror_mode: {
          name: 'ipython',
          version: 3
        },
        file_extension: '.py',
        mimetype: 'text/x-python',
        name: 'python',
        nbconvert_exporter: 'python',
        pygments_lexer: 'ipython3',
        version: '3.10.11'
      }
    } as any,
    nbformat: 4,
    nbformat_minor: 5
  };

  if (hasNotebookId) {
    notebookJSON.metadata.unianalytics_notebook_id = notebookId;
  }

  return notebookJSON;
};

export const createNamedNotebook = async (
  page: IJupyterLabPageFixture,
  fileName: string,
  hasNotebookId: boolean,
  notebookId: string,
  instanceId: string
) => {
  // create a temporary text file to populate it with notebook content so it's not opened as a notebook yet
  await page.getByRole('button', { name: 'New Launcher' }).click();
  await page.getByText('Text File', { exact: true }).last().click();
  await page
    .getByRole('region', { name: 'notebook content' })
    .getByRole('textbox')
    .fill(
      JSON.stringify(
        generateNotebookJSON(hasNotebookId, notebookId, instanceId)
      )
    );
  // save the change
  await page
    .getByRole('region', { name: 'notebook content' })
    .getByRole('textbox')
    .press('Control+s');
  await page.getByPlaceholder('File name').click({
    clickCount: 3
  });
  // rename it as a notebook
  await page.getByPlaceholder('File name').fill(fileName);
  await page.getByPlaceholder('File name').press('Enter');

  // close the editor and open it as notebook content
  await page.getByRole('tab', { name: fileName }).getByText(fileName).click({
    button: 'right'
  });
  await page
    .getByRole('menuitem', { name: 'Close Tab Alt+W' })
    .getByText('Close Tab')
    .click();
};

// to make sure special characters are preceded with a /
function escapeRegExp(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/\n/g, '\\\\n');
}

export const generateRegExp = (
  notebookId: string,
  instanceId: string,
  events: NotebookEvent[]
): RegExp[] => {
  const regs: RegExp[] = [];

  for (const e of events) {
    let regStr: string = `^Posting ${e.name}\\s*:\\s*\\{"notebook_id":"${notebookId}","instance_id":"${instanceId}",`;
    switch (e.name) {
      case 'Notebook Click':
        regStr += `"click_type":"${e.click_type}","time":".+","click_duration":.+\\}$`;
        break;

      case 'Cell Click':
        regStr += `"cell_id":"${e.cell_id}","orig_cell_id":".+","click_type":"${e.click_type}","time":".+","click_duration":.+\\}$`;
        break;

      case 'Cell Alteration':
        regStr += `"cell_id":"${e.cell_id}","alteration_type":"${e.alteration_type}","time":".+"\\}$`;
        break;

      case 'Code Execution':
        regStr += `"language_mimetype":"${e.language_mimetype}","cell_id":"${
          e.cell_id
        }","orig_cell_id":".+","t_start":".+","t_finish":".+","status":"${
          e.status
        }","cell_input":"${escapeRegExp(
          e.cell_input
        )}","cell_output_model":.+,"cell_output_length":${
          e.cell_output_length
        }\\}$`;
        break;

      case 'Markdown Execution':
        regStr += `"cell_id":"${
          e.cell_id
        }","orig_cell_id":".+","time":".+","cell_content":"${escapeRegExp(
          e.cell_content
        )}"\\}$`;
        break;

      default:
        throw new Error(`Unknown event type "${(e as any).name}"`);
    }
    regs.push(new RegExp(regStr));
  }

  return regs;
};

export const events_notebook_1_1: NotebookEvent[] = [
  new NotebookClickEvent('ON', null),
  new CellClickEvent('cell_1', 'cell_1', 'ON', null),
  new MarkdownExecutionEvent('cell_1', 'cell_1', '# Main Title'),
  new CellClickEvent('cell_1', 'cell_1', 'OFF', 2),
  new CellClickEvent('cell_2', 'cell_2', 'ON', null),
  new CellClickEvent('cell_2', 'cell_2', 'OFF', 2),
  new CellClickEvent('cell_3', 'cell_3', 'ON', null),
  new CodeExecutionEvent(
    'text/x-python',
    'cell_2',
    'cell_2',
    'ok',
    'import time',
    0
  ),
  new CellClickEvent('cell_3', 'cell_3', 'OFF', 2),
  new CellClickEvent('cell_4', 'cell_4', 'ON', null),
  new CodeExecutionEvent(
    'text/x-python',
    'cell_3',
    'cell_3',
    'ok',
    'time.sleep(1)\n2+3',
    3
  ),
  new MarkdownExecutionEvent('cell_4', 'cell_4', '## Function section'),
  new CellClickEvent('cell_4', 'cell_4', 'OFF', 2),
  new CellClickEvent('cell_5', 'cell_5', 'ON', null),
  new CellClickEvent('cell_5', 'cell_5', 'OFF', 2),
  new CellClickEvent('cell_6', 'cell_6', 'ON', null),
  new NotebookClickEvent('OFF', 2),
  new CellClickEvent('cell_6', 'cell_6', 'OFF', 2),
  new NotebookClickEvent('ON', null),
  new CellClickEvent('cell_6', 'cell_6', 'ON', null),
  new NotebookClickEvent('OFF', 2),
  new CellClickEvent('cell_6', 'cell_6', 'OFF', 2)
];

export const events_notebook_2: NotebookEvent[] = [
  new NotebookClickEvent('ON', null),
  new CellClickEvent('cell_1', 'cell_1', 'ON', null),
  new CellClickEvent('cell_1', 'cell_1', 'OFF', 2),
  new CellClickEvent('cell_3', 'cell_3', 'ON', null),
  new CellClickEvent('cell_3', 'cell_3', 'OFF', 2),
  new CellClickEvent('cell_4', 'cell_4', 'ON', null),
  new CodeExecutionEvent(
    'text/x-python',
    'cell_3',
    'cell_3',
    'error',
    'time.sleep(1)\n2+3',
    26
  ),
  new CellClickEvent('cell_4', 'cell_4', 'OFF', 2),
  new CellClickEvent('cell_2', 'cell_2', 'ON', null),
  new CellClickEvent('cell_2', 'cell_2', 'OFF', 2),
  new CellClickEvent('cell_3', 'cell_3', 'ON', null),
  new CodeExecutionEvent(
    'text/x-python',
    'cell_2',
    'cell_2',
    'ok',
    'import time',
    0
  ),
  new CellClickEvent('cell_3', 'cell_3', 'OFF', 2),
  new CellClickEvent('cell_4', 'cell_4', 'ON', null),
  new CodeExecutionEvent(
    'text/x-python',
    'cell_3',
    'cell_3',
    'ok',
    'time.sleep(1)\n2+3',
    3
  ),
  new CellClickEvent('cell_4', 'cell_4', 'OFF', 2),
  new CellClickEvent('cell_6', 'cell_6', 'ON', null),
  new CellAlterationEvent('.+', 'ADD'), //40
  new CellClickEvent('cell_6', 'cell_6', 'OFF', 2),
  new CellClickEvent('.+', '.+', 'ON', null),
  new CellAlterationEvent('.+', 'ADD'),
  new CellClickEvent('.+', '.+', 'OFF', 2),
  new CellClickEvent('.+', '.+', 'ON', null),
  new CellClickEvent('.+', '.+', 'OFF', 2),
  new CellAlterationEvent('.+', 'ADD'),
  new CellAlterationEvent('.+', 'REMOVE'),
  new CellClickEvent('.+', '.+', 'ON', null),
  new CellClickEvent('.+', '.+', 'OFF', 2),
  new CellClickEvent('.+', '.+', 'ON', null),
  new CellClickEvent('.+', '.+', 'OFF', 2),
  new CellClickEvent('.+', '.+', 'ON', null),
  new CodeExecutionEvent('text/x-python', '.+', '.+', 'ok', '2+3', 3),
  new CellClickEvent('.+', '.+', 'OFF', 2),
  new CellClickEvent('cell_3', 'cell_3', 'ON', null),
  new CellClickEvent('cell_3', 'cell_3', 'OFF', 2),
  new CellClickEvent('cell_2', 'cell_2', 'ON', null),
  new CellAlterationEvent('cell_3', 'REMOVE'),
  new CellClickEvent('cell_2', 'cell_2', 'OFF', 2),
  new CellClickEvent('cell_4', 'cell_4', 'ON', null),
  new CellClickEvent('cell_4', 'cell_4', 'OFF', 2),
  new CellClickEvent('cell_1', 'cell_1', 'ON', null),
  new NotebookClickEvent('OFF', 2) //64
  // new CellClickEvent('cell_1', 'cell_1', 'OFF', 2)
];

export const events_notebook_1_2: NotebookEvent[] = [
  new NotebookClickEvent('ON', null),
  new CellClickEvent('cell_6', 'cell_6', 'ON', null),
  new CellClickEvent('cell_6', 'cell_6', 'OFF', 2),
  new CellClickEvent('cell_5', 'cell_5', 'ON', null),
  new CellClickEvent('cell_5', 'cell_5', 'OFF', 2),
  new CellClickEvent('cell_4', 'cell_4', 'ON', null),
  new CellAlterationEvent('cell_5', 'REMOVE'),
  new CellClickEvent('cell_4', 'cell_4', 'OFF', 2),
  new CellClickEvent('cell_6', 'cell_6', 'ON', null),
  new CellClickEvent('cell_6', 'cell_6', 'OFF', 2),
  new CellClickEvent('cell_1', 'cell_1', 'ON', null),
  new NotebookClickEvent('OFF', 2),
  new CellClickEvent('cell_1', 'cell_1', 'OFF', 2)
];

// export const events_notebook_3: NotebookEvent[] = [];
