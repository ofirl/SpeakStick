import { useState } from "react";
import { Link } from "react-router-dom"

import ListItem from "@mui/material/ListItem"
import ListItemButton from "@mui/material/ListItemButton"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemText from "@mui/material/ListItemText"
import Modal from "@mui/material/Modal"
import Typography from "@mui/material/Typography"
import Box from "@mui/material/Box"
import Button from "@mui/material/Button"
import DeveloperModeIcon from '@mui/icons-material/DeveloperMode';
import WarningIcon from '@mui/icons-material/Warning';

const modalBoxStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: "50%",
    maxWidth: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem"
};

type AdvancedSettingsProps = {
    closeDrawer: () => void
}
export const AdvancedSettingsNavItem = ({ closeDrawer }: AdvancedSettingsProps) => {
    const [modalOpen, setModalOpen] = useState(false);

    return (
        <>
            <ListItem disablePadding>
                <ListItemButton onClick={(e) => {
                    e.stopPropagation();
                    setModalOpen(true)
                }}>
                    <ListItemIcon>
                        <DeveloperModeIcon />
                    </ListItemIcon>
                    <ListItemText sx={{ color: "#646cff" }} primary={"Advanced Settings"} />
                </ListItemButton>
            </ListItem>
            <Modal
                open={modalOpen}
                onClose={() => {
                    setModalOpen(false);
                }}
            >
                <Box sx={modalBoxStyle}>
                    <Typography variant="h6" component="h2" sx={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
                        <WarningIcon color="warning" fontSize="large" />
                        Advanced Settings
                    </Typography>
                    <Typography variant="body1">
                        These settings are dangerous and can break the application in unexpected ways
                    </Typography>
                    <Typography variant="body1">
                        Do not change anything here unless instructed to do so!
                    </Typography>
                    <Typography variant="body1">
                        Are you sure you want to continue?
                    </Typography>
                    <div style={{ display: "flex", gap: "0.5rem", justifyContent: "end" }}>
                        <Button variant="contained" style={{ marginTop: "1rem", alignSelf: "end" }} onClick={() => setModalOpen(false)}>
                            No
                        </Button>
                        <Link to="/advanced_settings" onClick={() => {
                            setModalOpen(false);
                            closeDrawer();
                        }}>
                            <Button variant="contained" color="warning" style={{ marginTop: "1rem", alignSelf: "end" }}>
                                Yes
                            </Button>
                        </Link>
                    </div>
                </Box>
            </Modal>
        </>
    )
}