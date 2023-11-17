import { useState } from "react";

import Autocomplete from "@mui/material/Autocomplete";
import CircularProgress from "@mui/material/CircularProgress";
import TextField from "@mui/material/TextField";
import { Services, servicesOptions, useGetServiceLogs } from "../../api/system";

export const Logs = () => {
  const [selectedService, setSelectedService] = useState<Services>(servicesOptions[0])
  const { data: serviceLogs, isLoading: isLoadingServiceLogs } = useGetServiceLogs(selectedService)

  return (
    <div style={{ maxWidth: "50rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
      <div>
        <Autocomplete
          style={{ flexGrow: "1" }}
          value={selectedService}
          options={servicesOptions}
          renderInput={(params) => <TextField {...params} label="Service" />}
          onChange={(_e, value) => setSelectedService(value as Services)}
          disableClearable
          blurOnSelect
        />
        {isLoadingServiceLogs ? <CircularProgress /> : serviceLogs}
      </div>
    </div>
  )
};