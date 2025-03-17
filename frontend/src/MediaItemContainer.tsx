
import React from 'react';

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Rating from '@mui/material/Rating';
import Card from '@mui/material/Card';
import { Chip } from '@mui/material';

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
      sx={{ width: "100vw", height: "100dvh", overflow: "hidden", position: "relative" }}>
      <img src={firstMediaItem} alt="Media" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      {
        item.summary && (<Card sx={{ position: "absolute", bottom: "3%", width: "85%", left: 0, right: 0, margin: "auto", padding: "10px" }}>
          <Box>
            <Typography variant="h6" sx={{ paddingRight: "4px" }}>{item.summary.title}</Typography>
            {item.summary.added_by && <Typography variant="body2">Added by: {item.summary.added_by}</Typography>}
            {item.summary.created_at && (
              <Typography variant="body2">
              Created at: {new Intl.DateTimeFormat(navigator.language, {
                dateStyle: "medium"
              }).format(
                new Date(item.summary.created_at)
              )}</Typography>
            )}
          </Box>
          <Rating name="half-rating-read" defaultValue={item.summary.rating} precision={0.5} readOnly />
          <Typography variant="body1">{item.summary.description}</Typography>
          {item.summary.tags && item.summary.tags.map((tag: string, index: number) => {
            return <Chip key={index} label={tag} variant="outlined" sx={{ marginTop: "6px", marginRight: "4px" }} />
          })}
        </Card>
        )}
    </Box>
  );
};