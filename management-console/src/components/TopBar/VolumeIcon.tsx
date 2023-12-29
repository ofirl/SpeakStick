import { useCallback, useMemo, useRef, useState } from 'react';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import VolumeDownIcon from '@mui/icons-material/VolumeDown';
import { Backdrop, IconButton, LinearProgress, Paper, Slider, Tooltip } from '@mui/material';
import {
  Unstable_Popup as BasePopup,
} from '@mui/base/Unstable_Popup';
import { useDebounce } from '../../customHooks/useDebounce';
import { useGetConfigs, useUpdateConfig } from '../../api/configs';

const SOUND_VOLUME_CONFIG = "VOLUME"

export const VolumeIcon = () => {
  const [volumeControlOpen, setVolumeControlOpen] = useState(false)
  const anchorElement = useRef<HTMLButtonElement>(null);

  const { data: configs, isPending: isPendingConfigs } = useGetConfigs();
  const { mutateAsync: updateConfig, isPending: isUpdatingConfig } = useUpdateConfig({
    onSuccess: () => {
      setVolumeControlOpen(false)
    }
  });

  const volume = useMemo(() =>
    parseInt(configs?.find(c => c.key === SOUND_VOLUME_CONFIG)?.value || "1"),
    [configs]
  )

  const onVolumeChange = useDebounce(useCallback((newValue: number) => {
    updateConfig({ key: SOUND_VOLUME_CONFIG, value: newValue.toString() })
  }, [updateConfig]), 500)

  return (
    <>
      <Tooltip title="Volume control">
        <IconButton
          size="large"
          color="inherit"
          aria-label="restart"
          onClick={() => setVolumeControlOpen(prev => !prev)}
          ref={anchorElement}
        >
          <VolumeUpIcon />
        </IconButton>
      </Tooltip>
      {
        volumeControlOpen &&
        <>
          <Backdrop open={volumeControlOpen} invisible onClick={() => setVolumeControlOpen(false)} />
          <BasePopup
            id="placement-popper"
            open={volumeControlOpen}
            anchor={anchorElement.current}
            placement={"bottom"}
            offset={10}
            slotProps={{ root: { style: { zIndex: 10000 } } }}
          >
            <Paper style={{ padding: "0 1rem", display: "flex", gap: "1rem", alignItems: "center", minWidth: "15rem", minHeight: "2.5rem" }} elevation={5}>
              {isPendingConfigs || isUpdatingConfig ? <LinearProgress style={{ width: "100%" }} /> :
                <>
                  <VolumeDownIcon />
                  <Slider valueLabelDisplay="auto" defaultValue={volume} style={{ width: "10rem" }} aria-label="Volume" onChange={(_e, value) => onVolumeChange(typeof value === "number" ? value : value[0])} />
                  <VolumeUpIcon />
                </>
              }
            </Paper>
          </BasePopup>
        </>

      }
    </>
  );
};