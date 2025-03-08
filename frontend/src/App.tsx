import React from 'react';

import SwipeableViews from 'react-swipeable-views';

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Rating from '@mui/material/Rating';
import Card from '@mui/material/Card';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ChecklistIcon from '@mui/icons-material/Checklist';
import RamenDiningIcon from '@mui/icons-material/RamenDining';

export type MediaItem = {
  type: "image" | "video";
  src: string;
};

const mediaItems: MediaItem[] = [
  { type: "image", src: "https://placehold.co/200x1000/000000/FFFFFF/png" },
  { type: "image", src: "https://placehold.co/350x1080/FF0000/000000/png" },
  { type: "image", src: "https://placehold.co/300x1020" }
];


const TransparentAppBar = () => {
  const [open, setOpen] = React.useState(false);

  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation" onClick={() => setOpen(false)}>
      <List>
        <ListItem disablePadding>
          <ListItemButton>
            <ListItemIcon>
              <RamenDiningIcon />
            </ListItemIcon>
            <ListItemText primary={"Recipes"} />
          </ListItemButton>
        </ListItem>
        <Divider />
        <ListItem disablePadding>
          <ListItemButton>
            <ListItemIcon>
              <ChecklistIcon />
            </ListItemIcon>
            <ListItemText primary={"My Lists"} />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );
  

  return (
    <AppBar position="absolute" sx={{ background: "transparent", boxShadow: "none" }}>
      <Drawer open={open} onClose={() => setOpen(false)}>
        {DrawerList}
      </Drawer>
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="menu" onClick={(_) => setOpen(!open) }>
          <MenuIcon />
        </IconButton>
        <Typography variant="h6">WasFeines</Typography>
      </Toolbar>
    </AppBar>
  );
};

type MediaItemProps = {
  item: MediaItem;
};

const MediaItemContainer: React.FC<MediaItemProps> = ({ item }) => {
  return (
    <Box sx={{ width: "100vw", height: "100vh", overflow: "hidden", position: "relative" }}>
      {item.type === "image" ? (
        <img src={item.src} alt="Media" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        <video src={item.src} controls autoPlay loop muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      )}
      <Card sx={{ position: "absolute", bottom: "3%", width: "85%", left: 0, right:0, margin: "auto", padding: "10px" }}>
        <Typography variant="h6">Title</Typography>
        <Rating name="half-rating-read" defaultValue={2.5} precision={0.5} readOnly />
        <Typography variant="body1">Description</Typography>
        <Typography variant="body1">Description</Typography>
        <Typography variant="body1">Description</Typography>
      </Card>
    </Box>
  );
};

const TikTokClone = () => {
  return (
    <SwipeableViews axis="y" containerStyle={{ height: "100vh" }}>
      {mediaItems.map((item, index) => (
        <MediaItemContainer key={index} item={item} />
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