import { useState } from 'react'
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';
import UpgradeIcon from '@mui/icons-material/Upgrade';
import { NavigationDrawer } from '../../components/NavigationDrawer/NavigationDrawer';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import { useRestartStickController, useUpgradeApplication } from '../../api/system';
import { Tooltip } from '@mui/material';
import { NetworkIcon } from './NetworkIcon';

export const TopBar = () => {
    const [drawerOpen, setDrawerOpen] = useState(false)
    const { mutate: restartStickController } = useRestartStickController()
    const { mutate: upgradeApplication } = useUpgradeApplication()

    return <>
        <AppBar position="sticky" sx={{ height: "4rem" }}>
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
                    Speak Stick
                </Typography>
                <div style={{ flexGrow: "1", textAlign: "end" }}>
                    <NetworkIcon />
                    <Tooltip title="Upgrade application">
                        <IconButton
                            size="large"
                            color="inherit"
                            aria-label="restart"
                            sx={{ mr: 2 }}
                            onClick={() => upgradeApplication()}
                        >
                            <UpgradeIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Restart stick controller">
                        <IconButton
                            size="large"
                            color="inherit"
                            aria-label="restart"
                            sx={{ mr: 2 }}
                            onClick={() => restartStickController()}
                        >
                            <RestartAltIcon />
                        </IconButton>
                    </Tooltip>
                </div>
            </Toolbar>
        </AppBar>
        <NavigationDrawer open={drawerOpen} onClose={() => setDrawerOpen(false)} />
    </>
};