import { IconButton } from '@mui/material';
import { BatteryPercentResult, useGetBatteryPercent } from '../../api/system';
import { ComponentType, useMemo } from 'react';

import Battery90Icon from '@mui/icons-material/Battery90';
import Battery80Icon from '@mui/icons-material/Battery80';
import Battery60Icon from '@mui/icons-material/Battery60';
import Battery50Icon from '@mui/icons-material/Battery50';
import Battery30Icon from '@mui/icons-material/Battery30';
import Battery20Icon from '@mui/icons-material/Battery20';
import BatteryCharging90Icon from '@mui/icons-material/BatteryCharging90';
import BatteryCharging80Icon from '@mui/icons-material/BatteryCharging80';
import BatteryCharging60Icon from '@mui/icons-material/BatteryCharging60';
import BatteryCharging50Icon from '@mui/icons-material/BatteryCharging50';
import BatteryCharging30Icon from '@mui/icons-material/BatteryCharging30';
import BatteryCharging20Icon from '@mui/icons-material/BatteryCharging20';
import BatteryAlertIcon from '@mui/icons-material/BatteryAlert';
import BatteryUnknownIcon from '@mui/icons-material/BatteryUnknown';

const batteryPercentIconMap: [number, ComponentType][] = [
    [90, Battery90Icon],
    [80, Battery80Icon],
    [60, Battery60Icon],
    [50, Battery50Icon],
    [30, Battery30Icon],
    [20, Battery20Icon],
    [0, BatteryAlertIcon],
]

const batteryPercentIconChargingMap: [number, ComponentType][] = [
    [90, BatteryCharging90Icon],
    [80, BatteryCharging80Icon],
    [60, BatteryCharging60Icon],
    [50, BatteryCharging50Icon],
    [30, BatteryCharging30Icon],
    [20, BatteryCharging20Icon],
    [0, BatteryCharging20Icon],
]

export const BatteryIcon = () => {
    const { data: { percent = 0, isCharging = false } = {} as BatteryPercentResult } = useGetBatteryPercent();
    const BatteryPercentIcon = useMemo(() =>
        (isCharging ? batteryPercentIconChargingMap : batteryPercentIconMap).find(([key]) => percent > key)?.[1] || BatteryUnknownIcon,
        [percent, isCharging])

    return (
        <IconButton sx={{ color: "white" }}>
            <BatteryPercentIcon />
        </IconButton>
    );
}