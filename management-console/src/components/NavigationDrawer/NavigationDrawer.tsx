import List from '@mui/material/List';
import Drawer from '@mui/material/Drawer';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import AbcIcon from '@mui/icons-material/Abc';
import SettingsIcon from '@mui/icons-material/Settings';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { Link } from 'react-router-dom';
import { AdvancedSettingsNavItem } from './AdvancedSettingsNavItem';
import { Divider } from '@mui/material';

const menuItems = [
    {
        text: "Settings",
        icon: SettingsIcon,
        link: "/settings"
    },
    {
        text: "Library",
        icon: AbcIcon,
        link: "/library"
    },
    {
        text: "Word Files",
        icon: CloudUploadIcon,
        link: "/words"
    }
]

type NavigationDrawerProps = {
    open: boolean
    onClose: () => void
}
export const NavigationDrawer = ({ open, onClose }: NavigationDrawerProps) => {
    return <Drawer
        anchor={"left"}
        open={open}
        onClose={onClose}
    >
        <div
            style={{ width: 250 }}
            role="presentation"
        >
            <List>
                {menuItems.map(({ text, icon: Icon, link }) => (
                    <ListItem disablePadding key={text}>
                        <Link to={link} style={{ width: "100%" }} onClick={() => onClose()}>
                            <ListItemButton>
                                <ListItemIcon>
                                    <Icon />
                                </ListItemIcon>
                                <ListItemText primary={text} />
                            </ListItemButton>
                        </Link>
                    </ListItem>
                ))}
                <Divider />
                <AdvancedSettingsNavItem closeDrawer={onClose} />
            </List>
        </div>
    </Drawer>
}