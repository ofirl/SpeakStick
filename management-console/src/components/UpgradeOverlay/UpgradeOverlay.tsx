import Box from "@mui/material/Box"
import Modal from "@mui/material/Modal"
import Typography from "@mui/material/Typography"
import { SxProps, Theme } from "@mui/material"

const boxStyle: SxProps<Theme> = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: "80%",
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    padding: "1rem",
    boxSizing: "border-box"
};

// type UpgradeOverlayProps = {}
export const UpgradeOverlay = () => {
    return (
        <Modal
            open={true}
        >
            <Box sx={boxStyle}>
                <Typography variant="h3">
                    Upgrading application!
                </Typography>
                <br />
                <Typography variant="body1">
                    This may take a minute, do not power off the machine while upgrading!
                </Typography>
            </Box>
        </Modal>
    )
}