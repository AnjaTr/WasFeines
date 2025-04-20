import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from "react-router";
import './index.css'
import App from './App.tsx'
import MyLists from './MyLists.tsx';
import { RecipeSwipeableView } from './RecipeSwipeableView.tsx';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { RecipeDetailView } from './RecipeDetailView.tsx';
import { RecipeAddView } from './RecipeAddView.tsx';
import { QueryClientProvider } from '@tanstack/react-query';
import {queryClient} from './api/client';


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route path="/lists" element={<MyLists />} />
          <Route path="/recipes" element={<RecipeSwipeableView />}>
            <Route path="/recipes/:recipeId" element={<RecipeDetailView />} />
          </Route>
          <Route index element={<RecipeSwipeableView />} />
          <Route path="/add-recipe" element={<RecipeAddView />} />
        </Route>
      </Routes>
    </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
)
