
import React from 'react';

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Rating from '@mui/material/Rating';
import Card from '@mui/material/Card';
import { Outlet } from 'react-router';

export type MediaItemProps = {
  item: MediaItem;
};

export type MediaItem = {
  type: "image" | "video";
  src: string;
};

export const MediaItemContainer: React.FC<any> = ({ item }) => {
  const firstMediaItem = item.media[0].content_url;
  return (
    <Box
      sx={{ width: "100vw", height: "100vh", overflow: "hidden", position: "relative" }}>
      <img src={firstMediaItem} alt="Media" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      <Card
        sx={{ position: "absolute", bottom: "3%", width: "85%", left: 0, right:0, margin: "auto", padding: "10px" }}>
        <Typography variant="h6">Title</Typography>
        <Rating name="half-rating-read" defaultValue={2.5} precision={0.5} readOnly />
        <Typography variant="body1">Description</Typography>
        <Typography variant="body1">Description</Typography>
        <Typography variant="body1">Description</Typography>
      </Card>
    </Box>
  );
};