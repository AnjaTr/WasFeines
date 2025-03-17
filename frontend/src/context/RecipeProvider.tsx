import React, { createContext, useReducer, useContext, ReactNode } from 'react';
import { recipeReducer, initialState, RecipeReducerAction } from './recipeReducer';

interface RecipeContextProps {
  state: typeof initialState;
  dispatch: React.Dispatch<RecipeReducerAction>;
}

const RecipeContext = createContext<RecipeContextProps | undefined>(undefined);

export const useRecipeContext = () => {
  const context = useContext(RecipeContext);
  if (!context) {
    throw new Error('useRecipeContext must be used within a RecipeProvider');
  }
  return context;
};

interface RecipeProviderProps {
  children: ReactNode;
}

export const RecipeProvider = ({ children }: RecipeProviderProps) => {
  const [state, dispatch] = useReducer(recipeReducer, initialState);

  return (
    <RecipeContext.Provider value={{ state, dispatch }}>
      {children}
    </RecipeContext.Provider>
  );
};
