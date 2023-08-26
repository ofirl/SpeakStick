import { useState } from 'react'
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';
import { NavigationDrawer } from '../../components/NavigationDrawer/NavigationDrawer';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import { useRestartStickController } from '../../api/system';

export const TopBar = () => {
    const [drawerOpen, setDrawerOpen] = useState(false)
    const { mutate: restartStickController } = useRestartStickController()

    return <>
        <AppBar position="sticky">
            <Toolbar>
                <IconButton
                    size="large"
                    edge="start"
                    color="inherit"
                    aria-label="open drawer"
                    sx={{ mr: 2 }}
                    onClick={() => setDrawerOpen(true)}
                >
                    <MenuIcon />
                </IconButton>
                <Typography
                    variant="h6"
                    noWrap
                    component="div"
                    sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block', textAlign: "center" } }}
                >
                    Speak Stick Management Console
                </Typography>
                <IconButton
                    size="large"
                    color="inherit"
                    aria-label="restart"
                    sx={{ mr: 2 }}
                    onClick={() => restartStickController()}
                >
                    <RestartAltIcon />
                </IconButton>
            </Toolbar>
        </AppBar>
        <NavigationDrawer open={drawerOpen} onClose={() => setDrawerOpen(false)} />
    </>
};