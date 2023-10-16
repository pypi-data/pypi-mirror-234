import { configureStore } from '@reduxjs/toolkit';
import ThemeReducer from './reducers/ThemeReducer';
import ToCDashboardReducer from './reducers/ToCDashboardReducer';
import SideDashboardReducer from './reducers/SideDashboardReducer';
import CommonDashboard from './reducers/CommonDashboardReducer';
import { localStorageMiddleware } from './localStorage';
import { STORAGE_KEY } from '../utils/constants';
import { initialSideDashboardState } from './reducers/SideDashboardReducer';

const preloadedState = {
  sidedashboard: localStorage.getItem(STORAGE_KEY)
    ? JSON.parse(localStorage.getItem(STORAGE_KEY) as string)
    : initialSideDashboardState
};

export const store = configureStore({
  reducer: {
    theme: ThemeReducer,
    tocdashboard: ToCDashboardReducer,
    sidedashboard: SideDashboardReducer,
    commondashboard: CommonDashboard
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware().concat(localStorageMiddleware),
  preloadedState: preloadedState
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
