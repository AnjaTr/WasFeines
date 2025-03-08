
import React from 'react';

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Rating from '@mui/material/Rating';
import Card from '@mui/material/Card';

export type MediaItemProps = {
  item: MediaItem;
};

export type MediaItem = {
  type: "image" | "video";
  src: string;
};

export const placeholderMediaItems: MediaItem[] = [
  { type: "image", src: "https://placehold.co/200x1000/000000/FFFFFF/png" },
  { type: "image", src: "https://placehold.co/350x1080/FF0000/000000/png" },
  { type: "image", src: "https://placehold.co/300x1020" }
];

export const MediaItemContainer: React.FC<MediaItemProps> = ({ item }) => {
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