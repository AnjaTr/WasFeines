import { Outlet } from 'react-router';

import { AppNavigationBar } from './AppNavigationBar';
import { RecipeProvider } from './context/RecipeProvider';

export default function App() {
  return (
    <RecipeProvider>
      <AppNavigationBar />
      <Outlet />
    </RecipeProvider>
  );
}