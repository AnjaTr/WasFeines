
import React from 'react';

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ChecklistIcon from '@mui/icons-material/Checklist';
import RamenDiningIcon from '@mui/icons-material/RamenDining';

export const AppNavigationBar = () => {
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
