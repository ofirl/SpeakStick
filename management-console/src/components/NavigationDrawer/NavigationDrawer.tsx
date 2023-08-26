import List from '@mui/material/List';
import Drawer, { DrawerProps } from '@mui/material/Drawer';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import AbcIcon from '@mui/icons-material/Abc';
import SettingsIcon from '@mui/icons-material/Settings';
import { Link } from 'react-router-dom';

const menuItems = [
    {
        text: "Settings",
        icon: SettingsIcon,
        link: "/settings"
    },
    {
        text: "Posistion List",
        icon: AbcIcon,
        link: "/positions"
    },
    {
        text: "Word List",
        icon: AbcIcon,
        link: "/words"
    }
]

type NavigationDrawerProps = {
    open: boolean
    onClose: DrawerProps["onClose"]
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
            onClick={(e) => onClose?.(e, "escapeKeyDown")}
            onKeyDown={(e) => onClose?.(e, "escapeKeyDown")}
        >
            <List>
                {menuItems.map(({ text, icon: Icon, link }) => (
                    <ListItem disablePadding key="text">
                        <Link to={link} style={{ width: "100%" }}>
                            <ListItemButton>
                                <ListItemIcon>
                                    <Icon />
                                </ListItemIcon>
                                <ListItemText primary={text} />
                            </ListItemButton>
                        </Link>
                    </ListItem>
                ))}
            </List>
        </div>
    </Drawer>
}