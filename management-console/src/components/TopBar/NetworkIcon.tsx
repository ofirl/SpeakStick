import { IconButton, ListItemIcon, ListItemText, MenuItem, MenuList, Tooltip } from "@mui/material"
import SignalWifiOffIcon from '@mui/icons-material/SignalWifiOff';
import { useGetNetworkStatus, useScanNetworks } from "../../api/system";

import SignalWifi0BarIcon from '@mui/icons-material/SignalWifi0Bar';
import SignalWifi1BarIcon from '@mui/icons-material/SignalWifi1Bar';
import SignalWifi1BarLockIcon from '@mui/icons-material/SignalWifi1BarLock';
import SignalWifi2BarIcon from '@mui/icons-material/SignalWifi2Bar';
import SignalWifi2BarLockIcon from '@mui/icons-material/SignalWifi2BarLock';
import SignalWifi3BarIcon from '@mui/icons-material/SignalWifi3Bar';
import SignalWifi3BarLockIcon from '@mui/icons-material/SignalWifi3BarLock';
import SignalWifi4BarIcon from '@mui/icons-material/SignalWifi4Bar';
import SignalWifi4BarLockIcon from '@mui/icons-material/SignalWifi4BarLock';

// import WifiFindIcon from '@mui/icons-material/WifiFind';

const wifiSignalIcons = [SignalWifi0BarIcon, SignalWifi1BarIcon, SignalWifi2BarIcon, SignalWifi3BarIcon, SignalWifi4BarIcon]
const wifiLockedSignalIcons = [SignalWifi0BarIcon, SignalWifi1BarLockIcon, SignalWifi2BarLockIcon, SignalWifi3BarLockIcon, SignalWifi4BarLockIcon]

export const NetworkIcon = () => {
    const { data: networkStatus } = useGetNetworkStatus()

    const SignalIcon = networkStatus ? wifiSignalIcons[networkStatus.signal_strength] : SignalWifiOffIcon

    const { data: networks } = useScanNetworks()

    return (
        <>
            <Tooltip title={networkStatus ? `SSID: ${networkStatus?.ssid}` : "Not connected"}>
                <IconButton
                    size="large"
                    color="inherit"
                    aria-label="restart"
                    sx={{ mr: 2 }}
                // onClick={() => upgradeApplication()}
                >
                    <SignalIcon />
                </IconButton>
            </Tooltip>
            <MenuList>
                {
                    networks?.map(network => {
                        const signalIconSet = network.secured ? wifiLockedSignalIcons : wifiSignalIcons
                        const SignalIcon = signalIconSet[network.signal_strength]
                        return (
                            <MenuItem>
                                <ListItemIcon>
                                    <SignalIcon fontSize="small" />
                                </ListItemIcon>
                                <ListItemText>{network.ssid}</ListItemText>
                            </MenuItem>
                        )
                    })
                }
            </MenuList>
        </>
    )
}