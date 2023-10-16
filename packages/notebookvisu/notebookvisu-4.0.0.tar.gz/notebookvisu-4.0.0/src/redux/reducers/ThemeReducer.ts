import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ThemeState } from '../types';

const initialThemeState: ThemeState = {
  isThemeLight: true
};

export const themeSlice = createSlice({
  name: 'theme',
  initialState: initialThemeState,
  reducers: {
    changeTheme: (state, action: PayloadAction<boolean>) => {
      // safe to mutate state inside since createSlice is using Immer internally to translate this to immutable changes
      state.isThemeLight = action.payload;
    }
  }
});

export const { changeTheme } = themeSlice.actions;

export default themeSlice.reducer;
