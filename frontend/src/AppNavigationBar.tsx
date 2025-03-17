
import React from 'react';
import { NavLink, useLocation } from "react-router";

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
    const location = useLocation();

    const color = location.pathname === "/recipes" ? "white" : "black";
    const background = location.pathname === "/recipes" ? "transparent" : "white";
    const textShadow = location.pathname === "/recipes" ? "-1px -1px 0 rgba(0,0,0,0.5),  1px -1px 0 rgba(0,0,0,0.5), -1px  1px 0 rgba(0,0,0,0.5), 1px  1px 0 rgba(0,0,0,0.5)" : "none";

    const DrawerList = (
        <Box sx={{ width: 250 }} role="presentation" onClick={() => setOpen(false)}>
            <List>
                <NavLink to="/recipes" style={{ textDecoration: "none", color: "inherit" }}>
                    <ListItem disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                <RamenDiningIcon />
                            </ListItemIcon>
                            <ListItemText primary={"Recipes"} />
                        </ListItemButton>
                    </ListItem>
                </NavLink>
                <Divider />
                <NavLink to="/lists" style={{ textDecoration: "none", color: "inherit" }}>
                    <ListItem disablePadding>
                        <ListItemButton>
                            <ListItemIcon>
                                <ChecklistIcon />
                            </ListItemIcon>
                            <ListItemText primary={"My Lists"} />
                        </ListItemButton>
                    </ListItem>
                </NavLink>
            </List>
        </Box>
    );


    return (
        <AppBar position="absolute" sx={{ background: background, boxShadow: "none", color: color }}>
            <Drawer open={open} onClose={() => setOpen(false)}>
                {DrawerList}
            </Drawer>
            <Toolbar>
                <IconButton edge="start" color="inherit" aria-label="menu" onClick={(_) => setOpen(!open)}>
                    <MenuIcon />
                </IconButton>
                <Typography sx={{ textShadow }} variant="h6">WasFeines</Typography>
            </Toolbar>
        </AppBar>
    );
};
