import { useRef, useState } from "react";
import { Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, IconButton, ListItemIcon, ListItemText, Menu, MenuItem, TextField, Tooltip } from "@mui/material"
import SignalWifiOffIcon from '@mui/icons-material/SignalWifiOff';
import { NetowrkScanResult, useGetNetworkStatus, useScanNetworks, useUpdateNetworkConfiguration } from "../../api/system";

import SignalWifi0BarIcon from '@mui/icons-material/SignalWifi0Bar';
import SignalWifi1BarIcon from '@mui/icons-material/SignalWifi1Bar';
import SignalWifi1BarLockIcon from '@mui/icons-material/SignalWifi1BarLock';
import SignalWifi2BarIcon from '@mui/icons-material/SignalWifi2Bar';
import SignalWifi2BarLockIcon from '@mui/icons-material/SignalWifi2BarLock';
import SignalWifi3BarIcon from '@mui/icons-material/SignalWifi3Bar';
import SignalWifi3BarLockIcon from '@mui/icons-material/SignalWifi3BarLock';
import SignalWifi4BarIcon from '@mui/icons-material/SignalWifi4Bar';
import SignalWifi4BarLockIcon from '@mui/icons-material/SignalWifi4BarLock';

const wifiSignalIcons = [SignalWifi0BarIcon, SignalWifi1BarIcon, SignalWifi2BarIcon, SignalWifi3BarIcon, SignalWifi4BarIcon]
const wifiLockedSignalIcons = [SignalWifi0BarIcon, SignalWifi1BarLockIcon, SignalWifi2BarLockIcon, SignalWifi3BarLockIcon, SignalWifi4BarLockIcon]

export const NetworkIcon = () => {
    const [networksMenuOpen, setNetworksMenuOpen] = useState(false)
    const menuAnchorElement = useRef(null)

    const [selectedNetwork, setSelectedNetwork] = useState<NetowrkScanResult | undefined>()
    const passKeyInputRef = useRef<HTMLInputElement>()
    const { mutateAsync: updateNetworkConfiguration, isLoading: isConnectingToNetwork } = useUpdateNetworkConfiguration()

    const { data: networkStatus } = useGetNetworkStatus()
    const { data: networks, isFetching: isScanningNetworks } = useScanNetworks({
        enabled: networksMenuOpen && selectedNetwork != null,
        refetchInterval: 5000
    })

    const SignalIcon = networkStatus ? wifiSignalIcons[networkStatus.signal_strength] : SignalWifiOffIcon

    const connectToNetwork = (ssid: string, key_mgmt: string, psk?: string) => {
        updateNetworkConfiguration({ ssid, psk, key_mgmt }).then(() => {
            setSelectedNetwork(undefined)
            setNetworksMenuOpen(false)
        })
    }

    return (
        <>
            <Tooltip title={networkStatus ? `SSID: ${networkStatus?.ssid}` : "Not connected"}>
                <IconButton
                    size="large"
                    color="inherit"
                    aria-label="restart"
                    sx={{ mr: 2 }}
                    onClick={() => setNetworksMenuOpen(prev => !prev)}
                    ref={menuAnchorElement}
                >
                    <SignalIcon />
                </IconButton>
            </Tooltip>
            <Menu
                open={networksMenuOpen}
                onClose={() => setNetworksMenuOpen(false)}
                anchorEl={menuAnchorElement.current}
                slotProps={{
                    paper: {
                        style: {
                            maxHeight: "500px",
                            width: '400px',
                        }
                    }
                }}
            >
                {
                    isScanningNetworks &&
                    <MenuItem>
                        <ListItemIcon>
                            <CircularProgress size={20} />
                        </ListItemIcon>
                        <ListItemText>Scanning...</ListItemText>
                    </MenuItem>

                }
                {networks?.map(network => {
                    const signalIconSet = network.secured ? wifiLockedSignalIcons : wifiSignalIcons
                    const SignalIcon = signalIconSet[network.signal_strength]
                    return (
                        <MenuItem onClick={() => network.secured ? setSelectedNetwork(network) : updateNetworkConfiguration({ ssid: network.ssid, key_mgmt: network.key_mgmt })}>
                            <ListItemIcon>
                                <SignalIcon fontSize="small" />
                            </ListItemIcon>
                            <ListItemText>{network.ssid}</ListItemText>
                        </MenuItem>
                    )
                })}
            </Menu>
            <Dialog open={selectedNetwork != null} onClose={() => setSelectedNetwork(undefined)}>
                <DialogTitle>Add pass key for {selectedNetwork?.ssid}</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Enter network pass key
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Pass key"
                        type="password"
                        fullWidth
                        variant="standard"
                        inputRef={passKeyInputRef}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setSelectedNetwork(undefined)}>Cancel</Button>
                    <Button onClick={() => selectedNetwork && connectToNetwork(selectedNetwork.ssid, selectedNetwork.key_mgmt, passKeyInputRef.current?.value)}>
                        {isConnectingToNetwork ? <CircularProgress /> : "Update"}
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    )
}