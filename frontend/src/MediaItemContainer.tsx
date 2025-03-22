
import React from 'react';

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Rating from '@mui/material/Rating';
import Card from '@mui/material/Card';
import { Chip } from '@mui/material';
import ImageWithSkeleton from './ImageWithSkeleton';

export type MediaItemProps = {
  item: MediaItem;
};

export type MediaItem = {
  type: "image" | "video";
  src: string;
};

const CompoundRating: React.FC<any> = ({ summary }) => {
  const sameRating = summary.rating_georg === summary.rating_anja
  return (
    <Box>
      {sameRating && <Rating name="half-rating-read" defaultValue={summary.rating_georg} precision={0.5} readOnly />}
      {!sameRating && <Box sx={{ display: "grid", gridTemplateColumns: "60px auto" }}>
        <Typography component="span" variant="body1">Georg:</Typography> <Rating name="half-rating-read" defaultValue={summary.rating_georg} precision={0.5} readOnly />
        <Typography component="span" variant="body1">Anja:</Typography> <Rating name="half-rating-read" defaultValue={summary.rating_anja} precision={0.5} readOnly />
      </Box>
      }
    </Box>
  );
}

export const MediaItemContainer: React.FC<any> = ({ item }) => {
  const firstMediaItem = item.media[0].content_url;
  return (
    <Box
      sx={{ height: "100dvh", overflow: "hidden", position: "relative" }}>
      <ImageWithSkeleton src={firstMediaItem} alt="Media" width="100%" height="100%" />
      {
        item.summary && (<Card sx={{
          background: "rgba(255, 255, 255, 0.92)",
          position: "absolute", bottom: "3%", width: "85%", left: 0, right: 0, margin: "auto", padding: "10px"
        }}>
          <Box sx={{}}>
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
          <CompoundRating summary={item.summary} />
          <Typography variant="body1">{item.summary.description}</Typography>
          {item.summary.tags && item.summary.tags.map((tag: string, index: number) => {
            return <Chip key={index} label={tag} variant="outlined" sx={{ marginTop: "6px", marginRight: "4px" }} />
          })}
        </Card>
        )}
    </Box>
  );
};