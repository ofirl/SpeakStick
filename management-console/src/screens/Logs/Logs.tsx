import { useState } from "react";

import Autocomplete from "@mui/material/Autocomplete";
import CircularProgress from "@mui/material/CircularProgress";
import TextField from "@mui/material/TextField";
import { Services, servicesOptions, useGetServiceLogs } from "../../api/system";

type LogViewerProps = {
  logs?: string
}
const LogViewer = ({ logs = "" }: LogViewerProps) => {
  return <textarea value={logs} style={{ width: "100%", height: "100%" }} />
}

export const Logs = () => {
  const [selectedService, setSelectedService] = useState<Services>(servicesOptions[0])
  const { data: serviceLogs, isLoading: isLoadingServiceLogs } = useGetServiceLogs(selectedService)

  return (
    <div style={{ maxWidth: "50rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
      <Autocomplete
        style={{ flexGrow: "1" }}
        value={selectedService}
        options={servicesOptions}
        renderInput={(params) => <TextField {...params} label="Service" />}
        onChange={(_e, value) => setSelectedService(value as Services)}
        disableClearable
        blurOnSelect
      />
      {isLoadingServiceLogs ? <CircularProgress /> : <LogViewer logs={serviceLogs} />}
    </div>
  )
};