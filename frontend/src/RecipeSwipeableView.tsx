import SwipeableViews from 'react-swipeable-views';

import { MediaItemContainer } from './MediaItemContainer';
import { useEffect, useState } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router';
import { useRecipeContext } from './context/RecipeProvider';
import { RecipeReducerAction } from './context/recipeReducer';
import { Box } from '@mui/material';

export const RecipeSwipeableView = () => {
  const { state, dispatch } = useRecipeContext();
  const location = useLocation();
  useEffect(() => {
    dispatch({ type: "FETCH_RECIPES_START" });
    fetch("/api/v1/recipes")
      .then((response) => {
        if (response.status === 401) {
            window.location.replace("/api/v1/login");
            return Promise.reject("Unauthorized"); 
        }
        return response;
      })
      .then(response => response.json())
      .then((data) => {
        dispatch({ type: "FETCH_RECIPES_SUCCESS", payload: data });
      })
      .catch((error) => {
        dispatch({ type: "FETCH_RECIPES_ERROR", payload: error });
      });
  }, [dispatch])
  if (state.isLoading && state.recipes.length === 0) {
    return <div>Loading...</div>;
  }
  if (state.error) {
    return <div>Error: {state.error}</div>;
  }
  const recipes = state.recipes;
  return (
    <Box sx={{ height: "100dvh" }}>
      { location.pathname === "/recipes" && <meta name="theme-color" content="#000000" /> }
      <SwipeableViews axis="y" containerStyle={{ height: "100dvh" }}>
        {recipes.map((item, index) => (
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