import { useMemo } from "react";
import { useApplicationCurrentVersion, useApplicationVersions, useSwitchApplicationVersion, useUpdateApplicationVersions } from "../../api/versions";

import Autocomplete from "@mui/material/Autocomplete";
import CircularProgress from "@mui/material/CircularProgress";
import IconButton from "@mui/material/IconButton";
import Switch from "@mui/material/Switch";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import RefreshIcon from '@mui/icons-material/Refresh';
import { Button, Divider, Tooltip } from "@mui/material";
import { useResetToFactorySettings } from "../../api/system";
import { AUTOMATIC_UPDATES_CONFIG, DEVELOPMENT_BUILDS_CONFIG, useGetConfigs, useUpdateConfig } from "../../api/configs";

export const AdvancedSettings = () => {
    const { data: versions = [] } = useApplicationVersions();
    const { data: currentVersion = "" } = useApplicationCurrentVersion();

    const { mutateAsync: switchApplicationVersion } = useSwitchApplicationVersion();
    const { mutateAsync: updateApplicationVersions, isLoading: isUpdatingApplicationVersions } = useUpdateApplicationVersions();
    const { mutateAsync: resetToFactorySettings } = useResetToFactorySettings()
    const { data: configs, isLoading: isLoadingConfigs } = useGetConfigs(true)
    const { mutateAsync: updateConfig, isLoading: isUpdatingConfig } = useUpdateConfig()

    const developmentBuilds = useMemo(() =>
        configs?.find(c => c.key === DEVELOPMENT_BUILDS_CONFIG)?.value === "1",
        [configs]
    )

    const automaticUpdates = useMemo(() =>
        configs?.find(c => c.key === AUTOMATIC_UPDATES_CONFIG)?.value === "1",
        [configs]
    )

    return (
        <div style={{ maxWidth: "50rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
            <div style={{ display: "flex", alignItems: "center" }}>
                {
                    isLoadingConfigs || isUpdatingConfig ?
                        <CircularProgress />
                        :
                        <Switch checked={automaticUpdates} onChange={() => updateConfig({ key: AUTOMATIC_UPDATES_CONFIG, value: automaticUpdates ? "0" : "1" })} />
                }
                <Typography variant="body1">
                    Enable automatic updates
                </Typography>
            </div>
            <div style={{ display: "flex", alignItems: "center" }}>
                {
                    isLoadingConfigs || isUpdatingConfig ?
                        <CircularProgress />
                        :
                        <Switch checked={developmentBuilds} onChange={() => updateConfig({ key: DEVELOPMENT_BUILDS_CONFIG, value: developmentBuilds ? "0" : "1" })} />
                }
                <Typography variant="body1">
                    Enable development builds
                </Typography>
            </div>
            <div style={{ display: "flex", gap: "0.5rem" }}>
                <Autocomplete
                    style={{ flexGrow: "1" }}
                    value={currentVersion}
                    options={versions}
                    renderInput={(params) => <TextField {...params} label="Version" />}
                    onChange={(_e, value) => switchApplicationVersion({ version: value })}
                    disableClearable
                    blurOnSelect
                />
                <Tooltip title="Refresh">
                    <IconButton onClick={() => updateApplicationVersions()}>
                        {isUpdatingApplicationVersions ? <CircularProgress /> : <RefreshIcon />}
                    </IconButton>
                </Tooltip>
            </div>
            <Divider />
            <Button color="error" variant="contained" onClick={() => resetToFactorySettings()}>
                Reset to Factory Settings (NON-REVERSIBLE)
            </Button>
        </div>
    )
};