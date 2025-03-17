type State = {
    recipes: any[];  
    isLoading: boolean;
    error: string | null;
  };
  
export type RecipeReducerAction =
  | { type: 'FETCH_RECIPES_START' }
  | { type: 'FETCH_RECIPES_SUCCESS'; payload: any[] }
  | { type: 'FETCH_RECIPES_ERROR'; payload: string };

const initialState: State = {
  recipes: [],
  isLoading: false,
  error: null,
};
  
const recipeReducer = (state: State, action: RecipeReducerAction): State => {
  switch (action.type) {
    case 'FETCH_RECIPES_START':
      return { ...state, isLoading: true, error: null };
    case 'FETCH_RECIPES_SUCCESS':
      return { ...state, isLoading: false, recipes: action.payload };
    case 'FETCH_RECIPES_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    default:
      return state;
  }
};

export { recipeReducer, initialState };
  