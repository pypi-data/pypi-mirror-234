import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { LocationData, ToCState } from '../types';

export const initialToCDashboardState: ToCState = {
  displayDashboard: true,
  hasNotebookId: false,
  locationData: null
};

export const tocDashboardSlice = createSlice({
  name: 'tocdashboard',
  initialState: initialToCDashboardState,
  reducers: {
    setDisplayHideDashboard: (state, action: PayloadAction<boolean>) => {
      state.displayDashboard = action.payload;
    },
    setHasNotebookId: (state, action: PayloadAction<boolean>) => {
      state.hasNotebookId = action.payload;
    },
    setFetchedLocationData: (state, action: PayloadAction<LocationData>) => {
      state.locationData = action.payload;
    }
  }
});

export const {
  setDisplayHideDashboard,
  setHasNotebookId,
  setFetchedLocationData
} = tocDashboardSlice.actions;

export default tocDashboardSlice.reducer;
