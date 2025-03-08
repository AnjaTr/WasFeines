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

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route path="/lists" element={<MyLists />} />
          <Route path="/recipes" element={<RecipeSwipeableView />} />
          <Route index element={<RecipeSwipeableView />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
