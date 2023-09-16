import { Autocomplete, Switch, TextField, Typography } from "@mui/material";
import { useApplicationCurrentVersion, useApplicationVersions, useSwitchApplicationVersion } from "../../api/system";
import { useMemo, useState } from "react";

export const AdvancedSettings = () => {
    const [developmentBuildsEnabled, setDevelopmentBuildsEnabled] = useState(false)
    const { data: versions = [] } = useApplicationVersions();
    const { data: currentVersion = "" } = useApplicationCurrentVersion();

    const { mutateAsync: switchApplicationVersion } = useSwitchApplicationVersion()

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
            <Autocomplete
                style={{ flexGrow: "1" }}
                value={currentVersion}
                options={filteredVersions}
                renderInput={(params) => <TextField {...params} label="Version" />}
                onChange={(_e, value) => switchApplicationVersion({ version: value })}
                disableClearable
                blurOnSelect
            />
        </div>
    )
};