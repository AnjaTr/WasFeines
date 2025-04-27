import SwipeableViews from 'react-swipeable-views';

import { MediaItemContainer } from './MediaItemContainer';
import { useEffect, useState } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router';
import { useRecipeContext } from './context/RecipeProvider';
import { RecipeReducerAction } from './context/recipeReducer';
import { Box } from '@mui/material';
import { useRecipes } from './api/useRecipes';

export const RecipeSwipeableView = () => {
  const { state, dispatch } = useRecipeContext();
  const location = useLocation();
  const { data: recipes, isLoading } = useRecipes();
  if (isLoading) {
    return <div>Loading...</div>;
  }
  if (state.error) {
    return <div>Error: {state.error}</div>;
  }
  return (
    <Box sx={{ height: "100dvh" }}>
      { location.pathname === "/recipes" && <meta name="theme-color" content="#000000" /> }
      <SwipeableViews axis="y" containerStyle={{ height: "100dvh" }}>
        {recipes && recipes.map((item, index) => (
          <Box key={index}>
            <NavLink to={`/recipes/${index}`} style={{ textDecoration: "none" }}>
              <MediaItemContainer item={item} />
            </NavLink>
          </Box>
        ))}
      </SwipeableViews>
      <Outlet />
    </Box>
  );
}