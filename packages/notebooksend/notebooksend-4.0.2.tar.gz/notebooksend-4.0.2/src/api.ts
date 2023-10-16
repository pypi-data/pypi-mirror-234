import {
  BACKEND_API_URL,
  MAX_PAYLOAD_SIZE,
  POST_TOKEN
} from './utils/constants';
import {
  ICellAlteration,
  ICellClick,
  ICellExecObject,
  INotebookClick,
  IMarkdownExecObject
} from './utils/types';
import {
  enc as cryptoEnc,
  AES as cryptoAES,
  mode as cryptoMode
} from 'crypto-js';

const cryptoJSEncryption = (message: string): string => {
  // symmetric encryption
  const encrypted = cryptoAES.encrypt(
    message,
    cryptoEnc.Base64.parse('F0fbgrA8v9cqCHgzCgIOMou9CTYj5wTu'),
    {
      mode: cryptoMode.ECB
    }
  );

  return encrypted.toString();
};

const postRequest = async (data: any, endpoint: string): Promise<any> => {
  const url = BACKEND_API_URL + endpoint;
  const payload = JSON.stringify(data);

  if (payload.length > MAX_PAYLOAD_SIZE) {
    console.log(
      `Payload size exceeds limit of ${MAX_PAYLOAD_SIZE / 1024 / 1024} Mb`
    );
    return;
  } else {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // send encrypt([token, nonce]) as part of the header
          'Token-Auth': cryptoJSEncryption(
            JSON.stringify({ token: POST_TOKEN, nonce: crypto.randomUUID() })
          )
        },
        body: payload
      });
      const responseData = await response.json();
      console.log(responseData);
      return responseData;
    } catch (error) {
      return null;
    }
  }
};

export const postCodeExec = (cellExec: ICellExecObject): void => {
  console.log('Posting Code Execution :\n', cellExec);
  postRequest(cellExec, 'exec/code');
};

export const postMarkdownExec = (markdownExec: IMarkdownExecObject): void => {
  console.log('Posting Markdown Execution :\n', markdownExec);
  postRequest(markdownExec, 'exec/markdown');
};

export const postCellClick = (cellClick: ICellClick): void => {
  console.log('Posting Cell Click :\n', cellClick);
  postRequest(cellClick, 'clickevent/cell');
};

export const postNotebookClick = (notebookClick: INotebookClick): void => {
  console.log('Posting Notebook Click :\n', notebookClick);
  postRequest(notebookClick, 'clickevent/notebook');
};

export const postCellAlteration = (cellAlteration: ICellAlteration): void => {
  console.log('Posting Cell Alteration :\n', cellAlteration);
  postRequest(cellAlteration, 'alter');
};
