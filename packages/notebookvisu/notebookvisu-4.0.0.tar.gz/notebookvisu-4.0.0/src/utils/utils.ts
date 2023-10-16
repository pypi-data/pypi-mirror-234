import { SHA256 } from 'crypto-js';
import { NotebookPanel } from '@jupyterlab/notebook';
import { Selectors } from './constants';

export const isNotebookValidForVisu = (panel: NotebookPanel): boolean => {
  if (panel && !panel.isDisposed) {
    return panel.context.model.getMetadata(Selectors.notebookId);
  } else {
    return false;
  }
};

export const areListsEqual = (
  list1: string[] | null | undefined,
  list2: string[] | null | undefined
): boolean => {
  // if any of them is not defined, return not equal
  if (!list1 || !list2) {
    return false;
  }
  // Check if the lengths are equal
  if (list1.length !== list2.length) {
    return false;
  }

  // Check if every element in list1 is equal to the corresponding element in list2
  return list1.every((item, index) => item === list2[index]);
};

export const hashCellList = (cellList: string[] | null | undefined): string => {
  if (cellList && cellList.length > 0) {
    const combinedString = cellList.join('');
    return SHA256(combinedString).toString();
  } else {
    return '';
  }
};

// calculates the delay (in ms) to the next full second
export const calculateDelay = () => {
  const now = new Date();
  const milliseconds = now.getMilliseconds();
  const delay = 1000 - milliseconds;
  return delay;
};
