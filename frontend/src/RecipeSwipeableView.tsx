import SwipeableViews from 'react-swipeable-views';

import { MediaItemContainer } from './MediaItemContainer';
import { useEffect, useState } from 'react';

export const RecipeSwipeableView = () => {
  const [recipes, setRecipes] = useState([]);
  useEffect(() => {
    fetch("/api/v1/recipes")
      .then(response => response.json())
      .then((data) => {
        setRecipes(data);
      })
  }, [])
  return (
    <SwipeableViews axis="y" containerStyle={{ height: "100vh" }}>
      {recipes.map((item, index) => (
        <MediaItemContainer key={index} item={item} />
      ))}
    </SwipeableViews>
  );
}