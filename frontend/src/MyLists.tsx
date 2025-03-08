import React from "react";

import { Box, Typography, List, ListItem, ListItemText, IconButton, Button } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const MyLists = () => {
  const lists = [
    { title: "Shopping List", sharedWith: "Anja", count: 5 },
    { title: "Chores", sharedWith: "Anja", count: 2 }
  ];

  return (
    <Box sx={{ maxWidth: 400, margin: "auto", padding: 2, marginTop: 5 }}>
      {/* Title */}
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        My Lists
      </Typography>

      {/* List Items */}
      <List>
        {lists.map((list, index) => (
          <ListItem key={index} sx={{ display: "flex", justifyContent: "space-between" }}>
            <ListItemText 
              primary={list.title} 
              secondary={`Shared with ${list.sharedWith}`} 
            />
            <Typography variant="h6">{list.count}</Typography>
          </ListItem>
        ))}
      </List>

      {/* Add List Button */}
      <Button startIcon={<ArrowBackIcon />} sx={{ mt: 2, textTransform: "none" }}>
        Add list
      </Button>
    </Box>
  );
};

export default MyLists;
