import { Box, Modal, Typography } from "@mui/material"

const boxStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

// type UpgradeOverlayProps = {}
export const UpgradeOverlay = () => {
    return (
        <Modal
            open={true}
        >
            <Box sx={boxStyle}>
                <Typography variant="h3">
                    Application is upgrading!
                </Typography>
                <Typography variant="body1">
                    This may take a minute, do not power off the machine while upgrading
                </Typography>
            </Box>
        </Modal>
    )
}