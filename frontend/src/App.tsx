import { Outlet } from 'react-router';

import { AppNavigationBar } from './AppNavigationBar';
import { RecipeProvider } from './context/RecipeProvider';
import { Box } from '@mui/material';

export default function App() {
  return (
    <RecipeProvider>
      <Box sx={{width: "clamp(320px, 100vw, 600px)", margin: "0 auto"}}>
      <AppNavigationBar />
      <Outlet />
      </Box>
    </RecipeProvider>
  );
}