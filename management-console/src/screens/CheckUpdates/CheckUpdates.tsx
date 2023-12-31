import { ReactNode, useEffect } from "react";
import { useApplicationCurrentVersion, useLatestVersion, useUpdateApplicationVersions, useUpgradeApplication } from "../../api/versions";
import { Button, CircularProgress, Typography } from "@mui/material";
import { useWaitForUpgrade } from "../../customHooks/useWaitForUpgrade";
import { UpgradeOverlay } from "../../components/UpgradeOverlay/UpgradeOverlay";

type VersionTextProps = {
  children: ReactNode
}
const VersionText = ({ children }: VersionTextProps) => (
  <Typography variant="body2" display={"inline"} sx={{ backgroundColor: "#e1e1e1", borderRadius: "0.35em", padding: "0 0.25em" }}>
    {children}
  </Typography>
);

export const CheckUpdates = () => {
  const { data: latestVersion = "" } = useLatestVersion();
  const { data: currentVersion = "" } = useApplicationCurrentVersion();

  const { startWaitingForUpgrade, isUpgrading } = useWaitForUpgrade();

  const { mutate: upgradeApplication, isPending: isUpgradingApplication } = useUpgradeApplication();

  const { mutateAsync: updateApplicationVersions, isPending: isUpdatingApplicationVersions } = useUpdateApplicationVersions();
  // this should happen on mount to update the avilable versions
  useEffect(() => {
    updateApplicationVersions()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div style={{ maxWidth: "50rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1, alignItems: "center" }}>
      {
        isUpdatingApplicationVersions ?
          <CircularProgress />
          :
          (
            currentVersion === latestVersion ?
              <div>
                {`Application is updated with the latest version `}
                <VersionText>
                  {latestVersion}
                </VersionText>
              </div>
              :
              <>
                <div>
                  <span> Current version is </span>
                  <VersionText> {currentVersion} </VersionText>
                  <span> , latest version is </span>
                  <VersionText> {latestVersion} </VersionText>
                </div>
                <Button disabled={isUpgradingApplication || isUpgrading} variant="contained" onClick={() => {
                  upgradeApplication({ version: latestVersion });
                  startWaitingForUpgrade();
                }}>
                  {
                    isUpgradingApplication ?
                      <CircularProgress />
                      :
                      "Upgrade now"
                  }
                </Button>
              </>
          )
      }
      {
        isUpgrading && <UpgradeOverlay />
      }
    </div>
  );
};