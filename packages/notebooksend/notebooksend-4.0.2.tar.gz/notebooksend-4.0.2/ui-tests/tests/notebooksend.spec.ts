import { expect, test } from '@jupyterlab/galata';
// import {
//   createNamedNotebook,
//   events_notebook_1_1,
//   events_notebook_2,
//   events_notebook_1_2,
//   generateRegExp
// } from './utils';

test.use({ autoGoto: false });

test('should emit an activation console message', async ({ page }) => {
  const logs: string[] = [];

  page.on('console', message => {
    logs.push(message.text());
  });

  await page.goto();

  expect(
    logs.filter(s => s === 'JupyterLab extension notebooksend is activated!')
  ).toHaveLength(1);
});
/*
  test('With settings disabled', async ({ page, tmpPath }) => {
    ///// RETRIEVING LOGS /////

    // catch the printed logs
    const receivedLogs: string[] = [];

    page.on('console', async msg => {
      let messageStr = '';
      for (const arg of msg.args()) {
        const value = await arg.jsonValue();
        if (typeof value === 'string') {
          messageStr += value;
        } else {
          messageStr += JSON.stringify(value);
        }
      }
      receivedLogs.push(messageStr);
    });

    const notebookId_settings_off = 'settings_off.ipynb';
    const instanceId_settings_off = 'instance_settings_off';

    // change the settings, disable everything
    await page.getByRole('menuitem', { name: 'Settings' }).click();
    await page
      .getByRole('menuitem', { name: 'Settings Editor Ctrl+,' })
      .click();
    await page
      .getByRole('tab', { name: 'Plugin Notebook Activity Recording' })
      .getByText('Notebook Activity Recording')
      .click();
    await page.getByLabel('Notebook & Cell Clicks').uncheck();
    await page.getByLabel('Cell Addition/Deletion').uncheck();
    await page.getByLabel('Cell Execution').uncheck();
    await page.waitForTimeout(2000);

    // create a notebook to check that nothing is posted when the settings are disabled
    await createNamedNotebook(
      page,
      notebookId_settings_off,
      true,
      notebookId_settings_off,
      instanceId_settings_off
    );
    await page.waitForTimeout(2000);
    await page.notebook.open(notebookId_settings_off);
    await page.waitForTimeout(2000);
    await page.notebook.runCell(0);
    await page.notebook.runCell(1);
    await page.notebook.runCell(2);
    await page.notebook.runCell(3);
    await page.notebook.deleteCells();
    await page.notebook.runCell(4);
    await page.notebook.addCell('code', 'print("hello")');
    await page.notebook.save();
    await page.notebook.close();

    ///// TESTS /////

    let hasSettingsOFFMessage = false;
    for (const receivedLog of receivedLogs) {
      if (
        receivedLog.includes(notebookId_settings_off) ||
        receivedLog.includes(instanceId_settings_off)
      ) {
        hasSettingsOFFMessage = true;
      }
    }

    // check that no log messages were posted when settings were disabled
    expect(hasSettingsOFFMessage).toBeFalsy();
  });

  test('Comparing posted signals with expected values', async ({
    page,
    tmpPath
  }) => {
    ///// RETRIEVING LOGS /////

    // catch the printed logs
    const receivedLogs: string[] = [];

    page.on('console', async msg => {
      let messageStr = '';
      for (const arg of msg.args()) {
        const value = await arg.jsonValue();
        if (typeof value === 'string') {
          messageStr += value;
        } else {
          messageStr += JSON.stringify(value);
        }
      }
      receivedLogs.push(messageStr);
    });

    // generate the RegExp for the expected logs
    const notebookId_1 = 'first.ipynb';
    const instanceId_1 = 'instance_1';

    const notebookId_2 = 'second.ipynb';
    const instanceId_2 = 'instance_2';

    const notebookId_no_id = 'no_id.ipynb';
    const instanceId_no_id = 'instance_no_id';

    // expected logs of the interactions with the 1st notebook
    const expectedLogs_1_1 = generateRegExp(
      notebookId_1,
      instanceId_1,
      events_notebook_1_1
    );

    // expected logs of the interactions with the 2nd notebook
    const expectedLogs_2 = generateRegExp(
      notebookId_2,
      instanceId_2,
      events_notebook_2
    );

    // expected logs of the second interactions with the 1st notebook
    const expectedLogs_1_2 = generateRegExp(
      notebookId_1,
      instanceId_1,
      events_notebook_1_2
    );

    // combine the logs
    const expectedLogs: RegExp[] = [
      ...expectedLogs_1_1
      // ...expectedLogs_2
      // ...expectedLogs_1_2
    ];

    ///// MANIPULATIONS /////

    // create notebooks and select/run cells to mimic activity

    // create 1st notebook
    await createNamedNotebook(
      page,
      notebookId_1,
      true,
      notebookId_1,
      instanceId_1
    );

    // manipulate 1st notebook
    await page.notebook.open(notebookId_1);
    await page.waitForTimeout(2000);
    // to move to a cell (index starts a 0)
    await page.notebook.selectCells(0);

    await page.notebook.runCell(0); // run all the cells
    await page.notebook.runCell(1);
    await page.notebook.runCell(2);
    await page.notebook.runCell(3);
    await page.notebook.runCell(4);
    await page.notebook.save();

    // create 2nd notebook
    await createNamedNotebook(
      page,
      notebookId_2,
      true,
      notebookId_2,
      instanceId_2
    );

    // manipulate 2nd notebook
    await page.notebook.open(notebookId_2);
    await page.waitForTimeout(2000);
    await page.notebook.runCell(2); // error expected due to import error
    await page.notebook.runCell(1);
    await page.notebook.runCell(2);
    await page.notebook.addCell('code', '2+3'); // add a cell
    await page.notebook.addCell('markdown', '# Last Cell'); // add a cell
    await page.notebook.runCell(6); // run that new cell, will create a new cell
    await page.notebook.selectCells(2);
    await page.notebook.deleteCells(); // deletes the last selected cell
    await page.notebook.save();
    await page.notebook.close(); // close the notebook, should switch back to the first notebook

    // 1st notebook
    await page.notebook.selectCells(4);
    await page.notebook.deleteCells();
    await page.notebook.save();
    await page.notebook.close();

    // create notebook with no notebook_id
    await createNamedNotebook(
      page,
      notebookId_no_id,
      false,
      notebookId_no_id,
      instanceId_no_id
    );
    await page.notebook.open(notebookId_no_id);
    await page.waitForTimeout(2000);
    await page.notebook.runCell(0);
    await page.notebook.runCell(1);
    await page.notebook.runCell(2);
    await page.notebook.runCell(3);
    await page.notebook.runCell(4);
    await page.notebook.save();
    await page.notebook.close();

    ///// TESTS /////

    // go through the received logs and see if all expected logs are there
    let hasIdNotebookMessage = false;
    let expectedIndex = 0;
    for (const receivedLog of receivedLogs) {
      if (
        expectedIndex < expectedLogs.length &&
        expectedLogs[expectedIndex].test(receivedLog)
      ) {
        expectedIndex++;
      }
      if (
        receivedLog.includes(notebookId_no_id) ||
        receivedLog.includes(instanceId_no_id)
      ) {
        hasIdNotebookMessage = true;
      }
    }

    expect(expectedIndex).toBe(expectedLogs.length);
    // check that no log message were posted with the notebook did not have a notebook_id
    expect(hasIdNotebookMessage).toBeFalsy();
  });
  */
