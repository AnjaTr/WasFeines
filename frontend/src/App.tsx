import SwipeableViews from 'react-swipeable-views';

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Rating from '@mui/material/Rating';

const mediaItems = [
  { type: "image", src: "https://placehold.co/200x1000/000000/FFFFFF/png" },
  { type: "image", src: "https://placehold.co/350x1080/FF0000/000000/png" },
  { type: "image", src: "https://placehold.co/300x1020" }
];

const TransparentAppBar = () => {
  return (
    <AppBar position="absolute" sx={{ background: "transparent", boxShadow: "none" }}>
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="menu">
          <MenuIcon />
        </IconButton>
        <Typography variant="h6">WasFeines</Typography>
      </Toolbar>
    </AppBar>
  );
};

const MediaItem = ({ item }) => {
  return (
    <Box sx={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
      {item.type === "image" ? (
        <img src={item.src} alt="Media" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        <video src={item.src} controls autoPlay loop muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      )}
    </Box>
  );
};

const TikTokClone = () => {
  return (
    <SwipeableViews axis="y" containerStyle={{ height: "100vh" }}>
      {mediaItems.map((item, index) => (
        <MediaItem key={index} item={item} />
      ))}
    </SwipeableViews>
  );
}

export default function ButtonAppBar() {
  return (
    <>
      <TransparentAppBar />
      <TikTokClone />
    </>
  );
}