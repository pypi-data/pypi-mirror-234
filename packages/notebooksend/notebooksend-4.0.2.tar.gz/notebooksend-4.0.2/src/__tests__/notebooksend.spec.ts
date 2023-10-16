import { PLUGIN_ID } from '../utils/constants';
import { computeLength, processCellOutput } from '../utils/utils';
import { IOutput } from '@jupyterlab/nbformat';

describe(`${PLUGIN_ID}`, () => {
  const s_10 = '0123456789';
  const s_20 = s_10 + '\n       01';

  it('utils: computeLength', () => {
    expect(computeLength(s_10)).toBe(10);
    expect(computeLength(s_20)).toBe(20);
  });

  const o_1 = JSON.parse(`[
    {
      "name": "stdout",
      "output_type": "stream",
      "text": [
        "This is the first function\\n"
      ]
    }
  ]`) as IOutput[];

  const o_2 = JSON.parse(`[
    {
     "ename": "SyntaxError",
     "evalue": "Identifier 'func' has already been declared",
     "execution_count": 5,
     "output_type": "error",
     "traceback": [
      "evalmachine.<anonymous>:1",
      "const func = () => {",
      "^",
      "",
      "SyntaxError: Identifier 'func' has already been declared",
      "    at Script.runInThisContext (node:vm:129:12)",
      "    at Object.runInThisContext (node:vm:307:38)",
      "    at run ([eval]:1020:15)",
      "    at onRunRequest ([eval]:864:18)",
      "    at onMessage ([eval]:828:13)",
      "    at process.emit (node:events:513:28)",
      "    at emit (node:internal/child_process:937:14)",
      "    at process.processTicksAndRejections (node:internal/process/task_queues:83:21)"
     ]
    }
   ]`) as IOutput[];

  const o_combined = JSON.parse(`[
    {
      "name": "stdout",
      "output_type": "stream",
      "text": [
        "This is the first function\\n"
      ]
    },
    {
      "ename": "SyntaxError",
      "evalue": "Identifier 'func' has already been declared",
      "execution_count": 5,
      "output_type": "error",
      "traceback": [
       "evalmachine.<anonymous>:1",
       "const func = () => {",
       "^",
       "",
       "SyntaxError: Identifier 'func' has already been declared",
       "    at Script.runInThisContext (node:vm:129:12)",
       "    at Object.runInThisContext (node:vm:307:38)",
       "    at run ([eval]:1020:15)",
       "    at onRunRequest ([eval]:864:18)",
       "    at onMessage ([eval]:828:13)",
       "    at process.emit (node:events:513:28)",
       "    at emit (node:internal/child_process:937:14)",
       "    at process.processTicksAndRejections (node:internal/process/task_queues:83:21)"
      ]
     }
   ]`) as IOutput[];

  it('utils: processCellOutput', () => {
    expect(processCellOutput(o_1)).toEqual({
      status: 'ok',
      cell_output_length: 27
    });
    expect(processCellOutput(o_2)).toEqual({
      status: 'error',
      cell_output_length: 43
    });
    expect(processCellOutput(o_combined)).toEqual({
      status: 'error',
      cell_output_length: 70
    });
  });
});
