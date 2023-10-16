import { MiddlewareAPI, Dispatch, AnyAction } from '@reduxjs/toolkit';
import { STORAGE_KEY } from '../utils/constants';

export const localStorageMiddleware =
  (store: MiddlewareAPI) => (next: Dispatch) => (action: AnyAction) => {
    const result = next(action);
    // regexp: only execute the middleware logic for actions with type starting with 'sidedashboard/'
    if (/^sidedashboard\//.test(action.type)) {
      const state = store.getState();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.sidedashboard));
    }
    return result;
  };
