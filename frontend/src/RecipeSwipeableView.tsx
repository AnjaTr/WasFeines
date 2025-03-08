import SwipeableViews from 'react-swipeable-views';

import { MediaItemContainer, placeholderMediaItems } from './MediaItemContainer';

export const RecipeSwipeableView = () => {
  return (
    <SwipeableViews axis="y" containerStyle={{ height: "100vh" }}>
      {placeholderMediaItems.map((item, index) => (
        <MediaItemContainer key={index} item={item} />
      ))}
    </SwipeableViews>
  );
}