import { Autocomplete, TextField } from "@mui/material";
import { useApplicationVersions } from "../../api/system";
import { useState } from "react";

export const AdvancedSettings = () => {
    const [developmentBuildsEnabled, setDevelopmentBuildsEnabled] = useState(false)
    const { data: versions } = useApplicationVersions();
    const currentVersion = "0.1";
    // const versions = ["0.1", "0.2"]

    return (
        <div style={{ maxWidth: "50rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
            <Autocomplete
                style={{ flexGrow: "1" }}
                value={currentVersion}
                options={versions || []}
                renderInput={(params) => <TextField {...params} label="Version" />}
                onChange={(_e, value) => { console.log(value) }}
                disableClearable
                blurOnSelect
            />
        </div>
    )
};