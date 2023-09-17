import { useMemo, useState } from "react";
import { useApplicationCurrentVersion, useApplicationVersions, useSwitchApplicationVersion, useUpdateApplicationVersions } from "../../api/versions";

import Autocomplete from "@mui/material/Autocomplete";
import CircularProgress from "@mui/material/CircularProgress";
import IconButton from "@mui/material/IconButton";
import Switch from "@mui/material/Switch";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import RefreshIcon from '@mui/icons-material/Refresh';
import { Button } from "@mui/material";
import { useResetToFactorySettings } from "../../api/system";

export const AdvancedSettings = () => {
    const [developmentBuildsEnabled, setDevelopmentBuildsEnabled] = useState(false);
    const { data: versions = [] } = useApplicationVersions();
    const { data: currentVersion = "" } = useApplicationCurrentVersion();

    const { mutateAsync: switchApplicationVersion } = useSwitchApplicationVersion();
    const { mutateAsync: updateApplicationVersions, isLoading: isUpdatingApplicationVersions } = useUpdateApplicationVersions();
    const { mutateAsync: resetToFactorySettings } = useResetToFactorySettings()

    const filteredVersions = useMemo(() =>
        developmentBuildsEnabled ? versions.filter(v => !v.includes("rc")) : versions,
        [versions, developmentBuildsEnabled]
    )

    return (
        <div style={{ maxWidth: "50rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
            <div style={{ display: "flex", alignItems: "center" }}>
                <Switch value={developmentBuildsEnabled} onChange={() => setDevelopmentBuildsEnabled(prev => !prev)} />
                <Typography variant="body1">
                    Enable development builds
                </Typography>
            </div>
            <div style={{ display: "flex", gap: "0.5rem" }}>
                <Autocomplete
                    style={{ flexGrow: "1" }}
                    value={currentVersion}
                    options={filteredVersions}
                    renderInput={(params) => <TextField {...params} label="Version" />}
                    onChange={(_e, value) => switchApplicationVersion({ version: value })}
                    disableClearable
                    blurOnSelect
                />
                <IconButton onClick={() => updateApplicationVersions()}>
                    {isUpdatingApplicationVersions ? <CircularProgress /> : <RefreshIcon />}
                </IconButton>
            </div>
            <Button color="error" variant="contained" onClick={() => resetToFactorySettings()}>
                Reset to Factory Settings (NON-REVERSIBLE)
            </Button>
        </div>
    )
};