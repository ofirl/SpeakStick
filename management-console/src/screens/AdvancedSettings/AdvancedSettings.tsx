import { useMemo, useRef } from "react";
import { useApplicationCurrentVersion, useApplicationVersions, useUpdateApplicationVersions, useUpgradeApplication } from "../../api/versions";

import Autocomplete from "@mui/material/Autocomplete";
import CircularProgress from "@mui/material/CircularProgress";
import IconButton from "@mui/material/IconButton";
import Switch from "@mui/material/Switch";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import RefreshIcon from '@mui/icons-material/Refresh';
import { Button, Divider, Tooltip } from "@mui/material";
import { useResetToFactorySettings } from "../../api/system";
import { AUTOMATIC_UPDATES_CONFIG, DEVELOPMENT_BUILDS_CONFIG, DEVICE_NAME_CONFIG, LOGS_API_KEY_CONFIG, useGetConfigs, useUpdateConfig } from "../../api/configs";

export const AdvancedSettings = () => {
  const { data: versions = [] } = useApplicationVersions();
  const { data: currentVersion = "" } = useApplicationCurrentVersion();

  const { mutateAsync: upgradeApplication } = useUpgradeApplication();
  const { mutateAsync: updateApplicationVersions, isLoading: isUpdatingApplicationVersions } = useUpdateApplicationVersions();
  const { mutateAsync: resetToFactorySettings } = useResetToFactorySettings()
  const { data: configs, isLoading: isLoadingConfigs } = useGetConfigs(true)
  const { mutateAsync: updateConfig, isLoading: isUpdatingConfig } = useUpdateConfig()

  const logsApiKeyTextFieldRef = useRef<HTMLInputElement>();
  const deviceNameTextFieldRef = useRef<HTMLInputElement>();

  const developmentBuilds = useMemo(() =>
    configs?.find(c => c.key === DEVELOPMENT_BUILDS_CONFIG)?.value === "1",
    [configs]
  )

  const automaticUpdates = useMemo(() =>
    configs?.find(c => c.key === AUTOMATIC_UPDATES_CONFIG)?.value === "1",
    [configs]
  )

  const deviceName = useMemo(() =>
    configs?.find(c => c.key === DEVICE_NAME_CONFIG)?.value || "",
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
            <Switch color="warning" checked={developmentBuilds} onChange={() => updateConfig({ key: DEVELOPMENT_BUILDS_CONFIG, value: developmentBuilds ? "0" : "1" })} />
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
          onChange={(_e, value) => upgradeApplication({ version: value })}
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
      <div style={{ display: "flex" }}>
        <TextField inputRef={logsApiKeyTextFieldRef} style={{ flexGrow: 1 }} label="Logs API key" />
        <Button style={{ flexShrink: 1 }} variant="text" onClick={() => logsApiKeyTextFieldRef.current?.value && updateConfig({ key: LOGS_API_KEY_CONFIG, value: logsApiKeyTextFieldRef.current.value })}>
          Update
        </Button>
      </div>
      <Divider />
      <div style={{ display: "flex" }}>
        <TextField defaultValue={deviceName} inputRef={deviceNameTextFieldRef} style={{ flexGrow: 1 }} label="Device name" />
        <Button style={{ flexShrink: 1 }} variant="text" onClick={() => deviceNameTextFieldRef.current?.value && updateConfig({ key: DEVICE_NAME_CONFIG, value: deviceNameTextFieldRef.current.value })}>
          Update
        </Button>
      </div>
      <Divider />
      <Button color="error" variant="contained" onClick={() => resetToFactorySettings()}>
        Reset to Factory Settings (NON-REVERSIBLE)
      </Button>
    </div>
  )
};