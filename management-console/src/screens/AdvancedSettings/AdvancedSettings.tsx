import { useMemo, useRef } from "react";
import { useApplicationCurrentVersion, useApplicationVersions, useUpdateApplicationVersions, useUpgradeApplication } from "../../api/versions";

import Autocomplete from "@mui/material/Autocomplete";
import CircularProgress from "@mui/material/CircularProgress";
import IconButton from "@mui/material/IconButton";
import Switch from "@mui/material/Switch";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import RefreshIcon from '@mui/icons-material/Refresh';
import { Button, FormControl, InputLabel, MenuItem, Select, Skeleton, Tooltip } from "@mui/material";
import { useResetToFactorySettings } from "../../api/system";
import { AUTOMATIC_UPDATES_CONFIG, DEVELOPMENT_BUILDS_CONFIG, DEVICE_NAME_CONFIG, LOGGING_LEVEL_CONFIG, LOGS_API_KEY_CONFIG, LOGS_HANDLER_LOGGING_LEVEL_CONFIG, useGetConfigs, useUpdateConfig } from "../../api/configs";
import { AdvancedSettingsSection } from "./AdvancedSettingsSection";

export const AdvancedSettings = () => {
  const { data: versions = [] } = useApplicationVersions();
  const { data: currentVersion = "" } = useApplicationCurrentVersion();

  const { mutateAsync: upgradeApplication } = useUpgradeApplication();
  const { mutateAsync: updateApplicationVersions, isPending: isUpdatingApplicationVersions } = useUpdateApplicationVersions();
  const { mutateAsync: resetToFactorySettings } = useResetToFactorySettings()
  const { data: configs, isPending: isLoadingConfigs } = useGetConfigs(true)
  const { mutateAsync: updateConfig, isPending: isUpdatingConfig } = useUpdateConfig()

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

  const loggingLevel = useMemo(() =>
    configs?.find(c => c.key === LOGGING_LEVEL_CONFIG)?.value || "",
    [configs]
  )

  const logsHandlerLoggingLevel = useMemo(() =>
    configs?.find(c => c.key === LOGS_HANDLER_LOGGING_LEVEL_CONFIG)?.value || "",
    [configs]
  )

  return (
    <div style={{ maxWidth: "50rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
      <AdvancedSettingsSection title="Versions & Updates">
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
      </AdvancedSettingsSection>
      <AdvancedSettingsSection title="Logs">
        <div style={{ display: "flex" }}>
          <TextField inputRef={logsApiKeyTextFieldRef} style={{ flexGrow: 1 }} label="Logs API key" />
          <Button style={{ flexShrink: 1 }} variant="text" onClick={() => logsApiKeyTextFieldRef.current?.value && updateConfig({ key: LOGS_API_KEY_CONFIG, value: logsApiKeyTextFieldRef.current.value })}>
            Update
          </Button>
        </div>
        <div style={{ display: "flex" }}>
          {
            isLoadingConfigs ? <Skeleton variant="rectangular" width={"100%"} height={"2rem"} /> :
              <TextField defaultValue={deviceName} inputRef={deviceNameTextFieldRef} style={{ flexGrow: 1 }} label="Device name" />
          }
          <Button style={{ flexShrink: 1 }} variant="text" onClick={() => deviceNameTextFieldRef.current?.value && updateConfig({ key: DEVICE_NAME_CONFIG, value: deviceNameTextFieldRef.current.value })}>
            Update
          </Button>
        </div>
        <FormControl fullWidth>
          <InputLabel id="logging-level-select-label">Logging level</InputLabel>
          <Select
            labelId="logging-level-select-label"
            value={loggingLevel}
            label="Logging level"
            onChange={(e) => updateConfig({ key: LOGGING_LEVEL_CONFIG, value: e.target.value })}
          >
            {
              ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"].map(level => (
                <MenuItem value={level}>{level}</MenuItem>
              ))
            }
          </Select>
        </FormControl>
      </AdvancedSettingsSection>
      <AdvancedSettingsSection title="Danger Zone">
        <FormControl fullWidth>
          <InputLabel id="logs-handler-logging-level-select-label">Logs handler logging level</InputLabel>
          <Select
            labelId="logs-handler-logging-level-select-label"
            value={logsHandlerLoggingLevel}
            label="Logs handler logging level"
            onChange={(e) => updateConfig({ key: LOGS_HANDLER_LOGGING_LEVEL_CONFIG, value: e.target.value })}
          >
            {
              ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"].map(level => (
                <MenuItem value={level}>{level}</MenuItem>
              ))
            }
          </Select>
        </FormControl>
        <Button color="error" variant="contained" onClick={() => resetToFactorySettings()}>
          Reset to Factory Settings (NON-REVERSIBLE)
        </Button>
      </AdvancedSettingsSection>
    </div>
  )
};