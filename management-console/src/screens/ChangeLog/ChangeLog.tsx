import { Skeleton, Typography } from "@mui/material";
import { useApplicationCurrentVersion, useVersionsChangeLog } from "../../api/versions"
import { ChangeLogItem } from "./ChangeLogItem";
import { DEVELOPMENT_BUILDS_CONFIG, useGetConfigs } from "../../api/configs";
import { useMemo } from "react";

export const ChangeLog = () => {
  const { data: changeLog = [], isLoading: isLoadingChangeLog } = useVersionsChangeLog();
  const { data: currentVersion, isLoading: isLoadingCurrentVersion } = useApplicationCurrentVersion();
  const isLoading = isLoadingChangeLog || isLoadingCurrentVersion;

  const { data: configs } = useGetConfigs(true);
  const developmentBuilds = useMemo(() =>
    configs?.find(c => c.key === DEVELOPMENT_BUILDS_CONFIG)?.value === "1",
    [configs]
  )

  const filteredChangeLog = useMemo(() => developmentBuilds ? changeLog : changeLog.filter(c => !c.title.includes("rc")), [changeLog, developmentBuilds])

  return (
    <div style={{ maxWidth: "70rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1 }}>
      <div>
        {
          isLoading ?
            <div style={{ display: "flex", gap: "0.5rem", flexDirection: "column" }}>
              {Array(4).fill(0).map((_v, i) =>
                <Skeleton key={i} variant="rounded" height={"3rem"} />
              )}
            </div>
            :
            (
              filteredChangeLog.length > 0 || false ? filteredChangeLog.map(c => (
                <ChangeLogItem key={c.title} defaultExpanded={currentVersion === c.title} {...c} />
              ))
                :
                <>
                  <Typography variant="h6">
                    You have hit the rate limit for this API :(
                  </Typography>
                  <Typography variant="subtitle1">
                    This limit is reset every hour, try again in ~30-60 minutes
                  </Typography>
                </>
            )
        }
      </div>
    </div>
  )
}